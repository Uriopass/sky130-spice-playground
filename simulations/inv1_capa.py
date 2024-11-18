from matplotlib import pyplot as plt
from spice import parse_voltage, run_spice
import numpy as np

if __name__ == "__main__":
    run_spice(open("inv_1_capa.spice").read())

    time_data, volt_data = parse_voltage("output.txt")

    time_data = time_data[10:] - time_data[10]
    volt_data = volt_data[10:]

    print(np.argmin(np.abs(volt_data - 0.9)))

    derivative_zero = (1.8 - volt_data[0]) * (time_data[1] - time_data[0]) / (volt_data[1] - volt_data[0])

    exp_fit = 1.8 - (1.8 - volt_data[0]) * np.exp(-time_data / derivative_zero)
    RES = 10000
    expected_capa = 0.009408e-12
    exp_lib = 1.8 - (1.8 - volt_data[0]) * np.exp(-time_data / (expected_capa * RES))

    print(np.round(derivative_zero / RES * 1e18))
    print((derivative_zero / RES) / expected_capa)
    print(derivative_zero / RES)

    plt.plot(time_data, volt_data)
    plt.plot(time_data, exp_fit, linestyle="--", color="red")
    plt.plot(time_data, exp_lib, linestyle="--", color="green")
    plt.show()