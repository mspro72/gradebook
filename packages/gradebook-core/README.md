# gradebook-core

Библиотека с основной логикой для сервиса GradeBook: модели данных, валидация и подсчёт статистики оценок.

## Установка

```bash
pip install -i https://test.pypi.org/simple/ gradebook-core
```

## Использование

```python
from gradebook_core.stats import mean, median, min_grade, max_grade
from gradebook_core.validation import validate_grade, validate_name
from gradebook_core.models import Student, Subject, Grade

# Статистика
grades = [4, 5, 3, 5, 4]
mean(grades)      # -> 4.2
median(grades)    # -> 4
min_grade(grades) # -> 3
max_grade(grades) # -> 5

# Валидация
validate_grade(4)   # -> 4
validate_grade(6)   # -> ValueError
validate_name("Иван") # -> "Иван"
```

## Состав

- `models.py` — датаклассы Student, Subject, Grade
- `validation.py` — валидация оценок и имён
- `stats.py` — среднее, медиана, минимум, максимум
