import streamlit as st
import pandas as pd
import re
from datetime import datetime

# 1. Tetapan Asas Halaman Aplikasi
st.set_page_config(
    page_title="Sistem Analisis Laporan Selangor",
    page_icon="👮‍♂️",
    layout="wide"
)

# Inisialisasi Pangkalan Data Dalam Memori (Session State)
if "pangkalan_data" not in st.session_state:
    st.session_state.pangkalan_data = pd.DataFrame(columns=[
        "ID Laporan", "Tarikh", "Kategori Utama", "Daerah / IPD", 
        "Ringkasan Ringkas & Profesional", "Teks Laporan Asal"
    ])

st.title("🛡️ Sistem Analisis & Ringkasan Laporan Kontinjen Selangor")
st.caption("Pilih Kategori → Tampal Laporan Penuh → Auto-Ringkas & Simpan")
st.markdown("---")

# Navigation Menu Sidebar
menu = st.sidebar.radio("PILIH MODUL:", ["📝 Masukkan Laporan", "📊 Papan Pemuka & Analisis", "📄 Jana Laporan Penuh Keseluruhan"])

# Senarai 5 Kategori Rasmi
SENARAI_KATEGORI = [
    "Ancaman Ekstremis Sosial",
    "Ancaman Ekstremis Luar",
    "Ancaman Ekstremis Politik",
    "Ancaman Ekstremis Ekonomi",
    "Keselamatan Dan Perlindungan"
]

# Senarai Daerah Selangor untuk Auto-Detect
SENARAI_DAERAH = [
    "Shah Alam", "Gombak", "Kajang", "Hulu Langat", "Hulu Selangor", 
    "Subang Jaya", "Petaling Jaya", "Klang Utara", "Klang Selatan", 
    "Sungai Buloh", "Kuala Langat", "Sepang", "Sabak Bernam"
]

# ==========================================
# MODUL 1: MASUKKAN LAPORAN (SELECTION + FULL TEXT)
# ==========================================
if menu == "📝 Masukkan Laporan":
    st.header("1. Pilih Kategori & Tampal Teks Laporan")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # STEP 1: Pilih Kategori Tajuk
        kategori_pilihan = st.selectbox(
            "📌 Pilih Kategori Tajuk:",
            SENARAI_KATEGORI
        )
        
        tarikh_laporan = st.date_input("Tarikh Laporan", datetime.now())

    with col2:
        # STEP 2: Tampal Teks Laporan Penuh bagi Kategori Tersebut
        teks_laporan_asal = st.text_area(
            "📥 Tampal Teks Laporan Penuh / Naratif Panjang Di Sini:",
            height=250,
            placeholder="Tampal keseluruhan perenggan/naratif laporan untuk kategori yang dipilih di sebelah..."
        )

    st.markdown("---")
    
    if st.button("🚀 Ringkaskan & Simpan Laporan", use_container_width=True):
        if not teks_laporan_asal.strip():
            st.warning("Sila tampal teks laporan terlebih dahulu sebelum menyimpan!")
        else:
            # LOGIK AUTO-RINGKAS TEKS (Secara Profesional)
            # 1. Kesan Daerah secara automatik dari teks
            daerah_dikesan = "Selangor (Keseluruhan)"
            for d in SENARAI_DAERAH:
                if d.lower() in teks_laporan_asal.lower():
                    daerah_dikesan = d
                    break

            # 2. Pembersihan & Meringkaskan Teks (Ambil poin utama / perenggan terawal & penting)
            ayat_senarai = [a.strip() for a in re.split(r'\n+|\.\s+', teks_laporan_asal) if len(a.strip()) > 10]
            
            # Membuang nombor perenggan seperti "2. ", "3. " dari ayat
            ayat_bersih = [re.sub(r'^\d+\.\s*', '', a) for a in ayat_senarai]
            
            # Ekstrak 3-4 isi paling penting sebagai ringkasan profesional
            ringkasan_teks = " • " + "\n • ".join(ayat_bersih[:4]) if ayat_bersih else teks_laporan_asal[:200]

            # 3. Simpan ke Pangkalan Data
            id_rep = f"REP-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.pangkalan_data) + 1:03d}"
            
            data_baru = {
                "ID Laporan": id_rep,
                "Tarikh": tarikh_laporan.strftime("%Y-%m-%d"),
                "Kategori Utama": kategori_pilihan,
                "Daerah / IPD": daerah_dikesan,
                "Ringkasan Ringkas & Profesional": ringkasan_teks,
                "Teks Laporan Asal": teks_laporan_asal
            }
            
            st.session_state.pangkalan_data = pd.concat([st.session_state.pangkalan_data, pd.DataFrame([data_baru])], ignore_index=True)
            
            st.success(f"✅ Laporan bagi kategori **[{kategori_pilihan}]** berjaya diringkaskan dan disimpan!")
            
            # Paparan Hasil Ringkasan
            st.subheader("💡 Hasil Ringkasan Automatik Sistem:")
            st.info(ringkasan_teks)

# ==========================================
# MODUL 2: PAPAN PEMUKA & ANALISIS
# ==========================================
elif menu == "📊 Papan Pemuka & Analisis":
    st.header("📊 Papan Pemuka Laporan Harian")
    df = st.session_state.pangkalan_data
    
    if df.empty:
        st.info("Tiada rekod data. Sila masukkan laporan terlebih dahulu.")
    else:
        st.metric("Jumlah Kategori Berisi Laporan", len(df))
        st.subheader("Taburan Laporan Mengikut 5 Kategori")
        st.bar_chart(df["Kategori Utama"].value_counts())

# ==========================================
# MODUL 3: JANA LAPORAN PENUH KESELURUHAN
# ==========================================
elif menu == "📄 Jana Laporan Penuh Keseluruhan":
    st.header("📄 Draf Laporan Penuh Kontinjen Selangor")
    df = st.session_state.pangkalan_data
    
    if df.empty:
        st.info("Pangkalan data kosong. Masukkan laporan terlebih dahulu.")
    else:
        st.caption("Berikut adalah gabungan semua laporan mengikut 5 kategori yang telah anda masukkan:")
        
        # Paparan Format Dokumen Rasmi
        st.markdown(f"### **ANALISIS HARIAN KONTINJEN SELANGOR ({datetime.now().strftime('%d %b %Y').upper()})**")
        st.markdown("---")
        
        for kat in SENARAI_KATEGORI:
            df_kat = df[df["Kategori Utama"] == kat]
            st.markdown(f"#### **{kat.upper()}**")
            
            if df_kat.empty:
                st.write("*Tiada sebarang laporan bagi kategori ini.*")
            else:
                for idx, row in df_kat.iterrows():
                    st.markdown(f"**[{row['Daerah / IPD']}]**")
                    st.write(row["Ringkasan Ringkas & Profesional"])
                    with st.expander("Lihat Teks Asal Penuh"):
                        st.write(row["Teks Laporan Asal"])
            st.markdown("---")

        # Butang Eksport
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Muat Turun Pangkalan Data (CSV)", csv, "Pangkalan_Data_Laporan.csv", "text/csv")
