import json
import os
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

    input_tensors = {case: np.zeros((int(1.1 * len(content_json) / len(case)), 3 + 7 * numb_fets + 1 * numb_fets * (numb_fets - 1)), dtype = "float64") for case in cases}
    output_tensors = {case: np.zeros((int(1.1 * len(content_json) / len(case)), 2), dtype = "float64") for case in cases}
    iis = {case: 0 for case in cases}

    for parsed in content_json:
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

                #cell_carac.append(w_j / w_k * capa)
                #cell_carac.append(w_j / w_k * transition)
                #cell_carac.append(np.cbrt(w_j / w_k * capa))
                #cell_carac.append(np.cbrt(w_j / w_k * transition))

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
            input_tensors, output_tensors, pin_list = read_data(data_path="data/" + file)
            for key in sorted(input_tensors.keys()):
                X, y = input_tensors[key], output_tensors[key]
                #print(len(y))

                #print(X.shape, y.shape)

                avg_error = 0

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

                    rel_err = np.mean(np.abs((y_validation - y_hat_val) / y_validation))
                    avg_error += rel_err

                    #print(rel_err, end= " ")

                #print()
                avg_error /= 10

                print(file, key, avg_error, len(y))

                # save configuration if avg_error is too high
                if avg_error > 0.05:
                    pin_config = ""
                    for i, pin in enumerate(pin_list):
                        pin_config += f"{pin}: {key[i]} "
                    with open("bad_configs_4000.txt", "a") as f:
                        f.write(f"{file} {pin_config}{avg_error}\n")

                xtx = np.matmul(X.T, X)
                xtx_pinv = np.linalg.pinv(xtx)

                linear_estimator = np.matmul(xtx_pinv, X.T @ y)







