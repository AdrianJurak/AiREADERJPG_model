import os
import csv
from PIL import Image, ImageDraw

def create_sample_dataset(dataset_dir="dataset"):
    """
    Tworzy przykładową strukturę folderów i plików potrzebną do trenowania EasyOCR.
    Model trenuje się na WYCIĘTYCH słowach, nie na całych stronach.
    """
    images_dir = os.path.join(dataset_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    labels_path = os.path.join(dataset_dir, "labels.csv")


    with open(labels_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

    print(f"Utworzono strukturę danych treningowych w folderze: '{dataset_dir}'")
    print(f"Wygenerowano plik: '{labels_path}'")
    print("\n--- CO DALEJ? ---")
    print("1. Zastąp przykładowe obrazki w 'dataset/images/' swoimi WYCIĘTYMI słowami ze zdjęć.")
    print("2. Zaktualizuj plik 'dataset/labels.csv' wpisując poprawne nazwy plików i to, co jest na nich napisane.")
    print("3. Postępuj zgodnie z instrukcjami z pliku README.md (Krok 3 i 4), aby rozpocząć proces uczenia sztucznej inteligencji.")

if __name__ == "__main__":
    print("Inicjalizacja środowiska do trenowania modelu OCR...")
    create_sample_dataset()
