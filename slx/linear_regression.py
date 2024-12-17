import json
import os

import matplotlib.pyplot as plt
import numpy as np

def read_data(data_path):
    content = open(data_path).readlines()
    content_json = [json.loads(line) for line in content if len(line) > 10]

    return read_data_numba(data_path, content_json)

def read_data_numba(data_path, content_json):
    # find number of fets
    numb_fets = 0
    pin_list = []
    for parsed in content_json:
        for key in parsed:
            if key.startswith("w_"):
                numb_fets += 1
            if key.startswith("val_"):
                pin_list.append(key)
        break

    cases = set()

    check_cases_until = 2000
    if len(content_json) > 80000:
        check_cases_until = 8000

    for parsed in content_json[:check_cases_until]:
        case = tuple([parsed[pin] for pin in pin_list])
        cases.add(case)

    input_tensors = {case: np.zeros((int(1.1 * len(content_json) / len(case)), 3 + 6 * numb_fets + 10 * numb_fets * (numb_fets - 1) + numb_fets * (numb_fets - 1) * (numb_fets - 2)), dtype = "float64") for case in cases}
    output_tensors = {case: np.zeros((int(1.1 * len(content_json) / len(case)), 2), dtype = "float64") for case in cases}
    iis = {case: 0 for case in cases}

    for parsed in content_json:
        if not(parsed["val_A1"] == "0" and parsed["val_B2"] == "0" and parsed["val_C2"] == "1.8" and parsed["val_B1"] == "0" and parsed["val_A2"] == "0" and parsed["val_C1"] == "fall"):
            continue

        case = tuple([parsed[pin] for pin in pin_list])

        ii = iis[case]
        input_tensor = input_tensors[case]
        output_tensor = output_tensors[case]

        capa = parsed["capa_out_fF"]
        transition = parsed["transition"]
        jj = 0

        def addval(v):
            nonlocal jj
            input_tensor[ii, jj] = v
            jj += 1

        addval(1.0)
        addval(transition)
        addval(capa)

        for j in range(numb_fets):
            w_j = parsed[f"w_{j}"]
            addval(w_j)

        for j in range(numb_fets):
            w_j = parsed[f"w_{j}"]
            addval(1.0 / w_j)
            addval(capa / w_j)
            addval(np.cbrt(capa / w_j))
            addval(np.sqrt(transition / w_j))
            addval(np.cbrt(transition * capa / w_j))

        for j in range(numb_fets):
            w_j = parsed["w_" + str(j)]
            for k in range(numb_fets):
                if j == k:
                    continue
                w_k = parsed["w_" + str(k)]
                addval(w_j / w_k)

                #addval(np.cbrt((1.0 / w_j + 1.0 / w_k) * capa))
                #addval(np.sqrt((1.0 / w_j + 1.0 / w_k) * capa * transition))
                #addval(np.cbrt(w_j / w_k * capa * transition))

                addval(w_j / w_k * capa)
                #addval(w_j / w_k * transition)
                #addval(np.cbrt(w_j / w_k * capa))
                #addval(np.cbrt(w_j / w_k * transition))

        output_tensor[ii, 0] = parsed["out_delta_time"] * 1e9
        output_tensor[ii, 1] = parsed["out_transition"] * 1e9

        iis[case] += 1

    for key in input_tensors:
        if iis[key] != len(input_tensors[key]):
            input_tensors[key] = input_tensors[key][:iis[key]]
            output_tensors[key] = output_tensors[key][:iis[key]]
        #print(f"Case: {key}, Total: {len(input_tensors[key])}")

    return input_tensors, output_tensors, pin_list

if __name__ == "__main__":
    #iterate of all files in data folder
    for file in os.listdir("data"):
        if "a222" not in file:
            continue

        if file.endswith(".njson"):
            input_tensors, output_tensors, pin_list = read_data(data_path="data/" + file)
            for key in sorted(input_tensors.keys()):
                X, y = input_tensors[key], output_tensors[key]
                if len(X) == 0:
                    continue
                #print(len(y))

                #print(X.shape, y.shape)

                avg_rele = 0
                avg_rmse = 0
                avg_abse = 0
                avg_proj = 0

                axis0 = X[:, 3+3]
                axis1 = X[:, 3+7]
                axis_z = None
                axis_z2 = None

                # cross validation
                for i in range(10):
                    v_start = int(i * X.shape[0] / 10)
                    v_end = int((i + 1) * X.shape[0] / 10)
                    X_validation = X[v_start:v_end]
                    y_validation = y[v_start:v_end]

                    X_train = np.concatenate([X[:v_start], X[v_end:]], axis=0)
                    y_train = np.concatenate([y[:v_start], y[v_end:]], axis=0)

                    xtx = np.matmul(X_train.T, X_train)
                    #print(xtx.shape)
                    xtx_pinv = np.linalg.pinv(xtx)

                    linear_estimator = np.matmul(xtx_pinv, X_train.T @ y_train)

                    #print(linear_estimator.shape)
                    y_hat_val = X_validation @ linear_estimator

                    avg_rmse += np.sqrt(np.mean((y_validation - y_hat_val) ** 2))
                    abse = np.mean(np.abs(y_validation - y_hat_val))
                    avg_abse += abse

                    dt = y_validation[:,0]
                    dt_hat = y_hat_val[:,0]

                    trans = y_validation[:,1]
                    trans_hat = y_hat_val[:,1]

                    in_transition = X_validation[:,1]

                    rel_err = np.abs(y_validation - y_hat_val) / (0.1 + np.abs(y_validation))
                    rel_err = 0 if abse < 0.02 else rel_err
                    avg_rele += np.mean(rel_err)

                    alpha = 0.5 / 0.6
                    proj_error = np.abs(dt - trans * alpha - (dt_hat - trans_hat * alpha)) / (dt - trans * alpha + in_transition / 2)

                    avg_proj += np.mean(proj_error)

                    axis_z = np.concatenate([axis_z, rel_err[:,0]]) if i > 0 else rel_err[:,0]
                    axis_z2 = np.concatenate([axis_z2, rel_err[:,1]]) if i > 0 else rel_err[:,1]


                    #worst_i = np.argmax(np.abs((y_validation[:, 0] - y_hat_val[:, 0]) / (0.1 + np.abs(y_validation[:, 0]))))
                    #wors_rel_err = X_validation[worst_i][:5]
                    #wors_val = y_validation[worst_i]


                    #print(rel_err, end= " ")

                # 3d scatter
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(np.log10(axis0), np.log10(axis1), axis_z, c='r', marker='o')
#                ax.scatter(axis0, np.log10(axis1), axis_z2, c='b', marker='o')
                ax.set_xlabel('W9')
                ax.set_ylabel('W10')
                ax.set_zlabel('diff of Relative Error')
                ax.set_zlim(0, 0.2)
                plt.show()

                #print()
                avg_proj /= 10
                avg_rele /= 10
                avg_rmse /= 10
                avg_abse /= 10

                print(file, key, avg_proj, avg_rele, avg_rmse, avg_abse, len(y))

                # save configuration if avg_error is too high
                if avg_rele > 0.05:
                    pin_config = ""
                    for i, pin in enumerate(pin_list):
                        pin_config += f"{pin}: {key[i]} "
                    with open("bad_configs_4000_max001.txt", "a") as f:
                        f.write(f"{file} {pin_config}{avg_abse:.6}\n")

                xtx = np.matmul(X.T, X)
                xtx_pinv = np.linalg.pinv(xtx)
                linear_estimator = np.matmul(xtx_pinv, X.T @ y)

