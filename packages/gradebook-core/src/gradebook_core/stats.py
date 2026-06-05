from statistics import mean as _mean, median as _median


def mean(grades: list[int]) -> float:
    """Возвращает среднее значение оценок.

    Args:
        grades: список целых оценок.

    Returns:
        Среднее округлённое до 2 знаков.

    Raises:
        ValueError: если список пустой.
    """
    if not grades:
        raise ValueError("Grade list is empty")
    return round(_mean(grades), 2)


def median(grades: list[int]) -> float:
    """Возвращает медиану оценок.

    Args:
        grades: список целых оценок.

    Returns:
        Медианное значение.

    Raises:
        ValueError: если список пустой.
    """
    if not grades:
        raise ValueError("Grade list is empty")
    return _median(grades)


def min_grade(grades: list[int]) -> int:
    """Возвращает минимальную оценку.

    Args:
        grades: список целых оценок.

    Returns:
        Минимальное значение.

    Raises:
        ValueError: если список пустой.
    """
    if not grades:
        raise ValueError("Grade list is empty")
    return min(grades)


def max_grade(grades: list[int]) -> int:
    """Возвращает максимальную оценку.

    Args:
        grades: список целых оценок.

    Returns:
        Максимальное значение.

    Raises:
        ValueError: если список пустой.
    """
    if not grades:
        raise ValueError("Grade list is empty")
    return max(grades)