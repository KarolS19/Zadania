import json

# Funkcja do zapisywania danych do pliku
def zapisz_do_pliku(ksiazka_adresowa, nazwa_pliku):
    with open(nazwa_pliku, 'w') as plik:
        json.dump(ksiazka_adresowa, plik)

# Funkcja do wczytywania danych z pliku
def wczytaj_z_pliku(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as plik:
            return json.load(plik)
    except FileNotFoundError:
        return {} 