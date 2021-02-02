#задача замены значений в ячейки на значение из название столбца
import pandas as pd
import numpy as np
data = pd.read_excel(r'', na_values='?',sheet_name='data')#подгружаем данные в данных содержатся пустые ячейки
print(data.head())
df = data.loc[:, "а-девелопмент":"d group"].replace(1, pd.Series(data.columns, data.columns))
df = df.replace(0, np.nan)#меняем 0 на NAN по всей таблице
cols = df.columns
print(cols)
df["combined"] = df[cols].apply(lambda x: ','.join(x.dropna()), axis=1) #объединение всех значений в строке и дроп NAN
writer = pd.ExcelWriter(r'')#записываем статистику по категорийным данным на отдельный лист
df.to_excel(writer,'data')
writer.save()
