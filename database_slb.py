import streamlit as st
import pandas as pd
import psycopg2
from PIL import Image
import base64

# Function to convert image to base64
def get_base64_image(image_file):
    with open(image_file, "rb") as image:
        return base64.b64encode(image.read()).decode()

# Set the path to your background image
background_image_path = "Bckg_SLB.jpg"  # Replace with your image file name

# CSS to set the background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/jpeg;base64,{get_base64_image(background_image_path)});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Function to load data from PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        dbname="Gudang Data",
        user="postgres",
        password="tytydkuda",
        host="localhost",
        port=5432
    )

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default page

# Function to navigate to a different page
def switch_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# Show different pages based on session state
if st.session_state.page == "home":
    st.image(Image.open("Schlumberger.png"))
    st.title("MNS CIB")
    st.write("Welcome To MNS CIB Database")
    
    st.write("Apa Kebutuhan Anda Saat Ini?")
    if st.button("Cari Barang"):
        switch_page("data_barang")
    elif st.button("Tambahkan Barang Baru"):
        switch_page("tambah_data")
    elif st.button("Ambil"):
        switch_page("ambil")

elif st.session_state.page == "data_barang":
        # Function to load data from PostgreSQL
    def load_data():
        with get_db_connection() as connection:
            query = 'SELECT * FROM "tableName"'  # Adjust the query as needed
            df = pd.read_sql(query, connection)
        return df

    # Streamlit UI
    st.title("MNS CIB DATABASE")

    # Load data
    data = load_data()

    # Display data in a table
    st.dataframe(data)

    st.write("Apakah Anda Ingin Mengupdate Quantity Data?")
    if st.button("Update Quantity"):
        switch_page("update_qty")
    elif st.button("Back"):
        switch_page("home")

elif st.session_state.page == "update_qty":
# Function to fetch all part numbers from the database
    def fetch_part_numbers():
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT \"Part Number\" FROM \"tableName\"")
            part_numbers = cursor.fetchall()
        connection.close()
        return [part[0] for part in part_numbers]

# Function to update the quantity of a part
    def update_quantity(part_number, quantity_change):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE \"tableName\" SET \"Quantity\" = \"Quantity\" + %s WHERE \"Part Number\" = %s",
                (quantity_change, part_number)
            )
            connection.commit()
        connection.close()

# Streamlit UI
    st.title("Update Item Quantity")

# Fetch part numbers from the database
    part_numbers = fetch_part_numbers()

# Dropdown to select a part number
    selected_part_number = st.selectbox("Pilih Part Number", part_numbers)

# Input for quantity change
    quantity_change = st.number_input("Masukkan Quantity Baru (positif untuk menambahkan, negatif untuk mengurangi)", min_value=-100, max_value=100)

# Button to update the quantity
    if st.button("Perbarui quantity"):
        if quantity_change != 0:  # Ensure that the change is not zero
            update_quantity(selected_part_number, quantity_change)
            st.success(f"Quantity untuk part number {selected_part_number} di perbarui dengan {quantity_change}.")
        else:
            st.warning("Masukkan quantity baru dengan angka selain 0.")

    if st.button("Back"):
        switch_page("data_barang")
    elif st.button("Home"):
        switch_page("home")

elif st.session_state.page == "tambah_data":
    # Function to insert new data into PostgreSQL
    def insert_data(category, rack, located, part_number, description, quantity):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO "tableName" ("Category", "Rack", "Located", "Part Number", "Description", "Quantity")
                    VALUES (%s, %s, %s, %s, %s, %s);
                ''', (category, rack, located, part_number, description, quantity))
                connection.commit()

    # Streamlit UI
    st.title("Tambahkan Item Baru")

    # Input fields for new data
    category = st.text_input("Category")
    rack = st.text_input("Rack")
    located = st.text_input("Located")
    part_number = st.text_input("Part Number")
    description = st.text_input("Description")
    quantity = st.number_input("Quantity", min_value=0)

    # Button to submit the new data
    if st.button("Tambahkan Item"):
        if category and rack and located and part_number and description and quantity is not None:
            insert_data(category, rack, located, part_number, description, quantity)
            st.success("Item Berhasil Ditambahkan!")
        else:
            st.error("Harap Mengisi Seluruh Kolom Data!")

    if st.button("Home"):
        switch_page('home')

elif st.session_state.page == "ambil":
    st.title("Ambil Item")

    def fetch_part_numbers():
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT \"Part Number\" FROM \"tableName\"")
            part_numbers = cursor.fetchall()
        connection.close()
        return [part[0] for part in part_numbers]

    def ambil_data(nama, tanggal, keperluan, part_number, quantity):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO "riwayat_ambil" ("nama", "tanggal", "keperluan", "Part Number", "Quantity")
                    VALUES (%s, %s, %s, %s, %s);
                ''', (nama, tanggal, keperluan, part_number, quantity))
                connection.commit()

    def quantity_cng(part_number, quantity):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE \"tableName\" SET \"Quantity\" = \"Quantity\" + %s WHERE \"Part Number\" = %s",
                (quantity, part_number)
            )
            connection.commit()
        connection.close()

    nama = st.text_input("nama")
    tanggal = st.date_input("tanggal")
    keperluan = st.text_input("keperluan")
    part_numbers = fetch_part_numbers()
    part_number = st.selectbox("Pilih Part Number", part_numbers)
    quantity = st.number_input("Masukkan Quantity Baru (positif untuk menambahkan, negatif untuk mengurangi)", min_value=-100, max_value=0)

    if st.button("Ambil Item"):
        if nama and tanggal and keperluan and part_number and  quantity is not None:
            if quantity != 0:  # Ensure that the change is not zero
                quantity_cng(part_number, quantity)
                ambil_data(nama, tanggal, keperluan, part_number, quantity)
                st.success("Item Berhasil Ambil!")
            else:
                st.warning("Masukkan quantity baru dengan angka selain 0.")
        else:
            st.error("Harap Mengisi Seluruh Kolom Data!")

    if st.button("Home"): 
        switch_page("home")