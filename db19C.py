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
        cursor.execute("SELECT * FROM references_19C")
        self.references_19C = tuple(cursor.fetchall())

    def close_connection(self):
        self.con.close()

    def push_new_19C(self, new_19C_tuple):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO references_19C(ref_19C_code, ref_19C_titre_doc, ref_19C_creation_date, ref_19C_auteur, ref_19C_ref_active, ref_19C_commentaire) "
            f"VALUES (?, ?, ?, ?, ?, ?)", new_19C_tuple)
        cursor.execute("SELECT * FROM references_19C")
        self.references_19C = tuple(cursor.fetchall())
        connection.commit()
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

