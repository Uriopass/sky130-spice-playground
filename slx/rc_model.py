import json
import math

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import time
import data_generation_xor as gen_xor

def read_data(numb_fets):
    content = open("out_and3.njson").readlines()
    one_hot_map = one_hot_map_and()

    input_tensor = np.zeros((len(content), numb_fets * 6 + numb_fets * numb_fets + (numb_fets * (numb_fets - 1)) // 2 + len(one_hot_map) + 1 + 1), dtype=np.float32)
    output_tensor = np.zeros((len(content), 1), dtype=np.float32)

    i = 0

    for line in content[:-2]:
        if line.strip() == "":
            continue
        parsed = json.loads(line)

        if parsed["out_delta_time"] > 2e-9:
            continue

        tensor_i = 0
        def add_input(x):
            nonlocal tensor_i, i
            input_tensor[i, tensor_i] = x
            tensor_i += 1

        add_input(parsed["transition"])
        add_input(parsed["capa_out_fF"])

        for j in range(numb_fets):
            W_temp = parsed["w_" + str(j)]
            #ar = gen_xor.area(W_temp) / W_temp
            pe = gen_xor.perim(W_temp) / W_temp
            add_input(W_temp)
            add_input(pe)
            add_input(1.0 / W_temp)
            add_input(parsed["capa_out_fF"] / W_temp)
            add_input(parsed["transition"] * W_temp)

        for j in range(numb_fets):
            for k in range(numb_fets):
                add_input(parsed["w_" + str(j)] / parsed["w_" + str(k)])

        for j in range(numb_fets):
            for k in range(j + 1, numb_fets):
                add_input(parsed["w_" + str(j)] * parsed["w_" + str(k)])

        val_a = parsed["val_a"]
        val_b = parsed["val_b"]
        val_c = parsed["val_c"]

        #if val_a != "1.8" or val_b != "1.8" or val_c != "rise":
        #    continue

        value = 0

        if val_a == "rise" or val_a == "fall":
            critical = 0
            value = 1 if val_a == "rise" else 0
        elif val_b == "rise" or val_b == "fall":
            critical = 1
            value = 1 if val_b == "rise" else 0
        elif val_c == "rise" or val_c == "fall":
            critical = 2
            value = 1 if val_c == "rise" else 0
        else:
            raise ValueError("Invalid critical")

        encoded_inputs = one_hot_map[(critical, value)]

        """
        if val_a == "rise" or val_a == "fall":
            critical = 0
            val_a = 1 if val_a == "rise" else 0
        elif val_b == "rise" or val_b == "fall":
            critical = 1
            val_b = 1 if val_b == "rise" else 0
        elif val_c == "rise" or val_c == "fall":
            critical = 2
            val_c = 1 if val_c == "rise" else 0
        else:
            raise ValueError("Invalid critical")

        # Convert strings "0" or "1.8" to numeric 0/1 if needed
        if val_a == "0": val_a = 0
        if val_b == "0": val_b = 0
        if val_c == "0": val_c = 0
        if val_a == "1.8": val_a = 1
        if val_b == "1.8": val_b = 1
        if val_c == "1.8": val_c = 1

        encoded_inputs = one_hot_map[(critical, val_a, val_b, val_c)]
"""
        for _ in range(encoded_inputs):
            add_input(0)
        add_input(1)

        output_tensor[i, 0] = parsed["out_delta_time"] * 1e9
        #output_tensor[i, 1] = parsed["out_transition"] * 1e9

        i += 1

    print(f"Total: {i}")

    input_tensor = input_tensor[:i]
    output_tensor = output_tensor[:i]

    return torch.from_numpy(input_tensor), torch.from_numpy(output_tensor)

if __name__ == "__main__":
    #from tensorboard import program
#
    #tracking_address = "./logs"
    #tb = program.TensorBoard()
    #tb.configure(argv=[None, '--logdir', tracking_address])
    #url = tb.launch()
    #print(f"Tensorflow listening on {url}")

    print("reading data...")
    numb_fets = 8

    X, y = read_data(numb_fets=numb_fets)

    validation_size = int(0.1 * len(X))
    X_train = X[:-validation_size]
    y_train = y[:-validation_size]

    X_val = X[-validation_size:]
    y_val = y[-validation_size:]

    print(len(X_train), len(X_val))

    input_size = X_train.shape[1]
    hidden_size = 64
    output_size = 1 # y_train.shape[1]
    learning_rate = 0.001
    num_epochs = 10000000000
    num_hidden_layers = 2
    minibatch_size = min(16384, len(X_train))
    decay = 0

    model = ConfigurableMLP(input_size, hidden_size, output_size, num_hidden_layers)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=decay)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if torch.cuda.is_available():
        print("CUDA is available")

    model.to(device)
    X_train = X_train.to(device)
    y_train = y_train.to(device)
    X_val = X_val.to(device)
    y_val = y_val.to(device)

    epochs_list = []
    train_losses = []
    val_losses = []

    print("Starting training...")

    # Set up the plot for real-time updates
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    ax.set_title("Training Progress")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("RMSE")
    ax.set_yscale('log')

    (train_line,) = ax.plot([], [], 'r-', label="Relative Error Train")
    (val_line,) = ax.plot([], [], 'b-', label="Relative Error")
    ax.legend()

    start_time = time.time()

    train_batches = []

    cuts = math.ceil(len(X_train) // minibatch_size)
    print(cuts)

    for i in range(cuts):
        i_start = int(i / cuts * len(X_train))
        i_end = int((i + 1) / cuts * len(X_train))

        train_batches.append((X_train[i_start:i_end], y_train[i_start:i_end]))

    for epoch in range(num_epochs):
        for _ in range(4):
            for X_batch, y_batch in train_batches:
                outputs = model(X_batch)
                loss = criterion(outputs, y_batch)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        if epoch == 250:
            learning_rate /= 2
            #decay*=10
            optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=decay)

        if epoch == 1000:
            #decay*=10
            learning_rate /= 2
            optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=decay)

        if epoch == 2000:
            #decay*=10
            learning_rate /= 5
            optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=decay)


        if epoch == 3000:
            #decay*=10
            learning_rate /= 2
            optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=decay)

        if epoch == 5000:
            #decay*=10
            learning_rate /= 2
            optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=decay)

        if epoch == 8000:
            #decay*=10
            learning_rate /= 2
            optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=decay)

        if epoch % 5 == 0:
            outputs = model(X_train)
            loss = criterion(outputs, y_train)
            if not np.isfinite(outputs.cpu().detach().numpy()).all():
                print("not finite detected")
                exit(1)

            relative_error_train = (outputs / y_train - 1).abs().mean().item()

            # Compute validation loss
            validation_outputs = model(X_val)
            validation_loss = criterion(validation_outputs, y_val).item()

            relative_error  = (validation_outputs / y_val - 1).abs().mean().item()

            train_rmse = loss.item()**0.5
            val_rmse = validation_loss**0.5

            epochs_list.append(epoch)
            train_losses.append(relative_error_train)
            val_losses.append(relative_error)

            print(f"Epoch [{epoch}/{num_epochs}], Train RMSE: {train_rmse:.10f}, Validation RMSE: {val_rmse:.10f}, Train relative: {relative_error_train:.10f}, Validation relerr: {relative_error:.10f}")

            # Update plot data
            train_line.set_xdata(epochs_list)
            train_line.set_ydata(train_losses)
            val_line.set_xdata(epochs_list)
            val_line.set_ydata(val_losses)

            # Adjust plot limits if necessary
            ax.set_xlim(0, max(epochs_list) if epochs_list else 1)
            current_max_loss = max(train_losses + val_losses) if train_losses and val_losses else 1
            current_min_loss = min(train_losses + val_losses) if train_losses and val_losses else 0.00001
            ax.set_ylim(current_min_loss, current_max_loss)

            # Redraw the figure
            fig.canvas.draw()
            fig.canvas.flush_events()
            #plt.pause(0.001)  # Brief pause to allow the UI to update

    end_time = time.time()
    print(f"Training completed in {end_time - start_time:.2f} seconds")

    # Turn off interactive mode and show the final plot
    plt.ioff()
    plt.show()
