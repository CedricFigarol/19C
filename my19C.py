class Sub19C:
    def __init__(self, tablerow):
        self.id = tablerow[0]       # Key id of the table row item
        self.code = tablerow[2]     # 19C subCode of the table row item
        self.content = tablerow[1]  # Description of the table row item


class My19C:
    def __init__(self, filiere_row, site_row, classement_row, contrat_row,
                 titulaire_row, service_row, type_row, auteur_row):
        self.existing_ref = []
        self.filiere = Sub19C(filiere_row)
        self.site = Sub19C(site_row)
        self.classement = Sub19C(classement_row)
        self.chrono = '---'
        self.contrat = Sub19C(contrat_row)
        self.titulaire = Sub19C(titulaire_row)
        self.service = Sub19C(service_row)
        self.type = Sub19C(type_row)
        self.auteur = Sub19C(auteur_row)
        self.titre = ''
        self.commentaire = ''
        self.reference = '-------------------'
        self.concatenate_codes()

    def list_existing_ref(self, table_of_19C):
        for row in table_of_19C:
            self.existing_ref.append(row[1])

    def get_first_available_chrono(self, table_of_19C):
        self.list_existing_ref(table_of_19C)
        chrono_count = 0
        self.chrono = f'{chrono_count:03d}'
        self.concatenate_codes()
        while self.reference in self.existing_ref:
            chrono_count += 1
            self.chrono = f'{chrono_count:03d}'
            self.concatenate_codes()

    def concatenate_codes(self):
        filiereC = self.filiere.code
        siteC = self.site.code
        classementC = self.classement.code
        chronoC = self.chrono
        contratC = self.contrat.code
        titulaireC = self.titulaire.code
        serviceC = self.service.code
        typeC = self.type.code
        self.reference = filiereC + siteC + classementC + chronoC + contratC + titulaireC + serviceC + typeC
        if not len(self.reference) == 19:
            self.reference = 'Error - 19C characters number is not 19'

