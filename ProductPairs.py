import pandas as pd
from itertools import combinations
from collections import Counter, defaultdict

# Nazwy plików wejściowego i wyjściowego
input_file = "dane.csv"
output_file = "Results_ProductPairs.csv"

try:
    # Wczytanie pliku CSV
    df = pd.read_csv(input_file, sep=None, engine='python')
    
    # Sprawdzenie, czy plik zawiera odpowiednie kolumny
    if list(df.columns) != ["ID ZAMÓWIENIA", "SKU", "ILOŚĆ"]:
        raise ValueError("Plik CSV powinien zawierać dokładnie trzy kolumny: ID_ZAMOWIENIA, SKU oraz ILOŚĆ.")
except Exception as e:
    # Obsługa błędów podczas wczytywania pliku
    print(f"Błąd podczas wczytywania pliku: {e}")
    df = None

# Jeśli plik został poprawnie wczytany, przystępujemy do przetwarzania danych
if df is not None:
    # Grupowanie produktów według numeru zamówienia
    # STARA WERSJA:
    # orders = df.groupby("ID ZAMÓWIENIA")["SKU"].apply(list)
    # Wersja ta nie usuwała duplikatów produktów w ramach zamówienia, co prowadziło do generowania niepoprawnych par,
    # np. (SKU_1, SKU_1), jeśli ten sam produkt występował wielokrotnie w zamówieniu.

    # NOWA WERSJA: Usunięcie duplikatów produktów w ramach każdego zamówienia za pomocą set()
    # ZMIANA: Użyto set(), aby usunąć duplikaty produktów w ramach każdego zamówienia.
    # Dzięki temu w liście produktów dla każdego zamówienia każdy SKU występuje tylko raz,
    # co eliminuje niepotrzebne pary typu (SKU_1, SKU_1) i zapewnia bardziej wiarygodne wyniki analizy.
    
    orders = df.groupby("ID ZAMÓWIENIA")["SKU"].apply(lambda x: list(set(x)))
    
    # Inicjalizacja licznika par produktów oraz mapy zamówień
    product_pairs_counter = Counter()
    orders_map = defaultdict(set)
    
    # Przetwarzanie każdego zamówienia
    for order_id, products in zip(orders.index, orders):
        # Sprawdzenie, czy zamówienie zawiera więcej niż jeden produkt
        if len(products) > 1:
            # Generowanie wszystkich możliwych par produktów w zamówieniu
            for pair in combinations(sorted(products), 2):
                # Zliczanie wystąpień par produktów
                product_pairs_counter[pair] += 1
                # Dodawanie numeru zamówienia do mapy par produktów
                orders_map[pair].add(order_id)
    
    # Tworzenie DataFrame z wynikami
    result_df = pd.DataFrame([
        (product1, product2, count, ";".join(map(str, orders_map[(product1, product2)])))
        for (product1, product2), count in product_pairs_counter.items()
    ], columns=["PRODUKT 1", "PRODUKT 2", "ILOŚĆ", "ZAMÓWIENIA"])
    
    try:
        # Zapis wyników do pliku CSV
        result_df.to_csv(output_file, index=False)
        print(f"Wynik zapisano do {output_file}")
    except Exception as e:
        # Obsługa błędów podczas zapisywania pliku
        print(f"Błąd zapisu pliku: {e}")