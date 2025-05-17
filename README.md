# 📊🛒Analiza Sprzedaży Produktów
Skrypty do analizy danych sprzedażowych z pliku CSV, identyfikujące kluczowe wzorce zakupowe.
## 🛠️Funkcjonalności  

### 1. Analiza Par Produktów  
Wczytuje plik CSV z zamówieniami i produktami, a następnie wyznacza **najczęściej występujące pary produktów** kupowanych razem.

### 2. Analiza Sprzedaży Wielosztukowej  
Identyfikuje produkty, które były sprzedawane **w ilości >1 szt. w ramach pojedynczego zamówienia**, wraz z liczbą takich zamówień.

## 📌 Dlaczego warto analizować dane sprzedażowe?
Identyfikacja najczęściej kupowanych razem produktów oraz sprzedaży wielosztukowej pozwala:
- **Optymalizować promocje** – tworzyć pakiety produktowe lub oferty bundlowe, które zwiększają średnią wartość zamówienia.
- **Personalizować rekomendacje** – sugerować klientom produkty komplementarne (np. "inni kupowali także...").
- **Planować kampanie marketingowe** – skupiać się na kombinacjach produktów o wysokiej sprzedaży.
- **Zarządzać zapasami** – przewidywać popyt na produkty często kupowane w zestawach.

## 📊 Przykładowe wyniki
### 1. Pary produktów

| PRODUKT 1 | PRODUKT 2 | ILOŚĆ | ZAMÓWIENIA |
|-----------|-----------|----------------:|-------------------------------:|
| P-001     | P-005     | 3               | 1001, 1005, 1008               |
| P-003     | P-007     | 5               | 1002, 1009, 1011, 1015, 1016   |
| P-002     | P-009     | 2               | 1003, 1007                     |

**Przykład interpretacji**:  
Produkty **P-001** i **P-005** były kupowane razem w **3 zamówieniach**, w zamówieniach o ID: 1001, 1005, 1008.

---

### 2. Sprzedaż wielosztukowa

| SKU | ILOŚĆ | LICZBA_WYSTĄPIEŃ | ZAMÓWIENIA |
|-------------|------:|----------------:|------------------------:|
| P-001       | 3     | 8               | 1002, 1005, 1008, ..., 1015 |
| P-005       | 2     | 14              | 1001, 1003, 1006, ..., 1014 |
| P-003       | 5     | 3               | 1007, 1010, 1013        |

**Przykład interpretacji**:  
Produkt **P-001** był kupowany w ilości **3 sztuk** w **8 różnych zamówieniach**.

---

## 🔍 Analiza Asocjacyjna – Opis Metryk
Skrypt analizuje, które produkty są często kupowane razem, wykorzystując klasyczne metryki analizy asocjacyjnej:
- **Support** – jak często para produktów `P1` i `P2` występuje razem we wszystkich zamówieniach.  
- **Confidence** – jak często kupowany jest `P2`, jeśli klient kupił `P1`.  
*(metryka asymetryczna: `P1→P2` ≠ `P2→P1`)*
- **Lift** – jak bardzo obecność `P1` zwiększa prawdopodobieństwo zakupu `P2`, względem niezależnego występowania.  
Interpretacja:
- `lift > 1` – pozytywna zależność (produkty współwystępują częściej niż losowo)
- `lift = 1` – brak zależności
- `lift < 1` – negatywna zależność

Metryki te pomagają wykrywać produkty, które warto promować razem lub analizować pod kątem nawyków zakupowych klientów.

---

📌 **Uwaga:**  
Domyślnie skrypt **nie oblicza metryk** (support, confidence, lift).
Jeśli chcesz otrzymać pełną analizę z metrykami, ustaw w kodzie:
```python
calculate_metrics = True
```

## 📂 Format danych wejściowych
Wymagany plik CSV (`dane.csv`) musi zawierać dokładnie 3 kolumny:
```csv
ID ZAMÓWIENIA,SKU,ILOŚĆ
1001,SKU-04,2
1001,SKU-07,1
1002,SKU-09,3
```
## ▶️ Jak uruchomić?

1. Upewnij się, że masz zainstalowanego **Pythona 3.8 lub nowszego** oraz bibliotekę `pandas`.

2. Zainstaluj pakiet (jeśli nie masz `pandas`):
   ```bash
   pip install pandas
   ```

3. Umieść plik `dane.csv` w tym samym folderze, co skrypty.

4. Uruchom skrypty za pomocą poleceń:
   ```bash
   python ProductPairs.py
   python ProductQuantityAnalysis.py
   ```

5. Wyniki zostaną zapisane automatycznie do plików:
   - `Results_ProductPairs.csv`
   - `Results_ProductQuantityAnalysis.csv`

Pliki CSV możesz otworzyć np. w Excelu lub załadować do narzędzi analitycznych (Power BI, Tableau itp.).

## 🧪 Dane testowe

W repozytorium znajduje się przykładowy plik z danymi testowymi:

- `dane_przykladowe.csv`

Można go użyć do przetestowania działania skryptów bez konieczności przygotowywania własnych danych.

Aby użyć tego pliku:

1. Skopiuj go jako `dane.csv` lub zmodyfikuj nazwy plików wejściowych w skryptach (`input_file = "dane_przykladowe.csv"`).
2. Uruchom skrypty jak opisano w sekcji **"Jak uruchomić?"**.



