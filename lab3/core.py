import time
import tkinter as tk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def bresenham(x1, y1, x2, y2):
    start_time = time.time()

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1

    if dx < dy:
        dx, dy = dy, dx
        sx, sy = sy, sx

    err = dx / 2.0
    points = []

    for _ in range(dx + 1):
        points.append((x, y))
        err -= dy
        if err < 0:
            y += sy
            err += dx
        x += sx

    print("Bresenham's Algorithm Execution Time: ", time.time() - start_time)

    return points

def dda(x1, y1, x2, y2):
    start_time = time.time()

    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    x_incr = dx / steps
    y_incr = dy / steps

    points = []
    for _ in range(steps):
        points.append((round(x1), round(y1)))
        x1 += x_incr
        y1 += y_incr

    print("DDA Algorithm Execution Time: ", time.time() - start_time)

    return points

def plot_algorithm(algorithm, smooth=False):
    x1 = int(entry_x1.get())
    y1 = int(entry_y1.get())
    x2 = int(entry_x2.get())
    y2 = int(entry_y2.get())

    points = algorithm(x1, y1, x2, y2)
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]

    if smooth:
        smooth_x_coords, smooth_y_coords = [], []
        for i in range(len(x_coords) - 1):
            smooth_x_coords.append(x_coords[i])
            smooth_y_coords.append(y_coords[i])
            x_diff = x_coords[i + 1] - x_coords[i]
            y_diff = y_coords[i + 1] - y_coords[i]

            for j in range(1, 10): 
                smooth_x_coords.append(x_coords[i] + j * x_diff / 10)
                smooth_y_coords.append(y_coords[i] + j * y_diff / 10)

        x_coords, y_coords = smooth_x_coords, smooth_y_coords

    ax.clear()
    ax.plot(x_coords, y_coords, 'ro-')
    ax.set_title(f"{algorithm.__name__} Line Algorithm {'(Smooth)' if smooth else ''}")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True)

    canvas.draw()

def plot_bresenham():
    plot_algorithm(bresenham)

def plot_bresenham_smooth():
    plot_algorithm(bresenham, smooth=True)

def plot_dda():
    plot_algorithm(dda)

def plot_dda_smooth():
    plot_algorithm(dda, smooth=True)



root = tk.Tk()
root.title("Line Drawing Algorithms")

frame = tk.Frame(root, bg='white')
frame.pack(fill=tk.BOTH, expand=True)

fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas.draw()

label_x1 = tk.Label(root, text="Start X:")
label_x1.pack(side=tk.LEFT)
entry_x1 = tk.Entry(root)
entry_x1.pack(side=tk.LEFT)

label_y1 = tk.Label(root, text="Start Y:")
label_y1.pack(side=tk.LEFT)
entry_y1 = tk.Entry(root)
entry_y1.pack(side=tk.LEFT)

label_x2 = tk.Label(root, text="End X:")
label_x2.pack(side=tk.LEFT)
entry_x2 = tk.Entry(root)
entry_x2.pack(side=tk.LEFT)

label_y2 = tk.Label(root, text="End Y:")
label_y2.pack(side=tk.LEFT)
entry_y2 = tk.Entry(root)
entry_y2.pack(side=tk.LEFT)

button_plot_bresenham = tk.Button(root, text="Bresenham", command=plot_bresenham)
button_plot_bresenham.pack(side=tk.LEFT)

button_plot_bresenham_smooth = tk.Button(root, text="Bresenham Smooth", command=plot_bresenham_smooth)
button_plot_bresenham_smooth.pack(side=tk.LEFT)

button_plot_dda = tk.Button(root, text="DDA", command=plot_dda)
button_plot_dda.pack(side=tk.LEFT)

button_plot_dda_smooth = tk.Button(root, text="DDA Smooth", command=plot_dda_smooth)
button_plot_dda_smooth.pack(side=tk.LEFT)

root.mainloop()