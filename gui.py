import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


class AppGUI(ctk.CTk):
    def __init__(self, process_image_callback):
        super().__init__()

        self.process_image_callback = process_image_callback

        self.title("AIreader JPG")
        self.geometry("1200x700")

        # Konfiguracja układu siatki (Grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)


        self.image_frame = ctk.CTkFrame(self)
        self.image_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.image_label = ctk.CTkLabel(self.image_frame, text="Wczytaj obraz, aby rozpocząć", font=("Arial", 16))
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)

        self.text_frame = ctk.CTkFrame(self)
        self.text_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.text_editor = ctk.CTkTextbox(self.text_frame, font=("Consolas", 14))
        self.text_editor.pack(expand=True, fill="both", padx=10, pady=10)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.btn_load = ctk.CTkButton(self.button_frame, text="Wczytaj obraz", command=self.open_file)
        self.btn_load.pack(side="left", padx=20, pady=10)

        self.btn_save = ctk.CTkButton(self.button_frame, text="Zapisz tekst (.txt)", command=self.save_to_txt)
        self.btn_save.pack(side="right", padx=20, pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Obrazy", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            processed_img, recognized_text = self.process_image_callback(file_path)

            self.display_image(processed_img)
            self.update_text_editor(recognized_text)

    def display_image(self, img_path_or_pil):
        if isinstance(img_path_or_pil, str):
            img = Image.open(img_path_or_pil)
        else:
            img = img_path_or_pil

        width, height = img.size
        ratio = min(550 / width, 550 / height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=new_size)
        self.image_label.configure(image=ctk_img, text="")

    def update_text_editor(self, text):
        self.text_editor.delete("1.0", "end")
        self.text_editor.insert("1.0", text)

    def save_to_txt(self):
        text = self.text_editor.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Błąd", "Brak tekstu do zapisania!")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Plik tekstowy", "*.txt")]
        )
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Sukces", "Tekst został zapisany!")

if __name__ == "__main__":
    def dummy_callback(path):
        return Image.open(path), "Przykładowy odczytany tekst z AI..."


    app = AppGUI(dummy_callback)
    app.mainloop()