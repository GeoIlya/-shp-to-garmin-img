import geopandas as gpd
import os

gdf = gpd.read_file("wgs.shp")
os.makedirs("mp_tiles", exist_ok=True)

# Разбиваем на части по 5000 объектов
chunk_size = 5000
chunks = [gdf.iloc[i:i+chunk_size] for i in range(0, len(gdf), chunk_size)]

print(f"Всего объектов: {len(gdf)}, частей: {len(chunks)}")

for chunk_idx, chunk in enumerate(chunks):
    map_id = 63240001 + chunk_idx
    lines = []
    lines.append("[IMG ID]")
    lines.append(f"ID={map_id}")
    lines.append("Name=Лесные кварталы")
    lines.append("Elevation=M")
    lines.append("Levels=5")
    lines.append("Level0=24")
    lines.append("Level1=23")
    lines.append("Level2=22")
    lines.append("Level3=21")
    lines.append("Level4=20")
    lines.append("Zoom0=0")
    lines.append("Zoom1=1")
    lines.append("Zoom2=2")
    lines.append("Zoom3=3")
    lines.append("Zoom4=4")
    lines.append("[END-IMG ID]")
    lines.append("")

    for idx, row in chunk.iterrows():
        geom = row.geometry
        if geom is None:
            continue
        polygons = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]

        for poly in polygons:
            coords = list(poly.exterior.coords)
            lines.append("[POLYGON]")
            lines.append("Type=0x50")
            lines.append(f"Label=Kv{row['Kv']} vid{row['vid']}")  # ← замените на ваши атрибуты
            lines.append("EndLevel=4")
            lines.append("Data0=(" + "),(".join(f"{lat:.6f},{lon:.6f}" for lon, lat in coords) + ")")
            lines.append("[END]")
            lines.append("")

    filename = f"mp_tiles/tile_{chunk_idx:03d}.mp"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Сохранён {filename}")

print("\nГотово! Все тайлы в папке mp_tiles/")
