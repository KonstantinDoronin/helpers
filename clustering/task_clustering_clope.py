import pyfpgrowth
#Сгенериуем паттерны
patterns = pyfpgrowth.find_frequent_patterns(transactions, 2)
#Выучим правила
rules = pyfpgrowth.generate_association_rules(patterns, 30);
#Покажем
print(rules)
