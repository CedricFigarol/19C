"""
Class user for creating a user object which attributes contain all the new's information.
MAIN METHODS purpose :
- Create the user's trigramme.
- Update the information.
"""


class UserManager:

    def __init__(self, prenom, nom, trigramme, email):
        self.prenom = prenom.upper()
        self.nom = nom.upper()
        self.trigramme = trigramme.upper()
        self.email = email.lower()
        self.refresh_user_tuple()

    def set_trigramme(self):
        """
        Method used to concatenate the first later of the firstname and the two fist letters of the lastname.
        :return: None
        """
        if len(self.prenom) > 0 and len(self.nom) > 1:
            self.trigramme = self.prenom[:1] + self.nom[:2]
        self.refresh_user_tuple()

    def refresh_user_tuple(self):
        self.user_tuple = [self.trigramme, self.email, self.nom, self.prenom]