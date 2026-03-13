import geopandas as gpd
import os

# Найти .shp файл в текущей папке
shp_files = [f for f in os.listdir(".") if f.endswith(".shp")]
print("Найденные .shp файлы:", shp_files)

gdf = gpd.read_file(shp_files[0])
print("\nАтрибуты (колонки):", list(gdf.columns))
print("\nПервые 2 строки:")
print(gdf.head(2))
print("\nСистема координат:", gdf.crs)
print("\nКоличество объектов:", len(gdf))
