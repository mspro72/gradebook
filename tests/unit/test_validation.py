import pytest
from gradebook_core.validation import validate_grade, validate_name


def test_validate_grade_accepts_valid_value():
    assert validate_grade(3) == 3


def test_validate_grade_accepts_boundaries():
    assert validate_grade(1) == 1
    assert validate_grade(5) == 5


def test_validate_grade_raises_on_too_low():
    with pytest.raises(ValueError):
        validate_grade(0)


def test_validate_grade_raises_on_too_high():
    with pytest.raises(ValueError):
        validate_grade(6)


def test_validate_grade_raises_on_string():
    with pytest.raises(TypeError):
        validate_grade("4")


def test_validate_name_returns_stripped_name():
    assert validate_name("  Александр  ") == "Александр"


def test_validate_name_accepts_normal_name():
    assert validate_name("Павел") == "Павел"


def test_validate_name_raises_on_empty():
    with pytest.raises(ValueError):
        validate_name("")


def test_validate_name_raises_on_spaces_only():
    with pytest.raises(ValueError):
        validate_name("   ")