import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema visualisasi Seaborn
sns.set_theme(style="whitegrid")

# Membaca data yang sudah bersih
main_df = pd.read_csv("dashboard/main_data.csv")

# Menambahkan logo atau gambar ke sidebar
st.sidebar.image("dashboard/bike-sharing.png", use_column_width=True)

# Sidebar untuk filter rentang waktu
st.sidebar.header("Filter Rentang Waktu")
start_date = st.sidebar.date_input("Pilih Tanggal Mulai", pd.to_datetime(main_df['dteday'].min()))
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", pd.to_datetime(main_df['dteday'].max()))

# Memfilter data berdasarkan rentang tanggal yang dipilih pengguna
filtered_df = main_df[(main_df['dteday'] >= str(start_date)) & (main_df['dteday'] <= str(end_date))]

# Judul Dashboard
st.title("🚴‍♂️ Bike Sharing Dashboard 🚴‍♀️")
st.write("""Selamat datang di **Bike Sharing Dashboard**! Temukan wawasan menarik tentang tren penyewaan sepeda melalui visualisasi yang menarik di bawah ini.""")

# 1. Visualisasi Tren Bulanan Penggunaan Sepeda dari Tahun ke Tahun
st.header("📅 Tren Bulanan Penggunaan Sepeda dari Tahun ke Tahun")
monthly_trend = filtered_df.groupby(['year', 'month'], observed=True)['count'].sum().reset_index()

# Mengubah kolom year menjadi integer untuk menghindari tanda koma
monthly_trend['year'] = monthly_trend['year'].astype(int)

# Mengatur urutan bulan
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_trend['month'] = pd.Categorical(monthly_trend['month'], categories=month_order, ordered=True)

# Membuat visualisasi
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_trend, x='month', y='count', hue='year', marker='o', palette=['#FF6347', '#4682B4', '#32CD32'])
plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.7)
plt.title('Tren Bulanan Penggunaan Sepeda dari Tahun ke Tahun', fontsize=16)
plt.xlabel('Bulan', fontsize=14)
plt.ylabel('Total Penyewaan Sepeda', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='Tahun')
st.pyplot(plt)

# Menampilkan tabel hasil
st.subheader("Tabel Tren Bulanan")
st.dataframe(monthly_trend)

# 2. Visualisasi Pengaruh Cuaca Terhadap Penggunaan Sepeda
st.header("🌤️ Pengaruh Cuaca Terhadap Penggunaan Sepeda")
weather_rentals = filtered_df.groupby('weather_situation', observed=True)['count'].agg(['sum', 'mean']).reset_index()

# Visualisasi pengaruh cuaca terhadap penggunaan sepeda
plt.figure(figsize=(10, 6))
sns.barplot(data=weather_rentals, x='weather_situation', y='sum', hue='weather_situation', palette='viridis', legend=False)
plt.title('Pengaruh Cuaca Terhadap Penggunaan Sepeda')
plt.xlabel('Cuaca')
plt.ylabel('Total Penyewaan Sepeda')
plt.xticks(rotation=45)
plt.grid(axis='y')
st.pyplot(plt)

# Menampilkan tabel hasil
st.subheader("Tabel Pengaruh Cuaca")
st.dataframe(weather_rentals)

# Pastikan kolom 'weekday' adalah kategori
if filtered_df['weekday'].dtype != 'category':
    filtered_df['weekday'] = filtered_df['weekday'].astype('category')

# 3. Visualisasi Rata-rata Penyewaan Sepeda pada Hari Kerja dan Akhir Pekan
st.header("📊 Rata-rata Penyewaan Sepeda pada Hari Kerja dan Akhir Pekan")
filtered_df['day_type'] = filtered_df['weekday'].cat.codes.apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
day_type_rentals = filtered_df.groupby('day_type')['count'].agg(['mean']).reset_index()

# Visualisasi rata-rata penyewaan sepeda berdasarkan jenis hari
plt.figure(figsize=(10, 6))
sns.barplot(data=day_type_rentals, x='day_type', y='mean', hue='day_type', palette='Set2', legend=False)
plt.title('Rata-rata Penyewaan Sepeda pada Hari Kerja dan Akhir Pekan')
plt.xlabel('Jenis Hari')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.xticks(rotation=0)
st.pyplot(plt)

# Menampilkan tabel hasil
st.subheader("Tabel Rata-rata Penyewaan per Jenis Hari")
st.dataframe(day_type_rentals)

# 4. Visualisasi Proporsi Penyewaan Sepeda berdasarkan Tipe Pengguna
st.header("👥 Proporsi Penyewaan Sepeda berdasarkan Tipe Pengguna")
user_type_counts = filtered_df[['casual', 'registered']].sum()

# Membuat pie chart berbentuk donat dengan persentase yang lebih rapi
plt.figure(figsize=(8, 8))
plt.pie(user_type_counts, labels=['Casual', 'Registered'], 
        autopct=lambda p: '{:.1f}%'.format(p) if p > 0 else '',  
        colors=['#66b3ff', '#ff9999'], startangle=90, 
        wedgeprops={'width': 0.4}, textprops={'fontsize': 12})  
plt.title('Proporsi Penyewaan Sepeda berdasarkan Tipe Pengguna')
plt.axis('equal')  
st.pyplot(plt)

# Menampilkan tabel hasil
st.subheader("Tabel Proporsi Penyewaan berdasarkan Tipe Pengguna")
st.dataframe(user_type_counts.reset_index(name='Total'))

# Pesan Penutup
st.sidebar.markdown("### 🌟 Terima kasih telah menjelajahi Bike Sharing Dashboard! ")
st.sidebar.write("Ayo, terus eksplorasi dengan memilih rentang tanggal yang berbeda di sidebar")
st.caption('Copyright © Ni Wayan Devi Pratiwi 2024')