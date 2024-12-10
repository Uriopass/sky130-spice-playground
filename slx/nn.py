import json

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.tensorboard import SummaryWriter

# Define the configurable MLP model with Batch Normalization
class ConfigurableMLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_hidden_layers):
        super(ConfigurableMLP, self).__init__()
        layers = []

        # Input layer
        layers.append(nn.Linear(input_size, hidden_size))
        #layers.append(nn.BatchNorm1d(hidden_size))
        layers.append(nn.Tanh())

        # Hidden layers
        for _ in range(num_hidden_layers - 1):
            layers.append(nn.Linear(hidden_size, hidden_size))
            #layers.append(nn.BatchNorm1d(hidden_size))
            layers.append(nn.Tanh())

        # Output layer
        layers.append(nn.Linear(hidden_size, output_size))

        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

def read_data():
    content = open("out.njson").readlines()

    one_hot_map = {}

    ii = 0
    for critical in range(3):
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    one_hot_map[(critical, a, b, c)] = ii
                    ii += 1

    print(one_hot_map)

    if ii != 24:
        raise ValueError("Invalid one-hot map")

    input_tensor = np.zeros((len(content), 22 + 22 + 24 + 1 + 1), dtype=np.float32)
    output_tensor = np.zeros((len(content), 2), dtype=np.float32)

    total = 0

    for i,line in enumerate(content[:-2]):
        if line.strip() == "":
            continue
        parsed = json.loads(line)

        input_tensor[i, 0] = parsed["transition"]
        input_tensor[i, 1] = parsed["capa_out_fF"]

        for w in range(22):
            input_tensor[i, 2+w] = parsed["w_" + str(w)]

        for w in range(22):
            input_tensor[i, 2+22+w] = 1.0 / parsed["w_" + str(w)]

        val_a = parsed["val_a"]
        val_b = parsed["val_b"]
        val_c = parsed["val_c"]

        if val_a == "rise" or val_a == "fall":
            critical = 0
            val_a = 1 if val_a == "rise" else 0
        elif val_b == "rise" or val_b == "fall":
            critical = 1
            val_b = 1 if val_b == "rise" else 0
        else:
            critical = 2
            val_c = 1 if val_c == "rise" else 0

        if val_a == "0":
            val_a = 0
        if val_b == "0":
            val_b = 0
        if val_c == "0":
            val_c = 0

        if val_a == "1.8":
            val_a = 1
        if val_b == "1.8":
            val_b = 1
        if val_c == "1.8":
            val_c = 1

        encoded_inputs = one_hot_map[(critical, val_a, val_b, val_c)]

        input_tensor[i, 2 + 22 + 22 + encoded_inputs] = 1

        output_tensor[i, 0] = parsed["out_delta_time"] * 1e9
        output_tensor[i, 1] = parsed["out_transition"] * 1e9

        total += 1

    print(f"Total: {total}")

    input_tensor = input_tensor[:total]
    output_tensor = output_tensor[:total]

    return torch.from_numpy(input_tensor), torch.from_numpy(output_tensor)

# Example usage
if __name__ == "__main__":
    from tensorboard import program

    tracking_address = "./logs"  # the path of your log file.

    tb = program.TensorBoard()
    tb.configure(argv=[None, '--logdir', tracking_address])
    url = tb.launch()
    print(f"Tensorflow listening on {url}")

    print("reading data...")
    X, y = read_data()

    validation_size = int(0.1 * len(X))

    X_train = X[:-validation_size]
    y_train = y[:-validation_size]

    X_val = X[-validation_size:]
    y_val = y[-validation_size:]

    print(len(X_train), len(X_val))

    # fet size + 1 / fet size + 1-hot input encoding + transition + capa_out
    input_size = 22 + 22 + 24 + 1 + 1
    hidden_size = 128
    output_size = 2
    learning_rate = 0.001
    num_epochs = 1000000
    num_hidden_layers = 3  # Configurable number of layers

    # Initialize the model, loss, and optimizer
    model = ConfigurableMLP(input_size, hidden_size, output_size, num_hidden_layers)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    writer = SummaryWriter("./logs")

    # Training loop
    for epoch in range(num_epochs):
        # Forward pass
        outputs = model(X_train)


        loss = criterion(outputs, y_train)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        validation_outputs = model(X_val)
        validation_loss = criterion(validation_outputs, y_val).item()

        if epoch % 500 == 0:
            print(torch.sqrt(torch.max(torch.square(outputs - y_train))))
            print(torch.argmax(torch.square(outputs - y_train)))
            #print(torch.square(y_val - validation_outputs))

            writer.add_scalar("Loss/train", loss.item() ** 0.5, epoch)
            writer.add_scalar("Loss/validation", validation_loss ** 0.5, epoch)

            print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item() ** 0.5:.7f} Validation loss: {validation_loss ** 0.5:.7f}")
