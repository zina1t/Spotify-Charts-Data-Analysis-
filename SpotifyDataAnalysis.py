import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
import calendar

df = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')
df.info()

df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
df.dropna(inplace=True)

track_name_to_id = {name: index for index, name in enumerate(df['track_name'].unique())}
df['track_id'] = df['track_name'].map(track_name_to_id)
df.drop(columns=['track_name'], inplace=True)

plt.figure(figsize = (10, 7))
years = df['released_year'].value_counts().sort_index()
years.plot(x = years.index, y = years, width=0.6, kind='bar')
plt.show()

months = df['released_month'].value_counts()
m_names = [calendar.month_name[i] for i in months.index]

plt.figure(figsize = (10, 7))
plt.pie(months, labels=m_names, autopct='%.1f%%')
plt.show()

columns_analysis = ['bpm', 'danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%']
plt.figure(figsize = (10, 7))
for i, column in enumerate(columns_analysis, 1):
    plt.subplot(3, 3, i)
    sns.histplot(data=df, x=column, bins=15, color='blue')
    plt.xlabel(column, fontsize=12)
    plt.ylabel("Score", fontsize=12)

plt.tight_layout()
plt.show()

correlation_matrix = df[columns_analysis].corr()
correlation_matrix

plt.figure(figsize=(10, 7))
sns.heatmap(correlation_matrix, vmin=-0.58, vmax=1, annot=True)

fig, axes = plt.subplots(3, 3, figsize=(10, 7))

axes = axes.flatten()

scaler = MinMaxScaler()
df['streams'] = scaler.fit_transform(df[['streams']])

for i, column in enumerate(columns_analysis):
    plt.sca(axes[i])
    plt.bar(df[column], df['streams'], color='blue')
    plt.xlabel(column, fontsize=12)
    plt.ylabel('Streams', fontsize=12)
    plt.title(f'Streams vs. {column}', fontsize=14)
    plt.grid(axis='y')
plt.tight_layout()
plt.show()

sorted_keys = sorted(df['key'].unique())
average_streams = df.groupby('key')['streams'].mean().sort_values().index.tolist()
plt.figure(figsize=(10,7))
sns.boxplot(x='streams', y='key', data= df, order=average_streams)
plt.xlabel('Streams')
plt.ylabel('Keys')
plt.title('Box Plot of Streams by Keys')
plt.show()

plt.figure(figsize=(10, 7))
key_count = df['key'].value_counts(ascending=True)
colors  = sns.color_palette("Set2", len(key_count))

key_count.plot(x = 'key', y = key_count, kind='bar', color=colors)
plt.xlabel('Keys')
plt.ylabel('Count')
plt.title('Count of each key')
plt.xticks(rotation=0)
plt.show()

key_df = df[['key', 'streams']].copy()
key_df = key_df.groupby('key')['streams'].agg(['mean', 'min', 'max'])
key_df = key_df.rename(columns={'mean' : 'avg_streams', 'min' : 'min_streams', 'max' : 'max_streams'})
key_df

plt.figure(figsize=(10, 7))
key_df.plot(y ='avg_streams', color=colors, kind='bar', legend=False)
plt.xlabel('Keys')
plt.ylabel('Average streams')
plt.title('Average streams by key')
plt.xticks(rotation=0)
plt.show()

fig, axes = plt.subplots(3, 3, figsize=(10, 7))

axes = axes.flatten()

scaler = MinMaxScaler()
df['streams'] = scaler.fit_transform(df[['streams']])

for i, column in enumerate(columns_analysis):
    plt.sca(axes[i])
    plt.bar(df['key'], df[column])
    plt.ylabel('Key')
    plt.title(f'Key vs. {column}')
    plt.grid(axis='y')
plt.tight_layout()
plt.show()
