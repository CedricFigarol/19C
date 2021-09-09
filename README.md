# 19C
Gestionnaire de références EDF 19 caractères avec base de données SQLite

EDF Deliverable references - called "19 caractères" or 19C - must follow predefined rules fixed by EDF.
The 19C references end up by having a constant length of 19 characters.
This tool written in Python 3.0 aims to guide the user through the management of the 19C.
Its main functions are :
- Manage the communication with the SQLite database
- Create of a new 19C by completing a form made of lists and entry fields
- Consult the list of the existing 19C
- Export the list of the existing 19C
- Manage users of the tool

A configuration file named "config_db_path.txt" defines the path of the database.
The database location must make it accessible by all the users: intranet is therefore the most probable location.

Every time a user makes an export of the 19C list, the application generates a csv file placed into the subfolder .\export
