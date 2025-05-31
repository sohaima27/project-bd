import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('hotel.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create database and tables
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
        -- Suppression des tables si elles existent déjà
        DROP TABLE IF EXISTS Hotel_Prestation;
        DROP TABLE IF EXISTS Reservation_Chambre;
        DROP TABLE IF EXISTS Evaluation;
        DROP TABLE IF EXISTS Prestation;
        DROP TABLE IF EXISTS Reservation;
        DROP TABLE IF EXISTS Chambre;
        DROP TABLE IF EXISTS TypeChambre;
        DROP TABLE IF EXISTS Client;
        DROP TABLE IF EXISTS Hotel;

        -- Création des tables
        CREATE TABLE Hotel (
            id_hotel INTEGER PRIMARY KEY AUTOINCREMENT,
            ville TEXT,
            pays TEXT,
            code_postal TEXT
        );

        CREATE TABLE TypeChambre (
            id_type INTEGER PRIMARY KEY AUTOINCREMENT,
            libelle TEXT,
            tarif REAL
        );

        CREATE TABLE Chambre (
            id_chambre INTEGER PRIMARY KEY AUTOINCREMENT,
            etage INTEGER,
            fumeurs BOOLEAN,
            id_hotel INTEGER,
            id_type INTEGER,
            FOREIGN KEY(id_hotel) REFERENCES Hotel(id_hotel),
            FOREIGN KEY(id_type) REFERENCES TypeChambre(id_type)
        );

        CREATE TABLE Client (
            id_client INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_complet TEXT,
            adresse TEXT,
            ville TEXT,
            code_postal TEXT,
            email TEXT,
            tel TEXT
        );

        CREATE TABLE Reservation (
            id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
            date_arrivee TEXT,
            date_depart TEXT,
            id_client INTEGER,
            FOREIGN KEY(id_client) REFERENCES Client(id_client)
        );

        CREATE TABLE Prestation (
            id_prestation INTEGER PRIMARY KEY AUTOINCREMENT,
            libelle TEXT,
            prix REAL
        );

        CREATE TABLE Evaluation (
            id_evaluation INTEGER PRIMARY KEY AUTOINCREMENT,
            date_eval TEXT,
            note INTEGER,
            commentaire TEXT,
            id_reservation INTEGER,
            FOREIGN KEY(id_reservation) REFERENCES Reservation(id_reservation)
        );

        CREATE TABLE Reservation_Chambre (
            id_reservation INTEGER,
            id_chambre INTEGER,
            PRIMARY KEY(id_reservation, id_chambre),
            FOREIGN KEY(id_reservation) REFERENCES Reservation(id_reservation),
            FOREIGN KEY(id_chambre) REFERENCES Chambre(id_chambre)
        );

        CREATE TABLE Hotel_Prestation (
            id_hotel INTEGER,
            id_prestation INTEGER,
            PRIMARY KEY(id_hotel, id_prestation),
            FOREIGN KEY(id_hotel) REFERENCES Hotel(id_hotel),
            FOREIGN KEY(id_prestation) REFERENCES Prestation(id_prestation)
        );

        -- Données pour Hotel
        INSERT INTO Hotel (id_hotel, ville, pays, code_postal) VALUES
        (1, 'Paris', 'France', '75001'),
        (2, 'Lyon', 'France', '69002');

        -- Données pour Client
        INSERT INTO Client (id_client, nom_complet, adresse, ville, code_postal, email, tel) VALUES
        (1, 'Jean Dupont', '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678'),
        (2, 'Marie Leroy', '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789'),
        (3, 'Paul Moreau', '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890'),
        (4, 'Lucie Martin', '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901'),
        (5, 'Emma Giraud', '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012');

        -- Données pour Prestation
        INSERT INTO Prestation (id_prestation, libelle, prix) VALUES
        (1, 'Petit-déjeuner', 15),
        (2, 'Navette aéroport', 30),
        (3, 'Wi-Fi gratuit', 0),
        (4, 'Spa et bien-être', 50),
        (5, 'Parking sécurisé', 20);

        -- Données pour TypeChambre
        INSERT INTO TypeChambre (id_type, libelle, tarif) VALUES
        (1, 'Simple', 80),
        (2, 'Double', 120);

        -- Données pour Chambre
        INSERT INTO Chambre (id_chambre, etage, fumeurs, id_hotel, id_type) VALUES
        (1, 2, 0, 1, 1),
        (2, 5, 1, 1, 2),
        (3, 3, 0, 2, 1),
        (4, 4, 0, 2, 2),
        (5, 1, 1, 2, 2),
        (6, 2, 0, 1, 1),
        (7, 3, 1, 1, 2),
        (8, 1, 0, 1, 1);

        -- Données pour Reservation
        INSERT INTO Reservation (id_reservation, date_arrivee, date_depart, id_client) VALUES
        (1, '2025-06-15', '2025-06-18', 1),
        (2, '2025-07-01', '2025-07-05', 2),
        (3, '2025-08-10', '2025-08-14', 3),
        (4, '2025-09-05', '2025-09-07', 4),
        (5, '2025-09-20', '2025-09-25', 5),
        (7, '2025-11-12', '2025-11-14', 2),
        (9, '2026-01-15', '2026-01-18', 4),
        (10, '2026-02-01', '2026-02-05', 2);

        -- Données pour Evaluation
        INSERT INTO Evaluation (id_evaluation, date_eval, note, commentaire, id_reservation) VALUES
        (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
        (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
        (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
        (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
        (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5);
    ''')
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Streamlit app
st.title("Hotel Management System")

# Sidebar navigation
menu = ["Liste des Réservations", "Liste des Clients", "Chambres Disponibles", "Ajouter un Client", "Ajouter une Réservation"]
choice = st.sidebar.selectbox("Menu", menu)

# 1. Liste des réservations
if choice == "Liste des Réservations":
    st.subheader("Liste des Réservations")
    conn = get_db_connection()
    query = '''
        SELECT r.id_reservation, r.date_arrivee, r.date_depart, c.nom_complet
        FROM Reservation r
        JOIN Client c ON r.id_client = c.id_client
    '''
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    conn.close()

# 2. Liste des clients
elif choice == "Liste des Clients":
    st.subheader("Liste des Clients")
    conn = get_db_connection()
    query = 'SELECT id_client, nom_complet, adresse, ville, code_postal, email, tel FROM Client'
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)
    conn.close()

# 3. Chambres disponibles
elif choice == "Chambres Disponibles":
    st.subheader("Chambres Disponibles")
    date_arrivee = st.date_input("Date d'arrivée")
    date_depart = st.date_input("Date de départ")
    
    if date_arrivee and date_depart:
        conn = get_db_connection()
        query = '''
            SELECT c.id_chambre, c.etage, c.fumeurs, h.ville, t.libelle, t.tarif
            FROM Chambre c
            JOIN Hotel h ON c.id_hotel = h.id_hotel
            JOIN TypeChambre t ON c.id_type = t.id_type
            WHERE c.id_chambre NOT IN (
                SELECT rc.id_chambre
                FROM Reservation_Chambre rc
                JOIN Reservation r ON rc.id_reservation = r.id_reservation
                WHERE (r.date_arrivee <= ? AND r.date_depart >= ?)
            )
        '''
        df = pd.read_sql_query(query, conn, params=(str(date_depart), str(date_arrivee)))
        st.dataframe(df)
        conn.close()

# 4. Ajouter un client
elif choice == "Ajouter un Client":
    st.subheader("Ajouter un Client")
    with st.form("client_form"):
        nom_complet = st.text_input("Nom Complet")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.text_input("Code Postal")
        email = st.text_input("Email")
        tel = st.text_input("Téléphone")
        submit = st.form_submit_button("Ajouter")
        
        if submit:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Client (nom_complet, adresse, ville, code_postal, email, tel)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nom_complet, adresse, ville, code_postal, email, tel))
            conn.commit()
            conn.close()
            st.success("Client ajouté avec succès!")

# 5. Ajouter une réservation
elif choice == "Ajouter une Réservation":
    st.subheader("Ajouter une Réservation")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get clients and rooms for selection
    clients = pd.read_sql_query("SELECT id_client, nom_complet FROM Client", conn)
    chambres = pd.read_sql_query("SELECT id_chambre, etage, fumeurs FROM Chambre", conn)
    
    with st.form("reservation_form"):
        client = st.selectbox("Client", clients['nom_complet'])
        date_arrivee = st.date_input("Date d'arrivée")
        date_depart = st.date_input("Date de départ")
        chambre = st.selectbox("Chambre", chambres['id_chambre'])
        submit = st.form_submit_button("Ajouter")
        
        if submit:
            client_id = clients[clients['nom_complet'] == client]['id_client'].iloc[0]
            cursor.execute('''
                INSERT INTO Reservation (date_arrivee, date_depart, id_client)
                VALUES (?, ?, ?)
            ''', (str(date_arrivee), str(date_depart), client_id))
            reservation_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO Reservation_Chambre (id_reservation, id_chambre)
                VALUES (?, ?)
            ''', (reservation_id, chambre))
            conn.commit()
            st.success("Réservation ajoutée avec succès!")
    
    conn.close()
