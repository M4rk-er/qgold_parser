# Парсер сайта qgold.com

## Для установки:
### 1. Клонировать репозиторий:
```
git@github.com:M4rk-er/qgold_parser.git
```
### 2. Перейдите в директорию с проектом и создайте виртуальное окружение
- Windows:
```
cd qgold_parser && python -m venv venv && source venv/Scripts/activate
```
- Linux:
```
cd qgold_parser && python3 -m venv venv && . venv bin activate
```
### 3. Установите необходимые пакеты и библиотеки:
```
pip install -r requirements.txt
```

### 4. Запустите функции:
```
python main.py

```
```
Требования к проекту: 
- Парсим не все товары, а первую страницу данной категории: https://qgold.com/pl/JewelryRings-2·Stone-Rings и первую страницу данной: https://qgold.com/pl/Jewelry-RingsAdjustable
- Пункты к парсингу: Sizes, MSRP (учесть, что для разных Sizes цена может
отличаться),Product Details ( а так же все, что отображается под show more), все фото и
видео товаров, наличие товара (Out of Stock или In Stock)
- Парсинг должен быть цикличным, то есть скрипт проходится по товарам с заданной в
минутах периодичностью и проверяет изменение каждого пункта
- Вывод спаршенных товаров в Excel таблицу/google sheets/numbers/веб форму, 
оформление в свободной форме

- Парсинг категорий должен происходить параллельно
```
