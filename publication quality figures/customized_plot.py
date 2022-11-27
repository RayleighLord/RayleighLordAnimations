import matplotlib.pyplot as plt
import numpy as np

from fig_config import (
    add_grid,
    figure_features,
)  # <--- import customized functions

x = np.linspace(-2, 2, 100)
f_1 = x
f_2 = x**2
f_3 = x**3

figure_features()  # <--- Add this line to every figure

fig = plt.figure(figsize=(8, 6))
ax = plt.axes(xlim=(-2, 2), ylim=(-2, 6))

ax.set_xlabel("$x$")
ax.set_ylabel("$f(x)$", labelpad=12.0)

add_grid(ax, locations=(0.5, 1, 1, 2))  # <--- Add this line to every figure

ax.plot(x, f_1, c="royalblue", label="$f_1(x) = x$")
ax.plot(x, f_2, "o-", ms=6, markevery=8, c="coral", label="$f_2(x) = x^2$")
ax.plot(
    x, f_3, "s-", ms=6, markevery=8, c="mediumseagreen", label="$f_3(x) = x^3$"
)

ax.legend()

plt.show()
