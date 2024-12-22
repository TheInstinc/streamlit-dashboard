import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk memuat data
def load_data():
    if st.config.get_option('server.headless'):
        # Berjalan di Streamlit Cloud
        file_path = 'data/PRSA_Data_Aotizhongxin_20130301-20170228.csv'
    else:
        # Berjalan di lokal
        file_path = 'D:/Code/.python/Dicoding/PRSA_Data_20130301-20170228/PRSA_Data_Aotizhongxin_20130301-20170228.csv'
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df['rainy_day'] = df['RAIN'].apply(lambda x: "Hujan" if x > 0 else "Tidak Hujan")
    df['weekday'] = df['date'].dt.dayofweek
    df['is_weekday'] = df['weekday'].apply(lambda x: "WeekDay" if x < 5 else "WeekEnd")
    return df

df = load_data()

st.title('Dashboard Analisis Kualitas Udara')

# Pertanyaan 1: Pengaruh Hujan Terhadap Konsentrasi PM2.5 dan PM10
st.subheader('Pengaruh Hujan Terhadap Konsentrasi PM2.5 dan PM10')
rain_effect = df.groupby('rainy_day')[['PM2.5', 'PM10']].mean()
categories = ['PM2.5', 'PM10']
values_hujan = rain_effect.loc['Hujan'].values
values_tidak_hujan = rain_effect.loc['Tidak Hujan'].values

fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
index = range(len(categories))
bars1 = plt.bar(index, values_hujan, bar_width, label='Hujan')
bars2 = plt.bar([p + bar_width for p in index], values_tidak_hujan, bar_width, label='Tidak Hujan')
plt.xlabel('Polutan')
plt.ylabel('Konsentrasi Rata-Rata')
plt.title('Pengaruh Hujan Terhadap Konsentrasi PM2.5 dan PM10')
plt.xticks([p + bar_width / 2 for p in index], categories)
plt.legend()
st.pyplot(fig)

# Pertanyaan 2: Perbandingan Konsentrasi PM2.5: Hari Kerja vs Akhir Pekan
st.subheader('Perbandingan Konsentrasi PM2.5: Hari Kerja vs Akhir Pekan')
weekday_effect = df.groupby('is_weekday')['PM2.5'].mean()
days = ['WeekDay', 'WeekEnd']
pm_values = [weekday_effect['WeekDay'], weekday_effect['WeekEnd']]

fig2, ax2 = plt.subplots(figsize=(8, 4))
bars = plt.bar(days, pm_values, color=['blue', 'green'])
plt.xlabel('Jenis Hari')
plt.ylabel('Konsentrasi PM2.5 Rata-Rata')
plt.title('Perbandingan Konsentrasi PM2.5: Hari Kerja vs Akhir Pekan')
st.pyplot(fig2)
