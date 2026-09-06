import streamlit as st
import requests

# Konfigurasi Halaman Web
st.set_page_config(page_title="Rekap Test Fisik Mahasiswa Akti", page_icon="⚙️", layout="centered")

# URL Web App Google Apps Script Anda
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzuNBeBPH6BiHr6MFjS03SIT3oAPYvjhnBL4V81Y5ylrZlzx3RIkQcLWGXcdRNcC99Xgw/exec"

# Daftar Referensi Nama Mahasiswa AKTI (Dapat diedit bebas di bawah)
MAHASISWA_LIST = [
    'ABDUL AZIS HERMAWAN', 'ABDULRAHMAN AL BARBASI', 'ADRIAN RIZKI ADITIYA', 'AFFAN HIDAYATUR RAKHMAN',
    'AGUS SINATRIYA', 'AHMAD HUMAEDI', 'AJIE ALAMSYAH', 'AKBAR FEBRIANO PERKASA', 'ALLAN YUDHA WIDANARTO',
    'ANDI HERMAWAN', 'ANDIK AWALURRIZQI', 'ANDRA', 'ANELKA RAHMAT SETYADI', 'AURELIA LUNA FARHANAH',
    'AZKA FAR\'AZ ARHAB', 'CAHYO KUSUMA PERMADI', 'CATUR MUBAROK', 'DAFA ADQILA', 'DANI ARDIANSYAH',
    'DEDI IRAWAN', 'DIMAS RAMADHAN', 'DIMAS RIFKI PERMANA', 'DIMAS SYAHPUTRA', 'ERLAND AS SAHLAN',
    'FAHMI RIDHO', 'FAIZ ABDILLAH', 'FAJAR RISKI', 'FAJAR RIZKI PRATAMA', 'FATHURRAHMAN AL GHOZY',
    'FELIX FEBRIAN HARI PANGESTU', 'HAFIS HIBATULLAH', 'HASBI NOVA RIANDA', 'HOPI NUROHMAN',
    'ILHAM SUCI ANSHORI', 'ILHAM YUSUF KHANAFI', 'ISLA KHOIRONUL IZAZ', 'ISYA SYAEFUDDIN TSALAS',
    'JAFFAR AS SIDHIQ', 'JAVARA FIRZI NURFAIDHILAH', 'KINANTI DWI PUTRI', 'LISA PUTRIANI',
    'LUTFHY ASROFUL ANAM', 'M. RAFFA ZEIN', 'M. RASSYA ADZIKRA', 'MAHADAYA BISMA PUTRA NUR ISTANTO',
    'MAHESA ALIF QUROTA AYUN', 'MERI MARLIANA', 'MUCH ULINNUHA', 'MUHAMAD AVISENNA',
    'MUHAMAD FADIL ARMAN', 'MUHAMMAD RAFLI', 'MUHAMMAD ADIEB ASSHULTHONI', 'MUHAMMAD AGASTYA DHAFA',
    'MUHAMMAD AMMAR FIRJATULLAH', 'MUHAMMAD DAVIN ALFIANSYAH', 'MUHAMMAD DIAS IBRAHIM',
    'MUHAMMAD DZAKKI RAMASYAH', 'MUHAMMAD FAIQ HAIDAR', 'MUHAMMAD HAFADZA ALGHIFARY',
    'MUHAMMAD HARY ADI SYAPUTRA PURBA', 'MUHAMMAD HATRAS', 'MUHAMMAD KHAIDAR ALI',
    'NARASHEVA MAHARDIKA', 'NAUFAL ARAFIF APRILIAN', 'NAUFAL KHOIRUDIN', 'NAYLA AULIA BERLIANA LUKMAN',
    'NAZWA HANIDA', 'NURWAHYU UMBARA', 'PANDU ALFIAN EZRA', 'PAULUS SADHANA KUS DANANG MUSTIKO',
    'PUTRI ANDINI', 'PUTRI APRILIA', 'RADIF MUHAMMAD SALMAN', 'RADJA PUTRA AKMAL MALIKI',
    'RAFID DAFFA ABIYYU', 'RANDY ARYANTO', 'REIHAN FADHILAH', 'RENDY ARJIYADI SAPUTRA',
    'RESTU PRANANDA ADITIYA', 'REVALDO', 'REYHAN ADLI DZAKI HAVILA', 'REYHAN KURNIAWAN',
    'RIFKY AL GHOZALI', 'RIFQI KHOERUS SAFI', 'RISKI SURYA PRATAMA', 'RIZQI MAULANA',
    'SINDI YANI', 'TARUNA', 'TEGGAR RAMADHAN', 'TRI SETYANI ANINDITA', 'USAMAH', 'VAREL MAULANA',
    'WAHYU AJI SASONGKO', 'ZICO BRILIYAN ANDREANO'
]

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
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        margin-bottom: 25px;
    }

    .app-header {
        text-align: center;
        padding: 15px 0 25px 0;
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
        margin-bottom: 12px;
    }

    .app-title {
        color: #ffffff !important;
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .app-subtitle {
        color: rgba(255, 255, 255, 0.65) !important;
        font-size: 0.95rem;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 12px 16px !important;
    }

    label, .stRadio label, p, span {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
        font-size: 0.9rem;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ffd700 0%, #d4af37 100%) !important;
        color: #1a0202 !important;
        border-radius: 16px;
        padding: 16px 20px;
        font-weight: 800;
        font-size: 1.05rem;
        border: none;
        box-shadow: 0 10px 25px rgba(212, 175, 55, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Header Utama Web
st.markdown("""
    <div class="app-header">
        <div class="akti-badge">AKADEMI KOMUNITAS TOYOTA INDONESIA</div>
        <div class="app-title">Rekap Test Fisik Mahasiswa Akti</div>
        <div class="app-subtitle">Sistem Penilaian & Konversi Otomatis Terintegrasi Cloud Database</div>
    </div>
""", unsafe_allow_html=True)

# Form Input Nilai
st.markdown('<div class="apple-glass-card">', unsafe_allow_html=True)
st.markdown("<div style='font-size: 1.2rem; font-weight: 700; color: #ffffff; margin-bottom: 6px;'>📝 Form Capaian Tes Fisik</div>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 0.85rem; color: rgba(255,255,255,0.7); margin-bottom: 20px;'>Pilih nama dari daftar atau ketik/edit langsung untuk menyesuaikan dengan spreadsheet.</p>", unsafe_allow_html=True)

with st.form("manual_input_form"):
    # Menggunakan st.selectbox untuk memilih, tapi kita sediakan text input agar bisa diedit jika ada yang kurang pas
    pilihan_nama = st.selectbox("1. Pilih Nama Mahasiswa dari Daftar", options=["-- Pilih Manual / Ketik Sendiri --"] + MAHASISWA_LIST)
    
    # Kotak teks untuk mengedit atau mengetik langsung nama jika berbeda
    default_val = "" if pilihan_nama == "-- Pilih Manual / Ketik Sendiri --" else pilihan_nama
    selected_nama = st.text_input("2. Konfirmasi / Edit Nama (Pastikan sama persis dengan Spreadsheet)", value=default_val)

    jk = st.radio("Jenis Kelamin", options=["Laki-laki (L)", "Perempuan (P)"], horizontal=True)
    
    c1, c2 = st.columns(2)
    with c1:
        input_tb = st.number_input("TB (CM)", value=0.0, format="%.2f")
        input_bb = st.number_input("BB (KG)", value=0.0, format="%.2f")
        capaian_bleep = st.number_input("Capaian Bleep Test (Misal: 11.7)", value=0.0, format="%.2f")
        
        if "Laki-laki" in jk:
            capaian_pull = st.number_input("Capaian Pull-Up", value=0, step=1)
        else:
            capaian_pull = st.number_input("Capaian Chinning (Perempuan)", value=0, step=1)
            
    with c2:
        capaian_sit = st.number_input("Capaian Sit-Up", value=0, step=1)
        capaian_push = st.number_input("Capaian Push-Up", value=0, step=1)
        capaian_shuttle = st.number_input("Capaian Shuttle Run (Detik, misal: 17.3)", value=0.0, format="%.2f")
        
    submitted = st.form_submit_button("✨ HITUNG & SIMPAN KE DATABASE")
    
    if submitted:
        if not selected_nama or selected_nama.strip() == "":
            st.error("⚠️ Nama mahasiswa tidak boleh kosong! Silakan pilih atau ketik namanya.")
        else:
            with st.spinner("⏳ Menghitung nilai konversi & mengirim ke spreadsheet..."):
                try:
                    is_laki = "Laki-laki" in jk
                    
                    # --- 1. BLEEP TEST (Proporsional: Maks 12.12 = 100) ---
                    max_bleep = 12.12
                    if capaian_bleep > 0:
                        calc_bleep = (capaian_bleep / max_bleep) * 100
                        if calc_bleep > 100: calc_bleep = 100.0
                        bleep_score = round(calc_bleep, 2)
                    else:
                        bleep_score = 0.0
                        
                    # --- 2. PULL-UP / CHINNING ---
                    pull_score = 25
                    if is_laki:
                        if capaian_pull >= 17: pull_score = 100
                        elif capaian_pull >= 10: pull_score = 75
                        elif capaian_pull >= 5: pull_score = 50
                    else:
                        if capaian_pull > 71: pull_score = 100
                        elif capaian_pull >= 53: pull_score = 75
                        elif capaian_pull >= 35: pull_score = 50
                        
                    # --- 3. SIT-UP ---
                    sit_score = 25
                    if is_laki:
                        if capaian_sit > 42: sit_score = 100
                        elif capaian_sit >= 30: sit_score = 75
                        elif capaian_sit >= 20: sit_score = 50
                    else:
                        if capaian_sit > 36: sit_score = 100
                        elif capaian_sit >= 28: sit_score = 75
                        elif capaian_sit >= 19: sit_score = 50
                        
                    # --- 4. PUSH-UP ---
                    push_score = 25
                    if is_laki:
                        if capaian_push > 42: push_score = 100
                        elif capaian_push >= 30: push_score = 75
                        elif capaian_push >= 20: push_score = 50
                    else:
                        if capaian_push > 36: push_score = 100
                        elif capaian_push >= 28: push_score = 75
                        elif capaian_push >= 18: push_score = 50
                        
                    # --- 5. SHUTTLE RUN ---
                    shuttle_score = 25
                    if is_laki:
                        if capaian_shuttle > 0 and capaian_shuttle < 17.0: shuttle_score = 100
                        elif capaian_shuttle < 18.0: shuttle_score = 75
                        elif capaian_shuttle <= 19.0: shuttle_score = 50
                    else:
                        if capaian_shuttle > 0 and capaian_shuttle < 19.0: shuttle_score = 100
                        elif capaian_shuttle < 20.0: shuttle_score = 75
                        elif capaian_shuttle <= 22.0: shuttle_score = 50

                    payload = {
                        "nama": selected_nama.strip().upper(),
                        "tb": input_tb,
                        "bb": input_bb,
                        "bleep": bleep_score,
                        "pull": pull_score,
                        "sit": sit_score,
                        "push": push_score,
                        "shuttle": shuttle_score
                    }
                    
                    response = requests.post(WEB_APP_URL, json=payload, timeout=15)
                    res_data = response.json()
                    
                    if res_data.get("status") == "success":
                        st.success(
                            f"🎉 Berhasil! Konversi nilai tersimpan di baris ke-{res_data.get('row')} "
                            f"untuk **{selected_nama.strip()}**:\n\n"
                            f"- Bleep Test ➔ **{bleep_score}**\n"
                            f"- Pull/Chinning ➔ **{pull_score}**\n"
                            f"- Sit-Up ➔ **{sit_score}**\n"
                            f"- Push-Up ➔ **{push_score}**\n"
                            f"- Shuttle Run ➔ **{shuttle_score}**"
                        )
                    else:
                        st.error(f"Gagal dari Server: {res_data.get('message')}")
                except Exception as e:
                    st.error(f"Gagal terhubung: {e}")
st.markdown('</div>', unsafe_allow_html=True)
