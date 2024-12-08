import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema visualisasi Seaborn
sns.set_theme(style="whitegrid")

# Membaca data dari file CSV
main_df = pd.read_csv("dashboard/main_data.csv")

# Menambahkan logo atau gambar ke sidebar
st.sidebar.image("dashboard/bike.jpg", use_column_width=True)

# Sidebar untuk filter rentang waktu
st.sidebar.header("Filter Rentang Waktu")
start_date = st.sidebar.date_input("Pilih Tanggal Mulai", pd.to_datetime(main_df['dteday'].min()))
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", pd.to_datetime(main_df['dteday'].max()))

# Memfilter data berdasarkan rentang waktu yang dipilih pengguna
filtered_df = main_df[(main_df['dteday'] >= str(start_date)) & (main_df['dteday'] <= str(end_date))]

# Judul Dashboard
st.title("🚴‍♂️ Dashboard Penyewaan Sepeda 🚴‍♀️")
st.write("""Selamat datang di **Dashboard Penyewaan Sepeda**! 
Mari temukan wawasan menarik dari data penyewaan sepeda melalui visualisasi interaktif.""")

# 1. Tren Bulanan Penggunaan Sepeda
st.header("📅 Tren Bulanan Penggunaan Sepeda")
monthly_trend = filtered_df.groupby(['year', 'month'], observed=True)['count'].sum().reset_index()

# Memastikan kolom year bertipe integer
monthly_trend['year'] = monthly_trend['year'].astype(int)

# Mengatur urutan bulan
months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_trend['month'] = pd.Categorical(monthly_trend['month'], categories=months_order, ordered=True)

# Membuat visualisasi
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_trend, x='month', y='count', hue='year', marker='o', palette='tab10', ax=ax)
ax.set_title('Tren Bulanan Penggunaan Sepeda', fontsize=16)
ax.set_xlabel('Bulan', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
ax.legend(title='Tahun', loc='upper right')
st.pyplot(fig)

# Menampilkan tabel data
st.subheader("Tabel Tren Bulanan")
st.dataframe(monthly_trend)

# 2. Pengaruh Cuaca terhadap Penggunaan Sepeda
st.header("🌤️ Pengaruh Cuaca terhadap Penggunaan Sepeda")
weather_rentals = filtered_df.groupby('weather_situation', observed=True)['count'].agg(['sum', 'mean']).reset_index()

# Visualisasi pengaruh cuaca
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=weather_rentals, x='weather_situation', y='sum', palette='coolwarm', ax=ax)
ax.set_title('Pengaruh Cuaca terhadap Penyewaan Sepeda', fontsize=16)
ax.set_xlabel('Kondisi Cuaca', fontsize=12)
ax.set_ylabel('Total Penyewaan', fontsize=12)
st.pyplot(fig)

# Menampilkan tabel data
st.subheader("Tabel Pengaruh Cuaca")
st.dataframe(weather_rentals)

# 3. Penyewaan Sepeda Berdasarkan Hari
st.header("📊 Penyewaan Sepeda Berdasarkan Hari")
filtered_df['day_type'] = filtered_df['weekday'].apply(lambda x: 'Akhir Pekan' if x in ['Sat', 'Sun'] else 'Hari Kerja')
day_type_rentals = filtered_df.groupby('day_type')['count'].mean().reset_index()

# Visualisasi jenis hari
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=day_type_rentals, x='day_type', y='count', palette='muted', ax=ax)
ax.set_title('Penyewaan Sepeda Berdasarkan Hari', fontsize=16)
ax.set_xlabel('Jenis Hari', fontsize=12)
ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
st.pyplot(fig)

# Menampilkan tabel data
st.subheader("Tabel Penyewaan per Jenis Hari")
st.dataframe(day_type_rentals)

# 4. Proporsi Penyewaan Sepeda
st.header("👥 Proporsi Penyewaan Sepeda")
user_type_counts = filtered_df[['casual', 'registered']].sum()

# Membuat visualisasi pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(user_type_counts, labels=['Casual', 'Registered'], autopct='%1.1f%%', startangle=90, colors=['#8fbc8f', '#d87093'])
ax.set_title('Proporsi Penyewaan Sepeda', fontsize=16)
st.pyplot(fig)

# Menampilkan tabel data
st.subheader("Tabel Proporsi Pengguna")
st.dataframe(user_type_counts.reset_index(name='Total'))

# Pesan Penutup
st.sidebar.markdown("### 🌟 Terima kasih telah menggunakan Dashboard Penyewaan Sepeda!")
st.caption("Copyright © Syaripatul Aini 2024")
