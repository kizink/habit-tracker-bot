## Совместный проект “Телеграм бот для отслеживания привычек”

Телеграм бот, который позволяет:
- добавлять для отслеживания пользовательские привычки
- отправлять напоминания
- сохранять и просматривать статистику выполнения
- отправлять мотивирующие сообщения

Требования к проекту
http://uneex.ru/LecturesCMC/PythonDevelopment2024/GraduateProject

## Для запуска нужно установить переменные окружения
Создать файл set_credentials.sh:
```bash
#!/bin/bash

export DB_NAME="..."
export DB_USER="..."
export DB_PASS="..."
export DB_HOST="..."
export DB_PORT="..."
export BOT_TOKEN="..."
```

Далее выполнить:
```bash
chmod +x set_credentials.sh && . ./set_credentials.sh
```

## Pre-commit hooks

Для проверки стиля оформления кода и документации перед коммитом использованы flake8 и pydocstyle

```bash
pre-commit install
pre-commit run --all-files
```

## Локализация
Создать файл po/en_US.UTF-8/LC_MESSAGES/all.mo
```bash
pybabel compile -D all -l en_US.UTF-8 -d po -i po/en_US.UTF-8/LC_MESSAGES/all.po
```
Для выбора русского языка:
```bash
export LC_CTYPE=ru_RU.UTF-8
```
Для выбора английского языка:
```bash
export LC_CTYPE=en_US.UTF-8
```

## Tests

Запустить тестовую базу данных
```bash
docker-compose -f db/test-docker-compose.yml up
```

Запустить тесты
```bash
pipenv run python run_tests.py
```

## Документация
```bash
cd docs
make html
```
Открываем docs/_build/html/index.html 

Аналогично для user_docs

## ToDo
- [x] **(3) тесты**
- [x] **(4) документация**
- [x] **(5) локализация**
- [x] **CI**
- [ ] **деплоймент**
- [ ] поправить начальное состояние (при перезапуске бота, первая команда (если это не /start) не распознается)
- [x] поправить формат ответов (показ списка привычек, выбор удаляемой привычки и мб где-то еще)
- [ ] добавить всевозможные проверки для данных, получаемых от пользователя
- [ ] добавить логирование в обработке ошибок (см. notifier.py)
- [x] при удалении привычки было бы неплохо не показывать настоящий habit_id, выводить привычки 1,2, ...  (если в базе будет 100500 привычек, а у пользователя их всего 2, хочется вводить 1 или 2, а не 100500)
