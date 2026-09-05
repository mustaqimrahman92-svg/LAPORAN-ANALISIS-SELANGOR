import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.set_page_config(page_title="Sistem Laporan Harian Kontinjen Selangor", page_icon="👮‍♂️", layout="wide")

if "pangkalan_data" not in st.session_state:
    st.session_state.pangkalan_data = pd.DataFrame(columns=[
        "ID Laporan", "Tarikh", "Kategori Utama", "Daerah / IPD", 
        "Ringkasan Kemas & Profesional", "Teks Laporan Asal"
    ])

st.title("🛡️ Sistem Laporan Harian Kontinjen Selangor")
st.caption("Modul Pemprosesan Laporan Intel Percuma")
st.markdown("---")

menu = st.sidebar.radio("PILIH MODUL:", ["📝 Masukkan Laporan", "📊 Papan Pemuka & Analisis", "📄 Jana Laporan Penuh Keseluruhan"])

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

def proses_laporan_kemas(teks):
    # Bersihkan nombor perenggan di awal ayat
    teks_clean = re.sub(r'^\d+\.\s*', '', teks.strip())
    perenggan = [p.strip() for p in teks_clean.split('\n') if p.strip()]
    
    hasil_poin = []
    for item in perenggan:
        # Tapis frasa pengenalan yang menggantungkan ayat
        if re.search(r'dikenali hadir adalah seperti berikut\s*:-?$', item, re.IGNORECASE):
            continue
        if re.search(r'^\*?kehadiran\*?$', item, re.IGNORECASE):
            continue
        
        item_bersih = re.sub(r'^[•\-\*]\s*', '', item)
        hasil_poin.append(f"• {item_bersih}")
        
    return "\n\n".join(hasil_poin) if hasil_poin else f"• {teks_clean}"

if menu == "📝 Masukkan Laporan":
    col1, col2 = st.columns([1, 2])
    with col1:
        kategori_pilihan = st.selectbox("📌 Pilih Kategori Tajuk:", SENARAI_KATEGORI)
        tarikh_laporan = st.date_input("Tarikh Laporan", datetime.now())
    with col2:
        teks_laporan_asal = st.text_area("📥 Tampal Teks Laporan Penuh Di Sini:", height=280)

    st.markdown("---")
    if st.button("🚀 Process & Simpan Laporan", use_container_width=True):
        if not teks_laporan_asal.strip():
            st.warning("Sila tampal teks laporan terlebih dahulu!")
        else:
            daerah_dikesan = "Selangor (Keseluruhan)"
            for d in SENARAI_DAERAH:
                if d.lower() in teks_laporan_asal.lower():
                    daerah_dikesan = d.upper()
                    break

            ringkasan_kemas = proses_laporan_kemas(teks_laporan_asal)
            id_rep = f"REP-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.pangkalan_data) + 1:03d}"
            
            data_baru = {
                "ID Laporan": id_rep,
                "Tarikh": tarikh_laporan.strftime("%Y-%m-%d"),
                "Kategori Utama": kategori_pilihan,
                "Daerah / IPD": daerah_dikesan,
                "Ringkasan Kemas & Profesional": ringkasan_kemas,
                "Teks Laporan Asal": teks_laporan_asal
            }
            st.session_state.pangkalan_data = pd.concat([st.session_state.pangkalan_data, pd.DataFrame([data_baru])], ignore_index=True)
            st.success(f"✅ Laporan **[{kategori_pilihan}]** berjaya disimpan!")
            st.markdown(ringkasan_kemas)

elif menu == "📊 Papan Pemuka & Analisis":
    st.header("📊 Papan Pemuka Analisis")
    df = st.session_state.pangkalan_data
    if not df.empty:
        st.metric("Jumlah Rekod Laporan", len(df))
        st.bar_chart(df["Kategori Utama"].value_counts())

elif menu == "📄 Jana Laporan Penuh Keseluruhan":
    st.header("📄 Draf Laporan Analisis Kontinjen Selangor")
    df = st.session_state.pangkalan_data
    if not df.empty:
        st.markdown(f"## **ANALISIS HARIAN KONTINJEN SELANGOR ({datetime.now().strftime('%d %b %Y').upper()})**")
        st.markdown("---")
        for kat in SENARAI_KATEGORI:
            df_kat = df[df["Kategori Utama"] == kat]
            st.markdown(f"### **{kat.upper()}**")
            if not df_kat.empty:
                for idx, row in df_kat.iterrows():
                    st.markdown(f"**[{row['Daerah / IPD']}]**")
                    st.markdown(row["Ringkasan Kemas & Profesional"])
            st.markdown("---")
