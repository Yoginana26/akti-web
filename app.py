import streamlit as st
import pandas as pd
import os
import base64
import re

APP_NAME = "VEGA"
APP_FULL = "Vehicle Evaluation Guide & Assistant"

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title=f"{APP_NAME} | {APP_FULL}",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATABASE USER (LOGIN MP) ---
# role: "user" = hanya melihat SOP, "admin" = bisa menambah SOP baru
USERS = {
    "mp01": {"password": "1234", "role": "user"},
    "mp02": {"password": "1234", "role": "user"},
    "admin": {"password": "admin123", "role": "admin"},
}

# --- DIREKTORI FILE ---
DATA_DIR = "Sop data"
MASTER_EXCEL = os.path.join(DATA_DIR, "master_tools.xlsx")
SOPS_DIR = os.path.join(DATA_DIR, "Sops")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
VIDEOS_DIR = os.path.join(DATA_DIR, "videos")

os.makedirs(SOPS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = None
if "selected_step" not in st.session_state:
    st.session_state.selected_step = None
if "role" not in st.session_state:
    st.session_state.role = "user"

# --- CUSTOM STYLING (navy, gold, ivory) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    --ink: #0f2230;  --ink-2: #16303f;
    --gold: #b08a3e;  --gold-dark: #8f6d2a;
    --ivory: #f7f5f0;  --sand: #efe9dc;  --line: #e6e0d2;
    --text: #14212b;  --muted: #6f7a85;
}
html, body, [class*="css"], .stApp, button, input { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background: var(--ivory); color: var(--text); }
[data-testid="stHeader"] { background: transparent; }
.stAppDeployButton, #MainMenu, footer { display: none !important; }
[data-testid="stHeaderActionElements"], h1 a, h2 a, h3 a { display: none !important; }
.block-container { padding-top: 2.2rem; max-width: 1240px; }

h1, h2, h3, p, label, span, li { color: var(--text); }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: var(--muted) !important; }
.serif { font-family: 'Playfair Display', Georgia, serif; }

/* ---------- Input ---------- */
.stTextInput [data-baseweb="input"] {
    background: #fff !important; border: 1px solid #d8d2c4 !important; border-radius: 10px !important;
}
.stTextInput [data-baseweb="input"]:focus-within { border-color: var(--gold) !important; box-shadow: 0 0 0 3px rgba(176,138,62,.15) !important; }
.stTextInput [data-baseweb="base-input"] { background: transparent !important; }
.stTextInput input {
    background: transparent !important; color: var(--text) !important; border: none !important;
    box-shadow: none !important; padding: .8rem 1rem !important; font-size: .95rem !important;
}
.stTextInput input::placeholder { color: #9aa3ad !important; }
.stTextInput label p { color: var(--text) !important; font-weight: 600; font-size: .85rem; }

/* ---------- Tombol ---------- */
.stButton > button, .stDownloadButton > button {
    background: #fff; color: var(--ink); border: 1px solid var(--ink); border-radius: 10px;
    font-weight: 600; font-size: .9rem; padding: .55rem 1rem; transition: all .18s;
}
.stButton > button p, .stDownloadButton > button p { color: inherit !important; }
.stButton > button:hover, .stDownloadButton > button:hover { background: var(--ink); color: #fff; border-color: var(--ink); }
.stFormSubmitButton > button {
    background: var(--ink); color: #fff; border: none; border-radius: 10px;
    font-weight: 600; padding: .75rem 1rem; width: 100%; letter-spacing: .3px;
}
.stFormSubmitButton > button p { color: #fff !important; }
.stFormSubmitButton > button:hover { background: var(--gold); color: #fff; }

/* ---------- Login ---------- */
.brand-panel {
    position: relative; min-height: 600px; padding: 2.8rem 2.6rem; border-radius: 22px; background-color: var(--ink);
    background-image: repeating-linear-gradient(135deg, rgba(255,255,255,.03) 0 1px, transparent 1px 16px);
    display: flex; flex-direction: column; justify-content: space-between;
}
.bp-label { color: var(--gold) !important; font-size: .78rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; }
.bp-name { font-family: 'Playfair Display', serif; color: #fff !important; font-size: 5.2rem; font-weight: 700; line-height: 1; margin: 1.6rem 0 0; letter-spacing: 4px; }
.bp-rule { width: 56px; height: 2px; background: var(--gold); margin: 1.4rem 0; }
.bp-full { color: #f3efe6 !important; font-size: 1.15rem; font-weight: 500; margin: 0 0 .8rem; }
.bp-text { color: #a9b6c1 !important; font-size: .95rem; line-height: 1.7; max-width: 380px; margin: 0; }
.bp-foot { color: #8fa0ae !important; font-size: .8rem; letter-spacing: .6px; }
.bp-foot b { color: var(--gold) !important; font-weight: 600; margin: 0 .35rem; }
.login-title { font-family: 'Playfair Display', serif; font-size: 2.3rem; font-weight: 700; margin: 0 0 .4rem; color: var(--ink); }
.login-sub { color: var(--muted); margin: 0 0 1.5rem; font-size: .95rem; }
[data-testid="stForm"] { background: #fff; border: 1px solid var(--line); border-radius: 16px; padding: 1.6rem; box-shadow: 0 8px 28px rgba(15,34,48,.06); }

/* ---------- Hero (katalog & detail) ---------- */
.hero {
    border-radius: 22px; padding: 2.2rem 2.4rem; margin-bottom: 1.6rem; background-color: var(--ink);
    background-image: repeating-linear-gradient(135deg, rgba(255,255,255,.03) 0 1px, transparent 1px 16px);
    display: flex; justify-content: space-between; align-items: center; gap: 2rem; flex-wrap: wrap;
}
.hero-label { color: var(--gold) !important; font-size: .75rem; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; }
.hero-title { font-family: 'Playfair Display', serif; color: #fff !important; font-size: 2.4rem; font-weight: 700; margin: .5rem 0 .4rem; line-height: 1.15; }
.hero p { color: #a9b6c1 !important; margin: 0; font-size: .98rem; max-width: 520px; }
.hero-rule { width: 48px; height: 2px; background: var(--gold); margin: .9rem 0 .9rem; }
.stats { display: flex; gap: 2.2rem; }
.stat { text-align: center; padding-left: 2.2rem; border-left: 1px solid rgba(255,255,255,.14); }
.stat:first-child { border-left: none; padding-left: 0; }
.stat b { font-family: 'Playfair Display', serif; display: block; color: var(--gold) !important; font-size: 2.3rem; font-weight: 700; line-height: 1; }
.stat span { color: #a9b6c1 !important; font-size: .78rem; letter-spacing: 1px; text-transform: uppercase; }

/* ---------- Filter kategori ---------- */
[data-testid="stBaseButton-pills"], [data-testid="stBaseButton-pillsActive"] {
    border-radius: 999px !important; font-size: .85rem !important; padding: .3rem 1rem !important;
}
[data-testid="stBaseButton-pills"] { background: #fff !important; border: 1px solid #d8d2c4 !important; color: var(--text) !important; }
[data-testid="stBaseButton-pillsActive"] { background: var(--ink) !important; border: 1px solid var(--ink) !important; color: #fff !important; }
[data-testid="stBaseButton-pills"] *, [data-testid="stBaseButton-pills"] p { color: var(--text) !important; }
[data-testid="stBaseButton-pillsActive"] *, [data-testid="stBaseButton-pillsActive"] p { color: #fff !important; }

/* ---------- Admin ---------- */
[data-testid="stSidebar"] [data-testid="stRadio"] label p { color: #f3efe6 !important; font-weight: 600; }
.stTextArea textarea { background: #fff !important; color: var(--text) !important; border: 1px solid #d8d2c4 !important; border-radius: 10px !important; }
[data-testid="stFileUploaderDropzone"] { background: #fff; border: 1px dashed #cfc7b3; border-radius: 12px; }
.admin-sec { font-family: 'Playfair Display', serif; font-size: 1.15rem; font-weight: 700; color: var(--ink); margin: 1.2rem 0 .4rem; }

/* ---------- Kartu ---------- */
[data-testid="stVerticalBlockBorderWrapper"]:has(.tool-marker) {
    background: #fff; border: 1px solid var(--line); border-radius: 16px; padding: .55rem; transition: all .22s;
}
[data-testid="stVerticalBlockBorderWrapper"]:has(.tool-marker):hover {
    border-color: var(--gold); transform: translateY(-4px); box-shadow: 0 14px 30px rgba(15,34,48,.10);
}
.tool-img { width: 100%; height: 160px; object-fit: cover; border-radius: 11px; margin-bottom: .9rem; }
.tool-ph {
    width: 100%; height: 160px; border-radius: 11px; margin-bottom: .9rem; background: var(--sand);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Playfair Display', serif; font-size: 3.4rem; font-weight: 700; color: var(--ink);
}
.tool-cat { color: var(--gold-dark); font-size: .72rem; font-weight: 700; letter-spacing: 1.4px; text-transform: uppercase; }
.tool-title { font-family: 'Playfair Display', serif; font-size: 1.25rem; font-weight: 700; margin: .35rem 0 .35rem; color: var(--ink); line-height: 1.3; }
.tool-desc { color: var(--muted); font-size: .9rem; line-height: 1.55; min-height: 2.9rem; margin-bottom: .6rem; }
.chips { min-height: 28px; margin-bottom: .6rem; }
.chip { display: inline-block; font-size: .7rem; font-weight: 600; padding: .15rem .65rem; border-radius: 999px;
        border: 1px solid var(--line); color: var(--muted); margin-right: .35rem; background: var(--ivory); }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] { background: var(--ink); border-right: none; }
[data-testid="stSidebar"] .stButton > button { background: transparent; color: #f3efe6; border: 1px solid rgba(255,255,255,.25); }
[data-testid="stSidebar"] .stButton > button:hover { background: var(--gold); border-color: var(--gold); color: #fff; }
[data-testid="stSidebar"] svg { color: #f3efe6; fill: #f3efe6; }
.side-brand { padding: .6rem 0 1.2rem; border-bottom: 1px solid rgba(255,255,255,.12); margin-bottom: 1.2rem; }
.side-brand b { font-family: 'Playfair Display', serif; color: #fff !important; font-size: 1.9rem; letter-spacing: 3px; display: block; }
.side-brand span { color: var(--gold) !important; font-size: .68rem; letter-spacing: 1.8px; text-transform: uppercase; font-weight: 600; }
.user-chip { display: flex; align-items: center; gap: .75rem; padding: .8rem; border-radius: 12px;
             background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.1); margin-bottom: 1rem; }
.avatar { width: 40px; height: 40px; border-radius: 50%; background: var(--gold); color: #fff !important;
          display: flex; align-items: center; justify-content: center; font-weight: 700; }
.user-chip small { color: #8fa0ae !important; display: block; font-size: .72rem; }
.user-chip b { color: #fff !important; font-size: .95rem; }

/* ---------- Detail ---------- */
.stTabs [data-baseweb="tab"] p { color: var(--muted); font-weight: 600; }
.stTabs [aria-selected="true"] p { color: var(--ink); }
.stTabs [data-baseweb="tab-highlight"] { background-color: var(--gold); }

[data-testid="stSidebar"] .stButton > button p { color: #f3efe6 !important; }
[data-testid="stSidebar"] .stButton > button:hover p { color: #fff !important; }

[data-testid="stImage"] img { border-radius: 12px; border: 1px solid var(--line); box-shadow: 0 8px 24px rgba(15,34,48,.08); }

.st-key-steppanel { position: sticky; top: 3.8rem; }
.panel-label { color: var(--gold-dark); font-size: .72rem; font-weight: 700; letter-spacing: 1.6px; text-transform: uppercase; margin-bottom: .6rem; }
.step-no { color: var(--gold-dark); font-size: .75rem; font-weight: 700; letter-spacing: 1.4px; text-transform: uppercase; margin-top: 1rem; }
.step-title { font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; color: var(--ink); line-height: 1.35; margin: .25rem 0 .9rem; }
.st-key-steprow .stButton > button { border-radius: 999px; height: 46px; padding: 0; font-weight: 700; font-size: 1rem; }
.st-key-steprow [data-testid="stBaseButton-primary"] { background: var(--ink) !important; border: 1px solid var(--ink) !important; color: #fff !important; }
.st-key-steprow [data-testid="stBaseButton-primary"] p { color: #fff !important; }
.st-key-steprow [data-testid="stBaseButton-primary"]:hover { background: var(--gold) !important; border-color: var(--gold) !important; }

.foot { text-align: center; color: var(--muted); font-size: .8rem; letter-spacing: .5px;
        margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--line); }
</style>
""", unsafe_allow_html=True)

# Sembunyikan sidebar saat belum login
if not st.session_state.logged_in:
    st.markdown("""<style>[data-testid="stSidebar"], [data-testid="collapsedControl"]
                 { display: none; }</style>""", unsafe_allow_html=True)


# --- LOAD MASTER DATA ---
@st.cache_data
def load_master_tools():
    if os.path.exists(MASTER_EXCEL):
        return pd.read_excel(MASTER_EXCEL)
    else:
        # Dummy data untuk pengujian
        return pd.DataFrame({
            "ID_Tool": [1, 2],
            "Nama_Tool": ["Centering Daisha Junbiki", "SOP Pulpen"],
            "Kategori": ["Logistics", "Alat Tulis"],
            "Deskripsi": ["Penanganan fault daisha no center dengan lorong di Junbiki.",
                          "Petunjuk penggunaan pulpen checklist."],
            "File_SOP": ["BS JUNBIKI.pdf", "SOP_Pulpen.pdf"],
            "Link_Video": ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", ""],
            "Gambar_Tool": ["daisha.jpg", "pulpen.jpg"]
        })


# --- GAMBAR TOOL -> base64 (untuk kartu) ---
@st.cache_data
def image_to_data_uri(path):
    ext = os.path.splitext(path)[1].lower().strip(".")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    with open(path, "rb") as f:
        return f"data:image/{mime};base64," + base64.b64encode(f.read()).decode()


# --- FUNGSI RENDER PDF INTERAKTIF ---
def display_pdf_viewer(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'''
        <iframe src="data:application/pdf;base64,{base64_pdf}#toolbar=0&navpanes=0"
                width="100%"
                height="850px"
                type="application/pdf"
                style="border: 1px solid #e6e0d2; border-radius: 14px; background: #fff;">
        </iframe>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)


# --- DATA LANGKAH (SHEET "Steps" di master_tools.xlsx) ---
@st.cache_data
def load_steps():
    cols = ["ID_Tool", "No_Step", "Judul_Step", "Video"]
    try:
        if os.path.exists(MASTER_EXCEL):
            df = pd.read_excel(MASTER_EXCEL, sheet_name="Steps")
        else:
            # Dummy data untuk pengujian (langkah SOP Centering Daisha Junbiki)
            df = pd.DataFrame({
                "ID_Tool": [1] * 7,
                "No_Step": list(range(1, 8)),
                "Judul_Step": [
                    "Pindahkan selector switch ke mode manual, pastikan tidak ada MP di area Junbiki",
                    "Pastikan daisha di home position dan tidak ada cylinder block di daisha",
                    "Pilih mode Teaching pada system dan masukkan password",
                    "Lakukan teaching sesuai sequence, jalankan daisha dari home position ke lorong 1-12",
                    "Centering daisha dengan lorong, tekan arah CW atau CCW pada system",
                    "Save koordinat saat lampu indikator center menyala, pastikan sequence 1-12",
                    "Setelah centering selesai, daisha kembali ke home position, ubah selector ke mode auto",
                ],
                "Video": [""] * 7,
            })
        df["No_Step"] = pd.to_numeric(df["No_Step"], errors="coerce")
        df = df.dropna(subset=["No_Step"])
        df["No_Step"] = df["No_Step"].astype(int)
        return df[cols].sort_values(["ID_Tool", "No_Step"])
    except Exception:
        return pd.DataFrame(columns=cols)


# --- PDF -> GAMBAR (tanpa toolbar viewer) ---
@st.cache_data(show_spinner=False)
def pdf_to_images(path, mtime):
    import fitz  # pip install pymupdf
    pages = []
    with fitz.open(path) as doc:
        for p in doc:
            if p.get_text().strip() or p.get_images():
                pages.append(p.get_pixmap(matrix=fitz.Matrix(2.2, 2.2)).tobytes("png"))
        if not pages:
            pages.append(doc[0].get_pixmap(matrix=fitz.Matrix(2.2, 2.2)).tobytes("png"))
    return pages


def render_sop_image(tool):
    fname = str(tool["File_SOP"])
    path = os.path.join(SOPS_DIR, fname)
    if not os.path.exists(path):
        st.error(f"File SOP `{fname}` belum diunggah ke folder `{SOPS_DIR}`.")
        return

    ext = os.path.splitext(fname)[1].lower()
    if ext in (".png", ".jpg", ".jpeg", ".webp"):
        st.image(path, use_container_width=True)
        return

    try:
        pages = pdf_to_images(path, os.path.getmtime(path))
        pg = 1
        if len(pages) > 1:
            pg = st.radio("Halaman", list(range(1, len(pages) + 1)), horizontal=True)
        st.image(pages[pg - 1], use_container_width=True)
    except ImportError:
        st.warning("Install dulu dengan perintah: pip install pymupdf  (sementara tampil mode PDF biasa)")
        display_pdf_viewer(path)

    with open(path, "rb") as f:
        st.download_button("Download PDF SOP", data=f, file_name=fname, mime="application/pdf")


def show_video(value):
    v = "" if pd.isna(value) else str(value).strip()
    local = os.path.join(VIDEOS_DIR, v)
    if v.startswith("http"):
        st.video(v)
    elif v and os.path.isfile(local):
        st.video(local)
    else:
        st.info("Video untuk langkah ini belum tersedia.")


def render_step_panel(tool, steps):
    full_url = str(tool["Link_Video"]).strip()
    full_url = full_url if video_ok(full_url) else ""
    options = ([0] if full_url else []) + [int(n) for n in steps["No_Step"]]

    st.markdown('<div class="panel-label">Video Per Langkah</div>', unsafe_allow_html=True)
    if not options:
        st.info("Video instruksi belum tersedia.")
        return

    if st.session_state.selected_step not in options:
        st.session_state.selected_step = options[0]
    cur = st.session_state.selected_step

    with st.container(key="steprow"):
        for start in range(0, len(options), 6):
            cols = st.columns(6)
            for c, n in zip(cols, options[start:start + 6]):
                label = "Full" if n == 0 else str(n)
                if c.button(label, key=f"step_{n}", type="primary" if n == cur else "secondary",
                            use_container_width=True):
                    st.session_state.selected_step = n
                    st.rerun()

    if cur == 0:
        st.markdown('<div class="step-no">Video Lengkap</div><div class="step-title">Seluruh Proses</div>',
                    unsafe_allow_html=True)
        show_video(full_url)
    else:
        row = steps[steps["No_Step"] == cur].iloc[0]
        judul = "" if pd.isna(row["Judul_Step"]) else row["Judul_Step"]
        st.markdown(f'<div class="step-no">Langkah {cur}</div><div class="step-title">{judul}</div>',
                    unsafe_allow_html=True)
        show_video(row["Video"])

    i = options.index(cur)
    b1, b2 = st.columns(2)
    if b1.button("← Sebelumnya", key="prev_step", disabled=i == 0, use_container_width=True):
        st.session_state.selected_step = options[i - 1]
        st.rerun()
    if b2.button("Berikutnya →", key="next_step", disabled=i == len(options) - 1, use_container_width=True):
        st.session_state.selected_step = options[i + 1]
        st.rerun()


# --- HELPER FOTO & VIDEO ---
def find_image(name):
    """Cari foto tool di folder images (toleran terhadap beda ekstensi)."""
    name = "" if pd.isna(name) else str(name).strip()
    if not name:
        return None
    p = os.path.join(IMAGES_DIR, name)
    if os.path.isfile(p):
        return p
    stem = os.path.splitext(name)[0]
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".jfif"):
        p = os.path.join(IMAGES_DIR, stem + ext)
        if os.path.isfile(p):
            return p
    return None


def video_ok(v):
    v = "" if pd.isna(v) else str(v).strip()
    return v.startswith("http") or (v != "" and os.path.isfile(os.path.join(VIDEOS_DIR, v)))


def tool_has_video(row, df_steps):
    if video_ok(row["Link_Video"]):
        return True
    s = df_steps[df_steps["ID_Tool"] == row["ID_Tool"]]
    return bool(len(s) and s["Video"].apply(video_ok).any())


# --- SIMPAN DATA (ADMIN) ---
VID_TYPES = ["mp4", "mov", "webm", "mkv"]
IMG_TYPES = ["jpg", "jpeg", "png", "webp"]


def slugify(text):
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")[:40] or "sop"


def save_upload(file, folder, base):
    fname = base + os.path.splitext(file.name)[1].lower()
    with open(os.path.join(folder, fname), "wb") as f:
        f.write(file.getbuffer())
    return fname


def save_data(df_tools, df_steps):
    sheets = {}
    if os.path.exists(MASTER_EXCEL):
        try:
            sheets = pd.read_excel(MASTER_EXCEL, sheet_name=None)
        except Exception:
            sheets = {}
    tool_sheet = next((n for n in sheets if n != "Steps"), "Tools")
    ordered = {tool_sheet: df_tools, "Steps": df_steps}
    for n, d in sheets.items():
        if n not in ordered:
            ordered[n] = d
    with pd.ExcelWriter(MASTER_EXCEL, engine="openpyxl") as w:
        for n, d in ordered.items():
            d.to_excel(w, sheet_name=n, index=False)


def update_tool_photo(tool_id, title, file):
    """Simpan foto baru ke folder images dan perbarui kolom Gambar_Tool di Excel."""
    try:
        df_t = load_master_tools().copy()
        fname = save_upload(file, IMAGES_DIR, f"{int(tool_id)}_{slugify(str(title))}")
        if "Gambar_Tool" not in df_t.columns:
            df_t["Gambar_Tool"] = ""
        df_t["Gambar_Tool"] = df_t["Gambar_Tool"].astype(object)
        df_t.loc[df_t["ID_Tool"] == tool_id, "Gambar_Tool"] = fname
        save_data(df_t, load_steps())
        st.cache_data.clear()
        return True, ""
    except PermissionError:
        return False, "Tutup dulu file master_tools.xlsx jika sedang terbuka di Excel."
    except ImportError:
        return False, "Library openpyxl belum terpasang. Jalankan: pip install openpyxl"
    except Exception as e:
        return False, f"Gagal menyimpan: {e}"


# --- HALAMAN ADMIN: TAMBAH SOP BARU ---
def admin_page():
    st.markdown(
        '<div class="hero"><div><span class="hero-label">Mode Admin</span>'
        '<div class="hero-title">Kelola SOP</div><div class="hero-rule"></div>'
        '<p>Tambahkan SOP tool baru lengkap dengan foto, file PDF, dan video.</p></div></div>',
        unsafe_allow_html=True
    )

    df_t = load_master_tools()
    cats = sorted(df_t["Kategori"].dropna().astype(str).unique().tolist())

    n_steps = st.number_input("Jumlah langkah SOP (untuk video per langkah, isi 0 jika tidak ada)",
                              min_value=0, max_value=20, value=0, step=1)

    with st.form("add_sop", clear_on_submit=True):
        st.markdown('<div class="admin-sec">Informasi SOP</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        judul = c1.text_input("Judul SOP *", placeholder="contoh: Centering Daisha Junbiki")
        kat_pilih = c2.selectbox("Kategori", ["— pilih —"] + cats)
        kat_baru = c2.text_input("Atau kategori baru", placeholder="kosongkan jika memakai kategori di atas")
        deskripsi = c1.text_area("Deskripsi singkat", height=100)

        st.markdown('<div class="admin-sec">File</div>', unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        foto = f1.file_uploader("Foto tools (JPG / PNG)", type=IMG_TYPES)
        pdf = f2.file_uploader("File SOP (PDF) *", type=["pdf"])

        st.markdown('<div class="admin-sec">Video lengkap (opsional)</div>', unsafe_allow_html=True)
        v1, v2 = st.columns(2)
        full_file = v1.file_uploader("Upload video", type=VID_TYPES, key="full_file")
        full_link = v2.text_input("Atau link video (https://...)", key="full_link")

        steps_in = []
        if n_steps:
            st.markdown('<div class="admin-sec">Video per langkah</div>', unsafe_allow_html=True)
        for i in range(1, int(n_steps) + 1):
            a, b, c = st.columns([1.3, 1.2, 1.2])
            j = a.text_input(f"Judul langkah {i}", key=f"sj{i}")
            vf = b.file_uploader(f"Video langkah {i}", type=VID_TYPES, key=f"sf{i}")
            vl = c.text_input(f"Atau link langkah {i}", key=f"sl{i}")
            steps_in.append((i, j, vf, vl))

        ok = st.form_submit_button("Simpan SOP", use_container_width=True)

    if not ok:
        return

    kat = kat_baru.strip() or (kat_pilih if kat_pilih != "— pilih —" else "")
    if not judul.strip():
        st.error("Judul SOP wajib diisi.")
        return
    if not kat:
        st.error("Pilih kategori atau isi kategori baru.")
        return
    if pdf is None:
        st.error("File SOP (PDF) wajib diunggah.")
        return
    if judul.strip().lower() in df_t["Nama_Tool"].astype(str).str.lower().values:
        st.error("Judul SOP sudah ada. Gunakan judul lain.")
        return

    mx = pd.to_numeric(df_t["ID_Tool"], errors="coerce").max()
    new_id = (0 if pd.isna(mx) else int(mx)) + 1
    base = f"{new_id}_{slugify(judul)}"

    try:
        pdf_name = save_upload(pdf, SOPS_DIR, base)
        foto_name = save_upload(foto, IMAGES_DIR, base) if foto is not None else ""
        full_val = save_upload(full_file, VIDEOS_DIR, f"{base}_full") if full_file is not None else full_link.strip()

        new_steps = []
        for i, j, vf, vl in steps_in:
            val = save_upload(vf, VIDEOS_DIR, f"{base}_step{i}") if vf is not None else vl.strip()
            if j.strip() or val:
                new_steps.append({"ID_Tool": new_id, "No_Step": i,
                                  "Judul_Step": j.strip() or f"Langkah {i}", "Video": val})

        row = {"ID_Tool": new_id, "Nama_Tool": judul.strip(), "Kategori": kat,
               "Deskripsi": deskripsi.strip(), "File_SOP": pdf_name,
               "Link_Video": full_val, "Gambar_Tool": foto_name}
        df_t2 = pd.concat([df_t, pd.DataFrame([row])], ignore_index=True)
        df_s = load_steps()
        df_s2 = pd.concat([df_s, pd.DataFrame(new_steps)], ignore_index=True) if new_steps else df_s

        save_data(df_t2, df_s2)
        st.cache_data.clear()
        st.success(f"SOP \"{judul.strip()}\" berhasil ditambahkan. Buka menu Katalog SOP untuk melihatnya.")
    except PermissionError:
        st.error("Gagal menyimpan: tutup dulu file master_tools.xlsx jika sedang terbuka di Excel.")
    except ImportError:
        st.error("Library openpyxl belum terpasang. Jalankan: pip install openpyxl")
    except Exception as e:
        st.error(f"Gagal menyimpan: {e}")


# --- HALAMAN LOGIN ---
def login_page():
    col1, col2 = st.columns([1.1, 1], gap="large")

    with col1:
        st.markdown(f"""
        <div class="brand-panel">
            <div>
                <span class="bp-label">Vehicle Evaluation</span>
                <div class="bp-name">{APP_NAME}</div>
                <div class="bp-rule"></div>
                <p class="bp-full">{APP_FULL}</p>
                <p class="bp-text">Pusat panduan penggunaan tools untuk tim Vehicle Evaluation.
                Temukan lembar SOP dan video tutorial dalam hitungan detik.</p>
            </div>
            <div class="bp-foot">SOP Terstruktur<b>·</b>Video Tutorial<b>·</b>Akses Cepat</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="height:9vh"></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Selamat Datang</div>'
                    '<div class="login-sub">Masuk dengan ID MP untuk mengakses SOP tools VE.</div>',
                    unsafe_allow_html=True)
        with st.form("login_form"):
            user = st.text_input("Username / ID MP", placeholder="contoh: mp01")
            pwd = st.text_input("Password", type="password", placeholder="Masukkan password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if user in USERS and USERS[user]["password"] == pwd:
                st.session_state.logged_in = True
                st.session_state.username = user
                st.session_state.role = USERS[user]["role"]
                st.rerun()
            else:
                st.error("ID MP atau Password tidak valid.")


# --- HALAMAN UTAMA DASHBOARD ---
def main_dashboard():
    uname = st.session_state.username
    is_admin = st.session_state.role == "admin"
    st.sidebar.markdown(
        f'<div class="side-brand"><b>{APP_NAME}</b><span>Vehicle Evaluation</span></div>'
        f'<div class="user-chip"><div class="avatar">{uname[:1].upper()}</div>'
        f'<div><small>{"Administrator" if is_admin else "MP Active"}</small><b>{uname}</b></div></div>',
        unsafe_allow_html=True
    )
    menu = "Katalog SOP"
    if is_admin:
        menu = st.sidebar.radio("Menu", ["Katalog SOP", "Kelola SOP"], label_visibility="collapsed")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.selected_tool = None
        st.session_state.role = "user"
        st.rerun()

    if is_admin and menu == "Kelola SOP":
        admin_page()
        return

    df_master = load_master_tools()

    # --- JIKA TERPILIH TAMPILAN SOP TOOL ---
    if st.session_state.selected_tool is not None:
        tool = st.session_state.selected_tool

        if st.button("← Kembali ke Daftar Tools"):
            st.session_state.selected_tool = None
            st.rerun()

        desc = "" if pd.isna(tool["Deskripsi"]) else tool["Deskripsi"]
        st.markdown(
            f'<div class="hero" style="margin-top:1rem"><div>'
            f'<span class="hero-label">{tool["Kategori"]}</span>'
            f'<div class="hero-title">{tool["Nama_Tool"]}</div><div class="hero-rule"></div><p>{desc}</p></div></div>',
            unsafe_allow_html=True
        )

        df_steps = load_steps()
        steps = df_steps[df_steps["ID_Tool"] == tool["ID_Tool"]]

        col_sop, col_vid = st.columns([1.35, 1], gap="large")
        with col_sop:
            render_sop_image(tool)
        with col_vid:
            with st.container(key="steppanel"):
                render_step_panel(tool, steps)

    # --- KATALOG TOOL / SEARCH VIEW ---
    else:
        df_steps_all = load_steps()
        n_video = sum(tool_has_video(r, df_steps_all) for _, r in df_master.iterrows())
        n_kat = df_master["Kategori"].dropna().nunique()
        st.markdown(
            f'<div class="hero"><div>'
            f'<span class="hero-label">{APP_NAME} &nbsp;·&nbsp; {APP_FULL}</span>'
            f'<div class="hero-title">Katalog SOP &amp; Tools</div><div class="hero-rule"></div>'
            f'<p>Temukan panduan penggunaan tools Vehicle Evaluation dengan cepat dan tepat.</p></div>'
            f'<div class="stats">'
            f'<div class="stat"><b>{len(df_master)}</b><span>SOP</span></div>'
            f'<div class="stat"><b>{n_kat}</b><span>Kategori</span></div>'
            f'<div class="stat"><b>{n_video}</b><span>Video</span></div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

        search = st.text_input(
            "Cari", placeholder="Cari SOP tool, contoh: Pulpen, Junbiki, Daisha",
            label_visibility="collapsed"
        )

        kategori_list = ["Semua"] + sorted(df_master["Kategori"].dropna().astype(str).unique().tolist())
        if hasattr(st, "pills"):
            kat = st.pills("Kategori", kategori_list, default="Semua", label_visibility="collapsed") or "Semua"
        else:
            kat = st.radio("Kategori", kategori_list, horizontal=True, label_visibility="collapsed")

        filtered = df_master.copy()
        if search:
            filtered = filtered[
                filtered["Nama_Tool"].astype(str).str.contains(search, case=False, na=False) |
                filtered["Deskripsi"].astype(str).str.contains(search, case=False, na=False)
            ]
        if kat != "Semua":
            filtered = filtered[filtered["Kategori"].astype(str) == kat]

        st.caption(f"{len(filtered)} SOP ditemukan")
        if filtered.empty:
            st.info("Tidak ada SOP yang cocok. Coba kata kunci lain.")

        cols = st.columns(3)
        for idx, row in filtered.reset_index(drop=True).iterrows():
            with cols[idx % 3]:
                with st.container(border=True):
                    img_path = find_image(row.get("Gambar_Tool"))
                    if img_path:
                        visual = f'<img class="tool-img" src="{image_to_data_uri(img_path)}">'
                    else:
                        visual = f'<div class="tool-ph">{str(row["Nama_Tool"])[:1].upper()}</div>'

                    chips = ""
                    if os.path.exists(os.path.join(SOPS_DIR, str(row["File_SOP"]))):
                        chips += '<span class="chip">PDF</span>'
                    if tool_has_video(row, df_steps_all):
                        chips += '<span class="chip">Video</span>'

                    desc = "" if pd.isna(row["Deskripsi"]) else row["Deskripsi"]
                    st.markdown(
                        f'<div class="tool-marker"></div>{visual}'
                        f'<div class="tool-cat">{row["Kategori"]}</div>'
                        f'<div class="tool-title">{row["Nama_Tool"]}</div>'
                        f'<div class="tool-desc">{desc}</div>'
                        f'<div class="chips">{chips}</div>',
                        unsafe_allow_html=True
                    )

                    if st.button("Lihat SOP  →", key=f"btn_{row['ID_Tool']}", use_container_width=True):
                        st.session_state.selected_tool = row
                        st.session_state.selected_step = None
                        st.rerun()

        st.markdown(f'<div class="foot">{APP_NAME} &nbsp;·&nbsp; {APP_FULL} &nbsp;·&nbsp; Divisi Vehicle Evaluation</div>',
                    unsafe_allow_html=True)


# --- RUNNING APP ---
if not st.session_state.logged_in:
    login_page()
else:
    main_dashboard()
