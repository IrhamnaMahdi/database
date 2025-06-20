import streamlit as st
import pandas as pd
import psycopg2

DB_HOST = "db.ogrudbnzguoqionhfbqe.supabase.co"
DB_PORT = 5432
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "tytydkuda134"

# Function to load data from PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=st.secrets["DB_HOST"],
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"],
        port=int(st.secrets["DB_PORT"])
    )

if "page" not in st.session_state:
    st.session_state.page = "home"  # Default page

def switch_page(page_name):
    st.session_state.page = page_name
    st.rerun()

st.title("Review Kunjungan BPS KOTA JAKARTA UTARA")

if st.session_state.page == "home":
    def insert_data(nama_pengunjung, instansi, tujuan, respon_pengunjung):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO "kunjungan" ("nama_pengunjung", "instansi", "tujuan", "respon_pengunjung")
                    VALUES (%s, %s, %s, %s);
                ''', (nama_pengunjung, instansi, tujuan, respon_pengunjung))
                connection.commit()
    
    st.title("REVIEW KUNJUNGAN")
    nama_pengunjung = st.text_input("Nama Pengunjung")
    instansi = st.text_input("Instansi Asal")
    tujuan = st.text_input("Tujuan")
    respon_pengunjung = st.radio("Bagaimana Kunjungan Anda:", ("☹️ Tidak Puas", "🙂 Puas", "😁 Sangat Puas"), horizontal=True)

    if st.button("Kirim"):
        if nama_pengunjung and instansi and tujuan and respon_pengunjung is not None:
            insert_data(nama_pengunjung, instansi, tujuan, respon_pengunjung)
            st.success(f"Terima Kasih {nama_pengunjung}, Respon anda sudah kami terima 😊")
        else:
            st.error("Harap Mengisi Seluruh Kolom Dengan Benar!")
    if st.button("Liat Riwayat Kunjungan"):
        switch_page("data")

elif st.session_state.page == "data":
    def load_data():
        with get_db_connection() as connection:
            query = 'SELECT * FROM "kunjungan"'  # Adjust the query as needed
            df = pd.read_sql(query, connection)
        return df

    data = load_data()
    st.dataframe(data)
    if st.button("Back"):
        switch_page("home")

