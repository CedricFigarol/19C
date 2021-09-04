
class UserManager:
    def __init__(self, prenom, nom, trigramme, email):
        self.prenom = prenom.upper()
        self.nom = nom.upper()
        self.trigramme = trigramme.upper()
        self.email = email.lower()
        self.user_tuple = [self.trigramme, self.email, self.nom, self.prenom]

    def set_trigramme(self):
        if len(self.prenom) > 0 and len(self.nom) > 1:
            self.trigramme = self.prenom[:1] + self.nom[:2]
        self.refresh_user_tuple()

    def refresh_user_tuple(self):
        self.user_tuple = [self.trigramme, self.email, self.nom, self.prenom]