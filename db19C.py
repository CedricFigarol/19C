import sqlite3
from sqlite3 import Error


class DataBaseManager:
    def __init__(self):
        self.config_file = 'config_db_path.txt'
        self.filieres = []
        self.sites = []
        self.classements = []
        self.contrats = []
        self.titulaires = []
        self.services = []
        self.types = []
        self.auteurs = []
        self.references_19C = []
        self.presentation_19C = []
        self.con = self.create_connection()
        self.build_tables(self.con)
        self.close_connection()
        self.config_file_error = False
        self.db_file_error = False
        self.db_file_error_message = ''

    def get_database_path(self):
        try:
            with open(self.config_file, 'r') as f:
                db_file_path = f.readline()
                self.config_file_error = False
            return db_file_path
        except FileNotFoundError:
            self.config_file_error = True
            print("Le fichier config_db_path.txt n'est pas présent dans le répertoire courant")

    def create_connection(self):
        db_file_path = self.get_database_path()
        if not self.config_file_error:
            try:
                connection = sqlite3.connect(db_file_path)
                print(f'Sqlite3 version {sqlite3.version}')
                return connection
            except Error as error_message:
                self.db_file_error = True
                self.db_file_error_message = error_message
                print(self.db_file_error_message)

    def build_tables(self, connection):
        # Feed the tables into list variables
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM cfi_filieres")
        self.filieres = tuple(cursor.fetchall())
        cursor.execute("SELECT * FROM cfi_sites")
        self.sites = tuple(cursor.fetchall())
        cursor.execute("SELECT * FROM cfi_classements")
        self.classements = tuple(cursor.fetchall())
        cursor.execute("SELECT * FROM cfi_contrats")
        self.contrats = tuple(cursor.fetchall())
        cursor.execute("SELECT * FROM cfi_titulaires")
        self.titulaires = tuple(cursor.fetchall())
        cursor.execute("SELECT * FROM cfi_services")
        self.services = tuple(cursor.fetchall())
        cursor.execute("SELECT * FROM cfi_types")
        self.types = tuple(cursor.fetchall())
        cursor.execute("SELECT * FROM cfi_auteurs")
        self.auteurs = tuple(cursor.fetchall())
        cursor.execute("SELECT * FROM cfi_19C_refs")
        self.references_19C = tuple(cursor.fetchall())
        self.refresh_presentation_19C()

    def close_connection(self):
        self.con.close()

    def refresh_presentation_19C(self):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
                        SELECT ref_code, ref_titre, ref_creation_date, cfi_auteurs.auteur_email, ref_actif, ref_commentaire 
                        FROM cfi_19C_refs
                        INNER JOIN cfi_auteurs
                        ON cfi_19C_refs.ref_auteur = cfi_auteurs.id_auteur''')
        self.presentation_19C = tuple(cursor.fetchall())
        self.close_connection()

    def push_new_19C(self, new_19C_tuple):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute('''
                        INSERT INTO cfi_19C_refs(ref_code, ref_titre, ref_creation_date, ref_auteur, ref_actif, ref_commentaire)
                        VALUES (?, ?, ?, ?, ?, ?)''', new_19C_tuple)
        cursor.execute("SELECT * FROM cfi_19C_refs")
        self.references_19C = tuple(cursor.fetchall())
        connection.commit()
        self.refresh_presentation_19C()
        self.close_connection()

    def push_new_auteur(self, new_auteur_tuple):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO cfi_auteurs(auteur_trigramme, auteur_email, auteur_nom, auteur_prenom) "
            f"VALUES (?, ?, ?, ?)", new_auteur_tuple)
        cursor.execute("SELECT * FROM cfi_auteurs")
        self.auteurs = tuple(cursor.fetchall())
        connection.commit()
        self.close_connection()
