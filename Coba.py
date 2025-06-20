import streamlit as st
import json
from datetime import datetime
import pytz
from pathlib import Path

# Konfigurasi file penyimpanan
DATA_FILE = "kunjungan_data.json"

# Fungsi untuk memastikan file ada
def ensure_data_file():
    if not Path(DATA_FILE).exists():
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

# Fungsi baca data
def load_data():
    ensure_data_file()
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

# Fungsi simpan data
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Inisialisasi data
if 'visitor_data' not in st.session_state:
    st.session_state.visitor_data = load_data()

# Navigasi halaman
if "page" not in st.session_state:
    st.session_state.page = "home"

def switch_page(page_name):
    st.session_state.page = page_name

# UI Halaman Utama
if st.session_state.page == "home":
    st.title("📝 Form Review Kunjungan BPS")
    
    with st.form("kunjungan_form", clear_on_submit=True):
        st.subheader("Data Pengunjung")
        nama = st.text_input("Nama Lengkap")
        instansi = st.text_input("Asal Instansi/Perusahaan")
        tujuan = st.text_area("Tujuan Kunjungan")
        rating = st.radio(
            "Rating Kepuasan", 
            ["😁 Sangat Puas", "🙂 Puas", "☹️ Kurang Puas"],
            horizontal=True,
            index=None
        )
        
        if st.form_submit_button("Simpan Data"):
            if all([nama, instansi, tujuan, rating]):
                # Mengatur zona waktu ke GMT+7
                timezone = pytz.timezone('Asia/Jakarta')
                current_time = datetime.now(timezone).strftime("%d/%m/%Y %H:%M")
                
                new_data = {
                    "id": len(st.session_state.visitor_data) + 1,
                    "nama": nama,
                    "instansi": instansi,
                    "tujuan": tujuan,
                    "rating": rating,
                    "waktu": current_time
                }
                
                st.session_state.visitor_data.append(new_data)
                save_data(st.session_state.visitor_data)
                
                st.success("Data berhasil disimpan!")
                st.balloons()
            else:
                st.error("Harap lengkapi semua field!")

    if st.button("Lihat Data Tersimpan"):
        switch_page("data")

# UI Halaman Data
elif st.session_state.page == "data":
    st.title("📊 Data Kunjungan Tersimpan")
    
    if not st.session_state.visitor_data:
        st.warning("Belum ada data yang tersimpan")
    else:
        # Tampilkan data dalam bentuk cards
        for item in reversed(st.session_state.visitor_data):
            with st.expander(f"{item['nama']} - {item['waktu']}"):
                cols = st.columns(2)
                with cols[0]:
                    st.markdown(f"**Instansi:** {item['instansi']}")
                    st.markdown(f"**Tujuan:** {item['tujuan']}")
                with cols[1]:
                    st.markdown(f"**Rating:** {item['rating']}")
                    st.markdown(f"**ID:** #{item['id']}")
    
    if st.button("Kembali ke Form"):
        switch_page("home")
