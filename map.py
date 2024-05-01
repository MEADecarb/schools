import folium
from folium.plugins import Geocoder
import requests

# Define a color palette
color_palette = ["#2C557E", "#fdda25", "#B7DCDF", "#000000"]  # Fixed color format

# Create a base map centered over Maryland
m = folium.Map(location=[39.0458, -76.6413], zoom_start=8)

# Function to add GeoJSON from a URL to a feature group with custom color and pop-up
def add_geojson_from_url(geojson_url, name, color, map_obj):
    feature_group = folium.FeatureGroup(name=name)
    style_function = lambda x: {'fillColor': color, 'color': color}
    response = requests.get(geojson_url)
    geojson_data = response.json()

    geojson_layer = folium.GeoJson(
        geojson_data,
        style_function=style_function
    )

    if name == "MDOT SHA County Boundaries":
        # Use 'County' as the label for 'COUNTY_NAME'
        geojson_layer.add_child(folium.GeoJsonPopup(fields=['COUNTY_NAME'], aliases=['County:'], labels=True))
    elif name == "MD HB 550 Census Tracts":
        # Custom handling for the new GeoJSON layer
        all_fields = list(geojson_data['features'][0]['properties'].keys())
        geojson_layer.add_child(folium.GeoJsonPopup(fields=all_fields, labels=True))

    geojson_layer.add_to(feature_group)
    feature_group.add_to(map_obj)

# Add each GeoJSON source as a separate feature group with a color, label, and pop-up
github_geojson_sources = [
    ("https://services.arcgis.com/njFNhDsUCentVYJW/arcgis/rest/services/MDOT_SHA_County_Boundaries/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson", "MDOT SHA County Boundaries"),
    ("https://raw.githubusercontent.com/MEADecarb/schools/main/MDHB550CensusTracts.geojson", "MD HB 550 Census Tracts")  # Corrected URL for raw GeoJSON
]

for i, (url, name) in enumerate(github_geojson_sources):
    color = color_palette[i % len(color_palette)]
    add_geojson_from_url(url, name, color, m)

# Add Layer Control to toggle feature groups
folium.LayerControl().add_to(m)

# Initialize the geocoder plugin
geocoder = Geocoder(
    collapse=True,
    position='topleft',
    add_marker=True,
    popup_on_found=True,
    zoom=12,
    search_label='address'
)

geocoder.add_to(m)

# Display the map
m
