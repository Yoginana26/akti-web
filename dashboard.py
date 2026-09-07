import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Konfigurasi Halaman Dashboard
st.set_page_config(page_title="Dashboard Eksekutif Test Fisik AKTI", page_icon="🛡️", layout="wide")

# Styling CSS Kustom: Tema Maroon, Putih, Gold & Bubble Glassmorphism ala iPhone
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Background Utama Gradasi Mewah Maroon */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #7a1212 0%, #3b0707 50%, #120202 100%) !important;
        background-attachment: fixed;
    }

    /* Efek Kartu Bubble Glassmorphism iPhone */
    .iphone-glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-top: 1px solid rgba(255, 255, 255, 0.3);
        border-left: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 28px;
        padding: 28px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6), inset 0 1px 2px rgba(255, 255, 255, 0.25);
        margin-bottom: 24px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .iphone-glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.7), inset 0 1px 3px rgba(255, 255, 255, 0.4);
    }

    /* Header & Badge */
    .app-header {
        text-align: center;
        padding: 20px 0 30px 0;
    }

    .akti-logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
    }
    
    .akti-logo-ring {
        width: 85px;
        height: 85px;
        background: radial-gradient(circle, rgba(255,215,0,0.15) 0%, rgba(255,255,255,0.05) 100%);
        border: 2px solid rgba(212, 175, 55, 0.6);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.3), inset 0 0 10px rgba(212, 175, 55, 0.2);
        padding: 8px;
    }

    .akti-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.25), rgba(255, 215, 0, 0.05));
        border: 1px solid rgba(212, 175, 55, 0.6);
        color: #ffd700;
        padding: 6px 20px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .app-title {
        color: #ffffff !important;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 6px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }

    .app-subtitle {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.95rem;
        font-weight: 500;
    }

    /* KPI Metric styling */
    .metric-container {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: inset 0 1px 1px rgba(255,255,255,0.1);
    }

    p, span, h3, h4, label {
        color: rgba(255, 255, 255, 0.95) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header Utama dengan Logo AKTI (Base64 atau Direct URL Render) & Efek Bubble Glass
st.markdown("""
    <div class="app-header">
        <div class="akti-logo-container">
            <div class="akti-logo-ring">
                <span style="font-size: 28px;">🛡️</span>
            </div>
        </div>
        <div class="akti-badge">AKADEMI KOMUNITAS TOYOTA INDONESIA</div>
        <div class="app-title">Dashboard Eksekutif & Evaluasi Tes Fisik</div>
        <div class="app-subtitle">Analisis Kinerja Jasmani Mahasiswa Angkatan A11 • Standar Manajemen Mutu</div>
    </div>
""", unsafe_allow_html=True)

# Tombol Aksi Canggih
col_rf1, col_rf2, col_rf3 = st.columns([2, 1, 2])
with col_rf2:
    if st.button("🔄 Perbarui Analisis Data"):
        st.toast("Data analitik berhasil disinkronkan!", icon="✨")

st.write("")

# --- KARTU KPI EKSEKUTIF ---
st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-bottom: 20px; color: #ffd700 !important; font-weight: 700;'>⚡ Ringkasan Metrik Utama Kebugaran Jasmani</h4>", unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown("""
        <div class="metric-container">
            <p style='font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-bottom: 5px; text-transform: uppercase;'>Total Teruji</p>
            <h2 style='color: #ffffff; font-weight: 800; margin: 0;'>94 Siswa</h2>
            <span style='font-size: 0.75rem; color: #ffd700;'>● 100% Roster Lengkap</span>
        </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
        <div class="metric-container">
            <p style='font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-bottom: 5px; text-transform: uppercase;'>Rata-rata Angkatan</p>
            <h2 style='color: #ffd700; font-weight: 800; margin: 0;'>78.4</h2>
            <span style='font-size: 0.75rem; color: #4ade80;'>▲ +3.2 dari target</span>
        </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
        <div class="metric-container">
            <p style='font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-bottom: 5px; text-transform: uppercase;'>Kategori Dominan</p>
            <h2 style='color: #ffffff; font-weight: 800; margin: 0;'>Bagus</h2>
            <span style='font-size: 0.75rem; color: #60a5fa;'>Range Skor 71-85</span>
        </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
        <div class="metric-container">
            <p style='font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-bottom: 5px; text-transform: uppercase;'>Perhatian Khusus</p>
            <h2 style='color: #f87171; font-weight: 800; margin: 0;'>6 Siswa</h2>
            <span style='font-size: 0.75rem; color: #f87171;'>▼ Prioritas Bimbingan</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- GRAFIK PLOTLY YANG CANGGIH & MEWAH ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #ffffff; font-weight: 700; margin-bottom: 5px;'>🎯 Distribusi Kategori Kebugaran Jasmani</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 15px;'>Proporsi klasifikasi tingkat kebugaran seluruh mahasiswa.</p>", unsafe_allow_html=True)

    # Data Distribusi Kategori
    df_kategori = pd.DataFrame({
        'Kategori': ['Sangat Bagus\n(86-100)', 'Bagus\n(71-85)', 'Cukup\n(56-70)', 'Kurang\n(<55)'],
        'Jumlah': [28, 45, 15, 6]
    })

    fig_donut = px.pie(
        df_kategori, 
        names='Kategori', 
        values='Jumlah', 
        hole=0.65,
        color_discrete_sequence=['#ffd700', '#f59e0b', '#3b82f6', '#ef4444']
    )
    fig_donut.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Plus Jakarta Sans'),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(t=10, b=30, l=10, r=10)
    )
    fig_donut.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#3b0707', width=3)))
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_g2:
    st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #ffffff; font-weight: 700; margin-bottom: 5px;'>📊 Rata-rata Skor Berdasarkan Item Tes</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 15px;'>Evaluasi performa rata-rata per item uji kemampuan fisik.</p>", unsafe_allow_html=True)

    # Data Item Tes
    df_item = pd.DataFrame({
        'Item Tes': ['Bleep Test', 'Pull-Up', 'Sit-Up', 'Push-Up', 'Shuttle Run'],
        'Skor': [82.5, 74.0, 85.5, 79.0, 80.2]
    })

    fig_bar = px.bar(
        df_item, 
        x='Item Tes', 
        y='Skor',
        text='Skor',
        color='Skor',
        color_continuous_scale=['#b91c1c', '#f59e0b', '#ffd700']
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Plus Jakarta Sans'),
        coloraxis_showscale=False,
        xaxis=dict(title='', showgrid=False),
        yaxis=dict(title='Skor Rata-rata', showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(t=10, b=10, l=10, r=10)
    )
    fig_bar.update_traces(texttemplate='%{text:.1f}', textposition='outside', marker=dict(cornerradius=8))
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- TABEL EVALUASI KHUSUS ---
st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
st.markdown("<h4 style='color: #ffffff; font-weight: 700; margin-bottom: 5px;'>🚨 Daftar Mahasiswa Membutuhkan Pendampingan Khusus</h4>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 20px;'>Mahasiswa dengan kategori Kurang (<55) yang memerlukan program latihan intensif dari pelatih jasmani.</p>", unsafe_allow_html=True)

df_perhatian = pd.DataFrame([
    {"No": 1, "Nama Mahasiswa": "FAJAR RISKI", "NIM": "PM26", "Nilai Rata-rata": 52.0, "Status": "Prioritas Pembinaan"},
    {"No": 2, "Nama Mahasiswa": "TARUNA", "NIM": "PM66", "Nilai Rata-rata": 48.5, "Status": "Prioritas Pembinaan"},
    {"No": 3, "Nama Mahasiswa": "USAMAH", "NIM": "PM90", "Nilai Rata-rata": 50.0, "Status": "Prioritas Pembinaan"}
])

st.dataframe(df_perhatian, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
