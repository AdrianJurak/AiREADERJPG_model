# AIreaderJPG - Rozpoznawanie Pisma Odręcznego

Aplikacja z interfejsem graficznym do odczytywania tekstu (w tym pisma odręcznego) ze zdjęć przy użyciu sztucznej inteligencji (EasyOCR).

## 🚀 Szybki start

1. **Zainstaluj wymagane biblioteki:**
   Otwórz terminal w swoim środowisku i uruchom polecenie:
   ```bash
   pip install easyocr customtkinter Pillow
   ```
   *(Opcjonalnie dla kart NVIDIA)* Aby program działał znacznie szybciej, zainstaluj PyTorch z obsługą CUDA, używając polecenia ze strony [pytorch.org](https://pytorch.org/).

2. **Uruchom aplikację:**
   ```bash
   python main.py
   ```

---

## 🧠 Jak dotrenować model do własnego pisma (Fine-Tuning EasyOCR)

EasyOCR jest świetny do druku, ale w przypadku specyficznego pisma odręcznego może wymagać dotrenowania. EasyOCR używa architektury CRNN. Trening polega na douczeniu rozpoznawania znaków na wyciętych fragmentach słów.

Oto pełna instrukcja, jak przygotować dane i wytrenować własny model.

### Krok 1: Przygotowanie danych (Dataset)
Model musi uczyć się na **pojedynczych wyciętych słowach** lub krótkich liniach, a nie na całych stronach A4.
1. Zbierz zdjęcia odręcznego pisma.
2. Wytnij z nich pojedyncze słowa (możesz do tego użyć zewnętrznych narzędzi lub skryptów).
3. Zapisz wycięte słowa w folderze, np. `dataset/images/`.

### Krok 2: Użycie skryptu train.py (Przygotowanie struktury)
Aby ułatwić Ci pracę, stworzyłem plik `train.py`. Jego zadaniem jest wygenerowanie poprawnej struktury folderów oraz pliku `labels.csv`, który jest wymagany przez narzędzie treningowe.
Uruchom go:
```bash
python train.py
```
Skrypt wygeneruje przykładowy folder `dataset` z plikiem `labels.csv`. Musisz podmienić tamtejsze pliki na własne wycinki słów i wpisać poprawny tekst w pliku CSV.

### Krok 3: Pobranie oficjalnego trenera EasyOCR
EasyOCR trenuje się za pomocą osobnego, oficjalnego repozytorium.
1. Sklonuj repozytorium treningowe:
   ```bash
   git clone https://github.com/JaidedAI/EasyOCR.git
   ```
2. Przejdź do folderu `EasyOCR/trainer` i zainstaluj wymagania:
   ```bash
   cd EasyOCR/trainer
   pip install -r requirements.txt
   ```

### Krok 4: Uruchomienie treningu
Gdy masz już przygotowany folder `dataset` z obrazkami i plikiem `labels.csv` (zgodnie z formatem wygenerowanym przez `train.py`), możesz rozpocząć trening.

W folderze `trainer` uruchom:
```bash
python train.py --train_data ../../dataset --valid_data ../../dataset --select_data "/" --batch_ratio 1 --Transformation None --FeatureExtraction VGG --SequenceModeling BiLSTM --Prediction CTC
```
*(Więcej parametrów znajdziesz w dokumentacji w folderze `trainer` repozytorium EasyOCR).*

### Krok 5: Podmiana modelu w aplikacji
Po udanym treningu w folderze `saved_models` pojawi się plik z rozszerzeniem `.pth` (np. `best_accuracy.pth`).
1. Zmień jego nazwę na `custom_model.pth`.
2. Skopiuj go do folderu modeli EasyOCR na swoim komputerze (zazwyczaj to `C:\Users\TwojaNazwa\.EasyOCR\model`).
3. W pliku `main.py` zmień inicjalizację na użycie Twojego modelu:
   ```python
   reader = easyocr.Reader(['pl'], recog_network='custom_model')
   ```