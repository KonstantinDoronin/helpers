#задача замены значений в ячейках <> 0 на имя столбца + значение ячейки
import pandas as pd
import numpy as np
df = pd.read_excel(r'', na_values='?',sheet_name='data')#подгружаем данные в данных содержатся пустые ячейки
df=df.transform(lambda x: np.where(x.isnull(), x, x.name+";"+x.map(str)))
cols = df.columns
df["combined"] = df[cols].apply(lambda x: ','.join(x.dropna()), axis=1) #объединение всех значений в строке и дроп NAN
writer = pd.ExcelWriter(r'', engine='xlsxwriter')#записываем статистику по категорийным данным на отдельный лист
df.to_excel(writer,'data')
writer.save()