import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for visitor data
if 'visitor_data' not in st.session_state:
    st.session_state.visitor_data = []

if "page" not in st.session_state:
    st.session_state.page = "home"

def switch_page(page_name):
    st.session_state.page = page_name
    st.rerun()

st.title("Review Kunjungan BPS KOTA JAKARTA UTARA")

if st.session_state.page == "home":
    st.title("REVIEW KUNJUNGAN")
    nama_pengunjung = st.text_input("Nama Pengunjung")
    instansi = st.text_input("Instansi Asal")
    tujuan = st.text_input("Tujuan")
    respon_pengunjung = st.radio("Bagaimana Kunjungan Anda:", ("☹️ Tidak Puas", "🙂 Puas", "😁 Sangat Puas"), horizontal=True)

    if st.button("Kirim"):
        if nama_pengunjung and instansi and tujuan and respon_pengunjung is not None:
            # Add new data to session state
            st.session_state.visitor_data.append({
                "id": len(st.session_state.visitor_data) + 1,
                "nama_pengunjung": nama_pengunjung,
                "instansi": instansi,
                "tujuan": tujuan,
                "respon_pengunjung": respon_pengunjung,
                "tanggal_kunjungan": datetime.now().strftime("%Y-%m-%d")
            })
            st.success(f"Terima Kasih {nama_pengunjung}, Respon anda sudah kami terima 😊")
        else:
            st.error("Harap Mengisi Seluruh Kolom Dengan Benar!")
    
    if st.button("Liat Riwayat Kunjungan"):
        switch_page("data")

elif st.session_state.page == "data":
    if st.session_state.visitor_data:
        # Convert to DataFrame and display
        df = pd.DataFrame(st.session_state.visitor_data)
        df = df.set_index('id')  # Set ID as index
        st.dataframe(df)
    else:
        st.warning("Belum ada data kunjungan.")
    
    if st.button("Kembali ke Form"):
        switch_page("home")
