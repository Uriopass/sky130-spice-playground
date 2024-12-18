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
    if len(content_json) > 120000:
        check_cases_until = 8000

    for parsed in content_json[:check_cases_until]:
        case = tuple([parsed[pin] for pin in pin_list])
        cases.add(case)

    input_tensors = {case: np.zeros((int(1.1 * len(content_json) / len(cases)), 3 + 5 * numb_fets + 2 * numb_fets * (numb_fets - 1)), dtype = "float64") for case in cases}
    output_tensors = {case: np.zeros((int(1.1 * len(content_json) / len(cases)), 2), dtype = "float64") for case in cases}
    iis = {case: 0 for case in cases}

    for parsed in content_json:
        #if not(parsed["val_A1"] == "0" and parsed["val_B2"] == "0" and parsed["val_C2"] == "1.8" and parsed["val_B1"] == "0" and parsed["val_A2"] == "0" and parsed["val_C1"] == "fall"):
        #    continue

        skip = False
        for j in range(numb_fets):
            if parsed[f"w_{j}"] > 5:
                skip = True
                break
        if skip:
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
            #addval(w_j)

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
                addval(capa / (w_j + w_k))
                #addval(np.sqrt(w_j / w_k))
                #addval(np.cbrt(w_j / w_k))

                #addval(np.cbrt((1.0 / w_j + 1.0 / w_k) * capa))
                #addval(np.sqrt((1.0 / w_j + 1.0 / w_k) * capa * transition))
                #addval(np.cbrt(w_j / w_k * capa * transition))

                #addval(w_j / w_k * capa)
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
        if file.endswith(".njson"):
            print("gonna do", file)
            input_tensors, output_tensors, pin_list = read_data(data_path="data/" + file)
            for key in sorted(input_tensors.keys()):
                X, y = input_tensors[key], output_tensors[key]
                if len(X) == 0:
                    continue
                #print(len(y))

                #print(X.shape, y.shape)

                avg_rele = 0
                avg_rele_max = 0
                avg_abse = 0

                #axis0 = X[:, 1]
                #axis1 = X[:, 2]
                #axis_dt = y[:, 0]
                #axis_z = None
                #axis_z2 = None

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

                    abse = np.abs(y_validation - y_hat_val)
                    avg_abse += np.mean(abse)

                    rel_err = np.abs(y_validation - y_hat_val) / (np.abs(y_validation))
                    #rel_err = 0 if abse < 0.02 else rel_err
                    avg_rele += np.mean(rel_err)

                    rel_err_max = np.abs(y_validation - y_hat_val) / (np.maximum(0.1, np.abs(y_validation)))
                    avg_rele_max += np.mean(rel_err_max)
                    #dt = y_validation[:,0]
                    #dt_hat = y_hat_val[:,0]
                    #trans = y_validation[:,1]
                    #trans_hat = y_hat_val[:,1]

                    #alpha = 0.5 / 0.6
                    #proj_error = np.abs(dt - trans * alpha - (dt_hat - trans_hat * alpha)) / (dt - trans * alpha + in_transition / 2)

                    #avg_proj += np.mean(proj_error)

                    #axis_z = np.concatenate([axis_z, abse[:,0]]) if i > 0 else abse[:,0]
                    #axis_z2 = np.concatenate([axis_z2, rel_err[:,0]]) if i > 0 else rel_err[:,0]


                    # worst_i = np.argmax(np.abs((y_validation[:, 0] - y_hat_val[:, 0]) / (0.1 + np.abs(y_validation[:, 0]))))
                    # wors_rel_err = X_validation[worst_i][:3+12]
                    # wors_val = y_validation[worst_i]

                    #print(wors_rel_err, wors_val, y_hat_val[worst_i])



                # make histogram instead of scatter
                #hist_dt = np.linspace(0.0, np.max(axis_dt), 50)
                #hist_abse = np.zeros(len(hist_dt) - 1)
                #hist_rele = np.zeros(len(hist_dt) - 1)
#
                #for i in range(len(hist_dt) - 1):
                #    hist_abse[i] = np.mean(axis_z[(axis_dt >= hist_dt[i]) & (axis_dt < hist_dt[i + 1])])
                #    hist_rele[i] = np.mean(axis_z2[(axis_dt >= hist_dt[i]) & (axis_dt < hist_dt[i + 1])])
#
                #plt.plot(hist_dt[:-1], hist_abse, label="abs_err")
                #plt.plot(hist_dt[:-1], hist_rele, label="rel_err")
                #plt.xlabel("Delta Time")
                #plt.ylabel("mean", rotation=0, ha="right")
                #plt.show()
#
                #plt.scatter(axis_dt, axis_z, c='r', marker='o')
                #linear_regression = np.polyfit(axis_dt, axis_z, 1)
                #plt.plot(axis_dt, linear_regression[0] * axis_dt + linear_regression[1], c='b', label="Linear Regression")
                #plt.xlabel("Delta Time")
                #plt.ylabel("Abs Error")
                #plt.legend()
                #plt.show()
                ## 3d scatter
                #fig = plt.figure()
                #ax = fig.add_subplot(111, projection='3d')
                #ax.scatter(axis0, np.log10(axis1), axis_z, c='r', marker='o')
                ##ax.scatter(axis0, np.log10(axis1), axis_z, c='b', marker='o')
                #ax.set_xlabel('Transition')
                #ax.set_ylabel('Capacitance')
                #ax.set_zlabel('abs Error')
                #ax.set_zlim(0, 0.04)
                #plt.show()

                #print()
                avg_rele /= 10
                avg_abse /= 10
                avg_rele_max /= 10

                xtx = np.matmul(X.T, X)
                xtx_pinv = np.linalg.pinv(xtx)
                linear_estimator = np.matmul(xtx_pinv, X.T @ y)

                y_hat_val = X @ linear_estimator

                rel_e_all = np.mean(np.abs(y - y_hat_val) / np.abs(y))
                #abs_e_all = np.mean(np.abs(y - y_hat_val))

                print(file, key, avg_rele, avg_abse, rel_e_all,  avg_rele_max, len(y))

                # save configuration if avg_error is too high
                if avg_rele > 0.05:
                    pin_config = ""
                    for i, pin in enumerate(pin_list):
                        pin_config += f"{pin}: {key[i]} "
                    with open("bad_configs_6000_fetlt5.txt", "a") as f:
                        f.write(f"{file} {pin_config} rel:{avg_rele:.6} abs:{avg_abse:.6} rel_train:{rel_e_all:.6} rel_max01:{avg_rele_max:.6}\n")

