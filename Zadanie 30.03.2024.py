import os
import shutil
import threading
from queue import Queue

# Funkcja do przetwarzania folderu
def process_folder(folder_path, destination_folder, extensions):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            _, file_ext = os.path.splitext(file)
            if file_ext.lower() in extensions:
                # Przeniesienie pliku do docelowego folderu
                shutil.move(file_path, destination_folder)
                print(f"Przeniesiono plik: {file_path} do {destination_folder}")

# Funkcja wykonywana przez wątek
def worker():
    while True:
        folder_path, destination_folder, extensions = queue.get()
        process_folder(folder_path, destination_folder, extensions)
        queue.task_done()

# Tworzenie kolejki zadań
queue = Queue()

# Tworzenie wątków
for _ in range(4):  # Możesz dostosować ilość wątków
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

# Lista folderów do przetworzenia
folders_to_process = [
    ("Bałagan", "Sorted", [".txt", ".pdf", ".jpg"]),  # Przykładowa lista folderów
    # Dodaj więcej folderów według potrzeb
]

# Dodanie zadań do kolejki
for folder_path, destination_folder, extensions in folders_to_process:
    queue.put((folder_path, destination_folder, extensions))

# Czekanie na zakończenie wszystkich zadań
queue.join()
