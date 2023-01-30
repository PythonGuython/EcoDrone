import folium
import numpy as np
import json
import geopandas as gpd

m_to_lat = .001/111                #based on rule of thumb that 1 degree of corresponds to 111km
m_to_long = .001/73                #1 degree of longitude corresponds to 73km
satbaev_gps = [43.23720, 76.93171] #latitude, longitude
grid_size = 5                      #square grid length and width **NEED TO IMPLEMENT**
distance = 30                      #distance between data points in meters

def geo_grid(points):
    '''
    input: list of coordinates as tuples, distance between points in meters
    output: geojson feature collection
    '''
    grid = {
        "type": "FeatureCollection",
        "features": []
    }
    for point in points:
        #points must be ordered counter-clockwise. I start with bottom left
        lat_midlength = distance*m_to_lat/2
        long_midlength = distance*m_to_long/2
        #IMPORTANT: geojson should be longitude, latitude. Polygons start and end with the same point
        p1 = (point[1] - long_midlength, point[0] - lat_midlength)
        p2 = (point[1] - long_midlength, point[0] + lat_midlength)
        p3 = (point[1] + long_midlength, point[0] + lat_midlength)
        p4 = (point[1] + long_midlength, point[0] - lat_midlength)
        square = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": []
            }
        }
        square["geometry"]["coordinates"].append([p1,p2,p3,p4,p1])
        grid["features"].append(square)
    with open("geo_data.json", "w") as file_obj:
        json.dump(grid, file_obj, indent=4)
    return None

lat = np.linspace(-10,10, num = 3)*m_to_lat + satbaev_gps[0]
long = np.linspace(-10,10, num = 3)*m_to_long +satbaev_gps[1]
mesh = np.meshgrid(lat, long)
positions = list(zip(*(x.flat for x in mesh))) #list of tuples
geo_grid(positions)
geojson = gpd.read_file('geo_data.json')
print(geojson.head())
m = folium.Map(satbaev_gps, zoom_start=20)
geo_j = folium.GeoJson(data=geojson, style_function=lambda x: {'fillColor': 'orange'})
geo_j.add_to(m)       
m.save("satbaev_heat_map.html")