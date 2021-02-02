import pandas as pd
import numpy as np
from pymining import itemmining, assocrules, perftesting
dff = pd.read_excel(r'', na_values='?', sheet_name='data')#подгружаем данные в данных содержатся пустые ячейки
print(dff.head())
dd = dff.replace(to_replace=np.nan, value=0)
print(dd.head())
writer = pd.ExcelWriter(r'C:\Users\kv.doronin\Desktop\test_output_3.xlsx')
dd.to_excel(writer, sheet_name = 'test')
writer.save()
def transaction_list(df): #функция для создания списка транзакция
    list_external=[]
    for i in range(df.shape[0]):
        list_internal=[]
        data=df.iloc[i]
        index=data[data>0]
        for element in index.index:
            list_internal.append(element)
        list_external.append(list_internal)
    return list_external
transactions = transaction_list(dd) #создаем список транзакция по каждому клиенту
print(transactions[0])#список магазинов, который посещает клиент под номером [0]
relim_input = itemmining.get_relim_input(transactions)  #подготавливаем функции для работы
item_sets = itemmining.relim(relim_input, min_support=1)
rules = assocrules.mine_assoc_rules(item_sets, min_support=10, min_confidence=0.3)#устанавливаем пороги поддержки (реализация правила) и порог вероятности
def write_rules2(rul): #функция для записи ассоицативных правил
    retMass=[]
    for el in rul:
        basis=''
        for iterator in iter(el[0]):
            basis=basis+iterator+'-'
        conclusion=''
        for iterator in iter(el[1]):
            conclusion=conclusion+iterator+'-'
        retMass.append([basis, conclusion, str(el[2]), str(el[3])])
    return retMass
rul1 = write_rules2(rules)
df_rules=pd.DataFrame(rul1, columns=('Посыл', 'Следствие', 'Поддержка', 'Достоверность')) #преобразуем выходной массив в DataFrame и сохраним в Excel
writer = pd.ExcelWriter(r'')
df_rules.to_excel(writer, sheet_name = 'test')
writer.save()

