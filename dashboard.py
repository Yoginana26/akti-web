import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Eksekutif Test Fisik AKTI", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stApp { background: radial-gradient(circle at 50% 0%, #7a1212 0%, #3b0707 50%, #120202 100%) !important; background-attachment: fixed; }
    .iphone-glass-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.12); border-top: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 28px; padding: 28px; box-shadow: 0 25px 50px rgba(0, 0, 0, 0.6); margin-bottom: 24px;
    }
    .app-header { text-align: center; padding: 20px 0 30px 0; }
    .akti-logo-ring {
        width: 85px; height: 85px; background: radial-gradient(circle, rgba(255,215,0,0.15) 0%, rgba(255,255,255,0.05) 100%);
        border: 2px solid rgba(212, 175, 55, 0.6); border-radius: 50%; display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 25px rgba(212, 175, 55, 0.3); margin: 0 auto 15px auto;
    }
    .akti-badge {
        display: inline-block; background: linear-gradient(135deg, rgba(212, 175, 55, 0.25), rgba(255, 215, 0, 0.05));
        border: 1px solid rgba(212, 175, 55, 0.6); color: #ffd700; padding: 6px 20px; border-radius: 50px;
        font-size: 0.8rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px;
    }
    .app-title { color: #ffffff !important; font-size: 2.2rem; font-weight: 800; margin-bottom: 6px; }
    .app-subtitle { color: rgba(255, 255, 255, 0.7) !important; font-size: 0.95rem; }
    .podium-card {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(255, 255, 255, 0.03));
        border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 20px; padding: 20px; text-align: center;
    }
    .metric-container {
        background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px; padding: 20px; text-align: center;
    }
    p, span, h3, h4, label { color: rgba(255, 255, 255, 0.95) !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="app-header">
        <div class="akti-logo-ring"><span style="font-size: 28px;">🛡️</span></div>
        <div class="akti-badge">AKADEMI KOMUNITAS TOYOTA INDONESIA</div>
        <div class="app-title">Dashboard Eksekutif & Evaluasi Tes Fisik</div>
        <div class="app-subtitle">Analisis Kinerja Jasmani Mahasiswa Angkatan A11 • Standar Manajemen Mutu</div>
    </div>
""", unsafe_allow_html=True)

# --- SIMULASI DATA MASTER MAHASISWA & SPREADSHEET ---
# Data mencakup nilai riil sesuai spreadsheet Anda (termasuk status Sakit dan nilai per item)
data_master = [
    {"Nama": "AGUS SINATRIYA", "Gender": "Laki-laki (L)", "Bleep": 95, "Pull": 100, "Sit": 100, "Push": 100, "Shuttle": 98, "Rata_rata": 98.2, "Kategori": "Sangat Bagus (86-100)", "Status": "Hadir"},
    {"Nama": "AFFAN HIDAYATUR RAKHMAN", "Gender": "Laki-laki (L)", "Bleep": 92, "Pull": 100, "Sit": 98, "Push": 95, "Shuttle": 92, "Rata_rata": 95.4, "Kategori": "Sangat Bagus (86-100)", "Status": "Hadir"},
    {"Nama": "ADRIAN RIZKI ADITIYA", "Gender": "Laki-laki (L)", "Bleep": 90, "Pull": 100, "Sit": 95, "Push": 95, "Shuttle": 90, "Rata_rata": 94.0, "Kategori": "Sangat Bagus (86-100)", "Status": "Hadir"},
    {"Nama": "ABDUL AZIS HERMAWAN", "Gender": "Laki-laki (L)", "Bleep": 85, "Pull": 75, "Sit": 100, "Push": 100, "Shuttle": 81, "Rata_rata": 88.2, "Kategori": "Sangat Bagus (86-100)", "Status": "Hadir"},
    {"Nama": "KINANTI DWI PUTRIA", "Gender": "Perempuan (P)", "Bleep": 79, "Pull": 25, "Sit": 100, "Push": 100, "Shuttle": 75, "Rata_rata": 75.8, "Kategori": "Bagus (71-85)", "Status": "Hadir"},
    {"Nama": "LISA PUTRIANI", "Gender": "Perempuan (P)", "Bleep": 75, "Pull": 75, "Sit": 100, "Push": 75, "Shuttle": 50, "Rata_rata": 75.0, "Kategori": "Bagus (71-85)", "Status": "Hadir"},
    {"Nama": "FAJAR RISKI", "Gender": "Laki-laki (L)", "Bleep": 45, "Pull": 50, "Sit": 50, "Push": 50, "Shuttle": 63, "Rata_rata": 51.6, "Kategori": "Kurang (<55)", "Status": "Hadir"},
    {"Nama": "TARUNA", "Gender": "Laki-laki (L)", "Bleep": 42, "Pull": 50, "Sit": 50, "Push": 50, "Shuttle": 50, "Rata_rata": 48.4, "Kategori": "Kurang (<55)", "Status": "Hadir"},
    {"Nama": "USAMAH", "Gender": "Laki-laki (L)", "Bleep": 44, "Pull": 50, "Sit": 50, "Push": 50, "Shuttle": 50, "Rata_rata": 48.8, "Kategori": "Kurang (<55)", "Status": "Hadir"},
    # Mahasiswa Berhalangan (Sakit sesuai spreadsheet Anda)
    {"Nama": "MERI MARLIANA", "Gender": "Perempuan (P)", "Bleep": 0, "Pull": 0, "Sit": 0, "Push": 0, "Shuttle": 0, "Rata_rata": 0, "Kategori": "Berhalangan", "Status": "Sakit", "Keterangan": "Surat Dokter (Istirahat)"},
    {"Nama": "MUHAMMAD ADIEB ASSHULTHONI", "Gender": "Laki-laki (L)", "Bleep": 0, "Pull": 0, "Sit": 0, "Push": 0, "Shuttle": 0, "Rata_rata": 0, "Kategori": "Berhalangan", "Status": "Sakit", "Keterangan": "Surat Dokter"},
    {"Nama": "MUHAMMAD HARY ADI SYAPUTRA PURBA", "Gender": "Laki-laki (L)", "Bleep": 0, "Pull": 0, "Sit": 0, "Push": 0, "Shuttle": 0, "Rata_rata": 0, "Kategori": "Berhalangan", "Status": "Sakit", "Keterangan": "Izin Medis"}
]
df_master = pd.DataFrame(data_master)

# --- PANEL FILTER INTERAKTIF MANAJEMEN ---
st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    filter_gender = st.selectbox("👥 Filter Jenis Kelamin", ["Semua Gender", "Laki-laki (L)", "Perempuan (P)"])
with col_f2:
    filter_kategori = st.selectbox("🎯 Filter Kategori Kebugaran", ["Semua Kategori", "Sangat Bagus (86-100)", "Bagus (71-85)", "Cukup (56-70)", "Kurang (<55)"])
with col_f3:
    st.write("")
    if st.button("🔄 Segarkan Data Analitik", use_container_width=True):
        st.toast("Data analitik berhasil disinkronkan!", icon="✨")
st.markdown('</div>', unsafe_allow_html=True)

# Logika Pemfilteran Data Sesuai Pilihan User
df_filtered = df_master[df_master['Status'] == 'Hadir']
if filter_gender != "Semua Gender":
    df_filtered = df_filtered[df_filtered['Gender'] == filter_gender]
if filter_kategori != "Semua Kategori":
    df_filtered = df_filtered[df_filtered['Kategori'] == filter_kategori]

# --- TAMPILAN HASIL FILTER (NAMA & PERINGKAT 1, 2, 3 BERDASARKAN FILTER) ---
st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
st.markdown(f"<h4 style='color: #ffd700; font-weight: 700; margin-bottom: 5px;'>🔍 Hasil Filter: {filter_gender} | {filter_kategori}</h4>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 15px;'>Daftar mahasiswa yang sesuai dengan kriteria filter beserta peringkat teratasnya.</p>", unsafe_allow_html=True)

if df_filtered.empty:
    st.warning("⚠️ Tidak ada data mahasiswa yang ditemukan dengan kriteria filter tersebut.")
else:
    # Urutkan berdasarkan nilai rata-rata tertinggi untuk menentukan peringkat
    df_sorted = df_filtered.sort_values(by='Rata_rata', ascending=False).reset_index(drop=True)
    
    col_res1, col_res2 = st.columns([1.2, 2])
    with col_res1:
        st.markdown("##### 🏅 Peringkat 1 - 3 (Berdasarkan Filter)")
        for idx, row in df_sorted.head(3).iterrows():
            medali = ["👑", "🥈", "🥉"][idx]
            st.markdown(f"""
                <div style='background: rgba(255,215,0,0.1); border: 1px solid rgba(212,175,55,0.4); border-radius: 12px; padding: 10px; margin-bottom: 8px;'>
                    <b>{medali} Peringkat {idx+1}: {row['Nama']}</b><br>
                    <span style='color: #ffd700; font-size: 0.85rem;'>Skor Rata-rata: {row['Rata_rata']} ({row['Gender']})</span>
                </div>
            """, unsafe_allow_html=True)
            
    with col_res2:
        st.markdown("##### 📋 Daftar Mahasiswa dalam Kategori Ini")
        st.dataframe(df_sorted[['Nama', 'Gender', 'Rata_rata', 'Kategori']], use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# Kartu KPI
st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-bottom: 20px; color: #ffd700 !important; font-weight: 700;'>⚡ Ringkasan Metrik Utama Kebugaran Jasmani</h4>", unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown("""<div class="metric-container"><p style='font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-bottom: 5px; text-transform: uppercase;'>Total Teruji</p><h2 style='color: #ffffff; font-weight: 800; margin: 0;'>94 Siswa</h2><span style='font-size: 0.75rem; color: #ffd700;'>● Roster Lengkap</span></div>""", unsafe_allow_html=True)
with kpi2:
    st.markdown("""<div class="metric-container"><p style='font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-bottom: 5px; text-transform: uppercase;'>Rata-rata Angkatan</p><h2 style='color: #ffd700; font-weight: 800; margin: 0;'>78.4</h2><span style='font-size: 0.75rem; color: #4ade80;'>▲ +3.2 dari target</span></div>""", unsafe_allow_html=True)
with kpi3:
    st.markdown("""<div class="metric-container"><p style='font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-bottom: 5px; text-transform: uppercase;'>Kategori Dominan</p><h2 style='color: #ffffff; font-weight: 800; margin: 0;'>Bagus</h2><span style='font-size: 0.75rem; color: #60a5fa;'>Range Skor 71-85</span></div>""", unsafe_allow_html=True)
with kpi4:
    st.markdown("""<div class="metric-container"><p style='font-size: 0.8rem; color: rgba(255,255,255,0.6); margin-bottom: 5px; text-transform: uppercase;'>Perhatian Khusus</p><h2 style='color: #f87171; font-weight: 800; margin: 0;'>6 Siswa</h2><span style='font-size: 0.75rem; color: #f87171;'>▼ Prioritas Bimbingan</span></div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Visualisasi Utama (Donut & Gauge)
col_g1, col_g2 = st.columns(2)
with col_g1:
    st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #ffffff; font-weight: 700; margin-bottom: 5px;'>🎯 Distribusi Kategori Kebugaran Jasmani</h4>", unsafe_allow_html=True)
    df_kategori_count = pd.DataFrame({'Kategori': ['Sangat Bagus (86-100)', 'Bagus (71-85)', 'Cukup (56-70)', 'Kurang (<55)'], 'Jumlah': [28, 45, 15, 6]})
    fig_donut = px.pie(df_kategori_count, names='Kategori', values='Jumlah', hole=0.65, color_discrete_sequence=['#ffd700', '#f59e0b', '#3b82f6', '#ef4444'])
    fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', family='Plus Jakarta Sans'), legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5), margin=dict(t=10, b=30, l=10, r=10))
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_g2:
    st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #ffffff; font-weight: 700; margin-bottom: 5px;'>⚡ Indikator Performa Institusi (Gauge)</h4>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta", value = 78.4,
        delta = {'reference': 75.0, 'increasing': {'color': "#4ade80"}},
        number = {'font': {'color': 'white', 'size': 45}},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "white"}, 'bar': {'color': "#ffd700"},
            'bgcolor': "rgba(255,255,255,0.05)", 'borderwidth': 2, 'bordercolor': "rgba(255,255,255,0.2)",
            'steps': [{'range': [0, 55], 'color': 'rgba(239, 68, 68, 0.4)'}, {'range': [55, 70], 'color': 'rgba(59, 130, 246, 0.4)'}, {'range': [70, 85], 'color': 'rgba(245, 158, 11, 0.4)'}, {'range': [85, 100], 'color': 'rgba(255, 215, 0, 0.4)}'}],
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 75.0}
        }
    ))
    fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', family='Plus Jakarta Sans'), margin=dict(t=20, b=20, l=20, r=20), height=270)
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- RADAR CHART CANGGIH DENGAN FUNGSI ANALISIS PERBANDINGAN ---
col_r1, col_r2 = st.columns(2)
with col_r1:
    st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #ffffff; font-weight: 700; margin-bottom: 5px;'>🕸️ Profil Kebugaran Jasmani Lanjutan (Radar Chart)</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 15px;'>Analisis perbandingan profil kemampuan antar komponen tes fisik.</p>", unsafe_allow_html=True)

    categories = ['Bleep Test', 'Pull-Up', 'Sit-Up', 'Push-Up', 'Shuttle Run']
    scores_avg = [82.5, 74.0, 85.5, 79.0, 80.2]
    scores_target = [85.0, 80.0, 85.0, 80.0, 85.0]  # Garis Target Standar Institusi

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=scores_avg, theta=categories, fill='toself',
        name='Rata-rata Aktual Angkatan',
        fillcolor='rgba(212, 175, 55, 0.3)',
        line=dict(color='#ffd700', width=3)
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=scores_target, theta=categories, fill='none',
        name='Target Standar Minimum',
        line=dict(color='#60a5fa', width=2, dash='dot')
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color='rgba(255,255,255,0.6)', gridcolor='rgba(255,255,255,0.1)'),
            angularaxis=dict(color='white', gridcolor='rgba(255,255,255,0.1)', tittle='')
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Plus Jakarta Sans'),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        margin=dict(t=20, b=30, l=20, r=20),
        height=320
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_r2:
    st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #ffffff; font-weight: 700; margin-bottom: 5px;'>📊 Perbandingan Skor per Item Tes</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 15px;'>Evaluasi detail tingkat pencapaian tiap komponen tes jasmani.</p>", unsafe_allow_html=True)

    df_item = pd.DataFrame({'Item Tes': ['Bleep Test', 'Pull-Up', 'Sit-Up', 'Push-Up', 'Shuttle Run'], 'Skor': [82.5, 74.0, 85.5, 79.0, 80.2]})
    fig_bar = px.bar(df_item, x='Item Tes', y='Skor', text='Skor', color='Skor', color_continuous_scale=['#b91c1c', '#f59e0b', '#ffd700'])
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Plus Jakarta Sans'),
        coloraxis_showscale=False,
        xaxis=dict(title='', showgrid=False),
        yaxis=dict(title='Skor Rata-rata', showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        margin=dict(t=10, b=10, l=10, r=10),
        height=320
    )
    fig_bar.update_traces(texttemplate='%{text:.1f}', textposition='outside', marker=dict(cornerradius=8))
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- TABEL MAHASISWA BERHALANGAN (SESUAI SPREADSHEET RIIL) ---
st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
st.markdown("<h4 style='color: #60a5fa; font-weight: 700; margin-bottom: 5px;'>🏥 Daftar Mahasiswa Berhalangan (Sakit / Izin)</h4>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 20px;'>Daftar mahasiswa yang tidak mengikuti tes fisik berdasarkan data aktual spreadsheet.</p>", unsafe_allow_html=True)

df_sakit_aktual = df_master[df_master['Status'] == 'Sakit'].reset_index(drop=True)
df_sakit_aktual.index = df_sakit_aktual.index + 1
df_sakit_display = df_sakit_aktual[['Nama', 'Gender', 'Status', 'Keterangan']].rename_columns = df_sakit_aktual.rename(columns={'Nama': 'Nama Mahasiswa'})

st.dataframe(df_sakit_aktual[['Nama', 'Gender', 'Status', 'Keterangan']], use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Podium Top 3 Keseluruhan
st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
st.markdown("<h4 style='color: #ffd700; font-weight: 700; margin-bottom: 5px;'>🏆 Podium Top 3 Mahasiswa Berprestasi Jasmani (Keseluruhan)</h4>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("""<div class="podium-card"><span style='font-size: 28px;'>🥈</span><h3 style='margin: 5px 0 0 0; color: white;'>AFFAN HIDAYATUR</h3><p style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin: 0;'>Laki-laki (L)</p><h2 style='color: #ffd700; margin-top: 10px;'>95.4</h2></div>""", unsafe_allow_html=True)
with p2:
    st.markdown("""<div class="podium-card" style='border: 2px solid #ffd700; background: linear-gradient(135deg, rgba(255,215,0,0.25), rgba(255,255,255,0.05));'><span style='font-size: 36px;'>👑</span><h3 style='margin: 5px 0 0 0; color: #ffd700;'>AGUS SINATRIYA</h3><p style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin: 0;'>Laki-laki (L)</p><h2 style='color: #ffd700; margin-top: 10px;'>98.2</h2></div>""", unsafe_allow_html=True)
with p3:
    st.markdown("""<div class="podium-card"><span style='font-size: 28px;'>🥉</span><h3 style='margin: 5px 0 0 0; color: white;'>ADRIAN RIZKI</h3><p style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin: 0;'>Laki-laki (L)</p><h2 style='color: #ffd700; margin-top: 10px;'>94.0</h2></div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
