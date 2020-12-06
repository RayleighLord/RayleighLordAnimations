import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---- Style for the background and font ---- #
plt.style.use('dark_background')
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# ---- Setting up the FPS and Physical Simulation Time of the animation ---- #
FPS = 60
SIMULATION_TIME = 4
ANIMATION_FRAMES = SIMULATION_TIME * FPS

# ---- Setting up some constants ---- #
LENGTH = 2.0  # Length of each string
N_MODES = 8  # Number of modes represented
AMPLITUDE = LENGTH / 8  # Amplitude of the vibration
PROP_SPEED = 1  # Propagation speed of the wave
SPATIAL_STEPS = 100  # Number of spatial steps in which to compute each strings displacements

nodes = []  # empty list to contain the nodes location to plot each point after
mode_shapes = []  # empty list containing the mode shape of each mode (the spatial part)

x = np.linspace(0, LENGTH, SPATIAL_STEPS)  # Position vector

# ---- Loop to compute the nodes and shape of each mode ---- #
for i in range(1, N_MODES + 1):
    node_list = [j / i * LENGTH for j in range(1, i)]  # Computes the nodes in the middle of the string
    nodes.append([[0.] + node_list + [LENGTH], [0.] * (i + 1)])  # Includes the boundaries which are Dirichlet
    mode_shapes.append(AMPLITUDE * np.sin(i * np.pi / LENGTH * x))  # Computes the mode shape of each mode

# ---- Creation of the figure ---- #
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)) = plt.subplots(4, 2)  # Creates the figure and subplots
fig.subplots_adjust(top=0.95, right=0.95, left=0.05, bottom=0.05)  # Adjusts the subplots to the window frame

lines = []  # empty list to contain the lines of each mode
nod_pts = []  # empty list to contain the nodes of each mode
axs = [ax1, ax3, ax5, ax7, ax2, ax4, ax6, ax8]  # putting all subplots in a list to easily loop through them afterwards
colors = plt.cm.magma(np.linspace(0.95, 0.4, N_MODES))  # Setting up different colors for the strings

for ix, ax in enumerate(axs):
    ax.set_xlim([-0.03, LENGTH * 1.03])  # Sets the horizontal limit of each subplot
    ax.set_ylim([-1.25 * AMPLITUDE, 1.25 * AMPLITUDE])  # Sets the vertical limit of each subplot
    ax.set_aspect('equal')  # Sets the aspect ratio of each subplot
    ax.axis('off')  # Eliminates the axis of the figures
    freq = str(ix + 1)
    ax.text(0.4, 1.2 * AMPLITUDE, fr'Mode ${freq}: \omega_{freq}=$' + r'$\frac{' + fr'{freq}' +
            r'\pi}{L}$', size=15, c=colors[ix])  # Adds the text to each string
    lines.append(ax.plot([], [], lw=2, c='coral')[0])  # Generates empty plots to animate the strings later
    nod_pts.append(ax.plot([], [], 'wo')[0])  # Generates empty plots to animate the nodes later


# ---- Animation function ---- #
#  This function is the main component of the animation. The index j denotes each frame of the simulation
#  For each j you want to create the subsequent frame
def animate(j):
    for idx, (mode, line, node, color) in enumerate(zip(mode_shapes, lines, nod_pts, colors)):
        line.set_data(x, mode * np.cos(PROP_SPEED * (idx + 1) * np.pi / LENGTH * j / FPS))  # Draws the strings
        line.set_color(color)  # Sets the colors of the strings
        node.set_data(*nodes[idx])  # Draws the nodes of each mode


anim = FuncAnimation(fig, animate, frames=ANIMATION_FRAMES, interval=1000 / FPS, blit=False, repeat=True)

plt.show()
anim.save('string_modes.mp4', writer='ffmpeg', fps=FPS, dpi=180)
