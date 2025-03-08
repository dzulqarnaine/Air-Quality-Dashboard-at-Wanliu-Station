import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

# Muat dataset
airquality_df = pd.read_csv("C:/KULIAH STATISTIKA UNIVERSITAS SYIAH KUALA/SEMESTER 6/Coding Camp by DBS/Project/Analisis Data With Python/PRSA_Data_Wanliu_20130301-20170228.csv")

# Judul dashboard
st.title('Dasbor Analisis Kualitas Udara: Stasiun Wanliu')

# Header dashboard
st.write("**Dasbor ini menampilkan data kualitas udara dan variabel yang memengaruhinya di Stasiun Wanliu.**")

# Histogram distribusi data
st.subheader('Distribusi Data')
fig, axes = plt.subplots(nrows=1, ncols=min(5, len(airquality_df.columns)), figsize=(15, 4))
for i, kolom in enumerate(airquality_df.columns[:5]):
    axes[i].hist(airquality_df[kolom], bins=20, color='royalblue', edgecolor='black')
    axes[i].set_title(kolom)
st.pyplot(fig)

# Heatmap korelasi indikator kualitas udara
st.subheader('Peta Korelasi Indikator Kualitas Udara')
korelasi = airquality_df[['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(korelasi, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
st.pyplot(fig)

# Tren PM2.5 dari bulan ke bulan
st.subheader('Tren PM2.5 dari Bulan ke Bulan')
airquality_df['tahun_bulan'] = airquality_df['year'].astype(str) + '-' + airquality_df['month'].astype(str).str.zfill(2)
pm25_bulanan = airquality_df.groupby('tahun_bulan')['PM2.5'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=pm25_bulanan, x='tahun_bulan', y='PM2.5', marker='o', color='b')
plt.xlabel('Tahun-Bulan')
plt.ylabel('Rata-rata PM2.5')
plt.xticks(rotation=90)
plt.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

# Hubungan antara NO2 dan CO
st.subheader('Hubungan antara NO2 dan CO')
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='NO2', y='CO', data=airquality_df, alpha=0.6, edgecolor='k')
plt.xlabel('Konsentrasi NO2')
plt.ylabel('Konsentrasi CO')
plt.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig)

# Perbandingan PM2.5 dan PM10 dari tahun ke tahun
st.subheader('Perbandingan PM2.5 dan PM10 dari Tahun ke Tahun')
pm_tahunan = airquality_df.groupby('year')[['PM2.5', 'PM10']].mean()

fig, ax = plt.subplots(figsize=(8, 5))
plt.plot(pm_tahunan.index, pm_tahunan['PM2.5'], marker='o', linestyle='-', label='PM2.5', color='royalblue')
plt.plot(pm_tahunan.index, pm_tahunan['PM10'], marker='s', linestyle='-', label='PM10', color='crimson')
plt.xlabel('Tahun')
plt.ylabel('Konsentrasi Rata-rata')
plt.xticks(pm_tahunan.index, rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='Polutan', loc='upper left')
st.pyplot(fig)