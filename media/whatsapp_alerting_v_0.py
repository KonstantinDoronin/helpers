import pandas as pd
from datetime import datetime, timedelta
import yagmail
import re
df = pd.read_csv(r'', header = None, error_bad_lines=False, sep=']')
df[["trash", "date_time"]] = pd.DataFrame(df[0].str.split('[',1).tolist())
df = df.dropna()
df[["name","text"]] = pd.DataFrame(df[1].str.split(':',1).tolist(),index=df.index)
df = df.dropna()
df = df.drop([0,1,"trash"],axis = 1)
df.head(2)
df['date_time'] =  pd.to_datetime(df['date_time'],errors = "coerce",dayfirst = True)
df.name.unique()
df['date_time'] = df['date_time'].astype(str)
df[['date', 'time']] = df['date_time'].str.split(' ',expand=True)
df['text'] = df['text'].str.lower()
df['text'] = df['text'].str.replace('[^\w\s#@/:%.,_-]', '', flags=re.UNICODE)
print(df.head())
df.to_excel(r'', sheet_name='общее', index=False)
labels = {'кто-нибудь': 'нужна помощь', 'устанавливал': 'нужна помощь', 'посоветуйте': 'нужна помощь'}
def matcher(k):
    x = (i for i in labels if i in k.split(' '))
    return ' | '.join(map(labels.get, x))
df['values'] = df['text'].map(matcher)
now = pd.Timestamp.today()
now = now.replace(microsecond=0)
tendaysago = now + timedelta(days=-5)
df = df[(df['values'] == 'нужна помощь') & df['date'] >= 1]
df['date_time'] = pd.to_datetime(df['date_time'])
df.to_excel(r'', sheet_name='выборка', index=False)
print(tendaysago)
mask = (df['date_time'] > tendaysago)
df = df.loc[mask]
if df.shape[0] > 0:
    yag = yagmail.SMTP(user='konstantindoronin10@gmail.com', password='')
    contents = format(df.to_string())
    recipients = {
        'zzdbs@mail.ru': 'Kostya'
    }
    yag.send(to=recipients, subject='scritps', contents=contents)
else:
    print('ничего нет')