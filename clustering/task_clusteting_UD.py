import pandas as pd
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import *
from matplotlib import pyplot as plt
from matplotlib import rc
import numpy as np
from sklearn.cluster import KMeans
# Загрузим данные из xls документа
# При необходимости надо изменить название файла и листа, на котором находятся данные
# Проще всего файл положить в папку, где находиться и сам скрипт. В это случае укажите только название
# sheet_name - название листа, с котрого надо загрузить данные
data = pd.read_excel('/Users/user/Desktop/research_uni.xlsx', sheet_name = 'test')
# команда data.head() выводит первые пять строчек загруженных в переменную дата данных
print(data.tail())
# посомтрим основные статистические параметры данных
print(data.describe())
# построим диаграммы рассеивания и гистограммы для столбцов
from pandas.plotting import scatter_matrix
scatter_matrix(data, alpha=0.05, figsize=(10, 10))
plt.show()
# посмотрим наличие корреляций между значениями
print(data.corr())
# Изменяя названия столбцов можно построить диаграммы рассеиванию двух параметров
# Замените названия стобцов col1 и col2
col1 = 'bill'
col2 = 'income'

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
#проверим результат, выведем первую строку
print(data_for_clust[0])
# загружаем библиотеку препроцесинга данных
# эта библиотека автоматически приведен данные к нормальным значениям
from sklearn import preprocessing
dataNorm = preprocessing.scale(data_for_clust)
# Вычислим расстояния между каждым набором данных,
# т.е. строками массива data_for_clust
# Вычисляется евклидово расстояние (по умолчанию)
data_dist = pdist(dataNorm, 'euclidean')
# Главная функция иерархической кластеризии
# Объедение элементов в кластера и сохранение в
# специальной переменной (используется ниже для визуализации
# и выделения количества кластеров
data_linkage = linkage(data_dist, method='average')
# Метод локтя. Позволячет оценить оптимальное количество сегментов.
# Показывает сумму внутри групповых вариаций
last = data_linkage[-10:, 2]
last_rev = last[::-1]
idxs = np.arange(1, len(last) + 1)
plt.plot(idxs, last_rev)

acceleration = np.diff(last, 2)
acceleration_rev = acceleration[::-1]
plt.plot(idxs[:-2] + 1, acceleration_rev)
plt.show()
k = acceleration_rev.argmax() + 2
print("clusters:", k)
#функция построения дендрограмм
def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata
#
# указываем количество кластеров!
#
nCluster=4

#строим дендрограмму
fancy_dendrogram(
    data_linkage,
    truncate_mode='lastp',
    p=nCluster,
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,
    annotate_above=10,
)
plt.show()

#МЕТОД ИЕРАРХИЧЕСКОЙ КЛАСТЕРИЗАЦИИ
#импортируем дополнительную библиотеку
from scipy.cluster.hierarchy import fcluster
max_d = 50 #максимальное расстояние, можно изменять
# находим количество кластеров, между которыми растояние более max_d
clusters = fcluster(data_linkage, max_d, criterion='distance')
print(clusters)

k=4 #заданное количество кластеров. Можно менять
clusters=fcluster(data_linkage, k, criterion='maxclust')
print(clusters)
# рисуем график. Выбираем лучшее с точки зрения разбиения.
plt.figure(figsize=(10, 8))
# изменяя номеря сечений, можем выводить распределения в любых осях
plt.scatter(data_for_clust[:,0], data_for_clust[:,2], c=clusters, cmap='flag')
plt.show()
# к оригинальным данным добавляем
dataI=data
dataI['cluster_no'] = clusters
# Имя и название файла ниже можно изменять. Если файл не существует, то будем создан
# sheet_name - имя листа на который будет записан результат
#writer = pd.ExcelWriter('/Users/user/Desktop/research_uni.xlsx')
#dataI.to_excel(writer, sheet_name = 'boot')
#writer.save()
#МЕТОД КЛАСТЕРИЗАЦИИ K-means
# строим кластеризаци методом KMeans
#
# n_clusters - укажите количество кластеров, которые вам необходимы
#
km = KMeans(n_clusters=4).fit(dataNorm)
# выведем полученное распределение по кластерам
# так же номер кластера, к котрому относится строка, так как нумерация начинается с нуля, выводим добавляя 1
print(km.labels_ +1)
plt.figure(figsize=(10, 8))
plt.scatter(data_for_clust[:,1], data_for_clust[:,2], c=km.labels_, cmap='flag')
plt.show()
# 3D визуализация


