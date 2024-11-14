import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText
from business.lab2 import MD5
from business.lab3 import RC5CBCPad
from business.lab1 import LemerGenerator


class Lab3App:
    def __init__(self, root):
        self.root = root
        self.root.title("RC5 CBC Pad Encryption/Decryption")
        self.root.geometry("600x400")

        self.saved_password = None


        self.passcode_label = tk.Label(root, text="Enter the password for encryption/decryption:")
        self.passcode_label.pack()
        self.passcode_entry = tk.Entry(root, show='*')
        self.passcode_entry.pack()

        self.encrypt_file_button = tk.Button(root, text="Encrypt a File", command=self.encrypt_file)
        self.encrypt_file_button.pack(pady=5)

        self.decrypt_file_button = tk.Button(root, text="Decrypt a File", command=self.decrypt_file)
        self.decrypt_file_button.pack(pady=5)

        self.encrypt_text_button = tk.Button(root, text="Encrypt Text", command=self.encrypt_text)
        self.encrypt_text_button.pack(pady=5)

        self.decrypt_text_button = tk.Button(root, text="Decrypt Text", command=self.decrypt_text)
        self.decrypt_text_button.pack(pady=5)

        self.output_label = tk.Label(root, text="Output:")
        self.output_label.pack(pady=10)

        self.output_text = ScrolledText(root, wrap=tk.WORD, height=10)
        self.output_text.pack()

    def get_rc5_instance(self):
        passcode = self.passcode_entry.get()
        if not passcode:
            messagebox.showerror("Error", "Please enter a password.")
            return None
        self.saved_password = passcode  # Зберігаємо пароль для подальшої перевірки
        md5_service = MD5()
        key = md5_service.hexdigest().encode('utf-8')[:16]
        return RC5CBCPad(key, word_size=32, num_rounds=20)

    def encrypt_file(self):
        rc5 = self.get_rc5_instance()
        if rc5:
            input_filename = filedialog.askopenfilename(title="Select File to Encrypt")
            if not input_filename:
                return

            output_filename = filedialog.asksaveasfilename(title="Save Encrypted File As")
            if not output_filename:
                return

            try:
                rc5.encrypt_file(input_filename, output_filename)
                self.output_text.insert(tk.END, f"File '{input_filename}' encrypted to '{output_filename}'\n")
                messagebox.showinfo("Success", "Password has been saved and file is encrypted.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def decrypt_file(self):
        # Спочатку вибираємо файл для дешифрування
        input_filename = filedialog.askopenfilename(title="Select File to Decrypt")
        if not input_filename:
            return

        output_filename = filedialog.asksaveasfilename(title="Save Decrypted File As")
        if not output_filename:
            return

        # Перевірка, чи збережений пароль для шифрування
        if not self.saved_password:
            messagebox.showerror("Error", "No password has been saved for decryption.")
            return

        # Тепер запитуємо пароль після вибору файлу
        entered_passcode = simpledialog.askstring("Password Check", "Enter the password to decrypt:")
        if entered_passcode != self.saved_password:
            messagebox.showerror("Error", "Incorrect password.")
            return

        # Отримуємо екземпляр RC5 після успішної перевірки пароля
        rc5 = self.get_rc5_instance()
        if rc5:
            try:
                # Дешифруємо файл
                rc5.decrypt_file(input_filename, output_filename)
                self.output_text.insert(tk.END, f"File '{input_filename}' decrypted to '{output_filename}'\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def encrypt_text(self):
        rc5 = self.get_rc5_instance()
        if rc5:
            plaintext = tk.simpledialog.askstring("Input", "Enter plaintext to encrypt:")
            if not plaintext:
                return

            try:
                seed = rc5.generate_seed()
                lemer_generator = LemerGenerator(seed)
                iv = lemer_generator.get_bytes(8)
                ciphertext = rc5.encrypt_console(plaintext.encode('utf-8'), iv)
                self.output_text.insert(tk.END, f'Encrypted text (hex): {(iv + ciphertext).hex()}\n')
                messagebox.showinfo("Success", "Password has been saved and text is encrypted.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def decrypt_text(self):
        if not self.saved_password:
            messagebox.showerror("Error", "No password has been saved for decryption.")
            return

        entered_passcode = simpledialog.askstring("Password Check", "Enter the password to decrypt:")
        if entered_passcode != self.saved_password:
            messagebox.showerror("Error", "Incorrect password.")
            return

        rc5 = self.get_rc5_instance()
        if rc5:
            ciphertext_input = tk.simpledialog.askstring("Input", "Enter ciphertext to decrypt (hex string):")
            if not ciphertext_input:
                return

            try:
                ciphertext = bytes.fromhex(ciphertext_input)
                iv = ciphertext[:8]  # Extract IV (first 8 bytes)
                ciphertext_body = ciphertext[8:]  # Remaining is the ciphertext
                decrypted = rc5.decrypt_console(ciphertext_body, iv)
                self.output_text.insert(tk.END, f'Decrypted text: {decrypted.decode("utf-8")}\n')
            except ValueError as e:
                messagebox.showerror("Error", f"Decryption failed: {e}")
            except Exception as e:
                messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = Lab3App(root)
    root.mainloop()
