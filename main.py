import easyocr
from PIL import Image, ImageDraw
import gui

print("Ładowanie modelu AI...")
reader = easyocr.Reader(['pl', 'en'], gpu=True) # Zmień gpu=True, jeśli masz odpowiednią kartę graficzną NVIDIA
print("Model gotowy!")

def process_image(file_path):
    print(f"Przetwarzam obraz: {file_path}")

    results = reader.readtext(file_path)

    img = Image.open(file_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    recognized_text_lines = []
    
    for (bbox, text, prob) in results:
        xs = [int(point[0]) for point in bbox]
        ys = [int(point[1]) for point in bbox]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)

        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=3)

        recognized_text_lines.append(text)

    full_text = "\n".join(recognized_text_lines)
    
    if not full_text.strip():
        full_text = "Nie udało się rozpoznać żadnego tekstu na obrazie."
        
    return img, full_text

if __name__ == "__main__":
    app = gui.AppGUI(process_image_callback=process_image)
    app.mainloop()
