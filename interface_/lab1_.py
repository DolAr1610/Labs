import tkinter as tk
from tkinter import messagebox
from business.lab1 import generate_lemer_numbers

class Lab1App:
    def __init__(self, root):
        self.root = root
        self.root.title("Lemer Generator Test")

        self.num_pairs_label = tk.Label(root, text="Enter number of pairs (n):")
        self.num_pairs_label.pack()
        self.num_pairs_entry = tk.Entry(root)
        self.num_pairs_entry.pack()

        self.start_button = tk.Button(root, text="Start Test", command=self.start_test)
        self.start_button.pack()

        self.result_text = tk.Text(root, height=15, width=50)
        self.result_text.pack()

    def start_test(self):
        try:
            num_pairs = int(self.num_pairs_entry.get())
            if num_pairs <= 0:
                raise ValueError("Number must be positive.")

            # Call backend function to generate Lemer numbers
            results = generate_lemer_numbers(num_pairs)

            # Display results in the text area
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Pi estimate (Lemer): {results['pi_lemer']}\n")
            self.result_text.insert(tk.END, f"Lemer Period: {results['period']}\n")
            self.result_text.insert(tk.END, "Generated numbers:\n")
            self.result_text.insert(tk.END, ', '.join(map(str, results['generated_numbers'])) + "\n")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = Lab1App(root)
    root.mainloop()
