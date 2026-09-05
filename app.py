import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Tetapan Asas Halaman Aplikasi
st.set_page_config(
    page_title="Sistem Laporan Harian Kontinjen Selangor",
    page_icon="👮‍♂️",
    layout="wide"
)

# 2. Inisialisasi Pangkalan Data Sementara (Session State)
if "pangkalan_data" not in st.session_state:
    st.session_state.pangkalan_data = pd.DataFrame(columns=[
        "ID Laporan", "Tarikh", "Jenis Laporan", "Kategori Utama", 
        "Daerah / IPD", "Lokasi / Premis", "Entiti / VIP Terlibat", 
        "No. Repot / Program", "Klasifikasi / Status", "Ringkasan Laporan", "Ulasan / Implikasi"
    ])

# Tajuk Utama Aplikasi
st.title("🛡️ Sistem Analisis & Laporan Harian Kontinjen Selangor")
st.caption("Aplikasi Pengurusan Laporan Operasi & Ketenteraman Awam")
st.markdown("---")

# Navigation Menu
menu = st.sidebar.radio("PILIH MODUL:", ["📝 Input Laporan", "📊 Papan Pemuka & Analisis", "🔍 Carian & Eksport Data"])

# ==========================================
# MODUL 1: INPUT LAPORAN
# ==========================================
if menu == "📝 Input Laporan":
    st.header("Borang Input Laporan Harian")
    st.caption("Masukkan maklumat laporan berstruktur mengikut pecahan kategori rasmi.")

    with st.form("borang_laporan_utama", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            tarikh = st.date_input("Tarikh Laporan", datetime.now())
            jenis_laporan = st.selectbox(
                "Jenis Laporan", 
                ["Laporan Aktiviti / Program", "Laporan Polis", "Ulasan & Implikasi Keselamatan"]
            )
            
        with col2:
            # 5 Kategori Utama Rasmi
            kategori_utama = st.selectbox(
                "Kategori Utama", 
                [
                    "Ancaman Ekstremis Sosial",
                    "Ancaman Ekstremis Luar",
                    "Ancaman Ekstremis Politik",
                    "Ancaman Ekstremis Ekonomi",
                    "Keselamatan Dan Perlindungan"
                ]
            )
            daerah = st.selectbox(
                "Daerah / IPD Terlibat",
                [
                    "Shah Alam", "Gombak", "Kajang", "Hulu Langat", "Hulu Selangor",
                    "Subang Jaya", "Petaling Jaya", "Klang Utara", "Klang Selatan", 
                    "Sungai Buloh", "Kuala Langat", "Sepang", "Sabak Bernam", "Selangor (Keseluruhan)"
                ]
            )

        st.markdown("---")

        # LOGIK PERCABANGAN INPUT (BRANCHING LOGIC)
        if jenis_laporan == "Laporan Aktiviti / Program":
            st.subheader("📌 Butiran Aktiviti / Program")
            col_a, col_b = st.columns(2)
            with col_a:
                nama_program = st.text_input("Nama Program / Majlis", placeholder="Contoh: CRC 2026 / Program Jelajah Merdeka Sihat")
                penganjur_vip = st.text_input("Penganjur Utama / Tokoh VIP Hadir", placeholder="Contoh: CSAM, IPSOM / Dr. Sathia Prakash")
            with col_b:
                lokasi_spesifik = st.text_input("Lokasi / Premis", placeholder="Contoh: Balairaya JPKK Kg Gesir Tengah")
                kehadiran = st.number_input("Anggaran Kehadiran (Orang)", min_value=0, value=50)
            
            no_repot_program = nama_program
            status_klasifikasi = f"Program Rasmi (Kehadiran: ~{kehadiran})"

        elif jenis_laporan == "Laporan Polis":
            st.subheader("🚨 Butiran Laporan Polis")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                balai_lokasi = st.text_input("Balai / Lokasi Kejadian", placeholder="Contoh: Kuang / Kg. Baru Subang / Kajang")
                no_repot_program = st.text_input("Nombor Repot Polis", placeholder="Contoh: KUANG Rpt. 4555/2026")
            with col_p2:
                status_klasifikasi = st.selectbox("Klasifikasi Kes", ["Dalam Siasatan", "ROA", "NFA", "Belum Diklasifikasi"])
                penganjur_vip = st.text_input("Pihak / Suspek / Pengadu Terlibat", placeholder="Contoh: Pengadu (Lelaki India) / Suspek ('Kecik')")
            
            lokasi_spesifik = balai_lokasi

        else: # Ulasan & Implikasi Keselamatan
            st.subheader("📋 Rumusan Ulasan Operasi")
            no_repot_program = "Rumusan Ulasan / Penilaian Risiko"
            penganjur_vip = "Cawangan Khas / PDRM Kontinjen Selangor"
            lokasi_spesifik = "Kontinjen Selangor"
            status_klasifikasi = "Pemantauan Berterusan"

        st.markdown("---")
        st.subheader("📄 Naratif & Implikasi Laporan")
        ringkasan = st.text_area(
            "Ringkasan Laporan / Kronologi Kes", 
            placeholder="Masukkan fakta ringkas kejadian, latar belakang, atau intipati ucapan secara profesional...",
            height=150
        )
        ulasan = st.text_area(
            "Ulasan & Implikasi Keselamatan / Langkah Pencegahan", 
            placeholder="Masukkan penilaian risiko ketenteraman awam, persepsi masyarakat, atau elemen persaingan politik/sosial...",
            height=100
        )

        submit_button = st.form_submit_button("Simpan Laporan 🚀")

    if submit_button:
        # Penjanaan ID Laporan Automatik
        id_laporan = f"REP-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.pangkalan_data) + 1:03d}"
        
        # Susun Data Baharu
        data_baharu = {
            "ID Laporan": id_laporan,
            "Tarikh": tarikh.strftime("%Y-%m-%d"),
            "Jenis Laporan": jenis_laporan,
            "Kategori Utama": kategori_utama,
            "Daerah / IPD": daerah,
            "Lokasi / Premis": lokasi_spesifik,
            "Entiti / VIP Terlibat": penganjur_vip,
            "No. Repot / Program": no_repot_program,
            "Klasifikasi / Status": status_klasifikasi,
            "Ringkasan Laporan": ringkasan,
            "Ulasan / Implikasi": ulasan
        }
        
        # Tambah ke DataFrame
        st.session_state.pangkalan_data = pd.concat(
            [st.session_state.pangkalan_data, pd.DataFrame([data_baharu])], 
            ignore_index=True
        )
        st.success(f"✅ Laporan [{id_laporan}] berjaya disimpan ke dalam pangkalan data!")

# ==========================================
# MODUL 2: PAPAN PEMUKA & ANALISIS
# ==========================================
elif menu == "📊 Papan Pemuka & Analisis":
    st.header("Papan Pemuka Analisis Harian")
    
    df = st.session_state.pangkalan_data

    if df.empty:
        st.info("Tiada rekod data buat masa ini. Sila masukkan laporan di modul 'Input Laporan'.")
    else:
        # Ringkasan Matrik KPI Utama
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Jumlah Keseluruhan Laporan", len(df))
        kpi2.metric("Laporan Polis", len(df[df["Jenis Laporan"] == "Laporan Polis"]))
        kpi3.metric("Aktiviti / Program", len(df[df["Jenis Laporan"] == "Laporan Aktiviti / Program"]))
        kpi4.metric("Ulasan Keselamatan", len(df[df["Jenis Laporan"] == "Ulasan & Implikasi Keselamatan"]))

        st.markdown("---")

        # Visualisasi Graf & Carta
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.subheader("Pecahan Mengikut 5 Kategori Utama")
            st.bar_chart(df["Kategori Utama"].value_counts())

        with col_c2:
            st.subheader("Taburan Laporan Mengikut Daerah / IPD")
            st.bar_chart(df["Daerah / IPD"].value_counts())

# ==========================================
# MODUL 3: CARIAN & EKSPORT DATA
# ==========================================
elif menu == "🔍 Carian & Eksport Data":
    st.header("Pangkalan Data & Carian Laporan")
    
    df = st.session_state.pangkalan_data

    if df.empty:
        st.info("Pangkalan data kosong. Masukkan laporan terlebih dahulu.")
    else:
        # Carian Kata Kunci Interaktif
        carian = st.text_input("🔍 Carian Kata Kunci (Contoh: Kuil, AI, PKR, Hulu Selangor, Deepfake):")
        
        if carian:
            filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(carian, case=False).any(), axis=1)]
            st.write(f"Menunjukkan {len(filtered_df)} rekod hasil carian untuk **'{carian}'**:")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

        st.markdown("---")
        
        # Butang Muat Turun Data CSV
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Muat Turun Pangkalan Data (Format CSV)",
            data=csv_data,
            file_name=f"Analisis_Laporan_Selangor_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv'
        )
