import pandas as pd
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import *
from matplotlib import pyplot as plt
import numpy as np

data = pd.read_excel(r'C:\Users\kv.doronin\Desktop\Посещаемость_ГП_Python\082018\test_hierar.xlsx', na_values='?')#подгружаем данные в данных содержатся пустые ячейки
print(data.head())
# посомтрим основные статистические параметры данных
print(data.describe())
# построим диаграммы рассеивания и гистограммы для столбцов
from pandas.plotting import scatter_matrix
scatter_matrix(data, alpha=0.05, figsize=(10, 10))
plt.show()
# посмотрим наличие корреляций между значениями
print(data.corr())
# Изменяя названия столбцов можно построить диаграммы рассеиванию двух параметров
# Заменяем названия стобцов col1 и col2
col1 = 'bill'
col2 = 'lenta_bill'
plt.figure(figsize=(10, 6))

plt.scatter(data[col1],
            data[col2],
            alpha=0.75,
            color='red')
plt.xlabel(col1)
plt.ylabel(col2)
plt.show()
# Выделим данные, начиная с первой колонки
# Это то, что подлежит анализу
# данную операцию надо проделывать на рядах с названием строк
# следующая команда удаляет столбец client, он не содержаит данных ядл кластеризации
data_for_clust = data.values
#выведем первую строку
print(data_for_clust[0])
# эта библиотека автоматически приведен данные к нормальным значениям
from sklearn import preprocessing
dataNorm = preprocessing.scale(data_for_clust)
# Вычислим расстояния между каждым набором данных, т.е. строками массива data_for_clust
# Вычисляется евклидово расстояние (по умолчанию)
data_dist = pdist(dataNorm, 'euclidean')
print(data_dist)
# Главная функция иерархической кластеризии
# Объедение элементов в кластера и сохранение в специальной переменной (используется ниже для визуализации и выделения количества кластеров
data_linkage = linkage(data_dist, method='average')
print(data_linkage)
# Метод локтя. Позволячет оценить оптимальное количество сегментов. Показывает сумму внутри групповых вариаций
last = data_linkage[-10:, 2]
last_rev = last[::-1]
idxs = np.arange(1, len(last) + 1)
plt.plot(idxs, last_rev)
acceleration = np.diff(last, 2)
acceleration_rev = acceleration[::-1]
plt.plot(idxs[:-2] + 1, acceleration_rev)
plt.show()
# выводим число кластеров
k = acceleration_rev.argmax() + 2
print("clusters:", k)
#МЕТОД ИЕРАРХИЧЕСКОЙ КЛАСТЕРИЗАЦИИ
#импортируем дополнительную библиотеку
from scipy.cluster.hierarchy import fcluster
max_d = 50 #максимальное расстояние, можно изменять
# находим количество кластеров, между которыми растояние более max_d
clusters = fcluster(data_linkage, max_d, criterion='distance')
print(clusters)
k = 5 #заданное количество кластеров. Можно менять
clusters=fcluster(data_linkage, k, criterion='maxclust')
print(clusters)
# рисуем график. Выбираем лучшее с точки зрения разбиения.
plt.figure(figsize=(10, 8))
# изменяя номеря сечений, можем выводить распределения в любых осях
plt.scatter(data_for_clust[:,0], data_for_clust[:,2], c=clusters, cmap='flag')
plt.show()
# к оригинальным данным добавляем
dataI = data
dataI['cluster_no'] = clusters
# Имя и название файла ниже можно изменять. Если файл не существует, то будем создан sheet_name - имя листа на который будет записан результат
writer = pd.ExcelWriter(r'C:\Users\kv.doronin\Desktop\Посещаемость_ГП_Python\082018\research_hierarch.xlsx')
dataI.to_excel(writer, sheet_name = 'boot')
writer.save()
