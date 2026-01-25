[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AnantShrey/projectile-motion-optimizer/blob/main/Projectile_Motion_Optimizer.ipynb)

# Projectile Motion Range Optimizer 🚀

A Python-based tool designed to calculate and visualize the optimal launch angle for maximum horizontal range, considering air resistance in the equation.

## Overview
This project was built to explore the intersection of classical mechanics and computational efficiency. It determines the maximum range $R$ using the formula:

$$R = \frac{v^2 \sin(2\theta)}{g}$$

## Features
* **Optimization Logic:** Iteratively tests angles to find the peak range.
* **Visualization:** Generates a trajectory plot using Matplotlib.
* **Physics Accuracy:** Built with standard kinematic equations.

## How to Run
1. Ensure you have Python installed.
2. Install dependencies: `pip install matplotlib` `pip install numpy`
3. Run the script: `python optimizer.py`

## Sample Output
![Trajectory Graph](./graph_output.png) 
