import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime

# Database connection configuration
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="hoteldb"
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None

# Function to execute a query and return a DataFrame
def run_query(query):
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except mysql.connector.Error as err:
            st.error(f"Error executing query: {err}")
            return None
    return None

# Streamlit app
st.title("Hotel Management Dashboard")
st.write("Explore reservations, clients, rooms, and more from the hotel database.")

# Sidebar for navigation
st.sidebar.header("Navigation")
section = st.sidebar.selectbox(
    "Select a section",
    [
        "Reservations with Client and Hotel",
        "Clients in Paris",
        "Number of Reservations per Client",
        "Number of Rooms per Type",
        "Available Rooms for a Date Range"
    ]
)

# Section 1: Reservations with Client and Hotel
if section == "Reservations with Client and Hotel":
    st.header("Reservations with Client and Hotel City")
    query = """
    SELECT r.id_reservation, c.nom_complet AS client, h.ville AS ville_hotel
    FROM Reservation r
    JOIN Client c ON r.id_client = c.id_client
    JOIN Reservation_Chambre rc ON r.id_reservation = rc.id_reservation
    JOIN Chambre ch ON rc.id_chambre = ch.id_chambre
    JOIN Hotel h ON ch.id_hotel = h.id_hotel;
    """
    df = run_query(query)
    if df is not None:
        st.dataframe(df)
        # Bar chart for reservations by hotel city
        fig = px.bar(df, x="ville_hotel", title="Reservations by Hotel City", color="ville_hotel",
                     color_discrete_map={"Paris": "#1f77b4", "Lyon": "#ff7f0e"})
        st.plotly_chart(fig)

# Section 2: Clients in Paris
elif section == "Clients in Paris":
    st.header("Clients Residing in Paris")
    query = """
    SELECT *
    FROM Client
    WHERE ville = 'Paris';
    """
    df = run_query(query)
    if df is not None:
        st.dataframe(df)
        st.write(f"Total clients in Paris: {len(df)}")
        # Pie chart for visual representation
        fig = px.pie(df, names="nom_complet", title="Clients in Paris")
        st.plotly_chart(fig)

# Section 3: Number of Reservations per Client
elif section == "Number of Reservations per Client":
    st.header("Number of Reservations per Client")
    query = """
    SELECT c.id_client, c.nom_complet, COUNT(r.id_reservation) AS nb_res
    FROM Client c
    LEFT JOIN Reservation r ON c.id_client = r.id_client
    GROUP BY c.id_client, c.nom_complet;
    """
    df = run_query(query)
    if df is not None:
        st.dataframe(df)
        # Bar chart for reservations per client
        fig = px.bar(df, x="nom_complet", y="nb_res", title="Reservations per Client",
                     color="nom_complet", color_discrete_sequence=px.colors.qualitative.Plotly)
        st.plotly_chart(fig)

# Section 4: Number of Rooms per Type
elif section == "Number of Rooms per Type":
    st.header("Number of Rooms per Type")
    query = """
    SELECT t.id_type, t.libelle, COUNT(ch.id_chambre) AS nb_chambres
    FROM TypeChambre t
    LEFT JOIN Chambre ch ON t.id_type = ch.id_type
    GROUP BY t.id_type, t.libelle;
    """
    df = run_query(query)
    if df is not None:
        st.dataframe(df)
        # Pie chart for room types
        fig = px.pie(df, names="libelle", values="nb_chambres", title="Room Distribution by Type",
                     color_discrete_sequence=["#1f77b4", "#ff7f0e"])
        st.plotly_chart(fig)

# Section 5: Available Rooms for a Date Range
elif section == "Available Rooms for a Date Range":
    st.header("Available Rooms for a Date Range")
    # Date input for range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2025, 7, 2))
    with col2:
        end_date = st.date_input("End Date", value=datetime(2025, 7, 3))
    
    if start_date <= end_date:
        query = f"""
        SELECT ch.*
        FROM Chambre ch
        LEFT JOIN Reservation_Chambre rc ON ch.id_chambre = rc.id_chambre
        LEFT JOIN Reservation r ON rc.id_reservation = r.id_reservation
            AND ('{start_date}' <= r.date_depart AND '{end_date}' >= r.date_arrivee)
        WHERE r.id_reservation IS NULL;
        """
        df = run_query(query)
        if df is not None:
            st.dataframe(df)
            # Bar chart for available rooms by hotel
            if not df.empty:
                df_hotel = df.merge(run_query("SELECT id_hotel, ville FROM Hotel"), on="id_hotel")
                fig = px.bar(df_hotel, x="ville", title="Available Rooms by Hotel",
                             color="ville", color_discrete_map={"Paris": "#1f77b4", "Lyon": "#ff7f0e"})
                st.plotly_chart(fig)
            else:
                st.write("No rooms available for the selected date range.")
    else:
        st.error("End date must be after start date.")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Built with Streamlit and MySQL")