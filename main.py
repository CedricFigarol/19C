"""
Fichier Python principal de l'interface avec la database SQLite des références EDF type "19 caractères".
Outil codé pour les IPs AKKA des plateaux EDF DIPDE
Cédric Figarol - cedric.figarol@akka.eu - Akka_2021
"""

VERSION = '1.0'

from ui19C import Application19C

if __name__ == '__main__':
    myUI = Application19C(VERSION)
    myUI.mainloop()
