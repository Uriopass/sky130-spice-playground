import pickle
import matplotlib.pyplot as plt
import numpy as np

cell_widths = pickle.load(open('hs_saved_cell_widths.pkl', 'rb'))
flat_widths = [
    x
    for xs in cell_widths
    for x in xs
]

print(np.sum(flat_widths))

cell_widths = np.array(flat_widths)

hist, bins = np.histogram(cell_widths, bins=1000, density=True, range=(0, 5))

plt.bar(bins[:-1], hist, width=(bins[1]-bins[0]))
plt.show()