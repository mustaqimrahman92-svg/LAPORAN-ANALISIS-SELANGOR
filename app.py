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

# Inisialisasi Pangkalan Data
if "pangkalan_data" not in st.session_state:
    st.session_state.pangkalan_data = pd.DataFrame(columns=[
        "ID Laporan", "Tarikh", "Kategori Utama", "Daerah / IPD", 
        "No. Repot / Program", "Ringkasan Laporan", "Ulasan / Implikasi"
    ])

st.title("🛡️ Sistem Pemprosesan Laporan Harian Kontinjen Selangor")
st.caption("Fungsi Automasi: Tampal Teks Laporan Penuh & Ekstrak Automatik")
st.markdown("---")

menu = st.sidebar.radio("PILIH MODUL:", ["📥 Tampal Laporan Penuh", "📊 Papan Pemuka & Analisis", "🔍 Carian & Eksport Data"])

# ==========================================
# MODUL 1: TAMPAL LAPORAN PENUH (BULK INPUT)
# ==========================================
if menu == "📥 Tampal Laporan Penuh":
    st.header("Tampal Teks Laporan Naratif")
    st.caption("Tampal keseluruhan dokumen laporan harian di bawah. Sistem akan memproses dan menyusun mengikut kategori secara automatik.")

    # Ruang Teks Besar untuk Paste Dokumen Penuh
    teks_laporan_penuh = st.text_area(
        "Tampal Dokumen Laporan Di Sini:", 
        height=350,
        placeholder="Contoh:\nANALISIS HARIAN KONTINJEN SELANGOR 2 SEPT 2026...\n\nANCAMAN EKSTREMIS SOSIAL...\n2. Majlis Perasmian Persidangan..."
    )

    if st.button("⚡ Proses & Susun Laporan Automatik"):
        if teks_laporan_penuh.strip() == "":
            st.warning("Sila tampal teks laporan terlebih dahulu!")
        else:
            # LOGIK EKSTRAK TEKS (Parsing Text)
            senarai_perenggan = teks_laporan_penuh.split("\n\n")
            kategori_semasa = "Ancaman Ekstremis Sosial" # Default
            rekod_baharu = []

            # Senarai 5 Kategori Rasmi
            kategori_list = [
                "ANCAMAN EKSTREMIS SOSIAL",
                "ANCAMAN EKSTREMIS LUAR",
                "ANCAMAN EKSTREMIS POLITIK",
                "ANCAMAN EKSTREMIS EKONOMI",
                "KESELAMATAN DAN PERLINDUNGAN",
                "ULASAN"
            ]

            # Senarai Daerah Selangor
            daerah_list = ["Shah Alam", "Gombak", "Kajang", "Hulu Langat", "Hulu Selangor", 
                           "Subang Jaya", "Petaling Jaya", "Klang Utara", "Klang Selatan", 
                           "Sungai Buloh", "Kuala Langat", "Sepang", "Sabak Bernam"]

            for blok in senarai_perenggan:
                blok_clean = blok.strip()
                
                # Kesan Tajuk Kategori Dalam Teks
                is_header = False
                for kat in kategori_list:
                    if kat in blok_clean.upper():
                        kategori_semasa = kat.title()
                        is_header = True
                        break
                
                if is_header or len(blok_clean) < 15:
                    continue

                # Kesan Daerah Automatik
                daerah_dikesan = "Selangor (Keseluruhan)"
                for d in daerah_list:
                    if d.lower() in blok_clean.lower():
                        daerah_dikesan = d
                        break

                # Ekstrak No Repot / Program jika ada
                match_repot = re.search(r'([A-Z\s]+Rpt\.\s*\d+/\d+)', blok_clean, re.IGNORECASE)
                no_repot = match_repot.group(1) if match_repot else "Laporan / Program Harian"

                # Penjanaan Rekod Data
                id_rep = f"REP-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.pangkalan_data) + len(rekod_baharu) + 1:03d}"
                
                rekod_baharu.append({
                    "ID Laporan": id_rep,
                    "Tarikh": datetime.now().strftime("%Y-%m-%d"),
                    "Kategori Utama": kategori_semasa if kategori_semasa != "Ulasan" else "Keselamatan Dan Perlindungan",
                    "Daerah / IPD": daerah_dikesan,
                    "No. Repot / Program": no_repot,
                    "Ringkasan Laporan": blok_clean,
                    "Ulasan / Implikasi": "Diproses secara automatik daripada teks penuh."
                })

            if rekod_baharu:
                new_df = pd.DataFrame(rekod_baharu)
                st.session_state.pangkalan_data = pd.concat([st.session_state.pangkalan_data, new_df], ignore_index=True)
                st.success(f"🎉 Berjaya! {len(rekod_baharu)} perenggan laporan telah diasingkan dan dimasukkan ke dalam Pangkalan Data mengikut 5 Kategori!")
                st.dataframe(new_df, use_container_width=True)

# ==========================================
# MODUL 2 & 3 (PAPAN PEMUKA & CARIAN)
# ==========================================
elif menu == "📊 Papan Pemuka & Analisis":
    st.header("📊 Papan Pemuka Analisis")
    df = st.session_state.pangkalan_data
    if df.empty:
        st.info("Tiada data. Sila tampal laporan penuh dahulu.")
    else:
        st.metric("Jumlah Rekod Ekstrak", len(df))
        st.bar_chart(df["Kategori Utama"].value_counts())
        st.bar_chart(df["Daerah / IPD"].value_counts())

elif menu == "🔍 Carian & Eksport Data":
    st.header("🔍 Pangkalan Data & Carian")
    df = st.session_state.pangkalan_data
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Muat Turun Data (CSV)", csv, "Laporan_Selangor.csv", "text/csv")
