import streamlit as st
import json
import pandas as pd
from datetime import datetime
import pytz
from pathlib import Path

# Konfigurasi file penyimpanan
DATA_FILE = "kunjungan_data.json"

def ensure_data_file():
    if not Path(DATA_FILE).exists():
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)

def load_data():
    ensure_data_file()
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

if 'visitor_data' not in st.session_state:
    st.session_state.visitor_data = load_data()

if "page" not in st.session_state:
    st.session_state.page = "login"

def switch_page(page_name):
    st.session_state.page = page_name

# Halaman Login
if st.session_state.page == "login":
    st.title("Harap login terlebih dahulu untuk masuk")

    uname = st.text_input("Username")
    pw = st.text_input("Password")
    
    if st.button("Login"):
        if nama == "bpsjakartakota" and pw == "bps3175":
            st.success(switch_page("home"))
        elif:
            st.error("Harap isi data dengan benar")

# Halaman Utama
elif st.session_state.page == "home":
    st.title("📝 Form Review Kunjungan BPS")
    
    with st.form("kunjungan_form", clear_on_submit=True):
        st.subheader("Data Pengunjung")
        nama = st.text_input("Nama Lengkap")
        instansi = st.text_input("Asal Instansi/Perusahaan")
        tujuan = st.text_area("Tujuan Kunjungan")
        rating = st.radio(
            "Rating Kepuasan", 
            ["⭐ Sangat Puas", "👍 Puas", "👎 Kurang Puas"],
            index=None
        )
        
        if st.form_submit_button("Simpan Data"):
            if all([nama, instansi, tujuan, rating]):
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

# Halaman Data
elif st.session_state.page == "data":
    st.title("📊 Data Kunjungan Tersimpan")
    
    if not st.session_state.visitor_data:
        st.warning("Belum ada data yang tersimpan")
    else:
        # Tampilkan data dengan kolom lebih rapi
        for item in reversed(st.session_state.visitor_data):
            with st.expander(f"{item['nama']} ({item['instansi']}) - {item['waktu']}"):
                st.markdown(f"**ID:** #{item['id']}")
                st.markdown(f"**Tujuan:** {item['tujuan']}")
                st.markdown(f"**Rating:** {item['rating']}")

        # Section Ekspor Data
        st.divider()
        st.subheader("Manajemen Data")
        
        # Dalam satu baris horizontal
        col1, col2 = st.columns(2)
        
        with col1:
            # Export Button
            csv = pd.DataFrame(st.session_state.visitor_data).to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Ekspor ke CSV",
                data=csv,
                file_name='data_kunjungan.csv',
                mime='text/csv',
                help="Unduh semua data dalam format CSV",
                use_container_width=True
            )
        
        with col2:
            # Delete Button
            if st.button("🗑️ Hapus Semua Data", 
                       use_container_width=True,
                       type="primary",
                       help="Hapus permanen semua data"):
                if st.session_state.visitor_data:
                    st.session_state.visitor_data = []
                    save_data([])
                    st.success("Semua data berhasil dihapus!")
                    st.rerun()
                else:
                    st.warning("Tidak ada data untuk dihapus")
    
    # Kembali ke form
    if st.button("← Kembali ke Form Utama"):
        switch_page("home")
