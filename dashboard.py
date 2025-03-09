import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

# Muat dataset
airquality_df = pd.read_csv("main_data.csv")

# Judul dashboard
st.title('Dashboard Analisis Kualitas Udara: Stasiun Wanliu')
st.write("**Dashboard ini menampilkan data kualitas udara dan variabel yang memengaruhinya di Stasiun Wanliu.**")

# Filter interaktif berdasarkan tahun dan bulan
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(airquality_df['year'].unique()), index=sorted(airquality_df['year'].unique()).index(2014))

bulan_dict = {1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"}
selected_month_num = st.sidebar.selectbox("Pilih Bulan", [bulan_dict[m] for m in sorted(airquality_df['month'].unique())], index=0)
selected_month = list(bulan_dict.keys())[list(bulan_dict.values()).index(selected_month_num)]

airquality_filtered = airquality_df[(airquality_df['year'] == selected_year) & (airquality_df['month'] == selected_month)]

# Histogram distribusi data
st.subheader('Distribusi Data')
fig, axes = plt.subplots(nrows=1, ncols=min(5, len(airquality_filtered.columns)), figsize=(15, 4))
for i, kolom in enumerate(airquality_filtered.columns[:5]):
    axes[i].hist(airquality_filtered[kolom], bins=20, color='royalblue', edgecolor='black')
    axes[i].set_title(kolom)
st.pyplot(fig)

# Pilihan variabel untuk heatmap korelasi
st.subheader('Peta Korelasi Indikator Kualitas Udara')
selected_vars = st.multiselect("Pilih Variabel untuk Korelasi", airquality_filtered.columns, default=['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'WSPM'])

if len(selected_vars) > 1:
    korelasi = airquality_filtered[selected_vars].corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(korelasi, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
    st.pyplot(fig)
else:
    st.warning("Pilih minimal dua variabel untuk menampilkan korelasi.")

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

# Scatter plot NO2 vs CO dengan filter rentang nilai
st.subheader('Hubungan antara NO2 dan CO')
min_no2, max_no2 = st.slider("Rentang NO2", float(airquality_filtered['NO2'].min()), float(airquality_filtered['NO2'].max()), (float(airquality_filtered['NO2'].min()), float(airquality_filtered['NO2'].max())))
min_co, max_co = st.slider("Rentang CO", float(airquality_filtered['CO'].min()), float(airquality_filtered['CO'].max()), (float(airquality_filtered['CO'].min()), float(airquality_filtered['CO'].max())))

filtered_scatter = airquality_filtered[(airquality_filtered['NO2'] >= min_no2) & (airquality_filtered['NO2'] <= max_no2) &
                                       (airquality_filtered['CO'] >= min_co) & (airquality_filtered['CO'] <= max_co)]

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='NO2', y='CO', data=filtered_scatter, alpha=0.6, edgecolor='k')
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
