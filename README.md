# SHP → Garmin IMG конвертер

Конвертация Polygon/MultiPolygon Shapefile в формат `.img` для GPS-навигаторов Garmin с сохранением атрибутов.

## Задача

Есть Shapefile с лесными кварталами и выделами (атрибуты `Kv` и `vid`). Нужно отобразить границы полигонов с подписями на Garmin.

## Требования

- Python 3.x
- Java (для mkgmap)
- [mkgmap](https://www.mkgmap.org.uk/download/mkgmap.html)

### Установка Python-библиотек

```bash
pip install geopandas gpxpy osmium
```

---

## Пошаговая инструкция

### Шаг 1: Проверить атрибуты файла

```bash
python check.py
```

Скрипт покажет названия колонок, первые строки и систему координат.

---

### Шаг 2: Конвертировать SHP → Polish Map тайлы (.mp)

Откройте `shp_to_mp_split.py` и при необходимости замените названия атрибутов:

```python
track.name = f"Kv{row['Kv']} vid{row['vid']}"  # ← ваши атрибуты
```

Запустите:

```bash
python shp_to_mp_split.py
```

Создастся папка `mp_tiles/` с файлами `tile_000.mp`, `tile_001.mp` и т.д.

---

### Шаг 3: Скомпилировать .mp → .img через mkgmap

**Шаг 3а** — компилируем тайлы с кодировкой (замените путь к mkgmap):

```bash
java -jar C:\mkgmap\mkgmap-r4924\mkgmap.jar --charset=windows-1251 --code-page=1251 --output-dir=img_out mp_tiles\*.mp
```

**Шаг 3б** — объединяем в один gmapsupp.img:

```bash
java -jar C:\mkgmap\mkgmap-r4924\mkgmap.jar --gmapsupp --output-dir=img_out img_out\*.img
```

Готовый файл: `img_out/gmapsupp.img`

---

### Шаг 4: Загрузить на Garmin

1. Подключите Garmin к компьютеру через USB
2. Скопируйте `gmapsupp.img` в папку `Garmin\` на устройстве
3. Перезагрузите устройство
4. Включите карту: **Настройки → Карта → Информация о карте**

---

## Структура репозитория

```
├── check.py             # Проверка атрибутов SHP файла
├── shp_to_mp_split.py   # Конвертация SHP → MP тайлы
├── shp_to_osm.py        # Альтернатив: конвертация SHP → OSM
└── README.md
```

## Примечания

- Файл `gmapsupp.img` на Garmin заменяет существующий — переименуйте старый перед копированием
- Подписи полигонов формируются как `Kv{номер} vid{номер}`
- Скрипты тестировались на файле с ~98 000 полигонов (385 674 треков)
- Предупреждения mkgmap о `different code page` при компиляции в два шага не влияют на результат
