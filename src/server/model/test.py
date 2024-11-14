from geopy.geocoders import Nominatim
import time

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")


# Sample of the data points to reduce processing time
data_points_sample = [
[-123.2789621, 44.5675374], [-123.2779238, 44.5675293], [-123.2793672, 44.5668333], [-123.2793669, 44.5667817],
 [-123.2778588, 44.5667836], [-123.2768697, 44.5667807], [-123.276861, 44.5672723], [-123.2768627, 44.5674442],
 [-123.2768565, 44.5683322], [-123.276363, 44.5682174], [-123.276364, 44.5685047], [-123.276377, 44.569182],
[-123.2758082, 44.5690788], [-123.2750774, 44.5689806], [-123.2750883, 44.569136], [-123.2745207, 44.5689861],
 [-123.2740349, 44.5699362], [-123.273553, 44.57091], [-123.27308, 44.571861], [-123.272633, 44.572754],
 [-123.272206, 44.57363], [-123.27315, 44.573866], [-123.274091, 44.574106], [-123.2739555, 44.5743832], [-123.2738394, 44.5746217], [-123.2735725, 44.5751688]]

# Function to get location names
def get_coordinates_from_address(coordinates):
    geolocator = Nominatim(user_agent="myapp")
    return geolocator.reverse(coordinates).address

# Getting names for the sample data points
location_names = [get_coordinates_from_address([lat_long[1], lat_long[0]]) for lat_long in data_points_sample]
print("loations are", location_names)

