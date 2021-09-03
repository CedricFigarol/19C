import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from db19C import DataBaseManager
from my19C import My19C, Sub19C
import datetime

COLOR1 = '#A3CDD9'
COLOR2 = '#FFFCE6'
COLOR3 = '#F2CC39'
COLOR4 = '#506AD4'
COLOR5 = '#C2B8AD'
FAVICON = "favicon.ico"


class Application19C(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.db = DataBaseManager()
        self.my19C = My19C(['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-'],
                           ['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-'])
        # Main window configuration
        self.title("Mon 19Caractères")
        self.minsize(width=700, height=480)
        self.config(bg=COLOR1, padx=30, pady=30)
        self.iconbitmap(FAVICON)
        self.set_label_widgets()
        self.set_combobox_widgets()
        self.set_text_entry_widgets()
        self.set_button_widgets()
        self.set_mandatory_tags()
        self.set_menu()

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
        menu_references_19C = tk.Menu(menu_bar, tearoff=0)
        menu_references_19C.add_command(label="Afficher la table des 19C", command=self.open_ref_table_window)
        menu_references_19C.add_command(label="Exporter la table des 19C", command=self.export_ref_table)
        menu_references_19C.add_command(label="Ajouter un IP", command=self.open_add_user_window)
        menu_bar.add_cascade(label='Options', menu=menu_references_19C)
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

    def open_ref_table_window(self):
        refs_win = tk.Toplevel(self)
        refs_win.iconbitmap(FAVICON)
        # Create 6 columns in a Treeview
        # ref_code, ref_titre, ref_creation_date, cfi_auteurs.auteur_trigramme, ref_actif, ref_commentaire
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

    def open_add_user_window(self):
        pass

    def export_ref_table(self):
        pass
