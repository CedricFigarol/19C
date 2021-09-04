"""
Fichier Python principal de l'interface avec la database SQLite des références EDF type "19 caractères".
Outil codé pour le besoin des IPs AKKA des plateaux EDF DIPDE.
Cédric Figarol - cedric.figarol@akka.eu - Akka_2021.
"""
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import datetime

my_19C_dic = {
    'filiere': '-',
    'site': '--',
    'classement': '-----',
    'chrono': '000',
    'contrat': '----',
    'titulaire': '-',
    'service': '--',
    'type': '-',
    'auteur': '',
}
my_19C='-------------------'

# -------------------------- Constantes -------------------
COLOR1 ='#A3CDD9'
COLOR2 ='#FFFCE6'
COLOR3 ='#F2CC39'
COLOR4 ='#506AD4'
COLOR5 ='#C2B8AD'


# -------------------------- Fonctions --------------------
def set_value(combobox, dic_key, table):
    global my_19C_dic
    my_19C_dic[dic_key] = table[combobox.current()][2]
    generate_19C()


def generate_19C():
    global my_19C, my_19C_dic
    my_19C = ''
    for key, value in my_19C_dic.items():
        if key != 'auteur':
            my_19C += value
    # Si seul le chrono manque
    print(f"Il manque {my_19C.count('-')} caractères dans le 19C")
    if my_19C.count('-') <= 3:
        # Si un même 19C sans la partie chrono existe déjà dans la DB alors incrémenter le chrono
        twin_nb = 0
        for record in table_19C:
            if record[1] == my_19C:
                print(f'{record[1]} versus {my_19C}')
                twin_nb += 1
                print(twin_nb)
        my_19C_dic['chrono'] = f'{twin_nb:03d}'
        my_19C = ''
        for key, value in my_19C_dic.items():
            if key != 'auteur':
                my_19C += value
    code_19C_label.config(text=my_19C)


def insert_19C_inDB():
    global table_19C, my_19C
    connection = sqlite3.connect("../19C_database.db")
    cursor = connection.cursor()
    code = my_19C
    titre = titre_entry.get()
    date = datetime.datetime.now()
    auteur_email = my_19C_dic['auteur']
    ref_active = '1'
    commentaire = commentaire_entry.get('1.0', 'end-1c')
    entry_tuple = (code, titre, str(date.date()), auteur_email, ref_active, commentaire)
    print(entry_tuple)
    cursor.execute(
        f"INSERT INTO references_19C(ref_19C_code, ref_19C_titre_doc, ref_19C_creation_date, ref_19C_auteur, ref_19C_ref_active, ref_19C_commentaire) "
        f"VALUES (?, ?, ?, ?, ?, ?)", entry_tuple)
    cursor.execute("SELECT * FROM references_19C")
    table_19C = tuple(cursor.fetchall())
    connection.commit()
    connection.close()
    filiere_combobox.set('')
    site_combobox.set('')
    classement_combobox.set('')
    contrat_combobox.set('')
    titulaire_combobox.set('')
    service_combobox.set('')
    type_combobox.set('')
    auteur_combobox.set('')
    my_19C = '-------------------'


# -------------------------- SQLite -----------------------
connection = sqlite3.connect("../19C_database.db")
cursor = connection.cursor()
# site_code = ("CS",)
# cursor.execute("SELECT * FROM cfi_sites WHERE site_code = ?", site_code)
cursor.execute("SELECT * FROM cfi_filieres")
table_filieres = tuple(cursor.fetchall())
cursor.execute("SELECT * FROM cfi_sites")
table_sites = tuple(cursor.fetchall())
cursor.execute("SELECT * FROM cfi_classements")
table_classements = tuple(cursor.fetchall())
cursor.execute("SELECT * FROM cfi_contrats")
table_contrats = tuple(cursor.fetchall())
cursor.execute("SELECT * FROM cfi_titulaires")
table_titulaires = tuple(cursor.fetchall())
cursor.execute("SELECT * FROM cfi_services")
table_services = tuple(cursor.fetchall())
cursor.execute("SELECT * FROM cfi_types")
table_types = tuple(cursor.fetchall())
cursor.execute("SELECT * FROM cfi_auteurs")
table_auteurs = tuple(cursor.fetchall())
cursor.execute("SELECT * FROM references_19C")
table_19C = tuple(cursor.fetchall())
connection.close()


# -------------------------- GUI --------------------------
# Création de la fenêtre principale root Tkinter
root = tk.Tk()
root.title("Mon 19Caractères")
root.minsize(width=700, height=480)
root.config(bg=COLOR1, padx=30, pady=30)
root.iconbitmap("favicon.ico")
# Déclaration et positionnement des labels Tkinter
labels_font = ("Arial", 15, 'bold')
filiere_label = tk.Label(root, text="Filière ou type d'installation ", bg=COLOR1, fg=COLOR2, font=labels_font)
site_label = tk.Label(root, text="Bigramme du site ", bg=COLOR1, fg=COLOR2, font=labels_font)
classement_label = tk.Label(root, text="Code de classement ", bg=COLOR1, fg=COLOR2, font=labels_font)
contrat_label = tk.Label(root, text="Numéro de contrat ", bg=COLOR1, fg=COLOR2, font=labels_font)
titulaire_label = tk.Label(root, text="Code du titulaire du contrat ", bg=COLOR1, fg=COLOR2, font=labels_font)
service_label = tk.Label(root, text="Bigramme du service destinataire ", bg=COLOR1, fg=COLOR2, font=labels_font)
type_label = tk.Label(root, text="Type du document ", bg=COLOR1, fg=COLOR2, font=labels_font)
titre_label = tk.Label(root, text="Nom du document ", bg=COLOR1, fg=COLOR2, font=labels_font)
auteur_label = tk.Label(root, text="Rédacteur du document ", bg=COLOR1, fg=COLOR2, font=labels_font)
commentaire_label = tk.Label(root, text="Commentaire ", bg=COLOR1, fg=COLOR2, font=labels_font)
code_19C_label = tk.Label(root, text=my_19C, heigh=2, bg=COLOR3, font=("Arial", 30, 'bold'))
filiere_label.grid(row=1, column=1, sticky='E')
site_label.grid(row=2, column=1, sticky='E')
classement_label.grid(row=3, column=1, sticky='E')
contrat_label.grid(row=4, column=1, sticky='E')
titulaire_label.grid(row=5, column=1, sticky='E')
service_label.grid(row=6, column=1, sticky='E')
type_label.grid(row=7, column=1, sticky='E')
titre_label.grid(row=9, column=1, sticky='E')
auteur_label.grid(row=8, column=1, sticky='E')
commentaire_label.grid(row=10, column=1, sticky='E')
code_19C_label.grid(row=11, column=1, pady=20, sticky='WE', columnspan= 2)
# Déclaration, positionnement et binding des listes de choix ttk + champ de text
combobox_width = 70
filiere_combobox = ttk.Combobox(root, values=table_filieres, width=combobox_width, state='readonly')
filiere_combobox.bind('<<ComboboxSelected>>',lambda event, combobox_name=filiere_combobox, dic_key='filiere', table_name=table_filieres:set_value(combobox_name, dic_key, table_name))
site_combobox = ttk.Combobox(root, values=table_sites, width=combobox_width, state='readonly')
site_combobox.bind('<<ComboboxSelected>>', lambda event, combobox_name=site_combobox, dic_key='site', table_name=table_sites:set_value(combobox_name, dic_key, table_name))
classement_combobox = ttk.Combobox(root, values=table_classements, width=combobox_width, state='readonly')
classement_combobox.bind('<<ComboboxSelected>>', lambda event, combobox_name=classement_combobox, dic_key='classement', table_name=table_classements:set_value(combobox_name, dic_key, table_name))
contrat_combobox = ttk.Combobox(root, values=table_contrats, width=combobox_width, state='readonly')
contrat_combobox.bind('<<ComboboxSelected>>', lambda event, combobox_name=contrat_combobox, dic_key='contrat', table_name=table_contrats:set_value(combobox_name, dic_key, table_name))
titulaire_combobox = ttk.Combobox(root, values=table_titulaires, width=combobox_width, state='readonly')
titulaire_combobox.bind('<<ComboboxSelected>>', lambda event, combobox_name=titulaire_combobox, dic_key='titulaire', table_name=table_titulaires:set_value(combobox_name, dic_key, table_name))
service_combobox = ttk.Combobox(root, values=table_services, width=combobox_width, state='readonly')
service_combobox.bind('<<ComboboxSelected>>', lambda event, combobox_name=service_combobox, dic_key='service', table_name=table_services:set_value(combobox_name, dic_key, table_name))
type_combobox = ttk.Combobox(root, values=table_types, width=combobox_width, state='readonly')
type_combobox.bind('<<ComboboxSelected>>', lambda event, combobox_name=type_combobox, dic_key='type', table_name=table_types:set_value(combobox_name, dic_key, table_name))
titre_entry = tk.Entry(root, width=73)
auteur_combobox = ttk.Combobox(root, values=table_auteurs, width=combobox_width, state='readonly')
auteur_combobox.bind('<<ComboboxSelected>>', lambda event, combobox_name=auteur_combobox, dic_key='auteur', table_name=table_auteurs:set_value(combobox_name, dic_key, table_name))
commentaire_entry = tk.Text(root, width=49, height=5, font='Arial')
filiere_combobox.grid(row=1, column=2, sticky='W')
site_combobox.grid(row=2, column=2, sticky='W')
classement_combobox.grid(row=3, column=2, sticky='W')
contrat_combobox.grid(row=4, column=2, sticky='W')
titulaire_combobox.grid(row=5, column=2, sticky='W')
service_combobox.grid(row=6, column=2, sticky='W')
type_combobox.grid(row=7, column=2, sticky='W')
titre_entry.grid(row=9, column=2, sticky='W')
auteur_combobox.grid(row=8, column=2, sticky='W')
commentaire_entry.grid(row=10, column=2, sticky='W')
# Labelisation des champs obligatoires
for i in range(8):
    mandatory = tk.Label(text='*', bg=COLOR1, fg='red', font=labels_font)
    mandatory.grid(row=i+1, column=3, sticky='W')
# Déclaration et positionnement des boutons Tkinter
generate_bt = tk.Button(root, text='Enregister le 19C dans la base de données', width=10, bg=COLOR5, fg=COLOR2, font=("Arial", 20, 'bold'), relief='flat', command=insert_19C_inDB)
generate_bt.grid(row=12, column=1, sticky='WE', columnspan=2)



root.mainloop()