import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style="whitegrid")  # Gaya grid yang lebih ringan

# Fungsi untuk memuat dataset secara langsung
@st.cache_data
def load_default_data():
    # Ganti path ini dengan file CSV Anda yang sudah di-embed
    try:
        data = pd.read_csv("main_data.csv")
        return data
    except FileNotFoundError:
        st.error("File main_data.csv tidak ditemukan. Pastikan file tersedia di direktori.")
        return pd.DataFrame()

# Fungsi untuk memuat logo default
def load_default_logo():
    return "logo_perusahaan.png"  # Ganti dengan path gambar logo perusahaan Anda

# Memuat dataset
main_data = load_default_data()

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
    
    # Menampilkan gambar logo default
    st.image(load_default_logo(), caption="Logo Perusahaan", use_column_width=True)

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

# Analisis data
daily_metrics = calculate_daily_metrics(filtered_data)

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
        ax=ax, marker="o", color="#FF6347", label="Orders"  # Warna garis dan titik
    )
    ax.set_title("Jumlah Pesanan Harian", fontsize=18, fontweight="bold")
    ax.set_xlabel("Tanggal", fontsize=14)
    ax.set_ylabel("Jumlah Pesanan", fontsize=14)
    ax.legend(fontsize=12, loc="upper left")
    ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.7)
    st.pyplot(fig)

    # Grafik: Tren Pendapatan Harian
    st.subheader("Tren Pendapatan Harian")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        x="order_approved_at", y="revenue", data=daily_metrics,
        ax=ax, marker="o", color="#4682B4", label="Revenue"  # Warna garis dan titik
    )
    ax.set_title("Pendapatan Harian", fontsize=18, fontweight="bold")
    ax.set_xlabel("Tanggal", fontsize=14)
    ax.set_ylabel("Pendapatan (IDR)", fontsize=14)
    ax.legend(fontsize=12, loc="upper left")
    ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.7)
    st.pyplot(fig)
else:
    st.warning("Tidak ada data untuk ditampilkan berdasarkan filter.")

# Footer
st.caption("Copyright © Syaripatul Aini 2024")
