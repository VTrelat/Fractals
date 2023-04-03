import subprocess
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class PPMViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("PPM Viewer")
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

        # make window non-resizable
        # self.master.resizable(False, False)

        # create buttons in a frame
        # self.buttons_frame = tk.Frame(master)

        # self.open_button = tk.Button(
        #     self.buttons_frame, text="Open", command=self.open_image)
        # self.quit_button = tk.Button(
        #     self.buttons_frame, text="Quit", command=self.master.quit)
        # self.compile_button = tk.Button(
        #     self.buttons_frame, text="Compile", command=compile_c)
        # self.run_button = tk.Button(
        #     self.buttons_frame, text="Run", command=self.run_and_open)

        # create entry box
        # self.entry_box = tk.Entry(self.buttons_frame)
        # self.entry_box.insert(0, "z_{n+1} = z_{n}^{2} + c")

        # add buttons to GUI on top but left aligned
        # self.buttons_frame.pack(side=tk.TOP, fill=tk.X)
        # self.open_button.pack(side=tk.LEFT)
        # self.quit_button.pack(side=tk.LEFT)
        # self.compile_button.pack(side=tk.LEFT)
        # self.run_button.pack(side=tk.LEFT)
        # self.entry_box.pack(side=tk.LEFT)

        # cascade menu
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Quit", command=self.master.quit)

        self.c_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="C", menu=self.c_menu)
        self.c_menu.add_command(label="Compile", command=compile_c)
        self.c_menu.add_command(label="Run", command=self.run_and_open)

        self.window_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Window", menu=self.window_menu)
        self.window_menu.add_command(label="Reset", command=self.reset_image)

        self.quality_menu = tk.Menu(self.window_menu)
        self.window_menu.add_cascade(label="Quality", menu=self.quality_menu)
        self.quality_menu.add_command(
            label="Very low", command=lambda: self.set_quality(640, 360))
        self.quality_menu.add_command(
            label="Low", command=lambda: self.set_quality(960, 540))
        self.quality_menu.add_command(
            label="Medium", command=lambda: self.set_quality(1280, 720))
        self.quality_menu.add_command(
            label="High", command=lambda: self.set_quality(1600, 900))

        # binds
        self.master.bind("<MouseWheel>", self.zoom)
        self.master.bind("<Configure>", self.display_on_resize)
        self.master.bind("<Command-q>", self.master.quit)
        self.master.bind("<Command-r>", lambda e: self.reset_image())

    def display_on_resize(self, event):
        new_w = event.width - event.width % 4
        new_h = event.height - event.height % 4
        if self.w != new_w or self.h != new_h:
            self.w = new_w
            self.h = new_h
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
            self.canvas = tk.Canvas(
                self.master, width=self.image.width, height=self.image.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.pack()

    def run_and_open(self):
        run_c(self.z, self.x, self.y, self.w, self.h)
        self.image = Image.open('py_image.ppm')
        self.image_tk = ImageTk.PhotoImage(self.image)
        if self.canvas:
            self.canvas.destroy()
        self.canvas = tk.Canvas(
            self.master, width=self.image.width, height=self.image.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.pack()

        # display zoom level on canvas
        self.canvas.create_rectangle(
            0, 0, 120, 30, fill="black", outline="")
        self.canvas.create_text(10, 8, anchor=tk.NW,
                                text="Zoom: " + '{:.{digits}e}'.format(1/self.z, digits=2))

    def zoom(self, event):
        # zoom in or out on mouse wheel scroll
        if event.delta > 0:
            old_z = self.z
            self.z /= (1 + event.delta / 20)
            print(event.x - self.w/2, event.y - self.h/2, self.z)
            self.x += (event.x - self.w/2) * abs(old_z - self.z)/100
            self.y += (event.y - self.h/2) * abs(old_z - self.z)/100
            print(self.x, self.y)
            self.run_and_open()
        else:
            old_z = self.z
            self.z *= (1 - event.delta / 20)
            print(event.x - self.w/2, event.y - self.h/2, self.z)
            self.x -= (event.x - self.w/2) * abs(old_z - self.z)/200
            self.y -= (event.y - self.h/2) * abs(old_z - self.z)/200
            print(self.x, self.y)
            self.run_and_open()


def compile_c():
    result = subprocess.run(['gcc-12', '-O3', '-fopenmp',
                             'parallel.c', '-o', 'py_compiled'], capture_output=True)
    if result.returncode == 0:
        print('C program compiled successfully!')
    else:
        print(result.stderr)


def run_c(z, x, y, w, h, filename='py_image.ppm'):
    subprocess.run(
        ['./py_compiled', '-z', str(z), '-x', str(x), '-y', str(y), '-w', str(w), '-h', str(h), '-o', filename], capture_output=True)
    print('C program ran successfully!')


def main():
    root = tk.Tk()
    app = PPMViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
