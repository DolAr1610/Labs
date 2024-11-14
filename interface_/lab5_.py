import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import business.lab5

class DigitalSignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSS Digital Signature Tool")
        self.root.geometry("500x600")

        self.private_key_path = None
        self.public_key_path = None

        self.create_widgets()

    def create_widgets(self):
        # Title label
        tk.Label(self.root, text="Digital Signature Tool", font=("Arial", 16)).pack(pady=10)

        # Generate keys button
        self.generate_key_btn = tk.Button(self.root, text="Generate Keys", command=self.generate_keys, width=20)
        self.generate_key_btn.pack(pady=5)

        # Load private key button
        self.load_private_key_btn = tk.Button(self.root, text="Load Private Key", command=self.load_private_key, width=20)
        self.load_private_key_btn.pack(pady=5)

        # Load public key button
        self.load_public_key_btn = tk.Button(self.root, text="Load Public Key", command=self.load_public_key, width=20)
        self.load_public_key_btn.pack(pady=5)

        # Sign text button
        self.sign_text_btn = tk.Button(self.root, text="Sign Text", command=self.sign_text, width=20)
        self.sign_text_btn.pack(pady=5)

        # Verify text signature button
        self.verify_text_btn = tk.Button(self.root, text="Verify Text Signature", command=self.verify_text_signature, width=20)
        self.verify_text_btn.pack(pady=5)

        # Sign file button
        self.sign_file_btn = tk.Button(self.root, text="Sign File", command=self.sign_file, width=20)
        self.sign_file_btn.pack(pady=5)

        # Verify file button
        self.verify_file_btn = tk.Button(self.root, text="Verify File Signature", command=self.verify_file, width=20)
        self.verify_file_btn.pack(pady=5)

        # Text input for signing
        tk.Label(self.root, text="Text to Sign:").pack(pady=5)
        self.text_input = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=5)
        self.text_input.pack(pady=5)

        # Signature display and input box
        tk.Label(self.root, text="Signature (Hex):").pack(pady=5)
        self.signature_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=5)
        self.signature_text.pack(pady=5)

    def generate_keys(self):
        """Generate new keys and save them to chosen file paths."""
        private_key_path = filedialog.asksaveasfilename(defaultextension=".pem", title="Save Private Key",
                                                        filetypes=[("PEM files", "*.pem")])
        public_key_path = filedialog.asksaveasfilename(defaultextension=".pem", title="Save Public Key",
                                                       filetypes=[("PEM files", "*.pem")])
        if private_key_path and public_key_path:
            business.lab5.generate_keys(private_key_path, public_key_path)
            self.private_key_path = private_key_path
            self.public_key_path = public_key_path
            messagebox.showinfo("Success", "Keys generated and saved successfully.")

    def load_private_key(self):
        """Load the private key from a file."""
        file_path = filedialog.askopenfilename(title="Select Private Key", filetypes=[("PEM files", "*.pem")])
        if file_path:
            self.private_key_path = file_path
            messagebox.showinfo("Success", "Private key loaded successfully.")

    def load_public_key(self):
        """Load the public key from a file."""
        file_path = filedialog.askopenfilename(title="Select Public Key", filetypes=[("PEM files", "*.pem")])
        if file_path:
            self.public_key_path = file_path
            messagebox.showinfo("Success", "Public key loaded successfully.")

    def sign_text(self):
        """Sign text from the input field and display the signature."""
        if not self.private_key_path:
            messagebox.showwarning("Warning", "Please load or generate a private key first.")
            return
        text = self.text_input.get("1.0", tk.END).strip()
        if text:
            signature = business.lab5.sign_data(text.encode(), self.private_key_path)
            self.signature_text.delete(1.0, tk.END)
            self.signature_text.insert(tk.END, signature)

    def verify_text_signature(self):
        """Verify the signature of the input text against the displayed signature."""
        if not self.public_key_path:
            messagebox.showwarning("Warning", "Please load or generate a public key first.")
            return
        text = self.text_input.get("1.0", tk.END).strip()
        hex_signature = self.signature_text.get("1.0", tk.END).strip()
        if text and hex_signature:
            is_valid = business.lab5.verify_signature(text.encode(), hex_signature, self.public_key_path)
            if is_valid:
                messagebox.showinfo("Verification", "Signature is valid.")
            else:
                messagebox.showwarning("Verification", "Signature is invalid.")

    def sign_file(self):
        """Sign a selected file and display the signature."""
        if not self.private_key_path:
            messagebox.showwarning("Warning", "Please load or generate a private key first.")
            return
        file_path = filedialog.askopenfilename(title="Select a file to sign")
        if file_path:
            with open(file_path, "rb") as f:
                data = f.read()
            signature = business.lab5.sign_data(data, self.private_key_path)
            self.signature_text.delete(1.0, tk.END)
            self.signature_text.insert(tk.END, signature)

    def verify_file(self):
        """Verify the signature of a selected file against the displayed signature."""
        if not self.public_key_path:
            messagebox.showwarning("Warning", "Please load or generate a public key first.")
            return
        file_path = filedialog.askopenfilename(title="Select a file to verify")
        if file_path:
            hex_signature = self.signature_text.get("1.0", tk.END).strip()
            with open(file_path, "rb") as f:
                data = f.read()
            is_valid = business.lab5.verify_signature(data, hex_signature, self.public_key_path)
            if is_valid:
                messagebox.showinfo("Verification", "Signature is valid.")
            else:
                messagebox.showwarning("Verification", "Signature is invalid.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalSignatureApp(root)
    root.mainloop()
