#%%

import pandas as pd
import pyodbc

# pyodbc.drivers()

#%%
# Connecting to server

#/usr/local/lib/libmsodbcsql.17.dylib;'
#{ODBC Driver 13 for SQL Server};'

conn = pyodbc.connect('Driver=/usr/local/lib/libmsodbcsql.17.dylib;'
                      'Server=;'
                      'Database=;'
                      'UID=;'
                      'PWD=;')

cursor = conn.cursor()

# Create a table if necessary
#%%
df = pd.read_csv("/Users/aliyadavletshina/Desktop/UD_Group/udg/users_data/newusers.csv")
                
cursor.execute('''
               CREATE TABLE UDtest.yandexmetrika.newusers
               (
               counterID nvarchar(MAX),
               clientID nvarchar(MAX),
               isNewUser nvarchar(MAX),
               hourMinute time,
               daysSinceFirstVisit int
               )
               ''')

for row in df.itertuples():
        cursor.execute('''
                set language english; INSERT INTO UDtest.yandexmetrika.newusers (counterID, clientID,isNewUser,\
                hourMinute, daysSinceFirstVisit)
                VALUES (?,?,?,CAST(? AS Time),?)
                ''',
                    row.counterID,
                    row.clientID,
                    row.isNewUser,
                    row.hourMinute,
                    row.daysSinceFirstVisit
    )
conn.commit()

# %%
df = pd.read_csv("")
df = df.where(pd.notnull(df), None)

# %%
cursor.execute('''
               CREATE TABLE UDtest.yandexmetrika.sources
               (
               counterID nvarchar(MAX),
               clientID nvarchar(MAX),
               UTMCampaign nvarchar(MAX),
               UTMSource nvarchar(MAX),
               UTMContent nvarchar(MAX),
               [date] date,
               regionCity nvarchar(MAX),
               lastsignTrafficSource nvarchar(MAX)
               )
               ''')

for row in df.itertuples():
        cursor.execute('''
                INSERT INTO UDtest.yandexmetrika.sources (counterID, clientID, UTMCampaign,\
                UTMSource, UTMContent, [date], regionCity,lastsignTrafficSource)
                VALUES (?,?,?,?,?, CAST(? AS Date),?,?)
                ''',
                    row.counterID,
                    row.clientID,
                    row.UTMCampaign,
                    row.UTMSource,
                    row.UTMContent,
                    row.date,
                    row.regionCity,
                    row.lastsignTrafficSource
    )
conn.commit()              


# %%
df = pd.read_csv("")
df = df.where(pd.notnull(df), None)

cursor.execute('''
               CREATE TABLE UDtest.yandexmetrika.users_40011245_users
               (
               [userID] nvarchar(MAX),
               [userVisits] int,
               [totalVisitsDuration] int,
               [userFirstVisitDate] date,
               [firstSourceEngine] nvarchar(MAX),
               [gender] nvarchar(MAX),
               [interest] nvarchar(MAX),
               [ageInterval] varchar(MAX)
               )
               ''')

for row in df.itertuples():
        cursor.execute('''
                INSERT INTO UDtest.yandexmetrika.users_40011245_users ([userID], [userVisits], [totalVisitsDuration],\
                [userFirstVisitDate], [firstSourceEngine], [gender], [interest], [ageInterval])
                VALUES (?,?,?,?,?,?,?,?)
                ''',
                    row.userID,
                    row.userVisits,
                    row.totalVisitsDuration,
                    row.userFirstVisitDate,
                    row.firstSourceEngine,
                    row.gender,
                    row.interest,
                    row.ageInterval
    )
conn.commit() 


# %%
df = pd.read_csv("")
df = df.where(pd.notnull(df), None)

cursor.execute('''
               CREATE TABLE UDtest.yandexmetrika.users_52015214_users
               (
               userID nvarchar(30),
               userVisits int,
               totalVisitsDuration int,
               userFirstVisitDate date,
               firstSourceEngine nvarchar(MAX),
               gender nvarchar(15),
               interest nvarchar(MAX),
               ageInterval nvarchar(30)
               )
               ''')

for row in df.itertuples():
        cursor.execute('''
                INSERT INTO UDtest.yandexmetrika.users_52015214_users (userID, userVisits, totalVisitsDuration,\
                userFirstVisitDate, firstSourceEngine, gender, interest, ageInterval)
                VALUES (?,?,?,?,?,?,?,?)
                ''',
                    row.userID,
                    row.userVisits,
                    row.totalVisitsDuration,
                    row.userFirstVisitDate,
                    row.firstSourceEngine,
                    row.gender,
                    row.interest,
                    row.ageInterval
    )
conn.commit() 

#%%
df = pd.read_csv("")
df = df.where(pd.notnull(df), None)

cursor.execute('''
               CREATE TABLE UDtest.yandexmetrika.users_53322454_users
               (
               userID nvarchar(30),
               userVisits int,
               totalVisitsDuration int,
               userFirstVisitDate date,
               firstSourceEngine nvarchar(MAX),
               gender nvarchar(15),
               interest nvarchar(MAX),
               ageInterval nvarchar(30)
               )
               ''')

for row in df.itertuples():
        cursor.execute('''
                INSERT INTO UDtest.yandexmetrika.users_53322454_users (userID, userVisits, totalVisitsDuration,\
                userFirstVisitDate, firstSourceEngine, gender, interest, ageInterval)
                VALUES (?,?,?,CAST(? AS Date),?,?,?,?)
                ''',
                    row.userID,
                    row.userVisits,
                    row.totalVisitsDuration,
                    row.userFirstVisitDate,
                    row.firstSourceEngine,
                    row.gender,
                    row.interest,
                    row.ageInterval
    )
conn.commit() 

# Check a table
sql_query = pd.read_sql_query('SELECT * FROM UDtest.yandexmetrika.sources',conn)
print (sql_query.shape)

# %%
sql_query = pd.read_sql_query('SELECT * FROM UDtest.yandexmetrika.users_40011245_users',conn)
print (sql_query.shape)
# %%
sql_query.head