# -*- coding: utf-8 -*-

"""
Created on 12. 06. 2026 at 14:14:44

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
    Testing
"""
import os
import numpy as np
import pytest
from cviceni_01 import (
    load_data, BasicStatistics, Scaler,
    EuclideanDistance, ManhattanDistance, CosineCoeficient,
)

# --- Sdílená testovací data (bez CSV) ---
DATA = np.array([
    [1.0, 2.0, 3.0],
    [4.0, 5.0, 6.0],
    [7.0, 8.0, 9.0],
    [2.0, 4.0, 6.0],
])

DATASET = "All_Pokemon.csv"

# --- load_data (přeskočeno, pokud dataset chybí) ---
@pytest.mark.skipif(not os.path.exists(DATASET), reason="Dataset není přítomen")
def test_load_data_returns_ndarray():
    """Testuje, zda funkce load_data vrací data jako numpy array."""
    data, _ = load_data(DATASET)
    assert isinstance(data, np.ndarray)

@pytest.mark.skipif(not os.path.exists(DATASET), reason="Dataset není přítomen")
def test_load_data_returns_header():
    """Testuje, zda funkce load_data vrací header jako seznam."""
    data, header = load_data(DATASET)
    assert isinstance(header, list)
    assert len(header) == data.shape[1]

@pytest.mark.skipif(not os.path.exists(DATASET), reason="Dataset není přítomen")
def test_load_data_is_numeric():
    """Testuje, zda načtená data jsou numerická."""
    data, _ = load_data(DATASET)
    assert np.issubdtype(data.dtype, np.number)

# --- Scaler ---
def test_zscore_mean_near_zero():
    """Testuje, zda z-score normalizace posouvá průměr každého sloupce blízko nule."""
    result = Scaler(DATA).z_score()
    assert np.allclose(result.mean(axis=0), 0, atol=1e-9)

def test_zscore_std_near_one():
    """Testuje, zda z-score normalizace nastavuje směrodatnou odchylku každého sloupce na 1."""
    result = Scaler(DATA).z_score()
    assert np.allclose(result.std(axis=0), 1, atol=1e-9)

def test_zscore_shape_preserved():
    """Testuje, zda z-score normalizace zachovává původní tvar dat."""
    result = Scaler(DATA).z_score()
    assert result.shape == DATA.shape

def test_minmax_range():
    """Testuje, zda Min-Max normalizace nastavuje hodnoty do rozsahu [0, 1]."""
    result = Scaler(DATA).min_max()
    assert result.min() >= 0.0 - 1e-9
    assert result.max() <= 1.0 + 1e-9

def test_minmax_shape_preserved():
    """Testuje, zda Min-Max normalizace zachovává původní tvar dat."""
    result = Scaler(DATA).min_max()
    assert result.shape == DATA.shape

# --- Distance ---
def test_euclidean_known_value():
    """Testuje, zda EuclideanDistance vrací správnou vzdálenost pro známé vektory."""
    d = EuclideanDistance().calculate(np.array([0, 0]), np.array([3, 4]))
    assert np.isclose(d, 5.0)

def test_euclidean_self_distance():
    """Testuje, zda vzdálenost mezi vektorem a sebou samým je 0."""
    v = np.array([1.0, 2.0, 3.0])
    assert np.isclose(EuclideanDistance().calculate(v, v), 0.0)

def test_manhattan_known_value():
    """Testuje, zda ManhattanDistance vrací správnou vzdálenost pro známé vektory."""
    d = ManhattanDistance().calculate(np.array([0, 0]), np.array([3, 4]))
    assert np.isclose(d, 7.0)

def test_cosine_parallel_vectors():
    """Testuje, zda CosineCoeficient vrací 1 pro paralelní vektory (úhel 0°)."""
    a = np.array([1.0, 2.0])
    b = np.array([2.0, 4.0])
    assert np.isclose(CosineCoeficient().calculate(a, b), 1.0, atol=1e-9)

def test_cosine_opposite_vectors():
    """Testuje, zda CosineCoeficient vrací -1 pro opačné vektory (úhel 180°)."""
    a = np.array([1.0, 0.0])
    b = np.array([-1.0, 0.0])
    assert np.isclose(CosineCoeficient().calculate(a, b), -1.0, atol=1e-9)

def test_cosine_perpendicular_vectors():
    """Testuje, zda CosineCoeficient vrací 0 pro kolmé vektory (úhel 90°)."""
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    assert np.isclose(CosineCoeficient().calculate(a, b), 0.0, atol=1e-9)

def test_euclidean_symmetry():
    """Testuje symetrii: d(a, b) == d(b, a)."""
    a, b = np.array([1.0, 2.0]), np.array([4.0, 6.0])
    assert np.isclose(EuclideanDistance().calculate(a, b), EuclideanDistance().calculate(b, a))

# --- Distance matrix ---
def test_distance_matrix_shape():
    """Testuje, zda vytvořená matice vzdáleností má správný tvar (n_samples x n_samples)."""
    dm = EuclideanDistance().create_distance_matrix(DATA)
    assert dm.shape == (len(DATA), len(DATA))

def test_distance_matrix_diagonal_zero():
    """Testuje, zda diagonální prvky matice vzdáleností jsou 0 (vzdálenost k sobě samému)."""
    dm = EuclideanDistance().create_distance_matrix(DATA)
    assert np.allclose(np.diag(dm), 0.0)

def test_distance_matrix_symmetric():
    """Testuje, zda matice vzdáleností je symetrická (dm[i, j] == dm[j, i])."""
    dm = EuclideanDistance().create_distance_matrix(DATA)
    assert np.allclose(dm, dm.T)

# --- BasicStatistics assert validation ---
# _autorun=False zabraňuje spuštění run() před ověřením assertů
def test_basicstats_rejects_non_ndarray():
    """Testuje, zda BasicStatistics vyhazuje AssertionError pro ne-numpy array vstup."""
    with pytest.raises(AssertionError):
        BasicStatistics([[1, 2], [3, 4]], _autorun=False)

def test_basicstats_rejects_1d():
    """Testuje, zda BasicStatistics vyhazuje AssertionError pro 1D numpy array."""
    with pytest.raises(AssertionError):
        BasicStatistics(np.array([1, 2, 3]), _autorun=False)

def test_basicstats_rejects_string_array():
    """Testuje, zda BasicStatistics vyhazuje AssertionError pro pole řetězců."""
    with pytest.raises(AssertionError):
        BasicStatistics(np.array([["a", "b"], ["c", "d"]]), _autorun=False)

def test_basicstats_accepts_valid_data():
    """Testuje, zda BasicStatistics přijme správná 2D numerická data bez výjimky."""
    stats = BasicStatistics(DATA, _autorun=False)
    assert stats.data is DATA
