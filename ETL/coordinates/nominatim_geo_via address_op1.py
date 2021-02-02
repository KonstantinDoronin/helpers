#receiving geo coordinate from csv by address via Nominatim
import pandas as pd
from geopy.geocoders import Nominatim
df = pd.read_csv(r'', sep='\t', error_bad_lines=False)
print(df.head())
geolocator = Nominatim(user_agent='konstantindoronin10@gmail.com')
latlon = df.addr.apply(lambda addr: geolocator.geocode(addr))
df["Latitude"] = [x.latitude for x in latlon]
df["Longitude"] = [x.longitude for x in latlon]
df.to_excel(r'', sheet_name='выборка', index=False)
