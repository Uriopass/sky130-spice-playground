from matplotlib import pyplot as plt
import numpy as np

from scipy.optimize import curve_fit


def fit_exponential(a, c, x_data, y_data):
    """
    Fits data to the function Y = a * e^(bX) + c.

    Parameters:
        x_data (array-like): The independent variable (X).
        y_data (array-like): The dependent variable (Y).

    Returns:
        tuple: Fitted parameters (b,)
    """

    # Define the exponential function
    def model(x, b):
        return a * np.exp(b * x) + c

    # Initial guesses for a, b, and c
    initial_guess = 1e15

    # Fit the model to the data
    params = curve_fit(model, x_data, y_data, p0=initial_guess)

    return params

def parse_voltage(file_path):
    time_data = []
    voltage_data = []

    # Open and read the file line by line
    with open(file_path, 'r') as file:
        content = file.read()
        for line in content.splitlines():
            line = line.strip()

            if len(line) == 0:
                continue

            if not line[0].isdigit():
                continue

            vals = line.split()

            alldigits = True
            for val in vals:
                if not val[0].isdigit():
                    alldigits = False

            if not alldigits:
                continue

            if len(vals) == 2:
                time_data.append(float(vals[1]))
            else:
                voltage_data.append(float(vals[0]))


    return np.array(time_data), np.array(voltage_data)

if __name__ == "__main__":
    time_data, volt_data = parse_voltage("output.txt")

    time_data = time_data[10:] - time_data[10]
    volt_data = volt_data[10:]

    print(np.argmin(np.abs(volt_data - 0.9)))

    derivative_zero = (1.8 - volt_data[0]) * (time_data[1] - time_data[0]) / (volt_data[1] - volt_data[0])

    exp_fit = 1.8 - (1.8 - volt_data[0]) * np.exp(-time_data / derivative_zero)
    RES = 10000
    expected_capa = 0.009408e-12
    exp_lib = 1.8 - (1.8 - volt_data[0]) * np.exp(-time_data / (expected_capa * RES))

    # fit to real exponential

    print(np.round(derivative_zero / RES * 1e18))


    print ((derivative_zero / RES) / expected_capa)

    b = fit_exponential(-(1.8 - volt_data[0]), 1.8, time_data, volt_data)[0]


    print(b)

    print(derivative_zero / RES)

    plt.plot(time_data, volt_data)
    plt.plot(time_data, exp_fit, linestyle="--", color="red")
    plt.plot(time_data, exp_lib, linestyle="--", color="green")
    plt.show()