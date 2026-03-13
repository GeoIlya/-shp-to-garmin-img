import geopandas as gpd
import osmium
import osmium.osm.mutable

gdf = gpd.read_file("wgs.shp")

writer = osmium.SimpleWriter("wgs.osm")

node_id = -1
way_id = -1

for idx, row in gdf.iterrows():
    geom = row.geometry
    if geom is None:
        continue
    polygons = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]

    for poly in polygons:
        coords = list(poly.exterior.coords)
        node_ids = []

        for lon, lat in coords:
            n = osmium.osm.mutable.Node(
                id=node_id,
                location=osmium.osm.Location(lon, lat)
            )
            writer.add_node(n)
            node_ids.append(node_id)
            node_id -= 1

        w = osmium.osm.mutable.Way(
            id=way_id,
            nodes=node_ids,
            tags={
                "name": f"Kv{row['Kv']} vid{row['vid']}",  # ← замените на ваши атрибуты
                "landuse": "forest",
                "kv": str(row["Kv"]),
                "vid": str(row["vid"])
            }
        )
        writer.add_way(w)
        way_id -= 1

    if idx % 1000 == 0:
        print(f"Обработано: {idx} / {len(gdf)}")

writer.close()
print("Готово! Сохранён wgs.osm")
