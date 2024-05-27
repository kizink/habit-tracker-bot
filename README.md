## Совместный проект “Телеграм бот для отслеживания привычек”

Телеграм бот, который позволяет:
- добавлять для отслеживания пользовательские привычки
- отправлять напоминания
- сохранять статистику выполнения
- отправлять мотивирующие сообщения

## Pre-commit hooks

Для проверки стиля оформления кода и документации перед коммитом использованы flake8 и pydocstyle

```bash
pre-commit install
pre-commit run --all-files
```

## Tests

Запустить тесты
```bash
pipenv run python run_tests.py
```

## ToDo
- initial state
- answer formatting
- input checks
- logging
- map num<->habit_id when delete habit
