import pandas as pd
from itertools import combinations
from collections import Counter, defaultdict

# Nazwy plików wejściowego i wyjściowego
input_file = "dane.csv"
output_file = "Results_ProductPairs.csv"

# Flaga sterująca obliczaniem wskaźników
calculate_metrics = False  # Ustaw na True, aby włączyć liczenie support/confidence/lift

try:
    # Wczytanie pliku CSV
    df = pd.read_csv(input_file, sep=None, engine='python')
    
    # Sprawdzenie, czy plik zawiera odpowiednie kolumny
    if list(df.columns) != ["ID ZAMÓWIENIA", "SKU", "ILOŚĆ"]:
        raise ValueError("Plik CSV powinien zawierać dokładnie trzy kolumny: ID ZAMÓWIENIA, SKU oraz ILOŚĆ.")
except Exception as e:
    # Obsługa błędów podczas wczytywania pliku
    print(f"Błąd podczas wczytywania pliku: {e}")
    df = None

# Funkcja obliczająca wskaźniki support, confidence, lift
def compute_metrics(pairs_counter, orders_map, sku_counts, total_orders):
    result = []
    for (p1, p2), count in pairs_counter.items():
        support = count / total_orders
        confidence = count / sku_counts[p1]
        lift = confidence / (sku_counts[p2] / total_orders)
        orders_str = ";".join(map(str, orders_map[(p1, p2)]))
        result.append((
            p1, p2, count,
            support,
            confidence,
            lift,
            orders_str
        ))
    return pd.DataFrame(result, columns=[
        "PRODUKT 1",
        "PRODUKT 2",
        "ILOŚĆ",
        "SUPPORT",
        "CONFIDENCE P1→P2",
        "LIFT",
        "ZAMÓWIENIA"
    ])

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

    # Zliczanie pojedynczych SKU (do metryk)
    sku_counts = Counter()
    total_orders = len(orders)

    # Przetwarzanie każdego zamówienia
    for order_id, products in zip(orders.index, orders):
        for sku in products:
            sku_counts[sku] += 1
        if len(products) > 1:
            # Generowanie wszystkich możliwych par produktów w zamówieniu
            for pair in combinations(sorted(products), 2):
                # Zliczanie wystąpień par produktów
                product_pairs_counter[pair] += 1
                # Dodawanie numeru zamówienia do mapy par produktów
                orders_map[pair].add(order_id)
    
    # Tworzenie DataFrame z wynikami
    if calculate_metrics:
        result_df = compute_metrics(product_pairs_counter, orders_map, sku_counts, total_orders)
    else:
        result_df = pd.DataFrame([
            (product1, product2, count, ";".join(map(str, orders_map[(product1, product2)])))
            for (product1, product2), count in product_pairs_counter.items()
        ], columns=["PRODUKT 1", "PRODUKT 2", "ILOŚĆ", "ZAMÓWIENIA"])

    try:
        # Zapis wyników do pliku CSV
        result_df.to_csv(output_file, index=False, sep=";", decimal=",")
        print(f"Wynik zapisano do {output_file}")
    except Exception as e:
        # Obsługa błędów podczas zapisywania pliku
        print(f"Błąd zapisu pliku: {e}")
