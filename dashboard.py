import streamlit as st
import pandas as pd
import requests

# Konfigurasi Halaman Dashboard
st.set_page_config(page_title="Dashboard Evaluasi Test Fisik AKTI", page_icon="📊", layout="wide")

# URL Web App Google Apps Script Anda (Gunakan URL yang sama untuk mengambil data spreadsheet)
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzuNBeBPH6BiHr6MFjS03SIT3oAPYvjhnBL4V81Y5ylrZlzx3RIkQcLWGXcdRNcC99Xgw/exec"

# Styling CSS Kustom: Tema iPhone Glassmorphism Premium (Maroon & Gold Elegan)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp {
        background: radial-gradient(circle at 50% 0%, #631010 0%, #2b0505 60%, #120202 100%) !important;
        background-attachment: fixed;
    }

    .apple-glass-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-top: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        margin-bottom: 25px;
    }

    .app-header {
        text-align: center;
        padding: 10px 0 20px 0;
    }

    .akti-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(255, 215, 0, 0.05));
        border: 1px solid rgba(212, 175, 55, 0.5);
        color: #ffd700;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .app-title {
        color: #ffffff !important;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .app-subtitle {
        color: rgba(255, 255, 255, 0.65) !important;
        font-size: 0.9rem;
    }

    p, span, h3, h4 {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Utama Dashboard
st.markdown("""
    <div class="app-header">
        <div class="akti-badge">AKADEMI KOMUNITAS TOYOTA INDONESIA</div>
        <div class="app-title">Dashboard Eksekutif & Evaluasi Tes Fisik</div>
        <div class="app-subtitle">Analisis Kinerja Jasmani Mahasiswa Angkatan A11 untuk Manajemen</div>
    </div>
""", unsafe_allow_html=True)

# Tombol Refresh Data
col_rf1, col_rf2, col_rf3 = st.columns([2, 1, 2])
with col_rf2:
    refresh_btn = st.button("🔄 Muat Ulang Data")

# Simulasi / Pengambilan Data (Jika Apps Script Anda mendukung GET untuk mengambil rekap data, 
# atau kita sediakan template analitik dari data dummy/live spreadsheet)
# Catatan: Pastikan Apps Script Anda dapat merespons method GET dengan mengembalikan seluruh data baris jika diperlukan.
# Jika menggunakan struktur standar, kita buatkan struktur penampil data analitik di bawah ini:

st.markdown('<div class="apple-glass-card">', unsafe_allow_html=True)
st.markdown("### 📈 Ringkasan Metrik Utama Kebugaran Jasmani")

# Contoh metrik KPI Eksekutif
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="Total Mahasiswa Teruji", value="94 Siswa", delta="100% Roster")
with kpi2:
    st.metric(label="Rata-rata Nilai Angkatan", value="78.4", delta="+3.2 dari target")
with kpi3:
    st.metric(label="Kategori Dominan", value="Bagus (71-85)", delta="Stabil")
with kpi4:
    st.metric(label="Perlu Perhatian Khusus", value="6 Siswa", delta="-2 siswa", delta_color="inverse")

st.markdown('</div>', unsafe_allow_html=True)

# Visualisasi Grafik Evaluasi Manajemen
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown('<div class="apple-glass-card">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Distribusi Kategori Kebugaran Jasmani")
    st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6);'>Jumlah mahasiswa berdasarkan klasifikasi nilai rata-rata keseluruhan.</p>", unsafe_allow_html=True)
    
    # Data dummy proporsi kategori untuk visualisasi manajemen awal
    df_kategori = pd.DataFrame({
        'Kategori': ['Sangat Bagus (86-100)', 'Bagus (71-85)', 'Cukup (56-70)', 'Kurang (<55)'],
        'Jumlah Mahasiswa': [28, 45, 15, 6]
    }).set_index('Kategori')
    
    st.bar_chart(df_kategori, color="#ffd700")
    st.markdown('</div>', unsafe_allow_html=True)

with col_g2:
    st.markdown('<div class="apple-glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 Rata-rata Skor Berdasarkan Item Tes")
    st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6);'>Evaluasi item tes fisik yang memerlukan peningkatan program latihan.</p>", unsafe_allow_html=True)
    
    df_item = pd.DataFrame({
        'Item Tes': ['Bleep Test', 'Pull-Up / Chinning', 'Sit-Up', 'Push-Up', 'Shuttle Run'],
        'Skor Rata-rata': [82.5, 74.0, 85.5, 79.0, 80.2]
    }).set_index('Item Tes')
    
    st.bar_chart(df_item, color="#e6c547")
    st.markdown('</div>', unsafe_allow_html=True)

# Tabel Rekomendasi Evaluasi Khusus untuk Manajemen
st.markdown('<div class="apple-glass-card">', unsafe_allow_html=True)
st.markdown("#### 🚨 Daftar Mahasiswa yang Membutuhkan Pendampingan / Latihan Khusus")
st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6);'>Mahasiswa dengan kategori Kurang (<55) yang menjadi prioritas bimbingan pelatih jasmani.</p>", unsafe_allow_html=True)

df_perhatian = pd.DataFrame([
    {"No": 1, "Nama Mahasiswa": "FAJAR RISKI", "NIM": "PM26", "Nilai Rata-rata": 52.0, "Status": "Perlu Pembinaan Fisik"},
    {"No": 2, "Nama Mahasiswa": "TARUNA", "NIM": "PM66", "Nilai Rata-rata": 48.5, "Status": "Perlu Pembinaan Fisik"},
    {"No": 3, "Nama Mahasiswa": "USAMAH", "NIM": "PM90", "Nilai Rata-rata": 50.0, "Status": "Perlu Pembinaan Fisik"}
])

st.dataframe(df_perhatian, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
