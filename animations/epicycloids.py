import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('dark_background')
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def dft(x):
    """
    Discrete Fourier Transform (DFT) of a data set x
    Parameters:
        - x: ndarray(N,) type :: complex
            data points to perform the DFT
    Returns:
        - X: ndarray(N,) type :: complex
            Fourier modes amplitudes
    """
    N = len(x)
    X = np.zeros_like(x, dtype=complex)

    for k in range(N):
        for n in range(N):
            X[k] += 1 / N * x[n] * np.exp(- 1j * (2 * np.pi * n / N) * k)

    return X


def path(xvals, yvals, frames):
    """
    Extend path values to match with the animation frames
    Parameters:
        - xvals: ndarray(N,) type :: float
            x values of the path
        - yvals: ndarray(N,) type :: float
            y values of the path
        - frames: float
            number of frames per cycle of the DFT
    Returns:
        - complex_path: ndarray(N,)
            complex path (x + 1j * y) to perform the DFT
    """

    N = len(xvals)
    dt, dt_anim = 2 * np.pi / N, 2 * np.pi / frames
    t_path = np.arange(0, 2 * np.pi, dt)
    t_frames = np.arange(0, 2 * np.pi, dt_anim)

    return np.interp(t_frames, t_path, xvals) + 1j * np.interp(t_frames, t_path, yvals)


FPS = 60  # Frames per second
frames_per_cycle = FPS * 6  # Choose how many frames do you want per period
dt_animation = 2 * np.pi / frames_per_cycle  # Time increment for the chosen frames per cycle

PERIODS = 2  # Animate the solution for this number of periods
ANIMATION_TIME = PERIODS * frames_per_cycle / FPS
ANIMATION_FRAMES = int(ANIMATION_TIME * FPS)

time = np.arange(0, 2 * np.pi, dt_animation)
time = np.hstack([time] * PERIODS)  # Time vector for the DFT (do not change this!)

# ----------------------------------- EDIT HERE ------------------------------------------ #
#  Write here the x and y values of the path you want to reconstruct using Fourier Series  #

t = np.linspace(0, 2 * np.pi, 100)  # With these two lines you paint a heart
xvalues, yvalues = 16 * np.sin(t) ** 3, 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)


# xvalues, yvalues = np.array([10, 10, -10, -10, 10]), np.array([10, -10, -10, 10, 10])  # This paints a square

# ----------------------------------- EDIT HERE ------------------------------------------ #

z = path(xvalues, yvalues, frames_per_cycle)  # Compute the complex path from the x and y values

Z = dft(z)  # Compute the complex amplitudes from the DFT

n_max = len(Z)  # Length of the complex amplitudes vector
x_p, y_p = np.zeros((n_max, len(time))), np.zeros((n_max, len(time)))

radii = np.abs(Z)  # Obtain radii of each of the circles
idx = np.flip(np.argsort(radii))
indices = np.hstack([0, idx[idx != 0]])  # Obtain indices to reorder radii from largest to smallest

# Compute the Inverse Fourier Transform to get the x and y values
for m in range(n_max):
    x_p[m, :] = np.real(Z[m] * np.exp(1j * m * time))
    y_p[m, :] = np.imag(Z[m] * np.exp(1j * m * time))

x_p, y_p = x_p[indices, :], y_p[indices, :]
radii = radii[indices]
x_t, y_t = np.cumsum(x_p, axis=0), np.cumsum(y_p, axis=0)  # Accumulate positions to plot the circles
M = n_max  # Choose how many circles to animate

# Make the figure for the animation
fig = plt.figure(figsize=(6.1, 5))
fig.subplots_adjust(left=0.1, bottom=0.05, top=0.85)
x_offset, y_offset = 10, 5
ax = plt.axes(xlim=(np.min(xvalues) - x_offset, np.max(xvalues) + x_offset),
              ylim=(np.min(yvalues) - y_offset, np.max(yvalues) + y_offset))
ax.set_aspect('equal')
ax.axis('off')
ax.text(0.825, -0.05, r'@RayleighLord', transform=ax.transAxes, size=15, alpha=0.6)

draw = ax.plot([], [], lw=2.5, color="#f23d4f", alpha=1, zorder=2000)[0]
lines = [ax.plot([], [], lw=1.75, color="w", alpha=0.35, zorder=k)[0] for k in range(n_max)]
circles = [ax.plot([], [], lw=2, color="#3a62f2", alpha=0.5, zorder=k)[0] for k in range(n_max)]

theta = np.linspace(0, 2 * np.pi, 100)  # Angle variable to plot the circles


def animate(i):
    for j, (line, circle) in enumerate(zip(lines[1: M], circles[1: M])):
        line.set_data([x_t[j, i], x_t[j + 1, i]], [y_t[j, i], y_t[j + 1, i]])
        circle.set_data(x_t[j, i] + radii[j + 1] * np.cos(theta), y_t[j, i] + radii[j + 1] * np.sin(theta))

    draw.set_data(x_t[M - 1, :i + 1], y_t[M - 1, :i + 1])


anim = FuncAnimation(fig, animate, frames=ANIMATION_FRAMES, interval=1000 / FPS, blit=False, repeat=True)
plt.show()

# anim.save('epicycle.mp4', writer='ffmpeg', fps=FPS, dpi=180)  ## Uncomment this to save the movie
