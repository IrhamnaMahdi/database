import streamlit as st
import json
import pandas as pd
from datetime import datetime
import pytz
from pathlib import Path

# Konfigurasi
DATA_FILE = "kunjungan_data.json"
LOGIN_INFO = {
    "username": "bpskotajakut",
    "password": "bps3175"
}

# Fungsi-fungsi data
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

# Inisialisasi session state
if 'visitor_data' not in st.session_state:
    st.session_state.visitor_data = load_data()

if "page" not in st.session_state:
    st.session_state.page = "login"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Fungsi navigasi
def switch_page(page_name):
    st.session_state.page = page_name

# Fungsi login
def authenticate(username, password):
    return username == LOGIN_INFO["username"] and password == LOGIN_INFO["password"]

# Halaman Login
if st.session_state.page == "login":
    st.title("🔐 Login Sistem Kunjungan BPS")
    st.divider()
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.page = "home"
            else:
                st.error("Username atau password salah")

# Halaman Utama (hanya bisa diakses setelah login)
if st.session_state.page == "home" and st.session_state.logged_in:
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

    # Tombol logout
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"

# Halaman Data
elif st.session_state.page == "data" and st.session_state.logged_in:
    st.title("📊 Data Kunjungan Tersimpan")
    
    if not st.session_state.visitor_data:
        st.warning("Belum ada data yang tersimpan")
    else:
        for item in reversed(st.session_state.visitor_data):
            with st.expander(f"{item['nama']} ({item['instansi']}) - {item['waktu']}"):
                st.markdown(f"**ID:** #{item['id']}")
                st.markdown(f"**Tujuan:** {item['tujuan']}")
                st.markdown(f"**Rating:** {item['rating']}")

        st.divider()
        st.subheader("Manajemen Data")
        
        col1, col2 = st.columns(2)
        with col1:
            csv = pd.DataFrame(st.session_state.visitor_data).to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Ekspor ke CSV",
                data=csv,
                file_name='data_kunjungan.csv',
                mime='text/csv',
                use_container_width=True
            )
        
        with col2:
            if st.button("🗑️ Hapus Semua Data", 
                       use_container_width=True,
                       type="primary"):
                if st.session_state.visitor_data:
                    st.session_state.visitor_data = []
                    save_data([])
                    st.success("Semua data berhasil dihapus!")
                else:
                    st.warning("Tidak ada data untuk dihapus")
    
    if st.button("← Kembali ke Form Utama"):
        switch_page("home")
    
    # Tombol logout
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"

# Redirect jika belum login
elif not st.session_state.logged_in:
    st.warning("Silakan login terlebih dahulu")
    switch_page("login")
