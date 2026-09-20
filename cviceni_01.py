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
import os
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
    df = pd.read_csv(filepath)
    df = df.drop_duplicates()
    df_num = df.select_dtypes(include="number")

    if 'Number' in df_num.columns:
        df_num = df_num.drop(columns=['Number'])

    header = df_num.columns.tolist()
    data_array = df_num.to_numpy(dtype=float)

    #raise NotImplementedError("Funkce 'load_data' ještě nebyla implementována!")

    return data_array, header


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
        assert isinstance(data, np.ndarray)
        assert data.ndim == 2
        assert np.issubdtype(data.dtype, np.number)

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
        for i in range(self.data.shape[1]):
            col = self.data[:, i]
            col_min = np.nanmin(col)
            col_max = np.nanmax(col)
            col_mean = np.nanmean(col)

            print(f"{self.header[i]}: min: {col_min} | max: {col_max} | mean: {col_mean}")



    def identify_outliers_z(self, threshold: float = 3.0) -> np.ndarray:
        """
        Úkol: Projděte všechny sloupce. Pomocí Z-skóre identifikujte odlehlé hodnoty.
        Spočítejte, kolik jich v daném sloupci je (Outliers_N) a zjistěte indexy
        řádků, na kterých se nacházejí (Outliers_index). Výsledky unifikovaně vypište.
        Pozor na NaN – použijte np.nanmean a np.nanstd.

        Vrací: Bool masku řádků (True = řádek obsahuje alespoň jednu odlehlou hodnotu).
        """
        row_mask = np.zeros(self.data.shape[0], dtype=bool)
        for i in range(self.data.shape[1]):
            col = self.data[:, i]
            col_mean = np.nanmean(col)
            col_std = np.nanstd(col)
            z_score = np.abs((col - col_mean) / col_std)
            outliers_idx = np.where(z_score > threshold)[0]
            print(f"{self.header[i]} | Outliers_N: {len(outliers_idx)} | Outliers_index: {outliers_idx.tolist()}")
            row_mask[outliers_idx] = True
        return row_mask

    def identify_outliers_iqr(self, threshold: float = 1.5) -> np.ndarray:
        """
        Úkol: Projděte všechny sloupce. Pomocí IQR identifikujte odlehlé hodnoty.
        Spočítejte, kolik jich v daném sloupci je (Outliers_N) a zjistěte indexy
        řádků, na kterých se nacházejí (Outliers_index). Výsledky unifikovaně vypište.
        Pozor na NaN – použijte np.nanpercentile.

        Vrací: Bool masku řádků (True = řádek obsahuje alespoň jednu odlehlou hodnotu).
        """
        row_mask = np.zeros(self.data.shape[0], dtype=bool)
        for i in range(self.data.shape[1]):
            col = self.data[:, i]
            q25, q75 = np.nanpercentile(col, [25, 75])
            iqr = q75 - q25
            lower_boundary = q25 - threshold * iqr
            upper_boundary = q75 + threshold * iqr
            outliers_idx = np.where((col < lower_boundary) & (col > upper_boundary))[0]
            print(f"{self.header[i]} | Outliers_N: {len(outliers_idx)} | Outliers_index: {outliers_idx.tolist()}")
            row_mask[outliers_idx] = True

        return row_mask


    def identify_nans(self) -> np.ndarray:
        """
        Úkol: Projděte všechny sloupce. Spočítejte, kolik v nich je NaN hodnot (NaN_N)
        a zjistěte indexy řádků, na kterých se nacházejí (NaN_index). Výsledky unifikovaně vypište.

        Vrací: Bool masku řádků (True = řádek obsahuje alespoň jednu NaN hodnotu).
        """
        row_mask = np.zeros(self.data.shape[0], dtype=bool)
        for i in range(self.data.shape[1]):
            col = self.data[:, i]
            nan_idx = np.where(np.isnan(col))[0]
            print(f"{self.header[i]} | NaN_N: {len(nan_idx)} | NaN_index: {nan_idx.tolist()}")
            row_mask[nan_idx] = True

        return row_mask

    def get_clean_data(self) -> np.ndarray:
        """
        Úkol: Vraťte data bez řádků, které obsahují NaN nebo odlehlou hodnotu (IQR).
        Využijte masky self.nan_rows a self.outlier_rows, které uloží metoda run().
        Vypište, kolik řádků bylo odstraněno.
        """
        mask_remove = self.nan_rows | self.outlier_rows
        clean_data = self.data[~mask_remove]
        print(f"Počet odstraněných řádků: {np.sum(mask_remove)}")
        return clean_data



    def plot_histograms(self) -> None:
        os.makedirs("graphs", exist_ok=True)
        for i in range(self.data.shape[1]):
            col = self.data[:, i]
            valid_col = col[~np.isnan(col)]

            plt.figure(figsize=(7, 5))
            plt.hist(valid_col, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
            plt.title(f"Histogram: {self.header[i]}")
            plt.xlabel(self.header[i])
            plt.ylabel("Četnost")
            plt.grid(True, linestyle='--', alpha=0.5)

            safe_title = "".join(c for c in self.header[i] if c.isalnum() or c in (" ", "_")).rstrip()
            safe_title = safe_title.replace(" ", "_").lower()

            plt.tight_layout()
            plt.savefig(os.path.join("graphs", f"hist_{safe_title}.png"))
            plt.close()

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
        mean = np.nanmean(self.data, axis=0)
        std = np.nanstd(self.data, axis=0)
        std_replaced = np.where(std == 0, 1.0, std)
        return (self.data - mean) / std_replaced

    def min_max(self) -> np.ndarray:
        """
        Úkol: Min-Max normalizace: (x - min) / (max - min)
        Vrací: Transformované numpy pole v rozsahu [0, 1].
        """
        min_val = np.nanmin(self.data, axis=0)
        max_val = np.nanmax(self.data, axis=0)
        range_val = max_val - min_val
        range_replaced = np.where(range_val == 0, 1.0, range_val)
        return (self.data - min_val) / range_replaced


def percentage(self) -> np.ndarray:
        """
        Úkol: Normalizace podílem sumy: x / sum(x) pro každý sloupec zvlášť.
        Vrací: Transformované numpy pole.
        """
        sum_val = np.nansum(self.data, axis=0)
        sum_replaced = np.where(sum_val == 0, 1.0, sum_val)
        return self.data / sum_replaced


# =========================================================================
# III. VZDÁLENOSTI OBJEKTŮ
# =========================================================================

class Distance(ABC):
    """
    Mateřská (bázová) třída pro výpočet vzdáleností mezi dvěma vektory (objekty).
    """

    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def is_metric(self) -> bool:
        raise NotImplementedError("Tato vlastnost musí být implementována v dceřiné třídě!")

    @abstractmethod
    def calculate(self, x: np.ndarray, y: np.ndarray) -> float:
        raise NotImplementedError("Tato metoda musí být implementována v dceřiné třídě!")

    def create_distance_matrix(
            self,
            data: np.ndarray,
    ) -> np.ndarray:
        """
        Sestrojí čtvercovou matici vzdáleností tvaru (n_samples x n_samples).
        """
        assert isinstance(data, np.ndarray), "Vstupní data musí být typu numpy.ndarray"
        assert data.ndim == 2, "Vstupní data musí být 2D matice"

        n_samples = data.shape[0]
        dist_matrix = np.zeros((n_samples, n_samples), dtype=float)

        for i in range(n_samples):
            for j in range(i + 1, n_samples):
                dist = self.calculate(data[i], data[j])
                dist_matrix[i, j] = dist
                dist_matrix[j, i] = dist

        return dist_matrix


class EuclideanDistance(Distance):
    """ Třída pro výpočet Euklidovské vzdálenosti mezi dvěma vektory.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def is_metric(self) -> bool:
        """Vrací True, protože Euklidovská vzdálenost splňuje definici metriky."""
        return True

    def calculate(self, x: np.ndarray, y: np.ndarray) -> float:
        """Spočte Euklidovskou vzdálenost mezi 1D vektory x a y."""
        return float(np.sqrt(np.sum((x - y) ** 2)))


class ManhattanDistance(Distance):
    """ Třída pro výpočet Manhattanské vzdálenosti mezi dvěma vektory.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def is_metric(self) -> bool:
        """Vrací True, protože Manhattanská vzdálenost splňuje definici metriky."""
        return True

    def calculate(self, x: np.ndarray, y: np.ndarray) -> float:
        """Spočte Manhattanskou vzdálenost mezi 1D vektory x a y."""
        return float(np.sum(np.abs(x - y)))


class CosineCoeficient(Distance):
    """ Třída pro výpočet Cosinové vzdálenosti (1 - cos_sim) mezi dvěma vektory.
    """

    def __init__(self) -> None:
        super().__init__()

    @property
    def is_metric(self) -> bool:
        """Vrací False, protože Cosinová vzdálenost nesplňuje trojúhelníkovou nerovnost."""
        return False

    def calculate(self, x: np.ndarray, y: np.ndarray) -> float:
        """Spočte Cosinovou vzdálenost mezi 1D vektory x a y."""
        cosine_sim = np.sum(x*y) / ((np.sum(np.square(x)) * np.sum(np.square(y)))**0.5)
        return cosine_sim


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
