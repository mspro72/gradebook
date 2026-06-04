import pytest
from gradebook_core.stats import mean, median, min_grade, max_grade


def test_mean_returns_correct_value():
    assert mean([4, 5, 3]) == 4.0


def test_mean_rounds_to_two_decimals():
    assert mean([4, 5, 3, 4]) == 4.0


def test_mean_single_value():
    assert mean([3]) == 3.0


def test_mean_raises_on_empty():
    with pytest.raises(ValueError):
        mean([])


def test_median_returns_correct_value():
    assert median([4, 5, 3]) == 4


def test_median_raises_on_empty():
    with pytest.raises(ValueError):
        median([])


def test_min_grade_returns_correct_value():
    assert min_grade([4, 5, 3]) == 3


def test_min_grade_raises_on_empty():
    with pytest.raises(ValueError):
        min_grade([])


def test_max_grade_returns_correct_value():
    assert max_grade([4, 5, 3]) == 5


def test_max_grade_raises_on_empty():
    with pytest.raises(ValueError):
        max_grade([])