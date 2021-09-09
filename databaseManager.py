"""
Class DataManager used for creating a database object which attributes mirror the db content, and for manipulating data.
MAIN METHODS purpose :
- Load the SQLite Database
- Inject new reference in the Database
- Inject new user in the Database
- Update the references table for presentation purpose
"""

import sqlite3
from sqlite3 import Error
import os
import json
import datetime
import time


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
        """
        Method used to read the DataBase file path in the confing_db_path.txt.
        :return: the DataBase file path.
        """
        try:
            with open(self.config_file, 'r') as f:
                db_file_path = f.readline()
                self.config_file_error = False
            return db_file_path
        except FileNotFoundError:
            self.config_file_error = True
            print("Le fichier config_db_path.txt n'est pas présent dans le répertoire courant")

    def create_connection(self):
        """
        Method used to load the SQLite data in the DataBaseManager object's attributes as lists.
        It uses the sqlite3 module and its connection method.
        :return: SQLite 3 connection object.
        """
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
        """
        Initializing Method used to initialize the attributes when creating an instance of the DataBaseManager class.
        The Execute methode of the Cursor object is used to generate SQL requests and the output is stored in the
        corresponding DataBaseManager attributes.
        :param connection: a DataBaseManager object.
        :return: None.
        """
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
        """
        Method used to close the connection with the SQLite DataBase file.
        :return: None
        """
        self.con.close()

    def refresh_presentation_19C(self):
        """
        Method used to fetch data contained in the references table and auteurs table
        in the attribute self.presentation_19C.
        The Execute methode of the Cursor object is used to generate SQL requests and the output is stored in the
        corresponding DataBaseManager attributes.
        :return: None
        """
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute(
            ''' SELECT ref_code, ref_titre, ref_creation_date, cfi_auteurs.auteur_email, ref_actif, ref_commentaire 
                FROM cfi_19C_refs
                INNER JOIN cfi_auteurs 
                ON cfi_19C_refs.ref_auteur = cfi_auteurs.id_auteur''')
        self.presentation_19C = tuple(cursor.fetchall())
        self.close_connection()

    def push_new_19C(self, new_19C_tuple):
        """
        Method us to feed the new 19C's information in the SQLite DataBase file.
        The Execute methode of the Cursor object is used to generate SQL requests and the output is stored in the
        corresponding DataBaseManager attributes.
        :param new_19C_tuple: a tuple containing all the new 19C's information set by the user.
        :return: new_19C_pushed ; boolean feedback to know if writing was done or not because of locked db
        """
        if self.check_if_db_valid_lockfile():
            print("Cannot write in the database, locked by another user")
            new_19C_pushed = False
            return new_19C_pushed
        else:
            self.lock_db_writing_access()
            connection = self.create_connection()
            cursor = connection.cursor()
            cursor.execute(
                ''' INSERT INTO cfi_19C_refs(ref_code, ref_titre, ref_creation_date, ref_auteur, ref_actif, ref_commentaire)
                    VALUES (?, ?, ?, ?, ?, ?)''', new_19C_tuple)
            cursor.execute("SELECT * FROM cfi_19C_refs")
            self.references_19C = tuple(cursor.fetchall())
            connection.commit()
            self.refresh_presentation_19C()
            self.close_connection()
            new_19C_pushed = True
            self.unlock_db_writing_access()
            return new_19C_pushed

    def push_new_auteur(self, new_auteur_tuple):
        """
        Method us to feed the new user's information in the SQLite DataBase file.
        The Execute methode of the Cursor object is used to generate SQL requests and the output is stored in the
        corresponding DataBaseManager attributes.
        :param new_auteur_tuple: a tuple containing all the new user's information set by the user.
        :return: new_auteur_pushed ; boolean feedback to know if writing was done or not because of locked db
        """
        if self.check_if_db_valid_lockfile():
            print("Cannot write in the database, locked by another user")
            new_auteur_pushed = False
            return new_auteur_pushed
        else:
            self.lock_db_writing_access()
            connection = self.create_connection()
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO cfi_auteurs(auteur_trigramme, auteur_email, auteur_nom, auteur_prenom) "
                f"VALUES (?, ?, ?, ?)", new_auteur_tuple)
            cursor.execute("SELECT * FROM cfi_auteurs")
            self.auteurs = tuple(cursor.fetchall())
            connection.commit()
            self.close_connection()
            new_auteur_pushed = True
            self.unlock_db_writing_access()
            return new_auteur_pushed

    def check_if_db_valid_lockfile(self):
        """
        SQLite does not well manage multi-user writing access. This could be an issue as this application aims to be
        used by several user: some of them could potentially try to store data at the same time.
        To prevent it, a lock file is created when a user is writing into the database and deleted once done.
        If another user attempts to write data when a lock file exists, a message pops up telling him/her that database
        is in-use and data writing must be done later on.
        Exception case: if the application of the user crashes while the lock file is created, the lock may not be
        suppressed - this would lead to permanently lock the application for all the users. Therefore, the date/time
        of file creation is also considered to manage database writing : if the lock file is "outdated", it will be
        bypassed and suppressed during the following writing attempt.
        METHOD: this method check if there is a lock file.
        :return: is_valid_lock_file ; boolean at True if there is a lock file not older than 5 minutes
        """
        path = self.get_database_path()[:-2] + 'lock'
        is_lock_file = os.path.isfile(path)
        print(f'There is a lock file: {is_lock_file}')
        is_valid_lock_file = False
        # If there is a database lock file in the db directory, read its locking data...
        if is_lock_file:
            try:
                with open(path, 'r') as json_lock_file:
                    lock_data = json.load(json_lock_file)
                    print(lock_data)
            except FileNotFoundError:
                print("Issue while accessing json file")

            finally:
                lock_date = lock_data["date"]
                lock_duration = datetime.datetime.now() - datetime.datetime.strptime(lock_date, '%Y-%m-%d %H:%M:%S.%f')
                # ... and check that last lock is no more than 5 minutes old
                if lock_duration.total_seconds() < (5 * 60):
                    is_valid_lock_file = True
                    print(f'THe database has been locked for {lock_duration.total_seconds()} s.')
                    print(f'Lock date makes it a valid lock file: {is_valid_lock_file}.')
                    print('ACCESS DENIED')
                # ... else, if too old, drop this lock file
                else:
                    is_valid_lock_file = False
                    os.remove(path)

        return is_valid_lock_file

    def lock_db_writing_access(self):
        """
        SQLite does not well manage multi-user writing access. This could be an issue as this application aims to be
        used by several user: some of them could potentially try to store data at the same time.
        To prevent it, a lock file is created when a user is writing into the database and deleted once done.
        If another user attempts to write data when a lock file exists, a message pops up telling him/her that database
        is in-use and data writing must be done later on.
        Exception case: if the application of the user crashes while the lock file is created, the lock may not be
        suppressed - this would lead to permanently lock the application for all the users. Therefore, the date/time
        of file creation is also considered to manage database writing : if the lock file is "outdated", it will be
        bypassed and suppressed during the following writing attempt.
        METHOD: this method check if there is a lock file.
        :return: None ; create the database lock file to limit the writing access to the current user
        """
        path = self.get_database_path()[:-2] + 'lock'
        locking_date = str(datetime.datetime.now())
        locking_user = os.getlogin()
        lock_data = {
            "date": locking_date,
            "user": locking_user,
        }
        print(f'db locked by {locking_user}')
        with open(path, 'w') as json_lock_file:
            json.dump(lock_data, json_lock_file)
        time.sleep(1)

    def unlock_db_writing_access(self):
        """
        SQLite does not well manage multi-user writing access. This could be an issue as this application aims to be
        used by several user: some of them could potentially try to store data at the same time.
        To prevent it, a lock file is created when a user is writing into the database and deleted once done.
        If another user attempts to write data when a lock file exists, a message pops up telling him/her that database
        is in-use and data writing must be done later on.
        Exception case: if the application of the user crashes while the lock file is created, the lock may not be
        suppressed - this would lead to permanently lock the application for all the users. Therefore, the date/time
        of file creation is also considered to manage database writing : if the lock file is "outdated", it will be
        bypassed and suppressed during the following writing attempt.
        METHOD: this method check if there is a lock file.
        :return: None ; drop the database lock file to free the writing access to other users
        """
        path = self.get_database_path()[:-2] + 'lock'
        os.remove(path)
