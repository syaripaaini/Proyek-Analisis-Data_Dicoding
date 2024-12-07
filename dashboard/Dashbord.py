import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import folium
from streamlit_folium import folium_static

sns.set(style="darkgrid")

# Fungsi untuk memuat dataset dengan caching
@st.cache_data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        st.error(f"File {file_path} tidak ditemukan. Pastikan file tersedia.")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika file tidak ditemukan

# Memuat dataset
main_data = load_data("main_data.csv")

# Validasi apakah dataset berhasil dimuat
if main_data.empty:
    st.stop()  # Menghentikan eksekusi Streamlit jika data kosong

# Validasi kolom 'order_approved_at'
if "order_approved_at" in main_data.columns:
    # Konversi kolom 'order_approved_at' menjadi datetime
    main_data["order_approved_at"] = pd.to_datetime(main_data["order_approved_at"], errors="coerce")
    # Pastikan tidak ada nilai NaT di 'order_approved_at'
    main_data = main_data.dropna(subset=["order_approved_at"])
else:
    st.error("Kolom 'order_approved_at' tidak ditemukan dalam dataset.")
    st.stop()  # Menghentikan eksekusi jika kolom tidak ada

# Menentukan rentang tanggal berdasarkan data
min_date = main_data["order_approved_at"].min()
max_date = main_data["order_approved_at"].max()

# Sidebar Configuration
with st.sidebar:
    st.title("Dashboard E-Commerce")
    st.image("gcl.png", caption="Logo Perusahaan")  # Pastikan file gambar tersedia
    st.write(f"Data tersedia dari {min_date.date()} hingga {max_date.date()}")

    # Input rentang tanggal
    try:
        start_date, end_date = st.date_input(
            "Pilih Rentang Tanggal",
            value=[min_date.date(), max_date.date()],
            min_value=min_date.date(),
            max_value=max_date.date(),
        )
    except Exception as e:
        st.error(f"Error pada input tanggal: {e}")
        st.stop()  # Menghentikan eksekusi jika ada error

# Filter data berdasarkan rentang tanggal
filtered_data = main_data[
    (main_data["order_approved_at"] >= pd.Timestamp(start_date)) &
    (main_data["order_approved_at"] <= pd.Timestamp(end_date))
]

# Fungsi untuk menghitung metrik harian
def calculate_daily_metrics(df):
    if df.empty:
        st.warning("Data kosong setelah difilter. Periksa rentang tanggal.")
        return pd.DataFrame()

    df = df.set_index("order_approved_at")  # Mengatur 'order_approved_at' sebagai index untuk resampling
    daily_df = df.resample("D").agg({
        "order_id": "nunique",  # Menghitung jumlah pesanan unik
        "payment_value": "sum"  # Menjumlahkan total harga (menggunakan kolom 'payment_value')
    }).reset_index()
    daily_df.rename(columns={"order_id": "order_count", "payment_value": "revenue"}, inplace=True)
    return daily_df

# Fungsi untuk menganalisis demografi pelanggan
def customer_demographics(df):
    if "customer_state" in df.columns:
        return df["customer_state"].value_counts()
    else:
        return pd.Series([])

# Fungsi untuk menghitung skor ulasan
def review_scores(df):
    if "review_score" in df.columns:
        return df["review_score"].value_counts().sort_index()
    else:
        return pd.Series([])

# Fungsi untuk membuat peta lokasi pelanggan
def create_customer_map(df):
    if "geolocation_lat" in df.columns and "geolocation_lng" in df.columns:
        # Memastikan tidak ada nilai NaN pada koordinat
        df = df.dropna(subset=["geolocation_lat", "geolocation_lng"])

        # Membuat peta dengan folium
        m = folium.Map(location=[-15.793889, -47.882778], zoom_start=4)  # Koordinat Brasil

        # Tambahkan layer untuk batas wilayah Brasil
        folium.GeoJson("brazil.geojson", name="Brasil", style={
            "fillColor": "none",
            "color": "black",
            "weight": 2
        }).add_to(m)

        for _, row in df.iterrows():
            folium.Marker(
                location=[row["geolocation_lat"], row["geolocation_lng"]],
                popup=f"City: {row['customer_city']}"
            ).add_to(m)

        return m
    else:
        return None

# Analisis data
daily_metrics = calculate_daily_metrics(filtered_data)
customer_data = customer_demographics(filtered_data)
review_data = review_scores(filtered_data)

if not daily_metrics.empty:
    # Header Dashboard
    st.title("E-Commerce Dashboard")

    # Menampilkan Metrik Utama
    total_orders = daily_metrics["order_count"].sum()
    total_revenue = daily_metrics["revenue"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Orders", value=f"{total_orders:,}")
    col2.metric("Total Revenue", value=format_currency(total_revenue, "IDR", locale="id_ID"))

    # Grafik: Tren Pesanan Harian
    st.subheader("Tren Pesanan Harian")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        x="order_approved_at", y="order_count", data=daily_metrics,
        ax=ax, marker="o", color="#42A5F5", label="Orders"
    )
    ax.set_title("Jumlah Pesanan Harian", fontsize=16)
    ax.set_xlabel("Tanggal", fontsize=12)
    ax.set_ylabel("Jumlah Pesanan", fontsize=12)
    ax.legend()
    st.pyplot(fig)

    # Grafik: Pendapatan Harian
    st.subheader("Tren Pendapatan Harian")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x="order_approved_at", y="revenue", data=daily_metrics,
        hue="order_approved_at", palette="Blues_d", legend=False, ax=ax  # Assigning hue to avoid deprecation warning
    )
    ax.set_title("Pendapatan Harian", fontsize=16)
    ax.set_xlabel("Tanggal", fontsize=12)
    ax.set_ylabel("Pendapatan (IDR)", fontsize=12)
    st.pyplot(fig)

    # Grafik: Demografi Pelanggan
    st.subheader("Demografi Pelanggan")
    if not customer_data.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        customer_data.plot(kind="bar", ax=ax, color="#FFA726")
        ax.set_title("Distribusi Pelanggan Berdasarkan Provinsi", fontsize=16)
        ax.set_xlabel("Provinsi", fontsize=12)
        ax.set_ylabel("Jumlah Pelanggan", fontsize=12)
        st.pyplot(fig)
    else:
        st.warning("Data demografi tidak tersedia.")

    # Grafik: Skor Ulasan
    st.subheader("Skor Ulasan")
    if not review_data.empty:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=review_data.index, y=review_data.values, hue=review_data.index, palette="Blues_d", legend=False, ax=ax)
        ax.set_title("Distribusi Skor Ulasan", fontsize=16)
        ax.set_xlabel("Skor", fontsize=12)
        ax.set_ylabel("Jumlah", fontsize=12)
        st.pyplot(fig)
    else:
        st.warning("Data skor ulasan tidak tersedia.")

    # Peta: Lokasi Pelanggan
    st.subheader("Peta Lokasi Pelanggan")
    customer_map = create_customer_map(filtered_data)
    if customer_map:
        folium_static(customer_map)
    else:
        st.warning("Data lokasi pelanggan tidak tersedia.")
else:
    st.warning("Tidak ada data untuk ditampilkan berdasarkan filter.")

# Footer
st.caption("Copyright © Syaripatul Aini 2024")
