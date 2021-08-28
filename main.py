"""
Fichier Python principal de l'interface avec la database SQLite des références EDF type "19 caractères".
Outil codé pour les IPs AKKA des plateaux EDF DIPDE
Cédric Figarol - cedric.figarol@akka.eu - 2021
"""
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3

# Palette de couleur
color1='#A3CDD9'
color2='#FFFCE6'
color3='#F2CC39'
color4='#506AD4'
color5='#C2B8AD'


# Création de la fenêtre princpale
monApp = tk.Tk()
monApp.title("Mon 19 caractères")
monApp.geometry("700x480")
monApp.iconbitmap("favicon.ico")


# Connexion à la database 19C et instanciation de la commande pour les requêtes
connection = sqlite3.connect("19C_database.db")
cursor = connection.cursor()

# REQUETES SQL
site_code = ("CS",)
cursor.execute("SELECT * FROM cfi_sites WHERE site_code = ?", site_code)
print(cursor.fetchall())

# Fermeture de la connexion à la database 19C
connection.close()

monApp.mainloop()