def validate_grade(value: int) -> int:
    
    """Проверяет что оценка целое число от 1 до 5.

    Args:
        value: проверяемое значение оценки.

    Returns:
        Исходное значение если оно корректно.

    Raises:
        TypeError: если value не целое число.
        ValueError: если value вне диапазона 1–5.
    """

    if not isinstance(value, int):
        raise TypeError("Grade must be an integer")
    if value < 1 or value > 5:
        raise ValueError("Grade must be between 1 and 5")
    return value


def validate_name(name: str) -> str:
    """Проверяет что имя непустая строка.

    Args:
        name: проверяемое имя.

    Returns:
        Имя без лишних пробелов по краям.

    Raises:
        ValueError: если строка пустая или состоит из пробелов.
    """
    if not name or not name.strip():
        raise ValueError("Name must not be empty")
    return name.strip()