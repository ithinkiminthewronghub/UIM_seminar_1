# Příklady k procvičení – Cvičení 1

Níže jsou uvedeny příklady určené k výpočtu na papíře. Každý příklad procvičuje jednu část analytické pipeline z `cviceni_01.py`. Vzorce, teoretický základ a definice jsou uvedeny v `README.md`.

---

## Část 1 – Popisné statistiky

**Datová sada** (5 vzorků, 2 příznaky):

| Vzorek | $x_1$ | $x_2$ |
|:------:|:-----:|:-----:|
| $a$    |   2   |  10   |
| $b$    |   6   |   4   |
| $c$    |  10   |   6   |
| $d$    |   4   |   8   |
| $e$    |   8   |   2   |

**Úkoly:**

1.1 Vypočítejte průměr $\mu$ pro oba příznaky.

1.2 Vypočítejte populační rozptyl $\sigma^2$ a směrodatnou odchylku $\sigma$ pro příznak $x_1$.

1.3 Určete $\min$ a $\max$ pro oba příznaky.

1.4 Jsou výsledky pro $x_1$ a $x_2$ symetrické? Proč?

---

## Část 2 – Detekce odlehlých hodnot

**Datový vektor** (8 vzorků, 1 příznak):

$$x = [2,\ 4,\ 4,\ 6,\ 6,\ 4,\ 4,\ 18]$$

**Úkoly:**

2.1 Vypočítejte průměr $\mu$ a populační směrodatnou odchylku $\sigma$.

2.2 Vypočítejte Z-skóre pro hodnotu $18$. Je tato hodnota odlehlá při prahu $|Z| > 3$?

2.3 Seřaďte vektor $x$ a určete kvartily $Q_1$, $Q_3$ a mezikvartilové rozpětí $IQR$.

2.4 Vypočítejte dolní a horní hradbu (threshold $k = 1.5$). Která hodnota leží mimo hradby?

2.5 Porovnejte výsledky metod Z-skóre a IQR. Proč dávají v tomto případě odlišné závěry?

---

## Část 3 – Škálování dat

Použijte příznak $x_1$ z datové sady v Části 1: $x_1 = [2,\ 6,\ 10,\ 4,\ 8]$.

**Úkoly:**

3.1 Proveďte **Min-Max normalizaci**. Zapište výsledný vektor s hodnotami v $[0, 1]$.

3.2 Proveďte **Z-score standardizaci**. Zapište výsledný vektor (výsledky lze ponechat ve tvaru $k/\sqrt{8}$).

3.3 Jaký bude průměr a směrodatná odchylka vektoru po Z-score standardizaci? Odpovězte bez výpočtu.

3.4 Při Min-Max normalizaci je výsledek citlivý na odlehlé hodnoty – proč? Uvažte, co by se stalo, kdyby $x_1$ obsahoval hodnotu $18$ z Části 2.

---

## Část 4 – Metriky vzdálenosti

Pro každý z níže uvedených párů vektorů vypočítejte:

- **Euklidovskou vzdálenost** $d_E$
- **Manhattanskou vzdálenost** $d_M$
- **Cosinový koeficient** $\cos(\theta)$ a z něj **Cosinovu vzdálenost** $d_C = 1 - \cos(\theta)$

---

**Pár 1:** $\mathbf{a} = [3,\ 4]$, $\quad \mathbf{b} = [6,\ 8]$

**Pár 2:** $\mathbf{a} = [4,\ 3]$, $\quad \mathbf{b} = [-4,\ -3]$

**Pár 3:** $\mathbf{a} = [3,\ 4]$, $\quad \mathbf{b} = [-4,\ 3]$

**Pár 4:** $\mathbf{a} = [2,\ 0]$, $\quad \mathbf{b} = [1,\ 1]$

---

**Doplňující úkoly:**

4.5 Seřaďte páry od nejpodobnějších po nejodlišnější podle $d_E$.

4.6 U kterých párů dosahuje $d_C$ krajních hodnot $0$ nebo $2$? Co to geometricky znamená?

4.7 Páry 1 a 2 mají stejné normy jako jiné páry, přesto se liší $d_E$. Proč nestačí znát pouze délku vektorů?

---

## Část 5 – Matice vzdáleností

Pro následující trojici vektorů sestavte matice vzdáleností. Použijte všechny tři metriky z Části 4.

**Datová sada** (3 vzorky, 5 příznaků):

| Vzorek | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ |
|:------:|:-----:|:-----:|:-----:|:-----:|:-----:|
| $a$    |   2   |  −6   |   2   |   0   |   4   |
| $b$    |   0   |  −4   |   8   |   3   |  −1   |
| $c$    |   5   | −12   |   7   |  −5   |   4   |

**Úkoly:**

5.1 Vyplňte tři prázdné matice vzdáleností – pro $d_E$, $d_M$ a $d_C$:

$$D_E = \begin{pmatrix} — & & \\ & — & \\ & & — \end{pmatrix} \qquad D_M = \begin{pmatrix} — & & \\ & — & \\ & & — \end{pmatrix} \qquad D_C = \begin{pmatrix} — & & \\ & — & \\ & & — \end{pmatrix}$$

5.2 Ověřte, že každá matice je symetrická a hlavní diagonála obsahuje nuly. Proč to musí vždy platit?

5.3 Který pár vzorků je nejpodobnější a který nejodlišnější? Závisí pořadí na volbě metriky?

5.4 Vzorek $c$ má největší normu ze všech tří vzorků ($|\mathbf{c}| \approx 16.1$). Přesto je $d_C(\mathbf{a}, \mathbf{c})$ nejmenší Cosinovou vzdáleností v celé matici. Jak je to možné?

5.5 Ověřte trojúhelníkovou nerovnost pro Euklidovskou vzdálenost: $d_E(\mathbf{a}, \mathbf{c}) \leq d_E(\mathbf{a}, \mathbf{b}) + d_E(\mathbf{b}, \mathbf{c})$.