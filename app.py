import streamlit as st
import pandas as pd
from datetime import datetime
import json
import urllib.request

# 1. Tetapan Asas Halaman Aplikasi
st.set_page_config(
    page_title="Sistem Laporan Harian Kontinjen Selangor",
    page_icon="👮‍♂️",
    layout="wide"
)

# Inisialisasi Pangkalan Data Dalam Memori (Session State)
if "pangkalan_data" not in st.session_state:
    st.session_state.pangkalan_data = pd.DataFrame(columns=[
        "ID Laporan", "Tarikh", "Kategori Utama", "Daerah / IPD", 
        "Ringkasan Perenggan Padat", "Teks Laporan Asal"
    ])

st.title("🛡️ Sistem Laporan Harian Kontinjen Selangor")
st.caption("Auto-Summarization Intelejen Berkuasa Google Gemini AI")
st.markdown("---")

SENARAI_KATEGORI = [
    "Ancaman Ekstremis Sosial",
    "Ancaman Ekstremis Luar",
    "Ancaman Ekstremis Politik",
    "Ancaman Ekstremis Ekonomi",
    "Keselamatan Dan Perlindungan"
]

SENARAI_DAERAH = [
    "Ampang", "Ampang Jaya", "Shah Alam", "Gombak", "Kajang", "Hulu Langat", 
    "Hulu Selangor", "Subang Jaya", "Petaling Jaya", "Klang Utara", 
    "Klang Selatan", "Sungai Buloh", "Kuala Langat", "Sepang", "Sabak Bernam"
]

# 2. Fungsi Gemini AI - Format Tepat 1 Perenggan Padat & Pembukaan Direct
def ringkas_satu_perenggan(teks_asal, kategori, api_key):
    prompt_arahan = f"""
    Anda adalah seorang Pegawai Analisis Intelejen Cawangan Khas PDRM Kontinjen Selangor.
    Tugas anda adalah merangkumkan laporan naratif berikut menjadi TEPAT SATU PERENGGAN PADAT (Single Solid Paragraph) sahaja.

    SYARAT STRICT FORMAT:
    1. PEMBUKAAN AYAT: WAJIB bermula terus dengan SUBJEK / NAMA PROGRAM UTAMA. Dilarang sama sekali menggunakan perkataan pembuka seperti "Telah berlangsung...", "Pada...", "Di...", atau "Berlangsungnya...".
       - Contoh BERSALAH: "Telah berlangsung Jualan Ehsan Rahmah..."
       - Contoh BETUL: "Program Jualan Ehsan Rahmah anjuran Pusat Khidmat Rakyat..."
    2. STRUCTURE: Tulis dalam SATU PERENGGAN SAHAJA. Dilarang sama sekali menggunakan bullet points (•), dash (-), nombor (1,2,3), atau perenggan baharu.
    3. ISI KANDUNGAN: Nyatakan lokasi, penganjur, kehadiran VIP/pemimpin utama, dan intipati kejadian dalam satu aliran ayat yang kemas, lancar, dan padat.
    4. PEMBERSIHAN: Buang semua tajuk kecil (seperti *Hadir*, *Jualan*), nombor perenggan asal, pecahan abjad (a, b, c), dan ayat menggantung (seperti "seperti berikut :-").
    5. LARAS BAHASA: Gunakan bahasa rasmi perkhidmatan intelejen PDRM yang tepat, rasmi, dan berasaskan fakta.

    Kategori Laporan: {kategori}

    Teks Laporan Asal:
    \"\"\"
    {teks_asal}
    \"\"\"
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key.strip()}"
    headers = {"Content-Type": "application/json"}
    
    data = {
        "contents": [{
            "parts": [{"text": prompt_arahan}]
        }]
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
    
    with urllib.request.urlopen(req) as response:
        res_body = response.read().decode('utf-8')
        res_json = json.loads(res_body)
        return res_json['candidates'][0]['content']['parts'][0]['text']

# 3. Sidebar Navigasi & Input API Key
menu = st.sidebar.radio("PILIH MODUL:", ["📝 Masukkan Laporan", "📊 Papan Pemuka & Analisis", "📄 Jana Laporan Penuh Keseluruhan"])

# ==========================================
# MODUL 1: MASUKKAN LAPORAN
# ==========================================
if menu == "📝 Masukkan Laporan":
    st.header("1. Pilih Kategori & Tampal Teks Laporan")
    
    with st.sidebar:
        st.markdown("---")
        st.subheader("🔑 Tetapan Gemini API")
        gemini_api_key = st.text_input("Masukkan Google Gemini API Key:", type="password")
        st.caption("Dapatkan API Key Percuma di: aistudio.google.com")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        kategori_pilihan = st.selectbox("📌 Pilih Kategori Tajuk:", SENARAI_KATEGORI)
        tarikh_laporan = st.date_input("Tarikh Laporan", datetime.now())

    with col2:
        teks_laporan_asal = st.text_area(
            "📥 Tampal Teks Laporan Penuh Di Sini:",
            height=280,
            placeholder="Tampal naratif laporan penuh di sini..."
        )

    st.markdown("---")
    
    if st.button("🚀 Process & Dapatkan 1 Perenggan Padat", use_container_width=True):
        if not gemini_api_key:
            st.error("Sila masukkan 'Google Gemini API Key' di bahagian menu tepi (Sidebar) terlebih dahulu!")
        elif not teks_laporan_asal.strip():
            st.warning("Sila tampal teks laporan terlebih dahulu!")
        else:
            with st.spinner("Gemini AI sedang menyusun laporan menjadi satu perenggan padat..."):
                try:
                    # Automatic District Detection
                    daerah_dikesan = "Selangor (Keseluruhan)"
                    for d in SENARAI_DAERAH:
                        if d.lower() in teks_laporan_asal.lower():
                            daerah_dikesan = d.upper()
                            break

                    ringkasan_perenggan = ringkas_satu_perenggan(teks_laporan_asal, kategori_pilihan, gemini_api_key)

                    id_rep = f"REP-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.pangkalan_data) + 1:03d}"
                    
                    data_baru = {
                        "ID Laporan": id_rep,
                        "Tarikh": tarikh_laporan.strftime("%Y-%m-%d"),
                        "Kategori Utama": kategori_pilihan,
                        "Daerah / IPD": daerah_dikesan,
                        "Ringkasan Perenggan Padat": ringkasan_perenggan,
                        "Teks Laporan Asal": teks_laporan_asal
                    }
                    
                    st.session_state.pangkalan_data = pd.concat([st.session_state.pangkalan_data, pd.DataFrame([data_baru])], ignore_index=True)
                    
                    st.success(f"✅ Laporan **[{kategori_pilihan}]** berjaya diringkaskan!")
                    st.info(ringkasan_perenggan)

                except Exception as e:
                    st.error(f"Ralat memproses Gemini API: {e}")

# ==========================================
# MODUL 2: PAPAN PEMUKA
# ==========================================
elif menu == "📊 Papan Pemuka & Analisis":
    st.header("📊 Papan Pemuka Analisis")
    df = st.session_state.pangkalan_data
    if df.empty:
        st.info("Pangkalan data kosong. Sila masukkan laporan terlebih dahulu.")
    else:
        st.metric("Jumlah Rekod Laporan", len(df))
        st.bar_chart(df["Kategori Utama"].value_counts())

# ==========================================
# MODUL 3: JANA LAPORAN PENUH KESELURUHAN
# ==========================================
elif menu == "📄 Jana Laporan Penuh Keseluruhan":
    st.header("📄 Draf Laporan Analisis Kontinjen Selangor")
    df = st.session_state.pangkalan_data
    
    if df.empty:
        st.info("Pangkalan data kosong. Sila masukkan laporan terlebih dahulu.")
    else:
        st.markdown(f"## **ANALISIS HARIAN KONTINJEN SELANGOR ({datetime.now().strftime('%d %b %Y').upper()})**")
        st.markdown("---")
        
        for kat in SENARAI_KATEGORI:
            df_kat = df[df["Kategori Utama"] == kat]
            st.markdown(f"### **{kat.upper()}**")
            
            if df_kat.empty:
                st.write("*Tiada sebarang laporan bagi kategori ini.*")
            else:
                for idx, row in df_kat.iterrows():
                    st.markdown(f"**[{row['Daerah / IPD']}]**")
                    st.markdown(row["Ringkasan Perenggan Padat"])
            st.markdown("---")

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Muat Turun Data (CSV)", csv, "Laporan_Selangor.csv", "text/csv")
