import easyocr
from PIL import Image, ImageDraw
import gui
import os

print("Ładowanie Twojego autorskiego modelu AI...")

# Ścieżka do folderu, w którym masz plik .pth i en_filtered.py
# '.' oznacza obecny folder
user_net_dir = os.path.abspath('user_network')

reader = easyocr.Reader(['pl', 'en'],
                        gpu=True,
                        model_storage_directory=user_net_dir,
                        user_network_directory=user_net_dir,
                        recog_network='en_filtered')  # Nazwa Twojego modelu (bez .pth)

print("Model gotowy i Twoje wagi zostały wczytane!")


def process_image(file_path):
    print(f"Przetwarzam obraz: {file_path}")

    # Twój model teraz czyta tekst!
    results = reader.readtext(file_path,
                              adjust_contrast=0.1,
                              add_margin=0.15,
                              width_ths=0.7,
                              paragraph=False)

    img = Image.open(file_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    recognized_text_lines = []

    for (bbox, text, prob) in results:
        # EasyOCR bbox to [[x,y], [x,y], [x,y], [x,y]]
        p0, p1, p2, p3 = bbox

        # Rysujemy ramkę
        draw.polygon([*p0, *p1, *p2, *p3], outline="red", width=2)

        # Dodajemy tekst do listy z pewnością (prob)
        recognized_text_lines.append(text)

    full_text = "\n".join(recognized_text_lines)

    if not full_text.strip():
        full_text = "Nie udało się rozpoznać żadnego tekstu na obrazie."

    return img, full_text


if __name__ == "__main__":
    app = gui.AppGUI(process_image_callback=process_image)
    app.mainloop()