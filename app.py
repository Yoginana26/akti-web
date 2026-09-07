import streamlit as st
import requests

st.set_page_config(page_title="Rekap Test Fisik Mahasiswa Akti", page_icon="⚙️", layout="centered")

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzuNBeBPH6BiHr6MFjS03SIT3oAPYvjhnBL4V81Y5ylrZlzx3RIkQcLWGXcdRNcC99Xgw/exec"

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
    .akti-badge {
        display: inline-block; background: linear-gradient(135deg, rgba(212, 175, 55, 0.25), rgba(255, 215, 0, 0.05));
        border: 1px solid rgba(212, 175, 55, 0.6); color: #ffd700; padding: 6px 20px; border-radius: 50px;
        font-size: 0.8rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px;
    }
    .app-title { color: #ffffff !important; font-size: 2.2rem; font-weight: 800; margin-bottom: 6px; }
    .app-subtitle { color: rgba(255, 255, 255, 0.7) !important; font-size: 0.95rem; }
    p, span, h3, h4, label { color: rgba(255, 255, 255, 0.95) !important; }
    .stButton>button {
        width: 100%; background: linear-gradient(135deg, #ffd700 0%, #d4af37 100%) !important;
        color: #1a0202 !important; border-radius: 16px; padding: 16px; font-weight: 800; border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="app-header">
        <div class="akti-badge">AKADEMI KOMUNITAS TOYOTA INDONESIA</div>
        <div class="app-title">Form Input Capaian Test Fisik</div>
        <div class="app-subtitle">Sistem Penilaian & Konversi Otomatis Terintegrasi Cloud Database</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="iphone-glass-card">', unsafe_allow_html=True)
with st.form("manual_input_form"):
    pilihan_nama = st.selectbox("Pilih Nama Mahasiswa dari Daftar", options=["-- Pilih --"] + MAHASISWA_LIST)
    selected_nama = st.text_input("Konfirmasi / Edit Nama (Pastikan sama persis dengan Spreadsheet)", value="" if pilihan_nama == "-- Pilih --" else pilihan_nama)
    
    status_kehadiran = st.selectbox("Status Kehadiran Tes", ["Hadir & Ikut Tes", "Sakit", "Izin", "Tanpa Keterangan"])
    jk = st.radio("Jenis Kelamin", options=["Laki-laki (L)", "Perempuan (P)"], horizontal=True)
    
    c1, c2 = st.columns(2)
    with c1:
        input_tb = st.number_input("TB (CM)", value=0.0, format="%.2f")
        input_bb = st.number_input("BB (KG)", value=0.0, format="%.2f")
        capaian_bleep = st.number_input("Capaian Bleep Test", value=0.0, format="%.2f")
        capaian_pull = st.number_input("Capaian Pull-Up / Chinning", value=0, step=1)
    with c2:
        capaian_sit = st.number_input("Capaian Sit-Up", value=0, step=1)
        capaian_push = st.number_input("Capaian Push-Up", value=0, step=1)
        capaian_shuttle = st.number_input("Capaian Shuttle Run (Detik)", value=0.0, format="%.2f")
        
    submitted = st.form_submit_button("✨ HITUNG & SIMPAN KE DATABASE")
    
    if submitted:
        if not selected_nama or selected_nama == "-- Pilih --":
            st.error("⚠️ Silakan pilih atau ketik nama mahasiswa!")
        else:
            if status_kehadiran != "Hadir & Ikut Tes":
                bleep_score, pull_score, sit_score, push_score, shuttle_score = status_kehadiran, status_kehadiran, status_kehadiran, status_kehadiran, status_kehadiran
            else:
                max_bleep = 12.12
                bleep_score = round(min((capaian_bleep / max_bleep) * 100, 100), 2) if capaian_bleep > 0 else 0.0
                
                is_laki = "Laki-laki" in jk
                pull_score = 100 if (is_laki and capaian_pull >= 17) or (not is_laki and capaian_pull > 71) else (75 if (is_laki and capaian_pull >= 10) or (not is_laki and capaian_pull >= 53) else 50)
                sit_score = 100 if (is_laki and capaian_sit > 42) or (not is_laki and capaian_sit > 36) else (75 if (is_laki and capaian_sit >= 30) or (not is_laki and capaian_sit >= 28) else 50)
                push_score = 100 if (is_laki and capaian_push > 42) or (not is_laki and capaian_push > 36) else (75 if (is_laki and capaian_push >= 30) or (not is_laki and capaian_push >= 28) else 50)
                shuttle_score = 100 if (is_laki and 0 < capaian_shuttle < 17.0) or (not is_laki and 0 < capaian_shuttle < 19.0) else (75 if capaian_shuttle < 18.0 else 50)

            payload = {
                "nama": selected_nama.strip().upper(),
                "status": status_kehadiran,
                "tb": input_tb,
                "bb": input_bb,
                "bleep": bleep_score,
                "pull": pull_score,
                "sit": sit_score,
                "push": push_score,
                "shuttle": shuttle_score
            }
            
            try:
                response = requests.post(WEB_APP_URL, json=payload, timeout=15)
                res_data = response.json()
                if res_data.get("status") == "success":
                    st.success(f"🎉 Berhasil! Data status **{status_kehadiran}** untuk **{selected_nama}** berhasil disimpan.")
                else:
                    st.error(f"Gagal dari Server: {res_data.get('message')}")
            except Exception as e:
                st.error(f"Gagal terhubung: {e}")
st.markdown('</div>', unsafe_allow_html=True)
