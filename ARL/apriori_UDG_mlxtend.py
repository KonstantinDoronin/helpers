import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
dff = pd.read_excel(r'C', na_values='?', sheet_name='data')#подгружаем данные в данных содержатся пустые ячейки
print(dff.head())
ddd = dff.pivot_table(values='Сумма', columns='Значение', index='ID')
ddd[np.isnan(ddd)] = 0
ddd[ddd>0]=1
print(ddd.head())
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
transactions = transaction_list(ddd) #создаем список транзакция по каждому клиенту
print(transactions[0])#список магазинов, который посещает клиент под номером [0]
te = TransactionEncoder() # создаем частные наборы с уровнем поддержки (сколько транзакций содержится в датасете) (min_support = 0,2)- это минимум
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)
frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True)
print(frequent_itemsets)
association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)#сгенерируем ассоциативные правила с уровнем доверия (как часто правила срабатывают для всего датасета) 0.1 (очень низкий)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.1)#сгенерируем ассоциативные правила с уровнем независимости (насколько  элементы события зависят друг от друга) больше 1.2
writer = pd.ExcelWriter(r'')#запишем в Excel
rules.to_excel(writer, sheet_name = 'test')
writer.save()
print("все гуд, чувак")