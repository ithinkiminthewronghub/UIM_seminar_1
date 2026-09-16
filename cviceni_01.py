# -*- coding: utf-8 -*-

"""
Created on 12. 06. 2026 at 10:30:59

Author: Richard Redina
Email: 195715@vut.cz
Affiliation:
         International Clinical Research Center, Brno
         Brno University of Technology, Brno
GitHub: RicRedi

(._.)
 <|>
_/|_

Description:
    Cvičení 1 Umělá inteligence v medicíně
"""
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================================
# NAČTENÍ DAT
# =========================================================================

def load_data(
    filepath: str = "All_Pokemon.csv",
) -> tuple[np.ndarray, list[str]]:
    """
    Úkol: Načtěte data ze souboru CSV pomocí knihovny 'pandas'. Vyberte pouze
    numerické sloupce a převeďte je na numpy array (float).

    Než data vrátíte, prohlédněte si je a zamyslete se:
        - Neobsahuje tabulka duplicitní řádky?
        - Jsou všechny numerické sloupce opravdu příznaky (např. 'Number')?
        - Mohou být hodnoty záporné? Jak naložit s nesmyslnými hodnotami?

    Vrací:
        tuple: (data_array, header)
            - data_array (np.ndarray): Matice dat (pacienti x příznaky)
            - header (list[str]): Seznam názvů sloupců (pouze těch vrácených)
    """
    # TODO: Zde doplňte kód pro načtení
    # Hint: df = pd.read_csv(filepath); df_num = df.select_dtypes(include="number")
    # Užitečné metody DataFrame: drop_duplicates(), drop(columns=...), mask(...)
    raise NotImplementedError("Funkce 'load_data' ještě nebyla implementována!")


# =========================================================================
# I. STATISTIKA
# =========================================================================

class BasicStatistics:
    """
    Třída pro automatický výpočet základních statistik, detekci odlehlých hodnot
    a vizualizaci datové sady.
    """
    def __init__(
        self,
        data: np.ndarray,
        header: list[str] | None = None,
        _autorun: bool = True
        ) -> None:
        """
        Inicializace třídy. Nejprve ověří integritu dat a následně automaticky
        spustí celou analytickou pipeline.
        """
        # --- ÚKOL PRO STUDENTY: VALIDACE VSTUPNÍCH DAT ---
        # assert  Doplň podmínku na to, že vstupní data jsou typu numpy array
        # assert  Doplň podmínku na počet dimenzí (musí být dim=2, tedy 2D tabulka)
        # assert  Doplň podmínku na datový typ prvků (musí obsahovat čísla - int/float)

        self.data: np.ndarray = data

        if header is not None:
            self.header: list[str] = header
        else:
            self.header = [f"Sloupec {i}" for i in range(data.shape[1])]

        # Automatické spuštění celé analýzy hned při vytvoření objektu
        if _autorun:
            self.run()

    def get_descriptive_stats(self) -> None:
        """
        Úkol: Projděte všechny sloupce v matici dat. Pro každý sloupec spočítejte
        min, max a průměr (mean). Výsledky vypište v unifikovaném formátu.
        
        Požadovaný formát výpisu pro každý sloupec:
        {Název proměnné} | min: {hodnota} | max: {hodnota} | mean: {hodnota}

        Pozor: data obsahují NaN, se kterými běžné np.min/np.max/np.mean vrátí NaN.
        Použijte np.nanmin, np.nanmax a np.nanmean.
        """
        raise NotImplementedError("Metoda 'get_descriptive_stats' ještě nebyla implementována!")

    def identify_outliers_z(self, threshold: float = 3.0) -> np.ndarray:
        """
        Úkol: Projděte všechny sloupce. Pomocí Z-skóre identifikujte odlehlé hodnoty.
        Spočítejte, kolik jich v daném sloupci je (Outliers_N) a zjistěte indexy
        řádků, na kterých se nacházejí (Outliers_index). Výsledky unifikovaně vypište.
        Pozor na NaN – použijte np.nanmean a np.nanstd.

        Vrací: Bool masku řádků (True = řádek obsahuje alespoň jednu odlehlou hodnotu).
        """
        raise NotImplementedError("Metoda 'identify_outliers_z' ještě nebyla implementována!")

    def identify_outliers_iqr(self, threshold: float = 1.5) -> np.ndarray:
        """
        Úkol: Projděte všechny sloupce. Pomocí IQR identifikujte odlehlé hodnoty.
        Spočítejte, kolik jich v daném sloupci je (Outliers_N) a zjistěte indexy
        řádků, na kterých se nacházejí (Outliers_index). Výsledky unifikovaně vypište.
        Pozor na NaN – použijte np.nanpercentile.

        Vrací: Bool masku řádků (True = řádek obsahuje alespoň jednu odlehlou hodnotu).
        """
        raise NotImplementedError("Metoda 'identify_outliers_iqr' ještě nebyla implementována!")

    def identify_nans(self) -> np.ndarray:
        """
        Úkol: Projděte všechny sloupce. Spočítejte, kolik v nich je NaN hodnot (NaN_N)
        a zjistěte indexy řádků, na kterých se nacházejí (NaN_index). Výsledky unifikovaně vypište.

        Vrací: Bool masku řádků (True = řádek obsahuje alespoň jednu NaN hodnotu).
        """
        raise NotImplementedError("Metoda 'identify_nans' ještě nebyla implementována!")

    def get_clean_data(self) -> np.ndarray:
        """
        Úkol: Vraťte data bez řádků, které obsahují NaN nebo odlehlou hodnotu (IQR).
        Využijte masky self.nan_rows a self.outlier_rows, které uloží metoda run().
        Vypište, kolik řádků bylo odstraněno.
        """
        raise NotImplementedError("Metoda 'get_clean_data' ještě nebyla implementována!")

    def plot_histograms(self) -> None:
        """
        Úkol: Projděte všechny sloupce a pro každý z nich vygenerujte histogram.
        Grafy ukládejte jako obrázky do složky 'graphs'.
        """
        raise NotImplementedError("Metoda 'plot_histograms' ještě nebyla implementována!")

    def run(self) -> None:
        """
        Spustí celou analytickou pipeline.
        """
        print("\n" + "="*50)
        print(" CHOD ANALÝZY: CHYBĚJÍCÍ HODNOTY")
        print("="*50)
        self.nan_rows = self.identify_nans()

        print("\n" + "="*50)
        print(" CHOD ANALÝZY: ZÁKLADNÍ POPISNÉ STATISTIKY")
        print("="*50)
        self.get_descriptive_stats()

        print("\n" + "="*50)
        print(" CHOD ANALÝZY: DETEKCE ODLEHLÝCH HODNOT (Z-SCORE)")
        print("="*50)
        self.identify_outliers_z()

        # Pro čištění používáme IQR: Z-skóre je zkreslené samotnými odlehlými
        # hodnotami (maskovací efekt). k = 3 odstraní jen extrémní hodnoty.
        print("\n" + "="*50)
        print(" CHOD ANALÝZY: DETEKCE ODLEHLÝCH HODNOT (IQR, k = 3)")
        print("="*50)
        self.outlier_rows = self.identify_outliers_iqr(threshold=3.0)


# =========================================================================
# II. STANDARDIZACE / NORMALIZACE
# =========================================================================

class Scaler:
    """
    Třída zodpovědná za transformaci dat (standardizace a normalizace).
    """
    def __init__(self, data: np.ndarray) -> None:
        """
        Uloží vstupní data do atributu třídy. Vstupem je 2D numpy pole.
        """
        self.data: np.ndarray = np.array(data)

    def z_score(self) -> np.ndarray:
        """
        Úkol: Přepočet všech proměnných do z-score: (x - mean) / std
        Vrací: Transformované numpy pole stejného tvaru.
        """
        raise NotImplementedError("Metoda 'z_score' ještě nebyla implementována!")

    def min_max(self) -> np.ndarray:
        """
        Úkol: Min-Max normalizace: (x - min) / (max - min)
        Vrací: Transformované numpy pole v rozsahu [0, 1].
        """
        raise NotImplementedError("Metoda 'min_max' ještě nebyla implementována!")

    def percentage(self) -> np.ndarray:
        """
        Úkol: Normalizace podílem sumy: x / sum(x) pro každý sloupec zvlášť.
        Vrací: Transformované numpy pole.
        """
        raise NotImplementedError("Metoda 'percentage' ještě nebyla implementována!")


# =========================================================================
# III. VZDÁLENOSTI OBJEKTŮ
# =========================================================================

class Distance(ABC):
    """
    Mateřská (bázová) třída pro výpočet vzdáleností mezi dvěma vektory (objekty).
    """
    def __init__(self) -> None:
        """
        Inicializace třídy. Zde není potřeba žádný atribut, ale můžete si přidat, pokud chcete.
        """
    @property
    @abstractmethod
    def is_metric(self) -> bool:
        """
        Abstraktní vlastnost, která by měla být přepsána v každé dceřiné třídě.
        Vrací: True pokud se jedná o metrickou vzdálenost, False jinak.
        """
        raise NotImplementedError("Tato vlastnost musí být implementována v dceřiné třídě!")
    @abstractmethod
    def calculate(self, x: np.ndarray, y: np.ndarray) -> float:
        """
        Metoda, kterou musí každá dceřiná třída přepsat.
        """
        raise NotImplementedError("Tato metoda musí být implementována v dceřiné třídě!")
    def create_distance_matrix(
        self,
        data: np.ndarray,
        ) -> np.ndarray:
        """
        Úkol: Sestrojte čtvercovou matici vzdáleností tvaru (n_samples x n_samples).
        Pro výpočet vzdálenosti je použita volaná podtřída (např. EuclideanDistance,
        ManhattanDistance, CosineCoeficient). Vrací: Matice vzdáleností, kde element [i, j] obsahuje
        vzdálenost mezi objekty i a j. Diagonální prvky (i, i) by měly být 0, protože vzdálenost
        objektu k sobě samému je vždy 0.
        """
        # assert  Doplň podmínku na to, že vstupní data jsou typu numpy array
        # assert  Doplň podmínku na počet dimenzí (musí být dim=2, tedy 2D tabulka)
        # Create an empty distance matrix
        # for i in range(number of samples):
        #     for j in range(i+1, number of samples):
        #         call self.calculate(x,y) to fill the distance matrix symmetrically
        # return the distance matrix
        raise NotImplementedError("Funkce 'create_distance_matrix' ještě nebyla implementována!")


class EuclideanDistance(Distance):
    """ Třída pro výpočet Euklidovské vzdálenosti mezi dvěma vektory.
    """
    def __init__(self) -> None:
        """
        Inicializace třídy. Zde není potřeba žádný atribut, ale můžete si přidat, pokud chcete."""

    @property
    def is_metric(self) -> bool:
        """Vrací ____, protože Euklidovská vzdálenost _____ definici metriky."""
        return None

    def calculate(self, x: np.ndarray, y: np.ndarray) -> float:
        """Úkol: Spočtěte Euklidovskou vzdálenost mezi 1D vektory x a y."""
        raise NotImplementedError("Metoda 'calculate' v EuclideanDistance nebyla implementována!")


class ManhattanDistance(Distance):
    """ Třída pro výpočet Manhattanské vzdálenosti mezi dvěma vektory.
    """
    def __init__(self) -> None:
        """
        Inicializace třídy. Zde není potřeba žádný atribut, ale můžete si přidat, pokud chcete.
        """

    @property
    def is_metric(self) -> bool:
        """Vrací ____, protože Manhattanská vzdálenost ________ definici metriky."""
        return None
    def calculate(self, x: np.ndarray, y: np.ndarray) -> float:
        """Úkol: Spočtěte Manhattanskou vzdálenost mezi 1D vektory x a y."""
        raise NotImplementedError("Metoda 'calculate' v ManhattanDistance nebyla implementována!")


class CosineCoeficient(Distance):
    """ Třída pro výpočet Cosinového koeficientu mezi dvěma vektory.
    """
    def __init__(self) -> None:
        """
        Inicializace třídy. Zde není potřeba žádný atribut, ale můžete si přidat, pokud chcete."""

    @property
    def is_metric(self) -> bool:
        """Vrací ____, protože Cosinový koeficient ________ definici metriky."""
        return None
    def calculate(self, x: np.ndarray, y: np.ndarray) -> float:
        """Úkol: Spočtěte Cosinový koeficient mezi 1D vektory x a y."""
        raise NotImplementedError("Metoda 'calculate' v CosineCoeficient nebyla implementována!")


# =========================================================================
# MAIN BLOCK (Pro lokální testování)
# =========================================================================
if __name__ == "__main__":
    print("--- Spouštím lokální testování studenta ---")

    try:
        # 1. Test načítání
        dataset, header = load_data("All_Pokemon.csv")
        print(f"Data úspěšně načtena. Tvar: {dataset.shape}")

        # 2. Test Statistiky
        stats = BasicStatistics(dataset, header=header)

        # 3. Test čištění – další kroky pracují pouze s vyčištěnými daty
        clean_data = stats.get_clean_data()
        print(f"Vyčištěná data. Tvar: {clean_data.shape}")

        print("\n" + "="*50)
        print(" ZÁKLADNÍ POPISNÉ STATISTIKY PO VYČIŠTĚNÍ")
        print("="*50)
        clean_stats = BasicStatistics(clean_data, header=header, _autorun=False)
        clean_stats.get_descriptive_stats()

        print("\n" + "="*50)
        print(" GENEROVÁNÍ HISTOGRAMŮ (VYČIŠTĚNÁ DATA)")
        print("="*50)
        clean_stats.plot_histograms()
        print(">>> Všechny histogramy byly úspěšně uloženy.\n")

        # 4. Test Scaleru
        scaler = Scaler(clean_data)
        standardized_data = scaler.z_score()

        # 5. Test Vzdáleností (pro rychlost jen prvních 10 vzorků)
        euclid = EuclideanDistance().create_distance_matrix(clean_data[:10])
        print(f"Matice vzdáleností úspěšně vytvořena. Tvar: {euclid.shape}")

    except NotImplementedError as e:
        print(f"\n[INFO] Chycena výjimka: {e}")
        print("[INFO] To je v pořádku. Pokračujte v implementaci této metody.")
    except AssertionError:
        print("\n[CHYBA] Validace selhala! Vstupní data nesplňují některou z podmínek (assert).")
        raise
