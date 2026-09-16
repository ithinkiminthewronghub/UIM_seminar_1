# Cvičení 1: Explorativní analýza dat, předzpracování a metriky vzdálenosti

Toto cvičení je prvním praktickým cvičením předmětu **Umělá inteligence v medicíně**. Cílem je přejít od skriptovacího přístupu k profesionálnímu psaní kódu v čistém Pythonu (`.py`). Student pracuje objektově, využívá typování (Type Hinting) a abstraktní třídy, a učí se psát kód, který je robustní a snadno testovatelný.

---

## Obsah

1. [Cíle cvičení](#cíle-cvičení)
2. [Struktura repozitáře](#struktura-repozitáře)
3. [Instalace a spuštění](#instalace-a-spuštění)
4. [Teoretický základ](#teoretický-základ)
5. [Pokyny k vypracování](#pokyny-k-vypracování)
6. [Lokální testování](#lokální-testování)
7. [Odevzdání](#odevzdání)

---

## Cíle cvičení

Po dokončení tohoto cvičení student:

1. **Umí pracovat objektově** – rozumí třídám, dědičnosti a abstraktním metodám (`ABC`, `@abstractmethod`).
2. **Dokáže validovat vstupní data** pomocí příkazů `assert`.
3. **Detekuje chybějící hodnoty** (NaN) a odlehlé hodnoty pomocí metod Z-skóre a IQR a **data na základě detekce vyčistí**.
4. **Ovládá transformaci dat** – standardizaci a normalizaci nezbytné pro většinu algoritmů strojového učení.
5. **Rozumí geometrickému významu vzdáleností** a dokáže posoudit, zda daná vzdálenostní funkce splňuje axiomy metriky.

---

## Struktura repozitáře

```
cviceni-01-template/
├── cviceni_01.py       # Hlavní soubor s kostrou implementace
├── graphs/             # Výstupní složka pro histogramy (generuje se automaticky)
├── requirements.txt    # Seznam Python závislostí
└── README.md           # Tento soubor
```

> **Poznámka:** Datový soubor `All_Pokemon.csv` není součástí repozitáře. Obdržíte jej od vyučujícího nebo jej stáhněte z odkazu uvedeného v systému Moodle.

---

## Instalace a spuštění

### 1. Vytvoření virtuálního prostředí

```bash
python -m venv .venv
```

Aktivace (Windows):
```bash
.venv\Scripts\activate
```

Aktivace (Linux / macOS):
```bash
source .venv/bin/activate
```

### 2. Instalace závislostí

```bash
pip install -r requirements.txt
```

### 3. Spuštění

```bash
python cviceni_01.py
```

---

## Teoretický základ

### 1. Chybějící hodnoty (NaN)

Reálná data – zejména v medicíně – téměř nikdy nejsou úplná. Chybějící hodnoty jsou reprezentovány jako `NaN` (*Not a Number*, `numpy.nan`). Jejich přítomnost způsobuje, že běžné statistické funkce (`np.mean`, `np.std`) vrátí `NaN` pro celý sloupec, aniž by na to upozornily. Před dalším zpracováním je proto nezbytné chybějící hodnoty detekovat a rozhodnout o strategii jejich řešení – nejčastěji se volí odstranění celého řádku, nebo nahrazení hodnotou (imputace, např. průměrem sloupce).

### 2. Detekce odlehlých hodnot

Odlehlé hodnoty mohou fatálně zkreslit výsledky analýzy nebo chování modelů. V tomto cvičení jsou implementovány dva přístupy:

**Z-skóre** vyjadřuje, o kolik směrodatných odchylek ($\sigma$) se hodnota liší od průměru ($\mu$):

$$Z = \frac{x - \mu}{\sigma}$$

Standardně se za odlehlé považují hodnoty s $|Z| > 3$. Metoda předpokládá přibližně normální rozdělení dat.

**IQR (Mezikvartilové rozpětí)** je robustní metoda nezávislá na rozložení dat. Odlehlé hodnoty leží mimo tzv. hradby:

$$\text{Dolní mez} = Q_1 - k \cdot IQR, \qquad \text{Horní mez} = Q_3 + k \cdot IQR$$

kde $IQR = Q_3 - Q_1$. Typicky se volí $k = 1{,}5$ pro odlehlé hodnoty a $k = 3{,}0$ pro extrémní hodnoty.

### 3. Čištění dat

Detekce sama o sobě data neopraví – její výsledek je potřeba **použít**. Standardizace, normalizace i výpočet vzdáleností proto pracují až s vyčištěnými daty:

1. **Kontrola dat** – odstraňte duplicitní řádky a sloupce, které nejsou příznaky (např. identifikátor). Hodnoty, které nemohou nastat (např. záporná hmotnost), jsou chybou a označí se jako `NaN`.
2. **Detekce** – najděte řádky s NaN a s odlehlými hodnotami. Pro čištění se používá IQR: odlehlé hodnoty zvětšují $\sigma$, a tím se Z-skóre samy „maskují“. Volí se $k = 3$, protože u zešikmených proměnných (např. hmotnost) by $k = 1{,}5$ označilo za odlehlou i velkou část běžných dat.
3. **Odstranění** – řádky s NaN nebo s odlehlou hodnotou z dat vyřaďte.

Ne každá odlehlá hodnota je chyba – v medicíně může jít o skutečně extrémního pacienta. O odstranění dat je proto třeba rozhodovat vědomě.

### 4. Transformace dat

Algoritmy strojového učení jsou citlivé na rozdílné rozsahy proměnných. Proměnná s rozsahem $0{-}1$ a proměnná s rozsahem $0{-}10\,000$ by zkreslila každý algoritmus závislý na vzdálenostech nebo gradientech. V tomto cvičení jsou implementovány tři metody:

| Metoda | Vzorec | Výstupní rozsah |
|---|---|---|
| Z-score (Standardizace) | $(x - \mu)\,/\,\sigma$ | $(-\infty,\,+\infty)$, přičemž $\mu=0$ a $\sigma=1$ |
| Min-Max (Normalizace) | $(x - x_{\min})\,/\,(x_{\max} - x_{\min})$ | $[0,\,1]$ |
| Procentuální normalizace | $x\,/\,\sum x$ | $[0,\,1]$ (relativní podíl na sumě sloupce) |

### 5. Metriky vzdálenosti a axiomy metriky

Vzdálenostní funkce $d(x, y)$ je **metrikou** tehdy a jen tehdy, pokud splňuje čtyři axiomy:

1. **Nezápornost:** $d(x, y) \geq 0$
2. **Identita:** $d(x, y) = 0 \iff x = y$
3. **Symetrie:** $d(x, y) = d(y, x)$
4. **Trojúhelníková nerovnost:** $d(x, z) \leq d(x, y) + d(y, z)$

V cvičení jsou implementovány tři vzdálenostní funkce. Součástí úkolu je posoudit, zda každá z nich tyto axiomy splňuje:

- **Euklidovská vzdálenost** – přímá geometrická vzdálenost v prostoru (délka přepony).
- **Manhattanská vzdálenost** – součet absolutních rozdílů souřadnic; odpovídá pohybu po pravoúhlé mřížce.
- **Cosinový koeficient** – definován jako $\cos(\theta)$, kde $\theta$ je úhel mezi dvěma vektory. Nezávisí na délce vektorů, pouze na jejich orientaci.

---

## Pokyny k vypracování

Otevřete soubor `cviceni_01.py` a postupně nahraďte všechny výskyty `raise NotImplementedError(...)` a komentáře `# TODO` funkčním kódem. Kostra implementace je rozdělena do čtyř logických bloků.

### Blok 0: Načtení dat – funkce `load_data()`

- Načtěte soubor `All_Pokemon.csv` pomocí knihovny `pandas`.
- Z načteného `DataFrame` vyberte **pouze numerické sloupce** – Pokémoni mají rovněž textové atributy (jméno, typ), které do výpočtů nepatří.
- Než data vrátíte, prohlédněte si je: odstraňte **duplicitní řádky**, vyřaďte sloupec `Number` (identifikátor, nikoliv příznak) a **nesmyslné záporné hodnoty** nahraďte `NaN`.
- Funkce vrací dvojici `(np.ndarray, list[str])` – datovou matici a seznam názvů vrácených sloupců.

> **Hint:** `df = pd.read_csv(filepath); df_num = df.select_dtypes(include='number')`. Užitečné metody: `drop_duplicates()`, `drop(columns=...)`, `mask(...)`.

### Blok I: Třída `BasicStatistics`

#### `__init__` – validace vstupních dat

Odkomentujte a doplňte příkazy `assert`. Zkontrolujte:

- zda jsou data typu `np.ndarray`,
- zda jsou dvourozměrná (tabulka má řádky a sloupce),
- zda datový typ prvků odpovídá číselným hodnotám.

#### `identify_nans()`

- Projděte všechny sloupce a zjistěte počet NaN hodnot (`NaN_N`) a indexy příslušných řádků (`NaN_index`).
- Výsledky vypište ve sjednoceném formátu.
- Vraťte **bool masku řádků** (`True` = řádek obsahuje alespoň jednu NaN), např. `rows = np.zeros(n_rows, dtype=bool)` a `rows[indices] = True`.

#### `get_descriptive_stats()`

- Pro každý sloupec spočítejte minimum, maximum a průměr.
- Data obsahují NaN – použijte `np.nanmin`, `np.nanmax` a `np.nanmean`.
- Výsledky zarovnejte pomocí f-strings pro přehledný výpis, například:

```
{název proměnné:<20} | min: {hodnota:>10.4f} | max: {hodnota:>10.4f} | mean: {hodnota:>10.4f}
```

#### `identify_outliers_z()` a `identify_outliers_iqr()`

- Pro každý sloupec detekujte odlehlé hodnoty příslušnou metodou.
- Pozor na NaN – použijte `np.nanmean`, `np.nanstd` a `np.nanpercentile`. S běžnými funkcemi by detekce tiše nenašla žádnou odlehlou hodnotu.
- Vypište počet odlehlých hodnot a indexy řádků, na kterých se nacházejí.
- Stejně jako `identify_nans()` vraťte bool masku řádků.

#### `get_clean_data()`

- Metoda `run()` uloží masky do atributů `self.nan_rows` a `self.outlier_rows` (IQR s $k = 3$).
- Vraťte data bez řádků, ve kterých je alespoň jedna z masek `True`, a vypište, kolik řádků bylo odstraněno.

#### `plot_histograms()`

- Vygenerujte histogram pro každý sloupec a uložte jej jako obrázek do složky `graphs/`.
- Pokud složka neexistuje, vytvořte ji programově – například `pathlib.Path("graphs").mkdir(exist_ok=True)`.
- Histogramy se v bloku `__main__` vykreslují až z vyčištěných dat.

### Blok II: Třída `Scaler`

Implementujte tři transformační metody. Každá přijímá `self.data` a vrací transformované `np.ndarray` stejného tvaru. Operace provádějte po sloupcích (každá proměnná se transformuje nezávisle).

| Metoda | Vzorec |
|---|---|
| `z_score()` | $(x - \mu)\,/\,\sigma$ |
| `min_max()` | $(x - x_{\min})\,/\,(x_{\max} - x_{\min})$ |
| `percentage()` | $x\,/\,\sum x$ |

### Blok III: Hierarchie tříd `Distance`

#### Struktura tříd

```
Distance  (abstraktní bázová třída – ABC)
│
├── is_metric              # abstraktní vlastnost – implementujte v podtřídách
├── calculate(x, y)        # abstraktní metoda    – implementujte v podtřídách
└── create_distance_matrix(data)   # konkrétní metoda – implementujte ZDE (jednou)
     │
     ├── EuclideanDistance
     ├── ManhattanDistance
     └── CosineCoeficient
```

Třída `Distance` je abstraktní (`ABC` https://docs.python.org/3/library/abc.html) a definuje rozhraní, které musí každá dceřiná třída splňovat. Klíčový princip: metoda `create_distance_matrix` je implementována **jednou v bázové třídě** a volá `self.calculate(x, y)`. Díky polymorfismu se toto volání za běhu programu automaticky přesměruje na implementaci příslušné podtřídy – není tedy nutné `create_distance_matrix` implementovat znovu v každé z nich.

#### Dceřiné třídy (`EuclideanDistance`, `ManhattanDistance`, `CosineCoeficient`)

V každé ze tří dceřiných tříd implementujte:

1. **`is_metric`** – vraťte `True` nebo `False` a v docstringu zdůvodněte, zda vzdálenostní funkce splňuje axiomy metriky.
2. **`calculate(x, y)`** – výpočet vzdálenosti mezi dvěma 1D vektory.

#### `create_distance_matrix(data)` – implementujte v bázové třídě `Distance`

Výsledkem je čtvercová symetrická matice tvaru `(n_samples, n_samples)`, kde prvek `[i, j]` obsahuje vzdálenost mezi objekty `i` a `j`. Platí:

- **Diagonála** obsahuje nuly (vzdálenost objektu k sobě samému je 0).
- **Symetrie:** $d(i, j) = d(j, i)$ – vzdálenost stačí spočítat jednou a zapsat na obě symetrická místa.

---

## Lokální testování

Na konci souboru se nachází blok:

```python
if __name__ == "__main__":
    ...
```

Spusťte jej příkazem:

```bash
python cviceni_01.py
```

Blok postupně načte data, spustí analýzu (`BasicStatistics`), data vyčistí (`get_clean_data()`), vypíše statistiky a vykreslí histogramy vyčištěných dat a nakonec na vyčištěných datech otestuje `Scaler` a matici vzdáleností (pro rychlost jen z prvních 10 vzorků).

Pokud kód nevyvolá výjimku `NotImplementedError` a vypíše očekávané výstupy, jsou příslušné části implementovány správně. Blok lze libovolně rozšiřovat o vlastní `print()` příkazy pro průběžné ověřování mezivýsledků.

---

## Odevzdání

Úloha se odevzdává prostřednictvím systému **GitHub Classroom**. Po dokončení implementace proveďte:

```bash
git add cviceni_01.py
git commit -m "Implementace cvičení 1"
git push
```

Po přijetí příkazu `push` se automaticky spustí testovací skripty, které ověří správnost výpočtů. Výsledek bude zobrazen přímo v rozhraní GitHub u vašeho repozitáře formou zelené fajfky (úspěch) nebo červeného křížku (neúspěch).