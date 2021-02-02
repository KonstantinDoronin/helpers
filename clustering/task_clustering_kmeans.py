import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, StandardScaler
data = pd.read_excel(r'C:\Users\kv.doronin\Desktop\Посещаемость_ГП_Python\082018\test_kmeans.xlsx', na_values='?')#подгружаем данные в данных содержатся пустые ячейки
print(data.head())
print(data.describe())
# normalize data
scaler = StandardScaler()
X = scaler.fit_transform(data.drop('user', 1))
print(X)
# clustering
n_clusters = 5
km = KMeans(n_clusters = n_clusters)
# fit & predict clusters
data['cluster'] = km.fit_predict(X)
# results - we should have 3 clusters: [0,1,2]
print(data)
# Имя и название файла ниже можно изменять. Если файл не существует, то будем создан sheet_name - имя листа на который будет записан результат
writer = pd.ExcelWriter(r'C:\Users\kv.doronin\Desktop\Посещаемость_ГП_Python\082018\research_kmeans.xlsx')
data.to_excel(writer, sheet_name = 'kmeans')
writer.save()
# cluster's centroids
#print(km.cluster_centers_)
#чтобы предсказать кластеры для новых строк — надо сначала нормализовать данные используя тот же scaler:
#X_new = scaler.transform(new_data.drop('Пользователь', 1))
#и собственно предсказание кластера:
#new_data['cluster'] = km.predict(X_new)
from matplotlib import pyplot as plt
import seaborn as sns
ax = sns.boxplot(x="bill", y="lenta_bill", hue="cluster", data=data)  # RUN PLOT
plt.show()
