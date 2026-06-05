# GradeBook

REST API для управления оценками студентов. Написан на Flask + SQLAlchemy, база данных — PostgreSQL. Логика статистики вынесена в отдельный пакет [`gradebook-core`](packages/gradebook-core).

## Стек

- Python 3.11
- Flask 3.x + Flask-SQLAlchemy + Flask-CORS
- PostgreSQL 16
- Poetry (управление зависимостями)
- pytest + pytest-cov (тесты)
- Docker / Docker Compose (деплой)

## Структура проекта

```
gradebook/
├── app/
│   ├── __init__.py          # фабрика приложения
│   ├── config.py            # Config / TestingConfig
│   ├── models.py            # ORM-модели: Student, Subject, Grade
│   └── routes/
│       ├── students.py      # CRUD /students
│       ├── subjects.py      # CRUD /subjects
│       ├── grades.py        # CRUD /grades
│       └── stats.py         # GET  /stats
├── docs/
│   └── diagrams/
│       ├── Sequence.png
│       └── Usecase.png
├── packages/
│   └── gradebook-core/      # переиспользуемая библиотека
│       └── src/gradebook_core/
│           ├── models.py    # датаклассы (без ORM)
│           ├── validation.py
│           └── stats.py
├── tests/
│   ├── conftest.py
│   ├── test_students.py
│   ├── test_subjects.py
│   ├── test_grades.py
│   └── unit/
│       ├── test_stats.py
│       └── test_validation.py
├── compose.yaml
├── Dockerfile
├── pyproject.toml
└── run.py
```

---

## Быстрый старт

### Вариант 1 — Docker Compose (рекомендуется)

Поднимает PostgreSQL и приложение одной командой:

```bash
docker compose up -d
# или через Make:
make compose-up
```

Приложение будет доступно на `http://localhost:5001`.

Остановить:

```bash
docker compose down
# или:
make compose-down
```

### Вариант 2 — локальный запуск

**Требования:** Python 3.11+, Poetry, PostgreSQL.

1. Установите зависимости:

```bash
poetry install
```

2. Скопируйте `.env.example` в `.env` и при необходимости поправьте строку подключения:

```bash
cp .env.example .env
```

По умолчанию ожидается PostgreSQL на `localhost:5432` с пользователем/паролем/БД `gradebook`.

3. Запустите сервер:

```bash
poetry run python run.py
# или:
make run
```

Приложение стартует на `http://localhost:5000`.

---

## Тесты

### Запуск всех тестов

```bash
make test
# эквивалентно:
poetry run pytest tests/
```

### Покрытие кода

```bash
make coverage
# эквивалентно:
poetry run pytest tests/ --cov=app --cov-report=term-missing
```

### Что и как тестируется

Тесты делятся на два уровня:

**Интеграционные** (`tests/`) — проверяют HTTP-эндпоинты через Flask test client. Перед каждым тестом БД полностью пересоздаётся (фикстура `clean_db` в `conftest.py`), поэтому нужен работающий PostgreSQL (переменная `TEST_DATABASE_URL`).

**Юнит-тесты** (`tests/unit/`) — проверяют чистую логику пакета `gradebook-core` без БД и HTTP. Их можно запускать отдельно:

```bash
poetry run pytest tests/unit/
```

---

## API

Базовый URL: `http://localhost:5000` (локально) или `http://localhost:5001` (Docker).

### Студенты `/students`

| Метод  | URL               | Описание                      |
|--------|-------------------|-------------------------------|
| GET    | `/students/`      | Список всех студентов         |
| GET    | `/students/{id}`  | Студент по ID                 |
| POST   | `/students/`      | Создать студента              |
| PUT    | `/students/{id}`  | Обновить данные студента      |
| DELETE | `/students/{id}`  | Удалить студента              |

**POST / PUT body:**
```json
{ "name": "Иван Петров", "email": "ivan@mail.ru" }
```

### Предметы `/subjects`

| Метод  | URL                | Описание                   |
|--------|--------------------|----------------------------|
| GET    | `/subjects/`       | Список всех предметов      |
| GET    | `/subjects/{id}`   | Предмет по ID              |
| POST   | `/subjects/`       | Создать предмет            |
| PUT    | `/subjects/{id}`   | Переименовать предмет      |
| DELETE | `/subjects/{id}`   | Удалить предмет            |

**POST / PUT body:**
```json
{ "name": "Математика" }
```

### Оценки `/grades`

| Метод  | URL             | Описание                    |
|--------|-----------------|-----------------------------|
| GET    | `/grades/`      | Список всех оценок          |
| GET    | `/grades/{id}`  | Оценка по ID                |
| POST   | `/grades/`      | Выставить оценку            |
| PUT    | `/grades/{id}`  | Изменить оценку             |
| DELETE | `/grades/{id}`  | Удалить оценку              |

**POST body:**
```json
{ "student_id": 1, "subject_id": 2, "value": 4.5 }
```

Значение `value` — число от 1 до 5 включительно. При нарушении возвращается `422`.

### Статистика `/stats`

| Метод | URL                        | Описание                              |
|-------|----------------------------|---------------------------------------|
| GET   | `/stats/student/{id}`      | Статистика оценок студента            |
| GET   | `/stats/subject/{id}`      | Статистика оценок по предмету         |

**Пример ответа:**
```json
{
  "mean": 4.25,
  "median": 4.5,
  "min": 3,
  "max": 5,
  "count": 4
}
```

---

## Демо-сценарий

Полный рабочий пример — от запуска до статистики.

**1. Поднимаем проект**
```bash
make compose-up
```

**2. Создаём студента**
```bash
curl -X POST http://localhost:5001/students/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Иван", "email": "ivan@mail.ru"}'
```

**3. Создаём предмет**
```bash
curl -X POST http://localhost:5001/subjects/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Математика"}'
```

**4. Выставляем оценки**
```bash
curl -X POST http://localhost:5001/grades/ \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "subject_id": 1, "value": 4}'

curl -X POST http://localhost:5001/grades/ \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "subject_id": 1, "value": 5}'
```

**5. Смотрим статистику по студенту**
```bash
curl http://localhost:5001/stats/student/1
```
```json
{"count": 2, "max": 5.0, "mean": 4.5, "median": 4.5, "min": 4.0}
```

**6. Проверяем валидацию — оценка 6 вне диапазона**
```bash
curl -X POST http://localhost:5001/grades/ \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "subject_id": 1, "value": 6}'
```
Вернёт `422 Unprocessable Entity` — сервер отклоняет невалидные данные.

**7. Запускаем тесты**
```bash
make test
```
43 положительных теста.

---

## Пакет gradebook-core

Переиспользуемая библиотека с бизнес-логикой, не зависящая от Flask и PostgreSQL.

Опубликована на TestPyPI:
```bash
pip install -i https://test.pypi.org/simple/ gradebook-core
```

Подробнее — в [packages/gradebook-core/README.md](packages/gradebook-core/README.md).

---

## Авторы

- [calexzz](https://github.com/calexzz)
- [mspro72](https://github.com/mspro72)

## Лицензия

MIT
