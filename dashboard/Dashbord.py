import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import zipfile
from PIL import Image
import requests
from io import BytesIO

sns.set(style="whitegrid")  # Gaya visualisasi

# Fungsi untuk memuat dataset bawaan
@st.cache_data
def load_default_data():
    return pd.DataFrame({
        "order_approved_at": pd.date_range("2023-01-01", periods=100, freq="D"),
        "order_id": range(1, 101),
        "payment_value": [i * 1000 for i in range(1, 101)],
        "weathersit": ["Clear" if i % 2 == 0 else "Rain" for i in range(1, 101)],
        "season": ["Winter" if i % 4 == 0 else "Summer" for i in range(1, 101)]
    })

# Fungsi untuk memuat dataset dari file ZIP
@st.cache_data
def load_data(zip_file):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            with zip_ref.open('main_data.csv') as csv_file:
                data = pd.read_csv(csv_file)
        return data
    except FileNotFoundError:
        st.error("File main_data.csv tidak ditemukan dalam ZIP. Pastikan file tersedia.")
        return pd.DataFrame()

# Fungsi untuk memuat logo dari URL
@st.cache_data
def load_logo(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Pastikan URL valid
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.error(f"Gagal memuat logo: {e}")
        return None

# Header aplikasi
st.title("E-Commerce Dashboard")

# Input URL untuk logo
logo_url = st.text_input("Masukkan URL logo perusahaan (contoh: https://raw.githubusercontent.com/user/repo/gcl.png):")

# Upload dataset
uploaded_file = st.file_uploader("Pilih file ZIP untuk dataset", type="zip")

# Load dataset (default atau user-uploaded)
main_data = load_default_data() if uploaded_file is None else load_data(uploaded_file)

# Validasi dataset
if main_data.empty:
    st.warning("Dataset kosong. Menggunakan dataset bawaan.")
else:
    # Konversi tanggal dan validasi kolom
    main_data["order_approved_at"] = pd.to_datetime(main_data.get("order_approved_at", pd.NaT), errors="coerce")
    main_data.dropna(subset=["order_approved_at"], inplace=True)

    # Sidebar
    with st.sidebar:
        st.subheader("Filter Data")
        
        # Tampilkan logo jika URL valid
        if logo_url:
            logo = load_logo(logo_url)
            if logo:
                st.image(logo, caption="Logo Perusahaan", use_column_width=True)
        else:
            st.info("Masukkan URL logo perusahaan untuk tampilan lebih menarik.")

        # Filter tanggal
        start_date, end_date = st.date_input(
            "Pilih Rentang Tanggal",
            value=[main_data["order_approved_at"].min().date(), main_data["order_approved_at"].max().date()],
            min_value=main_data["order_approved_at"].min().date(),
            max_value=main_data["order_approved_at"].max().date()
        )

        # Konversi tanggal filter ke datetime Pandas
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter cuaca
        weather_filter = st.selectbox("Pilih Cuaca", options=main_data["weathersit"].unique())
        
        # Filter musim
        season_filter = st.multiselect("Pilih Musim", options=main_data["season"].unique(), default=main_data["season"].unique())
    
    # Filter data berdasarkan input
    filtered_data = main_data[
        (main_data["order_approved_at"].between(start_date, end_date)) &
        (main_data["weathersit"] == weather_filter) &
        (main_data["season"].isin(season_filter))
    ]

    # Analisis metrik harian
    daily_metrics = filtered_data.set_index("order_approved_at").resample("D").agg({
        "order_id": "nunique",  # Jumlah pesanan unik
        "payment_value": "sum"  # Total pendapatan
    }).reset_index().rename(columns={"order_id": "order_count", "payment_value": "revenue"})

    # Menampilkan metrik utama
    st.header("Ringkasan Metrik")
    total_orders = daily_metrics["order_count"].sum()
    total_revenue = daily_metrics["revenue"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Orders", f"{total_orders:,}")
    col2.metric("Total Revenue", format_currency(total_revenue, "IDR", locale="id_ID"))

    # Visualisasi data
    if not daily_metrics.empty:
        # Grafik: Tren Pesanan Harian
        st.subheader("Tren Jumlah Pesanan Harian")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=daily_metrics, x="order_approved_at", y="order_count", ax=ax, marker="o")
        ax.set_title("Tren Jumlah Pesanan Harian")
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Jumlah Pesanan")
        st.pyplot(fig)

        # Grafik: Tren Pendapatan Harian
        st.subheader("Tren Pendapatan Harian")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=daily_metrics, x="order_approved_at", y="revenue", ax=ax, marker="o", color="green")
        ax.set_title("Tren Pendapatan Harian")
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Pendapatan (IDR)")
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data untuk ditampilkan berdasarkan filter.")

    # Dokumentasi markdown
    st.markdown("""
    ## Dokumentasi
    **Penjelasan Fitur:**
    1. **Filter Tanggal**: Pilih rentang tanggal untuk memfilter data.
    2. **Filter Cuaca**: Pilih cuaca tertentu (Clear, Rain, dll.).
    3. **Filter Musim**: Pilih musim tertentu (Summer, Winter, dll.).
    
    **Visualisasi:**
    - Grafik Tren Jumlah Pesanan Harian.
    - Grafik Tren Pendapatan Harian.
    """)

    # Footer
    st.caption("Copyright © 2024 Syaripatul Aini - Dashboard ini dibangun menggunakan Streamlit.")
