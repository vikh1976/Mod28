import random

email = 'olath@mail.ru'
password = 'r2XYfa'
neg_email = ['12345', '!@#$%^&*()', '好', 'Кириллица', 'a' * 255, 'b'*1001, '']
neg_password = ['12345', '!@#$%^&*()', '好', 'Кириллица', 'a' * 255, 'b'*1001, '']
neg_search = ['12345', '!@#$%^&*()', '好', 'Кириллица', 'a' * 100, '']
url = 'https://www.mirbeer.ru/'
auth_url = 'https://www.mirbeer.ru/login/'
reg_email = 'test' + str(random.randint(1, 1000)) + '@ddd.com'
search_url = 'https://www.mirbeer.ru/?digiSearch=true&term=&params=%7Csort%3DDEFAULT'
sorted_url = 'https://www.mirbeer.ru/catalog/pivovarenie/drozhzhi/'
sorted_values = ['price;asc', 'price;desc', 'title;asc']
search_values = ['дрожжи', 'бутылк', 'пробк', 'гриль']
filter_check_url = 'https://www.mirbeer.ru/?digiSearch=true&term=%D0%B4%D1%80%D0%BE%D0%B6%D0%B6%D0%B8&params=%7Csort' \
                   '%3DDEFAULT '
