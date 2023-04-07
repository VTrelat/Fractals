from tkinter.messagebox import showinfo
from tkinter import ttk
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import c_gen


class PPMViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Fractal Viewer")
        # initial size of window
        self.master.geometry("960x540")

        self.image = None
        self.image_tk = None
        self.canvas = None
        self.z = 1.0
        self.x = 0.0
        self.y = 0.0
        self.w = 960
        self.h = 540
        self.x_eq = "x * x - y * y + cx"
        self.y_eq = "2 * x * y + cy"
        self.clipping_eq = "2.0"
        self.eq_window_open = False
        self.render_window_open = False

        # make window non-resizable
        # self.master.resizable(False, False)

        # cascade menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.file_menu_cascade = tk.Menu(self.file_menu)
        self.file_menu.add_cascade(label="Open", menu=self.file_menu_cascade)
        self.file_menu_cascade.add_command(label="Mandelbrot", command=self.open_mandelbrot)
        self.file_menu_cascade.add_command(label="Burning ship", command=self.open_burning_ship)
        self.file_menu_cascade.add_command(label="Custom", command=self.equation_window)
        
        self.file_menu.add_command(label="Render", command=self.create_render_window)
        self.file_menu.add_command(label="Quit", command=self.master.quit)

        self.c_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="C", menu=self.c_menu)
        self.c_menu.add_command(label="Compile", command=self.compile)
        self.c_menu.add_command(label="Run", command=self.run_and_open)

        self.image_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Image", menu=self.image_menu)

        self.image_menu.add_command(label="Reset", command=self.reset_image)
        self.quality_menu = tk.Menu(self.image_menu)
        self.image_menu.add_cascade(label="Quality", menu=self.quality_menu)

        self.quality_menu.add_command(label="Very low", command=lambda: self.set_quality(640, 360))
        self.quality_menu.add_command(label="Low", command=lambda: self.set_quality(960, 540))
        self.quality_menu.add_command(label="Medium", command=lambda: self.set_quality(1280, 720))
        self.quality_menu.add_command(label="High", command=lambda: self.set_quality(1600, 900))

        # binds
        self.master.bind("<MouseWheel>", self.zoom)
        self.master.bind("<Configure>", self.display_on_resize)
        self.master.bind("<Command-q>", self.master.quit)
        self.master.bind("<Command-r>", lambda e: self.reset_image())

    def open_mandelbrot(self):
        self.x_eq = "x * x - y * y + cx"
        self.y_eq = "2 * x * y + cy"
        self.clipping_eq = "2.0"

        self.compile()
        self.reset_image()
        self.run_and_open()

    def open_burning_ship(self):
        self.x_eq = "x * x - y * y + cx"
        self.y_eq = "2 * fabsl(x * y) + cy"
        self.clipping_eq = "2.0"

        self.compile()
        self.reset_image()
        self.run_and_open()

    def equation_window(self):
        if not self.eq_window_open:
            self.eq_window_open = True
            self.entry_window = tk.Toplevel(self.master)
            self.entry_window.title("Equation")
            self.entry_window.resizable(False, False)
            # aligns text to the right for labels
            self.label_x = tk.Label(self.entry_window, text="x: ")
            self.label_x.grid(row=0, column=0)
            self.entry_x = tk.Entry(self.entry_window)
            self.entry_x.grid(row=0, column=1)
            self.entry_x.insert(0, self.x_eq)
            self.label_y = tk.Label(self.entry_window, text="y: ")
            self.label_y.grid(row=1, column=0)
            self.entry_y = tk.Entry(self.entry_window)
            self.entry_y.grid(row=1, column=1)
            self.entry_y.insert(0, self.y_eq)
            self.label_clipping = tk.Label(self.entry_window, text="Clipping: ")
            self.label_clipping.grid(row=2, column=0)
            self.entry_clipping = tk.Entry(self.entry_window)
            self.entry_clipping.grid(row=2, column=1)
            self.entry_clipping.insert(0, self.clipping_eq)
            self.eq_window_ok_button = tk.Button(self.entry_window, text="OK", command=self.set_equation)
            self.eq_window_ok_button.grid(row=3, column=0, columnspan=2)
            self.entry_window.bind("<Return>", lambda e: self.set_equation())

    def set_equation(self):
        self.x_eq = self.entry_x.get()
        self.y_eq = self.entry_y.get()
        self.clipping_eq = self.entry_clipping.get()
        self.entry_window.destroy()
        self.eq_window_open = False

        self.compile()
        self.reset_image()
        self.run_and_open()

    def display_on_resize(self, event):
        new_w = event.width - event.width % 4
        new_h = event.height - event.height % 4
        if self.w != new_w or self.h != new_h:
            self.w = new_w
            self.h = new_h
            if self.canvas:
                self.run_and_open()

    def set_quality(self, w, h):
        self.w = w
        self.h = h
        self.master.geometry(f"{w}x{h}")
        self.run_and_open()

    def reset_image(self):
        self.z = 1.0
        self.x = 0.0
        self.y = 0.0
        self.run_and_open()

    def open_image(self):
        # use filedialog to select a PPM file
        file_path = filedialog.askopenfilename(
            filetypes=[("PPM Files", "*.ppm")])
        if file_path:
            # open and display the image
            self.image = Image.open(file_path)
            self.image_tk = ImageTk.PhotoImage(self.image)
            if self.canvas:
                self.canvas.destroy()
            self.canvas = tk.Canvas(self.master, width=self.image.width, height=self.image.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.pack()

    def run_and_open(self):
        run_c(self.z, self.x, self.y, self.w, self.h, self.clipping_eq)
        self.image = Image.open('py_image.ppm')
        self.image_tk = ImageTk.PhotoImage(self.image)
        if self.canvas:
            self.canvas.destroy()
        self.canvas = tk.Canvas(self.master, width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.pack()

        # display zoom level on canvas
        self.canvas.create_rectangle(0, 0, 120, 30, fill="black", outline="")
        self.canvas.create_text(10, 8, anchor=tk.NW,text="Zoom: " + '{:.{digits}e}'.format(1/self.z, digits=2), fill="white")

    def zoom(self, event):
        if self.canvas:
            if event.delta > 0:
                old_z = self.z
                self.z /= (1 + event.delta / 20)
                self.x += (event.x - self.w/2)/(self.w) * self.z
                self.y += (event.y - self.h/2)/(self.h) * self.z
                self.run_and_open()
            else:
                old_z = self.z
                self.z *= (1 - event.delta / 20)
                self.x -= (event.x - self.w/2)/(self.w) * self.z
                self.y -= (event.y - self.h/2)/(self.h) * self.z
                self.run_and_open()

    def compile(self):
        write_c = c_gen.c_program(self.x_eq, self.y_eq)
        if write_c == 0:
            compile_c()
        else:
            print("C program not compiled!")

    def create_render_window(self):
        if not self.render_window_open:
            self.render_window_open = True
            self.render_window = tk.Toplevel(self.master)
            self.render_window.title("Render Settings")
            self.label_x = tk.Label(self.render_window, text="Width ")
            self.label_x.grid(row=0, column=0)
            self.entry_x = tk.Entry(self.render_window)
            self.entry_x.grid(row=0, column=1)
            self.label_y = tk.Label(self.render_window, text="Height ")
            self.label_y.grid(row=1, column=0)
            self.entry_y = tk.Entry(self.render_window)
            self.entry_y.grid(row=1, column=1)
            self.render_window_ok_button = tk.Button(self.render_window, text="OK", command=self.render_image)
            self.render_window_ok_button.grid(row=2, column=0, columnspan=2)

    def render_image(self):
        w = self.entry_x.get()
        h = self.entry_y.get()
        c = self.clipping_eq
        self.render_window.destroy()
        self.render_window_open = False
        run_c(self.z, self.x, self.y, w, h, c, 'render.ppm')
        # show info message
        messagebox.showinfo("Render Complete", "Rendered image saved to render.ppm")


def compile_c():
    result = subprocess.run(['gcc-12', '-O3', '-fopenmp', 'py_code.c', '-o', 'py_compiled'], capture_output=True)
    if result.returncode == 0:
        # print('C program compiled successfully!')
        messagebox.showinfo("Compile Complete", "C program compiled successfully!")
    else:
        print(result.stderr)


def run_c(z, x, y, w, h, clipping, filename='py_image.ppm'):
    result = subprocess.run(['./py_compiled', '-z', str(z), '-x', str(x), '-y', str(y), '-w', str(w), '-h', str(h), '-c', clipping, '-o', filename], capture_output=False)
    # print('C program ran successfully!')


def main():
    root = tk.Tk()
    app = PPMViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
