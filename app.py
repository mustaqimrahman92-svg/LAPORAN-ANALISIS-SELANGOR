import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

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
        "Ringkasan Profesional (AI)", "Teks Laporan Asal"
    ])

st.title("🛡️ Sistem Laporan Harian Kontinjen Selangor")
st.caption("Auto-Summarization Berkuasa OpenAI ChatGPT (Format Intelejen PDRM)")
st.markdown("---")

menu = st.sidebar.radio("PILIH MODUL:", ["📝 Masukkan Laporan (Auto-AI)", "📊 Papan Pemuka & Analisis", "📄 Jana Laporan Penuh Keseluruhan"])

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

# 2. Fungsi Meringkaskan Teks Menggunakan ChatGPT API
def ringkas_guna_chatgpt(teks_asal, kategori, api_key):
    client = OpenAI(api_key=api_key)
    
    prompt_arahan = f"""
    Anda adalah seorang Pegawai Analisis Intelejen Cawangan Khas PDRM Kontinjen Selangor.
    Tugas anda adalah meringkaskan laporan naratif panjang berikut menjadi laporan intel/operasi yang sangat profesional, padat, dan berasaskan fakta.

    Kategori Laporan: {kategori}

    SYARAT RINGKASAN:
    1. Ekstrak maklumat berikut sahaja dalam bentuk bullet points:
       - Subjek / Program / Kejadian Utama
       - Penganjur / VIP / Entiti Terlibat
       - Kehadiran / Impak
       - Intipati / Kronologi Ringkas
       - Implikasi Keselamatan / Politik / Sosiopolitik (jika ada)
    2. Gunakan bahasa rasmi perkhidmatan keselamatan/polis.
    3. Buang sebarang ayat tergantung, ayat pengenalan yang tidak berguna, atau format nombor perenggan asal.
    4. Pastikan hasil akhir adalah ringkas tetapi padat (3 hingga 5 poin sahaja).

    Teks Laporan Naratif:
    \"\"\"
    {teks_asal}
    \"\"\"
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Anda adalah pakar penganalisis laporan keselamatan PDRM yang tepat dan profesional."},
            {"role": "user", "content": prompt_arahan}
        ],
        temperature=0.2
    )
    
    return response.choices[0].message.content

# ==========================================
# MODUL 1: MASUKKAN LAPORAN (AUTO-AI)
# ==========================================
if menu == "📝 Masukkan Laporan (Auto-AI)":
    st.header("1. Pilih Kategori & Tampal Teks Laporan")
    
    # Input OpenAI API Key di Sidebar atau Ruang Input
    with st.sidebar:
        st.markdown("---")
        st.subheader("🔑 Tetapan API ChatGPT")
        openai_api_key = st.text_input("Masukkan OpenAI API Key:", type="password")
        st.caption("Dapatkan API Key di: platform.openai.com")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        kategori_pilihan = st.selectbox("📌 Pilih Kategori Tajuk:", SENARAI_KATEGORI)
        tarikh_laporan = st.date_input("Tarikh Laporan", datetime.now())

    with col2:
        teks_laporan_asal = st.text_area(
            "📥 Tampal Teks Laporan Penuh Di Sini:",
            height=280,
            placeholder="Tampal keseluruhan naratif laporan panjang di sini..."
        )

    st.markdown("---")
    
    if st.button("🤖 Process & Ringkaskan Guna ChatGPT", use_container_width=True):
        if not openai_api_key:
            st.error("Sila masukkan 'OpenAI API Key' di bahagian menu tepi (Sidebar) terlebih dahulu!")
        elif not teks_laporan_asal.strip():
            st.warning("Sila tampal teks laporan terlebih dahulu!")
        else:
            with st.spinner("ChatGPT sedang menganalisis dan meringkaskan laporan mengikut format intel..."):
                try:
                    # 1. Automatic District Detection
                    daerah_dikesan = "Selangor (Keseluruhan)"
                    for d in SENARAI_DAERAH:
                        if d.lower() in teks_laporan_asal.lower():
                            daerah_dikesan = d.upper()
                            break

                    # 2. Call ChatGPT API
                    hasil_ringkasan_ai = ringkas_guna_chatgpt(teks_laporan_asal, kategori_pilihan, openai_api_key)

                    # 3. Save to Database
                    id_rep = f"REP-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.pangkalan_data) + 1:03d}"
                    
                    data_baru = {
                        "ID Laporan": id_rep,
                        "Tarikh": tarikh_laporan.strftime("%Y-%m-%d"),
                        "Kategori Utama": kategori_pilihan,
                        "Daerah / IPD": daerah_dikesan,
                        "Ringkasan Profesional (AI)": hasil_ringkasan_ai,
                        "Teks Laporan Asal": teks_laporan_asal
                    }
                    
                    st.session_state.pangkalan_data = pd.concat([st.session_state.pangkalan_data, pd.DataFrame([data_baru])], ignore_index=True)
                    
                    st.success(f"✅ Laporan **[{kategori_pilihan}]** berjaya diringkaskan oleh ChatGPT dan disimpan!")
                    st.subheader("💡 Hasil Ringkasan Format Intel ChatGPT:")
                    st.markdown(hasil_ringkasan_ai)

                except Exception as e:
                    st.error(f"Ralat semasa membuat sambungan ke API ChatGPT: {e}")

# ==========================================
# MODUL 2: PAPAN PEMUKA
# ==========================================
elif menu == "📊 Papan Pemuka & Analisis":
    st.header("📊 Papan Pemuka Analisis")
    df = st.session_state.pangkalan_data
    if df.empty:
        st.info("Tiada data. Sila masukkan laporan terlebih dahulu.")
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
                    st.markdown(row["Ringkasan Profesional (AI)"])
                    with st.expander("Lihat Teks Asal Penuh"):
                        st.write(row["Teks Laporan Asal"])
            st.markdown("---")

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Muat Turun Data (CSV)", csv, "Laporan_Selangor.csv", "text/csv")
