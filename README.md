# Mod28
Тестирование сайта https://www.mirbeer.ru/
Запуск тестов:
python -m pytest -vv --driver Chrome --driver-path webdriver\chromedriver.exe test.py

Тесты:
логин(негативные - цифры, символы, иероглиф, кириллица, 255 символов, пустое)
пароль(негативные - цифры, символы, иероглиф, кириллица, 255 символов, пустое)
регистрация (негативные - цифры, символы, иероглиф, кириллица, 255 символов, пустое)
поиск (негативные - цифры, символы, иероглиф, кириллица, 100 символов, пустое)
правильный логин и пароль, регистация с правильной почтой
сортировка - по возрастанию, убыванию, название.
Добавление товара в корзину
Поиск товара по названию.
Фильтр по цене.
