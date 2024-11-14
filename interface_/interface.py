import tkinter as tk
from interface_.lab1_ import Lab1App
from interface_.lab2_ import Lab2App
from interface_.lab3_ import Lab3App
from interface_.lab4_ import Lab4App
from interface_.lab5_ import Lab5App

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab Selection")

        self.navigation_frame = tk.Frame(root)
        self.navigation_frame.pack(side=tk.TOP, fill=tk.X)

        self.label = tk.Label(root, text="Choose a Lab:")
        self.label.pack(pady=10)

        self.lab1_button = tk.Button(self.navigation_frame, text="Lab 1", command=self.start_lab1)
        self.lab1_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.lab2_button = tk.Button(self.navigation_frame, text="Lab 2", command=self.start_lab2)
        self.lab2_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.lab3_button = tk.Button(self.navigation_frame, text="Lab 3", command=self.start_lab3)
        self.lab3_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.lab4_button = tk.Button(self.navigation_frame, text="Lab 4", command=self.start_lab4)
        self.lab4_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.lab5_button = tk.Button(self.navigation_frame, text="Lab 5", command=self.start_lab5)
        self.lab5_button.pack(side=tk.LEFT, padx=5, pady=5)


    def start_lab1(self):
        self.open_lab_window(Lab1App)

    def start_lab2(self):
        self.open_lab_window(Lab2App)

    def start_lab3(self):
        self.open_lab_window(Lab3App)

    def start_lab4(self):
        self.open_lab_window(Lab4App)

    def start_lab5(self):
        self.open_lab_window(Lab5App)

    def open_lab_window(self, lab_class):
        lab_root = tk.Toplevel(self.root)
        lab_class(lab_root)
        lab_root.protocol("WM_DELETE_WINDOW", lambda: self.on_lab_close(lab_root))

    def on_lab_close(self, lab_root):
        lab_root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    main_app = MainApp(root)
    root.mainloop()