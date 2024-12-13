import json
import math

import numpy as np
#import torch
#import torch.nn as nn
#import torch.optim as optim
import matplotlib.pyplot as plt
import time
from scipy.linalg import solve


import data_generation_xor as gen_xor

from mpmath import mp

"""
class PolyLayer(nn.Module):
    def __init__(self, input_size, output_size):
        super(PolyLayer, self).__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.weights = nn.Parameter(torch.randn(output_size, input_size * input_size))

    def forward(self, x):
        outer = torch.bmm(x.unsqueeze(2), x.unsqueeze(1)).view(self.input_size * self.input_size, -1)
        return torch.matmul(self.weights, outer).transpose(0, 1)

class ConfigurableMLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_hidden_layers):
        super(ConfigurableMLP, self).__init__()
        layers = []
        linear = True

        if linear:
            layers.append(nn.Linear(input_size, output_size))
        else:
            layers.append(nn.Linear(input_size, hidden_size))
            layers.append(nn.LeakyReLU())
            for _ in range(num_hidden_layers - 1):
                layers.append(nn.Linear(hidden_size, hidden_size))
                layers.append(nn.BatchNorm1d(hidden_size))
                layers.append(nn.LeakyReLU())
            layers.append(nn.Linear(hidden_size, output_size))
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)
"""
def one_hot_map_xor_gen():
    one_hot_map = {}
    ii = 0
    for critical in range(3):
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    one_hot_map[(critical, a, b, c)] = ii
                    ii += 1

    if ii != 24:
        raise ValueError("Invalid one-hot map")

    return one_hot_map

def one_hot_map_and_gen():
    one_hot_map = {}
    ii = 0
    for critical in range(3):
        for value in range(2):
            one_hot_map[(critical, value)] = ii
            ii += 1
    return one_hot_map

def read_data(data_path="out_and3.njson"):
    is_xor = data_path == "out_xor3.njson" or data_path == "out_xor3_test.njson"

    content = open(data_path).readlines()
    one_hot_map_xor = one_hot_map_xor_gen()
    one_hot_map_and = one_hot_map_and_gen()

    one_hot_length = len(one_hot_map_xor)
    if not is_xor:
        one_hot_length = len(one_hot_map_and)

    #input_tensor = np.zeros((len(content), 2 + numb_fets * 5 + numb_fets * (numb_fets - 1) + (numb_fets * (numb_fets - 1)) // 2), dtype=np.float64)
    input_tensor = []
    output_tensor = []

    for line in content[:-2]:
        cell_carac = []
        if line.strip() == "":
            continue
        parsed = json.loads(line)

        #if parsed["out_delta_time"] > 2e-9:
        #    continue

        val_a = parsed["val_a"]
        val_b = parsed["val_b"]
        val_c = parsed["val_c"]

        if is_xor:
            numb_fets = 22
            if val_a != "fall" or val_b != "0" or val_c != "1.8":
                continue
        else:
            numb_fets = 8
            if val_a != "1.8" or val_b != "1.8" or val_c != "fall":
                continue
#        tensor_i = 0
#        def add_input(x):
#            nonlocal tensor_i, i
#            input_tensor[i, tensor_i] = x
#            tensor_i += 1

        capa = parsed["capa_out_fF"]
        transition = parsed["transition"]

        cell_carac.append(transition)
        cell_carac.append(capa)

        for j in range(numb_fets):

            w_j = parsed["w_" + str(j)]
            cell_carac.append(w_j)
            cell_carac.append(1.0 / w_j)
            cell_carac.append(capa / w_j)
            #cell_carac.append(transition * w_j)

            #ordre 2
            cell_carac.append(np.cbrt(capa / w_j))
            cell_carac.append(np.sqrt(transition / w_j))
            #cell_carac.append(np.cbrt(transition * w_j))
            #cell_carac.append(np.sqrt(capa / w_j))

            #tests viables

            #cell_carac.append(np.sqrt(transition * w_j))

            #cell_carac.append(np.sqrt(capa / transition))
            #cell_carac.append(np.sqrt(capa / (transition * w_j)))

        for j in range(numb_fets):
            for k in range(numb_fets):
                if j == k:
                    continue
                w_j = parsed["w_" + str(j)]
                w_k = parsed["w_" + str(k)]
                cell_carac.append(w_j / w_k)

                #tests viables
                cell_carac.append(w_j / w_k * capa)
                cell_carac.append(w_j / w_k * transition)
                cell_carac.append(np.cbrt(w_j / w_k * capa))
                cell_carac.append(np.cbrt(w_j / w_k * transition))

                #cell_carac.append(np.sqrt(w_j / (w_k*transition)))


#        if data_path == "out_xor3.njson" or data_path == "out_xor3_test.njson":
#            if val_a == "rise" or val_a == "fall":
#                critical = 0
#                val_a = 1 if val_a == "rise" else 0
#            elif val_b == "rise" or val_b == "fall":
#                critical = 1
#                val_b = 1 if val_b == "rise" else 0
#            elif val_c == "rise" or val_c == "fall":
#                critical = 2
#                val_c = 1 if val_c == "rise" else 0
#            else:
#                raise ValueError("Invalid critical")
#
#            # Convert strings "0" or "1.8" to numeric 0/1 if needed
#            if val_a == "0": val_a = 0
#            if val_b == "0": val_b = 0
#            if val_c == "0": val_c = 0
#            if val_a == "1.8": val_a = 1
#            if val_b == "1.8": val_b = 1
#            if val_c == "1.8": val_c = 1
#
#            encoded_inputs = one_hot_map_xor[(critical, val_a, val_b, val_c)]
#        elif data_path == "out_and3.njson":
#            if val_a == "rise" or val_a == "fall":
#                critical = 0
#                value = 1 if val_a == "rise" else 0
#            elif val_b == "rise" or val_b == "fall":
#                critical = 1
#                value = 1 if val_b == "rise" else 0
#            elif val_c == "rise" or val_c == "fall":
#                critical = 2
#                value = 1 if val_c == "rise" else 0
#            else:
#                raise ValueError("Invalid critical")
#
#            encoded_inputs = one_hot_map_and[(critical, value)]
#        else:
#            raise ValueError("Invalid data path")

        #for _ in range(encoded_inputs):
        #    add_input(0)
        #add_input(1)
        output_tensor.append([parsed["out_delta_time"] * 1e9, parsed["out_transition"] * 1e9])

        input_tensor.append(cell_carac)

    print(f"Total: {len(input_tensor)}")

    input_tensor = np.array(input_tensor, dtype = "float64")
    output_tensor = np.array(output_tensor, dtype = "float64")

    return input_tensor, output_tensor
    #return torch.from_numpy(input_tensor), torch.from_numpy(output_tensor)

if __name__ == "__main__":
    #from tensorboard import program
#
    #tracking_address = "./logs"
    #tb = program.TensorBoard()
    #tb.configure(argv=[None, '--logdir', tracking_address])
    #url = tb.launch()
    #print(f"Tensorflow listening on {url}")

    print("reading data...")
    X, y = read_data()


    size = np.linspace(1000, 9000, 10)

    lol = []

    for s in size:
        X_validation = X[int(s):]
        y_validation = y[int(s):]

        X_train = X[:int(s)]
        y_train = y[:int(s)]

        # add one to X vectors
        X_train = np.concatenate([X_train, np.ones((X_train.shape[0], 1))], axis=1)
        X_validation = np.concatenate([X_validation, np.ones((X_validation.shape[0], 1))], axis=1)

        xtx = np.matmul(X_train.T, X_train)
#        xtx_inv = np.linalg.inv(xtx)
        xtx_pinv = np.linalg.pinv(xtx)
#
#        linear_estimator = (xtx_inv @ X_train.transpose()) @ y_train
#        y_hat_val = X_validation @ linear_estimator
#
#        rel_err = np.mean(np.abs(y_validation - y_hat_val) / y_validation)


#        #mpmath
#
#        mp.prec = 64
#        X_train = mp.matrix(np.concatenate([X_train, np.ones((X_train.shape[0], 1))], axis=1, dtype=np.float64))
#        X_validation = mp.matrix(np.concatenate([X_validation, np.ones((X_validation.shape[0], 1))], axis=1))
#        y_validation = mp.matrix(y_validation)
#        y_train = mp.matrix(y_train)
#        xtx = X_train.T * X_train
#        xtx_inv = xtx**-1
#        linear_estimator = (xtx_inv * X_train.transpose()) * y_train
#        y_hat_val = X_validation * linear_estimator
#        rel_err = np.mean(
#            [abs(yv - yh) / yv for yv, yh in zip(y_validation, y_hat_val) if yv != 0]
#        )

        #xty = np.matmul(X_train.T, y_train)  # X^T * y
        #print(xtx.shape)
        #print(xty.shape)
        #linear_estimator = solve(xtx, xty)

        # Predict validation set
        y_hat_val = X_validation @ np.matmul(xtx_pinv, X_train.T @ y_train)

        # Compute relative error
        rel_err = np.mean(np.abs(y_validation - y_hat_val) / y_validation)
        print(rel_err)

        lol.append(rel_err)

    plt.plot(size, lol)
    plt.show()
    exit(0)

    X = torch.from_numpy(X).float()
    y = torch.from_numpy(y).float()

    X_test, y_test = read_data(data_path="out_xor3_test.njson")
    X_test = np.concatenate([X_test, np.ones((X_test.shape[0], 1))], axis=1)

    X_test = torch.from_numpy(X_test).float()
    y_test = torch.from_numpy(y_test).float()

    validation_size = int(0.1 * len(X))
    X_train = X[:-validation_size]
    y_train = y[:-validation_size]

    X_val = X[-validation_size:]
    y_val = y[-validation_size:]

    print(len(X_train), len(X_val))

    input_size = X_train.shape[1]
    hidden_size = 64
    output_size = 2
    learning_rate = 0.001
    num_epochs = 10000000000
    num_hidden_layers = 3
    minibatch_size = min(4096, len(X_train))
    decay = 1e-5

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
    X_test = X_test.to(device)
    y_test = y_test.to(device)

    epochs_list = []
    train_losses = []
    val_losses = []
    test_losses = []

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
    (test_line,) = ax.plot([], [], 'g-', label="Test Error")
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
        for _ in range(5):
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


            test_outputs = model(X_test)
            test_relative_error = (test_outputs / y_test - 1).abs().mean().item()

            train_rmse = loss.item()**0.5
            val_rmse = validation_loss**0.5

            epochs_list.append(epoch)
            train_losses.append(relative_error_train)
            val_losses.append(relative_error)
            test_losses.append(test_relative_error)

            print(f"Epoch [{epoch}/{num_epochs}], Train RMSE: {train_rmse:.10f}, Validation RMSE: {val_rmse:.10f}, Train relative: {relative_error_train:.10f}, Validation relerr: {relative_error:.10f}")

            # Update plot data
            train_line.set_xdata(epochs_list)
            train_line.set_ydata(train_losses)
            val_line.set_xdata(epochs_list)
            val_line.set_ydata(val_losses)
            test_line.set_xdata(epochs_list)
            test_line.set_ydata(test_losses)

            # Adjust plot limits if necessary
            ax.set_xlim(0, max(epochs_list) if epochs_list else 1)
            current_max_loss = max(train_losses + val_losses) if train_losses and val_losses else 1
            current_min_loss = min(train_losses + val_losses + test_losses) if train_losses and val_losses else 0.00001
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
