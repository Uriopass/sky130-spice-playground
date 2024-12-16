import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.spatial import Voronoi, voronoi_plot_2d

# Generate discretized points in the unit square
def generate_points(n_points):
    """
    Generate a grid of points over the unit square.
    """
    x = np.linspace(0, 1, n_points)
    y = np.linspace(0, 1, n_points)
    X, Y = np.meshgrid(x, y)
    points = np.vstack((X.ravel(), Y.ravel())).T
    return points

# Define the cost function
def cost_function_n(params, points, n_centers):
    """
    Cost function for N Voronoi centers.
    params: Flattened coordinates of the N centers [x1, y1, x2, y2, ...].
    points: Points in the unit square to approximate the integral.
    n_centers: Number of Voronoi centers.
    """
    centers = params.reshape((n_centers, 2))  # Reshape to Nx2
    distances = np.array([np.linalg.norm(points - center, axis=1) for center in centers])
    min_distances = np.min(distances, axis=0)  # Minimum distance for each point
    return np.sum(min_distances) / len(points)  # Average cost

# Optimize the Voronoi centers
def optimize_voronoi_n(points, n_centers, initial_guess):
    """
    Optimize the positions of N Voronoi centers using L-BFGS-B.
    points: Discretized points in the unit square.
    n_centers: Number of Voronoi centers.
    initial_guess: Initial guess for the center positions.
    """
    result = minimize(
        cost_function_n,
        initial_guess,
        args=(points, n_centers),
        method='L-BFGS-B',
        bounds=[(0, 1)] * (2 * n_centers)  # Bounds for all coordinates
    )
    return result

# Plot the Voronoi regions
def plot_voronoi(points, centers):
    """
    Plot Voronoi diagram given points and optimized centers.
    """
    vor = Voronoi(centers)  # Generate Voronoi diagram
    plt.figure(figsize=(8, 8))
    plt.scatter(points[:, 0], points[:, 1], s=1, label="Unit Square Points", alpha=0.3)
    plt.scatter(centers[:, 0], centers[:, 1], color="red", label="Optimized Points", zorder=5)
    voronoi_plot_2d(vor, ax=plt.gca(), show_vertices=False, line_colors="blue")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title("Voronoi Regions")
    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Main script
n_points = 200  # Grid resolution
n_centers = 25   # Number of Voronoi centers
points = generate_points(n_points)  # Generate grid points

# Initial guess for N centers (random positions in [0, 1])
initial_guess = np.random.rand(n_centers * 2)

# Optimize the Voronoi centers
result = optimize_voronoi_n(points, n_centers, initial_guess)
optimized_centers = result.x.reshape((n_centers, 2))

# Plot the optimized Voronoi regions
plot_voronoi(points, optimized_centers)

#import numpy as np
#import matplotlib.pyplot as plt
#import math
#
#randfet = lambda: min(100.0, 1.0 / (np.random.uniform(0, 1))**(1/2) - 1 + 0.36)
#randfet2 = lambda: min(100.0, 1.0 / (np.random.uniform(0, 1))**(3/4) - 1 + 0.36)
#
#
#
## Generate samples
#n_samples = 100000  # Number of samples
#samples = [randfet() for _ in range(n_samples)]
#samples2 = [randfet2() for _ in range(n_samples)]
#
## Plot the distribution
#plt.figure(figsize=(10, 6))
#plt.hist(samples, bins=1000, density=True, color="skyblue", edgecolor="skyblue", alpha=0.7, label="cbrt()")
#plt.hist(samples2, bins=1000, density=True, color="green", edgecolor="green", alpha=0.7, label="sqrt()")
#plt.legend()
#plt.title("Distribution of randfet()", fontsize=16)
#plt.xlabel("Value", fontsize=14)
#plt.ylabel("Density", fontsize=14)
#plt.grid(alpha=0.3)
#plt.show()
