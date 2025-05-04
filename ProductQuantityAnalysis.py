import pandas as pd
from collections import defaultdict

# Nazwy plików wejściowego i wyjściowego
input_file = "dane.csv"
output_file = "Results_ProductQuantityAnalysis.csv"

try:
    # Wczytanie pliku CSV
    df = pd.read_csv(input_file, sep=None, engine='python')

    # Sprawdzenie, czy plik zawiera odpowiednie kolumny
    if list(df.columns) != ["ID ZAMÓWIENIA", "SKU", "ILOŚĆ"]:
        raise ValueError("Plik CSV powinien zawierać dokładnie trzy kolumny: ID_ZAMOWIENIA, SKU i ILOŚĆ.")
except Exception as e:
    # Obsługa błędów podczas wczytywania pliku
    print(f"Błąd podczas wczytywania pliku: {e}")
    df = None

# Jeśli plik został poprawnie wczytany, przystępujemy do przetwarzania danych
if df is not None:
    # Słownik do przechowywania informacji o ilościach produktów w zamówieniach
    product_quantity_map = defaultdict(list)

    # Przetwarzanie każdego wiersza danych
    for _, row in df.iterrows():
        order_id = row["ID ZAMÓWIENIA"]
        sku = row["SKU"]
        quantity = row["ILOŚĆ"]

        # Sprawdzenie, czy ilość jest większa niż 1
        if quantity > 1:
            # Dodanie informacji o ilości produktu w zamówieniu do słownika
            # TYLKO jeśli ilość > 1
            product_quantity_map[(sku, quantity)].append(order_id)

    results = []
    for (sku, quantity), order_ids in product_quantity_map.items():
        # Liczba wystąpień danej ilości produktu
        count = len(order_ids)
        # Lista zamówień, w których wystąpiła dana ilość produktu
        orders = ";".join(map(str, order_ids))
        # Dodanie wyniku do listy
        results.append((sku, quantity, count, orders))

    # Sprawdzenie, czy są jakieś wyniki do zapisania
    if results:
        # Tworzenie DataFrame z wynikami
        result_df = pd.DataFrame(results, columns=["SKU", "ILOŚĆ", "LICZBA_WYSTĄPIEŃ", "ZAMÓWIENIA"])

        try:
            # Zapis wyników do pliku CSV
            result_df.to_csv(output_file, index=False)
            print(f"Wynik zapisano do {output_file}")
        except Exception as e:
            # Obsługa błędów podczas zapisywania pliku
            print(f"Błąd zapisu pliku: {e}")
    else:
        # Informacja, jeśli nie znaleziono pasujących danych
        print("Nie znaleziono żadnych danych do zapisania.")
