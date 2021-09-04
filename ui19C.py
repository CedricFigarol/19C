import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from db19C import DataBaseManager
from my19C import My19C, Sub19C
from user19C import UserManager
import datetime
import csv
import pyperclip

COLOR1 = '#A3CDD9'
COLOR2 = '#FFFCE6'
COLOR3 = '#F2CC39'
COLOR4 = '#506AD4'
COLOR5 = '#C2B8AD'
FAVICON = "favicon.ico"


class Application19C(tk.Tk):
    def __init__(self, VERSION):
        tk.Tk.__init__(self)
        self.db = DataBaseManager()
        self.my19C = My19C(['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-'],
                           ['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-'])
        # Main window configuration
        self.title("Mon 19C")
        self.minsize(width=700, height=480)
        self.config(bg=COLOR1, padx=30, pady=30)
        self.iconbitmap(FAVICON)
        self.set_label_widgets()
        self.set_combobox_widgets()
        self.set_text_entry_widgets()
        self.set_button_widgets()
        self.set_mandatory_tags()
        self.set_menu()
        self.version_application = VERSION

    def file_error_report(self):
        pass

    def set_label_widgets(self):
        labels_font = ("Arial", 15, 'bold')
        self.filiere_label = tk.Label(self, text="Filière ou type d'installation ", bg=COLOR1, fg=COLOR2,
                                      font=labels_font)
        self.filiere_label.grid(row=1, column=1, sticky='E')
        self.site_label = tk.Label(self, text="Bigramme du site ", bg=COLOR1, fg=COLOR2, font=labels_font)
        self.site_label.grid(row=2, column=1, sticky='E')
        self.classement_label = tk.Label(self, text="Code de classement ", bg=COLOR1, fg=COLOR2, font=labels_font)
        self.classement_label.grid(row=3, column=1, sticky='E')
        self.contrat_label = tk.Label(self, text="Numéro de contrat ", bg=COLOR1, fg=COLOR2, font=labels_font)
        self.contrat_label.grid(row=4, column=1, sticky='E')
        self.titulaire_label = tk.Label(self, text="Code du titulaire du contrat ", bg=COLOR1, fg=COLOR2,
                                        font=labels_font)
        self.titulaire_label.grid(row=5, column=1, sticky='E')
        self.service_label = tk.Label(self, text="Bigramme du service destinataire ", bg=COLOR1, fg=COLOR2,
                                      font=labels_font)
        self.service_label.grid(row=6, column=1, sticky='E')
        self.type_label = tk.Label(self, text="Type du document ", bg=COLOR1, fg=COLOR2, font=labels_font)
        self.type_label.grid(row=7, column=1, sticky='E')
        self.auteur_label = tk.Label(self, text="Rédacteur du document ", bg=COLOR1, fg=COLOR2, font=labels_font)
        self.auteur_label.grid(row=8, column=1, sticky='E')
        self.titre_label = tk.Label(self, text="Titre du livrable ", bg=COLOR1, fg=COLOR2, font=labels_font)
        self.titre_label.grid(row=9, column=1, sticky='E')
        self.commentaire_label = tk.Label(self, text="Commentaire ", bg=COLOR1, fg=COLOR2, font=labels_font, pady=50)
        self.commentaire_label.grid(row=10, column=1, sticky='E')

    def set_combobox_widgets(self):
        combobox_width = 70
        self.filiere_combobox = ttk.Combobox(self, values=self.db.filieres, width=combobox_width, state='readonly')
        self.filiere_combobox.grid(row=1, column=2, sticky='W')
        self.site_combobox = ttk.Combobox(self, values=self.db.sites, width=combobox_width, state='readonly')
        self.site_combobox.grid(row=2, column=2, sticky='W')
        self.classement_combobox = ttk.Combobox(self, values=self.db.classements, width=combobox_width,
                                                state='readonly')
        self.classement_combobox.grid(row=3, column=2, sticky='W')
        self.contrat_combobox = ttk.Combobox(self, values=self.db.contrats, width=combobox_width, state='readonly')
        self.contrat_combobox.grid(row=4, column=2, sticky='W')
        self.titulaire_combobox = ttk.Combobox(self, values=self.db.titulaires, width=combobox_width, state='readonly')
        self.titulaire_combobox.grid(row=5, column=2, sticky='W')
        self.service_combobox = ttk.Combobox(self, values=self.db.services, width=combobox_width, state='readonly')
        self.service_combobox.grid(row=6, column=2, sticky='W')
        self.type_combobox = ttk.Combobox(self, values=self.db.types, width=combobox_width, state='readonly')
        self.type_combobox.grid(row=7, column=2, sticky='W')
        self.auteur_combobox = ttk.Combobox(self, values=self.db.auteurs, width=combobox_width, state='readonly')
        self.auteur_combobox.grid(row=8, column=2, sticky='W')

    def set_text_entry_widgets(self):
        self.titre_entry = tk.Entry(self, width=73)
        self.titre_entry.grid(row=9, column=2, sticky='W')
        self.commentaire_entry = tk.Text(self, font=('Arial', 10), width=63, height=3)
        self.commentaire_entry.grid(row=10, column=2, sticky='W')

    def set_button_widgets(self):
        self.generate_bt = tk.Button(self, text='Générer le 19C', font=('Arial', 25, 'bold'), width=30,
                                     command=self.generate_19C)
        self.generate_bt.grid(row=11, column=1, columnspan=2)

    def set_mandatory_tags(self):
        for i in range(8):
            mandatory = tk.Label(text='*', bg=COLOR1, fg='red', font=("Arial", 15, 'bold'))
            mandatory.grid(row=i + 1, column=3, sticky='W')

    def set_menu(self):
        menu_bar = tk.Menu()
        # Menu des références
        menu_references_19C = tk.Menu(menu_bar, tearoff=0)
        menu_references_19C.add_command(label="Afficher la table des 19C", command=self.open_ref_table_window)
        menu_references_19C.add_command(label="Exporter la table des 19C", command=self.export_ref_table)
        menu_references_19C.add_separator()
        menu_references_19C.add_command(label="Afficher les utilisateurs", command=self.open_show_users_window)
        menu_references_19C.add_command(label="Ajouter un utilisateur", command=self.open_add_user_window)
        menu_bar.add_cascade(label='Options', menu=menu_references_19C)
        # Menu aide
        menu_aide_19C = tk.Menu(menu_bar, tearoff=0)
        menu_aide_19C.add_command(label="À propos", command=self.open_info_window)
        menu_bar.add_cascade(label='Aide', menu=menu_aide_19C)
        self.config(menu=menu_bar)

    def generate_19C(self):
        mandatory_fields = [self.filiere_combobox.current(), self.site_combobox.current(),
                            self.classement_combobox.current(),
                            self.contrat_combobox.current(), self.titulaire_combobox.current(),
                            self.service_combobox.current(),
                            self.type_combobox.current(), self.auteur_combobox.current()]
        if -1 in mandatory_fields:
            messagebox.showerror(title='Données insuffisantes',
                                 message='Tous les champs avec un * doivent être renseignés')
        else:
            self.my19C.filiere = Sub19C(self.db.filieres[self.filiere_combobox.current()])
            self.my19C.site = Sub19C(self.db.sites[self.site_combobox.current()])
            self.my19C.classement = Sub19C(self.db.classements[self.classement_combobox.current()])
            self.my19C.contrat = Sub19C(self.db.contrats[self.contrat_combobox.current()])
            self.my19C.titulaire = Sub19C(self.db.titulaires[self.titulaire_combobox.current()])
            self.my19C.service = Sub19C(self.db.services[self.service_combobox.current()])
            self.my19C.type = Sub19C(self.db.types[self.type_combobox.current()])
            self.my19C.auteur = Sub19C(self.db.auteurs[self.auteur_combobox.current()])
            self.my19C.titre = self.titre_entry.get()
            self.my19C.commentaire = self.commentaire_entry.get('1.0', 'end-1c')
            self.my19C.get_first_available_chrono(self.db.references_19C)
            self.my19C.concatenate_codes()
            db_new_19C_entry_tuple = [self.my19C.reference, self.my19C.titre,
                                      str(datetime.datetime.utcnow().now())[:19],
                                      self.my19C.auteur.id, '1', self.my19C.commentaire]
            if self.my19C.chrono == '000':
                confirmation_message = f"La référence {self.my19C.reference} va être enregistré dans la base de donnée.\n" \
                                       f"Confirmez-vous l'exactitude de vos données d'entrée ?"
            else:
                confirmation_message = f"La référence {self.my19C.reference} va être enregistré dans la base de donnée.\n\n" \
                                       f"Note : pour éviter les références jumelles, le numéro chrono a été incrémenté à la valeur " \
                                       f"{self.my19C.chrono}.\n\nConfirmez-vous l'exactitude de vos données d'entrée ?"
            confBox = messagebox.askquestion('Confirmation avant enregistrement', confirmation_message)
            if confBox == 'yes':
                self.db.push_new_19C(db_new_19C_entry_tuple)
                print(f"Le 19C {db_new_19C_entry_tuple} a été enregistré dans la base de donnée.")
                pyperclip.copy(self.my19C.reference)
                messagebox.showinfo(title='Attention', message='Nouvelle entrée crée dans la base de donnée.\n\n'
                                            'Hint : la référence du nouveau 19C est dans le presse-papier. Ctrl+V pour coller la référence.')

    def open_ref_table_window(self):
        refs_win = tk.Toplevel(self)
        refs_win.title('Mon 19C - Table des références')
        refs_win.iconbitmap(FAVICON)
        refs_win.grab_set()     # The window keeps the focus until closed
        # Create columns in a Treeview
        headings = ('19C', 'titre', 'date', 'auteur', 'actif', 'commentaire')
        columns_widths = (160, 320, 120, 160, 40, 400)
        refs_table = ttk.Treeview(refs_win, columns=headings, show='headings', selectmode='extended', height=20)
        # Set the headings title for each column
        for column, width in zip(headings, columns_widths):
            refs_table.heading(column, text=column)
            refs_table.column(column, anchor='center', width=width, stretch=True)
        # Set the values in the table
        for row in self.db.presentation_19C:
            refs_table.insert('', 'end', values=row)
        # Position the table in the window
        refs_table.grid(row=0, column=0, columnspan=2)

    def open_show_users_window(self):
        users_win = tk.Toplevel(self)
        users_win.title('Mon 19C - Table des utilisateurs')
        users_win.iconbitmap(FAVICON)
        users_win.grab_set()  # The window keeps the focus until closed
        # Create columns in a Treeview
        headings = ('id', 'trigramme', 'email', 'nom', 'prénom')
        columns_widths = (30, 90, 160, 120, 120)
        users_table = ttk.Treeview(users_win, columns=headings, show='headings', selectmode='extended', height=20)
        # Set the headings title for each column
        for column, width in zip(headings, columns_widths):
            users_table.heading(column, text=column)
            users_table.column(column, anchor='center', width=width, stretch=True)
        # Set the values in the table
        for row in self.db.auteurs:
            users_table.insert('', 'end', values=row)
        # Position the table in the window
        users_table.grid(row=0, column=0, columnspan=2)

    def open_add_user_window(self):

        def add_new_user():
            new_user = UserManager('prénom', 'nom', 'trigramme', 'email')
            new_user.nom = nom_entry.get().upper()
            new_user.prenom = prenom_entry.get().upper()
            new_user.email = email_entry.get().lower()
            new_user.set_trigramme()
            if new_user.nom == '' or new_user.prenom == '' or new_user.email == '':
                messagebox.showerror(title='Attention', message='Complétez tous les champs.')
            else:
                self.db.push_new_auteur(new_user.user_tuple)
                add_user_win.destroy()
                messagebox.showinfo(title='Info', message='Utilisateur ajouté.')

        labels_font = ("Arial", 15, 'bold')
        add_user_win = tk.Toplevel(self)
        add_user_win.minsize(width=380, height=200)
        add_user_win.config(bg=COLOR1, padx=30, pady=30)
        add_user_win.title('Mon 19C - Ajouter un utilisateur')
        add_user_win.iconbitmap(FAVICON)
        add_user_win.grab_set()     # The window keeps the focus until closed
        nom_label = tk.Label(add_user_win, text="Nom", bg=COLOR1, fg=COLOR2, font=labels_font, padx=10)
        nom_label.grid(row=1, column=1, sticky='E')
        nom_entry = tk.Entry(add_user_win, width=30)
        nom_entry.grid(row=1, column=2)
        prenom_label = tk.Label(add_user_win, text='Prénom', bg=COLOR1, fg=COLOR2, font=labels_font, padx=10)
        prenom_label.grid(row=2, column=1, sticky='E')
        prenom_entry = tk.Entry(add_user_win, width=30)
        prenom_entry.grid(row=2, column=2)
        email_label = tk.Label(add_user_win, text='Email', bg=COLOR1, fg=COLOR2, font=labels_font, padx=10, pady=20)
        email_label.grid(row=3, column=1, sticky='E')
        email_entry = tk.Entry(add_user_win, width=30)
        email_entry.grid(row=3, column=2)
        add_user_bt = tk.Button(add_user_win, text='Ajouter', width=20, command=add_new_user)
        add_user_bt.grid(row=5, column=1, columnspan=2)

    def export_ref_table(self):
        export_date = str(datetime.datetime.utcnow().now())[:19].replace(":", "_")
        file_path = f'.\exports\export_{export_date}.csv'
        try:
            with open(file_path, 'w+') as csv_file:
                csv_content_writer = csv.writer(csv_file)
                for row in self.db.presentation_19C:
                    csv_content_writer.writerow(row)
        except:
            messagebox.showerror(title='Attention', message='Erreur durant la génération du fichier .csv\n\n'
                                         'Hint : vérifiez que vous avez un répertoire \exports dans le répertoire courant. '
                                         'Si non, créez-le.')
        else:
            messagebox.showinfo(title='Attention', message=f'Fichier csv généré :\n{file_path}')

    def open_info_window(self):
        messagebox.showinfo(title='À propos', message=f'Mon 19C - Version {self.version_application} - 2021\n\n'
                                                      f'Outil codé pour les IPs AKKA des plateaux EDF DIPDE\n\n'
                                                      f'Pour toute question, veuillez contacter :\n'
                                                      f'Cédric Figarol - cedric.figarol@akka.eu')


