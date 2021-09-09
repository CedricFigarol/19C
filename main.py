"""
Main python file of the application.
This application provides a convenient interface to manage the "19 caractères" EDF references according the rules.
It uses a SQLite database to store all the required information.
The Tkinter module is used for the GUI.

Made for the AKKA Project Engineers of the EDF DIPDE "plateaux".

Cédric Figarol - cedric.figarol@akka.eu - Akka_2021
"""

from gui19C import Application19C

VERSION = '1.0'

if __name__ == '__main__':
    myUI = Application19C(VERSION)
    myUI.mainloop()
