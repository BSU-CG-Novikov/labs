import tkinter as tk
from tkinter import colorchooser

RGB_SCALE = 255
CMYK_SCALE = 100

def rgb2cmyk(r, g, b):
    """
    rgb to cmyk
    1) check black
    2) rgb [0,255] -> cmy [0,1]
    3) k = min_cmy
    4) scale CMYK
    """
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, CMYK_SCALE

    c = 1 - r / RGB_SCALE
    m = 1 - g / RGB_SCALE
    y = 1 - b / RGB_SCALE

    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    return c * CMYK_SCALE, m * CMYK_SCALE, y * CMYK_SCALE, k * CMYK_SCALE

def rgb2hsv(r, g, b):
    r = float(r)
    g = float(g) 
    b = float(b)
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, v = high, high, high

    d = high - low
    s = 0 if high == 0 else d / high

    if high == low:
        h = 0.0
    else:
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    return 360 * h, 100 * s, 100 * v

class ColorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Lab1-Novikov")
        self.rgb_vars = [tk.StringVar() for _ in range(3)]
        self.hsv_vars = [tk.DoubleVar() for _ in range(3)]
        self.cmyk_vars = [tk.DoubleVar() for _ in range(4)]
        self.create_widgets()

    def create_widgets(self):
        rgb_frame = tk.Frame(self.master)
        rgb_frame.pack(side=tk.LEFT, padx=10, pady=10)
        tk.Label(rgb_frame, text="RGB").pack()

        tk.Button(rgb_frame, text="Choose Color", command=self.choose_color).pack()

        for i, color in enumerate(["Red", "Green", "Blue"]):
            tk.Label(rgb_frame, text=color).pack()
            slider = tk.Scale(rgb_frame, from_=0, to=255, variable=self.rgb_vars[i], orient=tk.HORIZONTAL, command=self.update_sliders)
            slider.pack()
            entry = tk.Entry(rgb_frame, textvariable=self.rgb_vars[i], validate="focusout", validatecommand=(self.master.register(self.validate_entry), "%P"))
            entry.pack()
            entry.bind("<FocusOut>", self.update_sliders)
            entry.bind("<Return>", self.update_sliders)

        hsv_frame = tk.Frame(self.master)
        hsv_frame.pack(side=tk.LEFT, padx=10, pady=10)
        tk.Label(hsv_frame, text="HSV").pack()

        for i, color in enumerate(["Hue", "Saturation", "Value"]):
            tk.Label(hsv_frame, text=color).pack()
            if(color == "Hue"):
                slider = tk.Scale(hsv_frame, from_=0, to=360, resolution=1, variable=self.hsv_vars[i], orient=tk.HORIZONTAL, command=self.update_sliders)
            else:
                slider = tk.Scale(hsv_frame, from_=0, to=100, resolution=1, variable=self.hsv_vars[i], orient=tk.HORIZONTAL, command=self.update_sliders)
            slider.pack()

        cmyk_frame = tk.Frame(self.master)
        cmyk_frame.pack(side=tk.LEFT, padx=10, pady=10)
        tk.Label(cmyk_frame, text="CMYK").pack()
        for i, color in enumerate(["Cyan", "Magenta", "Yellow", "Black"]):
            tk.Label(cmyk_frame, text=color).pack()
            slider = tk.Scale(cmyk_frame, from_=0, to=CMYK_SCALE, resolution=1, variable=self.cmyk_vars[i], orient=tk.HORIZONTAL, command=self.update_sliders)
            slider.pack()

        self.color_preview = tk.Canvas(self.master, width=100, height=100, bg="white")
        self.color_preview.pack(side=tk.LEFT, padx=10, pady=10)
        self.update_sliders()

    def update_sliders(self, event=None):
        r = int(self.rgb_vars[0].get()) if self.rgb_vars[0].get() else 0
        g = int(self.rgb_vars[1].get()) if self.rgb_vars[1].get() else 0
        b = int(self.rgb_vars[2].get()) if self.rgb_vars[2].get() else 0

        h, s, v = rgb2hsv(r / RGB_SCALE, g / RGB_SCALE, b / RGB_SCALE)
        c, m, y, k = rgb2cmyk(r, g, b)

        self.hsv_vars[0].set(h)
        self.hsv_vars[1].set(s)
        self.hsv_vars[2].set(v)
        self.cmyk_vars[0].set(c)
        self.cmyk_vars[1].set(m)
        self.cmyk_vars[2].set(y)
        self.cmyk_vars[3].set(k)

        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        self.color_preview.config(bg=hex_color)

    def validate_entry(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def choose_color(self):
        color = colorchooser.askcolor(title="Pick a color")
        if color[1]:
            r, g, b = color[0] 
            self.rgb_vars[0].set(int(r))
            self.rgb_vars[1].set(int(g))
            self.rgb_vars[2].set(int(b))
            self.update_sliders()


root = tk.Tk()
app = ColorApp(root)
root.mainloop()
