import streamlit as st
import pandas as pd

# Initialize an empty list to store visitor data
visitor_data = []

if "page" not in st.session_state:
    st.session_state.page = "home"  # Default page

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
            # Append the new visitor data to the list
            visitor_data.append({
                "nama_pengunjung": nama_pengunjung,
                "instansi": instansi,
                "tujuan": tujuan,
                "respon_pengunjung": respon_pengunjung,
                "tanggal_kunjungan": pd.to_datetime("today").date()  # Store the current date
            })
            st.success(f"Terima Kasih {nama_pengunjung}, Respon anda sudah kami terima 😊")
        else:
            st.error("Harap Mengisi Seluruh Kolom Dengan Benar!")
    
    if st.button("Liat Riwayat Kunjungan"):
        switch_page("data")

elif st.session_state.page == "data":
    # Convert the visitor data list to a DataFrame for display
    if visitor_data:
        data = pd.DataFrame(visitor_data)
        st.dataframe(data)
    else:
        st.write("Belum ada data kunjungan.")
    
    if st.button("Back"):
        switch_page("home")
