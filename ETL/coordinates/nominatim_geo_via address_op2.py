#receiving geo coordinate from xlsx by address via Nominatim op2
from geopy.geocoders import Nominatim
import pandas as pd
geolocator = Nominatim(user_agent="Kazan_GP", timeout=1000)
df = pd.read_excel(r'', na_values='?', sheet_name='data')#подгружаем данные в данных содержатся пустые ячейки
def eval_results(x):
    try:
        return (x.latitude, x.longitude)
    except:
        return (None, None)
df['city_coord'] = df['Example'].apply(geolocator.geocode).apply(lambda x: eval_results(x))
writer = pd.ExcelWriter(r'', engine='xlsxwriter')#записываем статистику по категорийным данным на отдельный лист
df.to_excel(writer,'data')
writer.save()
print("done")
