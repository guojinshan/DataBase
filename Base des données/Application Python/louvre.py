# !/usr/bin/python3

# ========================Bloc1: IMPORTATION DE LIBRAIRIE========================
import pymysql
import pymysql.cursors
import pandas as pd
import datetime
import os

# Python 3
from tkinter import *
import tkinter.ttk as ttk
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk
# ========================Bloc1 - END========================

# ========================Bloc2: VARIABLES GLOBALS======================
    # Définir différentes couleurs d'affichage
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
    # Définir le chemin des photos 
PATH = os.path.dirname(__file__)
BG_ICON_PATH = os.path.abspath(os.path.join (PATH, "background.jpg"))
USER_ICON_PATH = os.path.abspath(os.path.join (PATH, "username.png"))
PWD_ICON_PATH = os.path.abspath(os.path.join (PATH, "password.png"))
LOGIN_ICON_PATH = os.path.abspath(os.path.join (PATH, "login.jpg"))
CURRENT_USER_ICON_PATH = os.path.abspath(os.path.join (PATH, "current_user.png"))
    # Définir les attributs de chaque relation
Musee_Exterieur = pd.DataFrame(columns=['Nom','Adresse'])
Auteur = pd.DataFrame(columns=['Nom', 'Prenom', 'Naissance', 'Mort'])
Exposition_Permanante = pd.DataFrame(columns=['Nom'])
Exposition_Temporaire = pd.DataFrame(columns=['Nom', 'debut', 'fin'])
Oeuvre_Louvre = pd.DataFrame(columns=['Titre', 'Date', 'Dimension', 'Deja_empruntee', 'Type_oeuvre', 'Nom_auteur', 'Prenom_auteur', 'Naissance_auteur', 'Exposition', 'Prix'])
Oeuvre_Ext = pd.DataFrame(columns=['Titre', 'Date', 'Dimension', 'Deja_empruntee', 'Type_oeuvre', 'Nom_auteur', 'Prenom_auteur', 'Naissance_auteur', 'Exposition'])
Emprunt = pd.DataFrame(columns=['Debut', 'Fin', 'Musee', 'Titre_oeuvre', 'Data_oeuvre', 'Prix'])
Pret = pd.DataFrame(columns=['Debut', 'Fin', 'Musee', 'Titre_oeuvre', 'Data_oeuvre', 'Prix'])
Prestataire = pd.DataFrame(columns=['Nom', 'Raison_social'])
Restauration = pd.DataFrame(columns=['Date', 'Type', 'Prix', 'Prestataire', 'Titre_oeuvre', 'Data_oeuvre'])
Creneau = pd.DataFrame(columns=['Jour', 'Horaire_debut', 'Expostion_permanante'])
Guide = pd.DataFrame(columns=['Id', 'Nom', 'Prenom', 'Adresse', 'Embauche', 'Exposition_temporaire'])
Creneau_Guide = pd.DataFrame(columns=['Guide', 'Jour', 'Horaire_debut', 'Exposition_permanente']) 
Salle = pd.DataFrame(columns=['Numero', 'Capacite', 'Exposition_temporaire'])
Panneau = pd.DataFrame(columns=['Numero', 'Texte', 'Salle'])

# vExposition nom de colonne et reqête sql
view_Exposition = pd.DataFrame(columns=['Nom'])
vExposition_sql = "SELECT * FROM vExposition;"
# vOeuvreLouvreEnRestau nom de colonne et reqête sql
view_OeuvreLouvreEnRestau = pd.DataFrame(columns=['Titre', 'Date_oeuvre', 'Prestataire', 'Date_restau', 'Type', 'Prix'])
vOeuvreLouvreEnRestau_sql = "SELECT * FROM vOeuvreLouvreEnRestau;"
# vOeuvreDejaPretee nom de colonne et reqête sql
view_OeuvreDejaPretee= pd.DataFrame(columns=['Titre', 'Date_oeuvre', 'Musee', 'Debut', 'Fin', 'Prix'])
vOeuvreDejaPretee_sql = "SELECT * FROM vOeuvreDejaPretee;"
# vOeuvreDejaEmpruntee nom de colonne et reqête sql
view_OeuvreDejaEmpruntee = pd.DataFrame(columns=['Titre', 'Date_oeuvre', 'Musee', 'Debut', 'Fin', 'Prix'])
vOeuvreDejaEmpruntee_sql = "SELECT * FROM vOeuvreDejaEmpruntee;"
# vOeuvreDejaEchangee nom de colonne et reqête sql
view_OeuvresDejaEchangee= pd.DataFrame(columns=['Titre', 'Date_oeuvre', 'Musee', 'Debut', 'Fin', 'Prix'])
vOeuvresDejaEchangee_sql = "SELECT * FROM vOeuvresDejaEchangee;"
#  vCreneau nom de colonne et reqête sql
view_Creneau= pd.DataFrame(columns=['Jour', 'Horaire', 'Exposition'])
vCreneau_sql = "SELECT * FROM vCreneau;"
# vCreneauGuide nom de colonne et reqête sql
view_CreneauGuide = pd.DataFrame(columns=['Guide', 'Jour', 'Horaire', 'Exposition'])
vCreneauGuide_sql = "SELECT * FROM vCreneauGuide;"
# vOeuvreLouvreAMettreAJour nom de colonne et reqête sql
view_OeuvreLouvreAMettreAJour  = pd.DataFrame(columns=['Titre', 'Date_oeuvre', 'Musee'])
vOeuvreLouvreAMettreAJour_sql = "SELECT * FROM vOeuvreLouvreAMettreAJour;"
# vOeuvreExtAMettreAJour nom de colonne et reqête sql
view_OeuvreExtAMettreAJour  = pd.DataFrame(columns=['Titre', 'Date_oeuvre', 'Musee'])
vOeuvreExtAMettreAJour_sql = "SELECT * FROM vOeuvreExtAMettreAJour;"
# statistic_1 nom de colonne et reqête sql
view_statistic_1 = pd.DataFrame(columns=['Montant'])
statistic_1_sql = "SELECT * FROM vMontantRestau;"
# statistic_2 nom de colonne et reqête sql
view_statistic_2 = pd.DataFrame(columns=['Musee', 'Prix_Moyen'])
statistic_2_sql = "SELECT * FROM vEmpruntMoyen;"
# statistic_3 nom de colonne et reqête sql
view_statistic_3 = pd.DataFrame(columns=['Musee', 'Montant'])
statistic_3_sql = "SELECT * FROM vMontantPret;"
# statistic_4 nom de colonne et reqête sql
view_statistic_4 = pd.DataFrame(columns=['Expostion', 'Duree_Par_Jour'])
statistic_4_sql = "SELECT * FROM vDureeExpoTemp;"
# statistic_5 nom de colonne et reqête sql
view_statistic_5 = pd.DataFrame(columns=['Exposition', 'Prix_Moyen'])
statistic_5_sql = "SELECT * FROM vPrixMoyenAcqui;"
# statistic_6 nom de colonne et reqête sql
view_statistic_6 = pd.DataFrame(columns=['Musee', 'Temps_Moye'])
statistic_6_sql = "SELECT * FROM vTempsMoyenPrets;"
# ========================Bloc2 - END========================

# =================================== Bloc3: FONCTION A APPELER====================================
def get_table_columns(table_current, return_view=False):
    '''Function to get all the columns of a selected table'''
    global  Musee_Exterieur, Exposition_Temporaire, Type_Oeuvre, Auteur, Exposition_Permanante, Exposition_Temporaire, Oeuvre_Louvre, \
            Oeuvre_Ext, Emprunt, Pret, Prestataire, Restauration, Creneau, Guide, Creneau_Guide, Salle, Panneau
    if table_current == "Musee_Exterieur":
        columns = Musee_Exterieur.columns
        if return_view:
            tree_view = create_view(App, Musee_Exterieur)
    if table_current == "Type_Oeuvre":
        columns = Type_Oeuvre.columns
        if return_view:
            tree_view = create_view(App, Type_Oeuvre)
    if table_current == "Auteur":
        columns = Auteur.columns
        if return_view:
            tree_view = create_view(App, Auteur)
    if table_current == "Exposition_Permanante":
        columns = Exposition_Permanante.columns
        if return_view:
            tree_view = create_view(App, Exposition_Permanante)
    if table_current == "Exposition_Temporaire":
        columns = Exposition_Temporaire.columns
        if return_view:
            tree_view = create_view(App, Exposition_Temporaire)
    if table_current == "Oeuvre_Louvre":
        columns = Oeuvre_Louvre.columns
        if return_view:
            tree_view = create_view(App, Oeuvre_Louvre)
    if table_current == "Oeuvre_Ext":
        columns = Oeuvre_Ext.columns
        if return_view:
            tree_view = create_view(App, Oeuvre_Ext)
    if table_current == "Emprunt":
        columns = Emprunt.columns
        if return_view:
            tree_view = create_view(App, Emprunt)
    if table_current == "Pret":
        columns = Oeuvre_Louvre.columns
        if return_view:
            tree_view = create_view(App, Pret)
    if table_current == "Prestataire":
        columns = Prestataire.columns
        if return_view:
            tree_view = create_view(App, Prestataire)
    if table_current == "Restauration":
        columns = Restauration.columns
        if return_view:
            tree_view = create_view(App, Restauration)
    if table_current == "Creneau":
        columns = Creneau.columns
        if return_view:
            tree_view = create_view(App, Creneau)
    if table_current == "Guide":
        columns = Guide.columns
        if return_view:
            tree_view = create_view(App, Guide)
    if table_current== "Creneau_Guide":
        columns = Creneau_Guide.columns
        if return_view:
            tree_view = create_view(App, Creneau_Guide)
    if table_current == "Salle":
        columns = Salle.columns
        if return_view:
            tree_view = create_view(App, Salle)
    if table_current == "Panneau":
        columns = Panneau.columns
        if return_view:
            tree_view = create_view(App, Panneau)
    if return_view:
        return columns, tree_view
    else:
        return columns

def get_all_entry_widgets_text_content(parent_widget):
    '''Function to get all the content of input box'''
    list_value = []
    children_widgets = parent_widget.winfo_children()
    for child_widget in children_widgets:
        if child_widget.winfo_class() == 'Entry':
            list_value.append(child_widget.get())
    return list_value     

def convert_dict_to_list(dict_value):
    '''Function to convert dict returned by database to list'''
    list_value = []
    for i in dict_value:
        temp = []
        for j, value in enumerate(i.values()):
            if isinstance(value, datetime.date):
                value = value.strftime("%d/%m/%Y")
            if (j+1) % len(i.values()) != 0:
                temp.append(value)
            else:
                temp.append(value)
                list_value.append(temp)
    return list_value

def get_index_of_key(index_not_null, table_current, return_index_to_update=False):
    '''Function to split all the input box with content into primary key part and non-primary part'''
    index_key = []
    if table_current in ["Musee_Exterieur", "Type_Oeuvre", "Exposition_Permanante", "Exposition_Temporaire", "Prestataire", "Guide", "Salle", "Panneau"]:
        for i in index_not_null:
            if i in [0]:
                index_key.append(i)
    if table_current in ["Oeuvre_Louvre", "Oeuvre_Ext"]:
        for i in index_not_null:
            if i in [0, 1]:
                index_key.append(i)
    if table_current in ["Auteur", "Creneau_Guide"]:
        for i in index_not_null:
            if i in [0, 1, 2]:
                index_key.append(i)
    if table_current in ["Emprunt", "Pret"]:
        for i in index_not_null:
            if i in [2, 3, 4]:
                index_key.append(i)
    if table_current in ["Restauration", "Creneau"]:
        for i in index_not_null:
            if i in [0, 4, 5]:
                index_key.append(i)
    if return_index_to_update:
        index_to_update = list(set(index_not_null) - set(index_key))
        return index_key, index_to_update
    else:
        return index_key

def update_area(event):
    '''Function to update information area when a new table seleted,  bound to table menu'''
    table_current =  table_name.get()
    global app, frame_input, tree_view
            # Clear Information Area
    for widget in frame_input.winfo_children():
        widget.destroy()
    columns, tree_view = get_table_columns(table_current, return_view=True)
        # Change Information Area
    for i, column in enumerate(columns):
        label_name = Label(frame_input, text=column, pady=5, width=25, borderwidth=2, relief="groove")
        label_name.grid(row=i, column=0)
        input_name = Entry(frame_input, width=80)
        input_name.grid(row=i, column=1)
    return

def create_view(Parent, table):
    '''Function to create a result dashbord by tree view'''
    tree_view = ttk.Treeview(Parent, columns=table.columns)
    tree_view.grid(row=2, sticky='nsew')
    tree_view.heading('#0', text='Item')
    tree_view.column('#0', stretch=YES)
    for i, column in enumerate(table.columns):
        Num = '#' + str(i+1)
        tree_view.heading(Num, text=column)
        tree_view.column(Num, stretch=YES)
    return tree_view 

def insert_view(view, list_value):
    '''Funtion to insert result list item to view'''
    view.delete(*view.get_children())
    for i in range(len(list_value)):
        view.insert('', 'end', text="Item_"+str(i+1), values=list_value[i])
    return

def search_accurate():
    '''Function to realize accurate query in app, bound to Search(A) button'''
    global frame_input
    global tree_view
    global conn
    fuzzy = False
         # Get the current table
    table_current = table_name.get()
        # Get all the input values
    list_value = get_all_entry_widgets_text_content(frame_input)
        # Check if all the input values are nulls and return the index of value if not
    index_not_null = check_input(list_value, table_current)
    if index_not_null:
            # Search into Database
        search_db(conn, list_value, table_current, index_not_null, fuzzy)
    return

def search_fuzzy():
    '''Function to realize Fuzzy query in app, bound to Searrch(A) button'''
    global frame_input
    global tree_view
    global conn
    fuzzy = True
        # Get the current table
    table_current = table_name.get()
        # Get all the input values
    list_value = get_all_entry_widgets_text_content(frame_input)
        # Check if all the input values are nulls and return the index of value if not
    index_not_null = check_input(list_value, table_current)
    if index_not_null:
            # Search into Database
        search_db(conn, list_value, table_current, index_not_null, fuzzy)
    return

def search_db(conn, list_value, table_current, index_not_null, fuzzy=None):
    '''Function to realize query in database'''
    columns = get_table_columns(table_current, return_view=False)
    try:
        with conn.cursor() as cur:
            sql = "SELECT * FROM " +  table_current + " WHERE " 
            for i, index in  enumerate(index_not_null):
                if fuzzy:
                    sql = sql + columns[index]  +  " like \'%{}%\'".format(list_value[index])
                else:
                    sql = sql + columns[index]  +  "= \'{}\'".format(list_value[index])
                if i < len(index_not_null)-1 :
                    sql = sql + " and "
                else:
                    sql = sql + ";"
            cur.execute(sql)
            fetch_result = cur.fetchall()
            list_value = convert_dict_to_list(fetch_result)
            insert_view(tree_view, list_value)
            if len(fetch_result) != 0:
                return True
            else:
                return False
    except Exception as e:
            print((FAIL + "{}"  + ENDC).format(e))
            return False

def insert_db(conn, list_value, table_current):
    global is_admin
    '''Function to insert new record in database'''
    list_value = tuple(list_value)
    if len(list_value) == 1:
        list_value = str(list_value).replace(',', '')
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO " +  table_current + " VALUES {0};".format(list_value)
            cur.execute(sql)
            if is_admin:
                conn.commit()
                print(OKGREEN + "Votre donnée a été bien insérée dans la base de données"  + ENDC)
            else:
                print(WARNING + "Insertion en échec, manque du droit Admin dans la base de données"  + ENDC)
    except Exception as e:
            print((FAIL + "{}"  + ENDC).format(e))
    return
    
def insert():
    '''Function to insert new record in app, bound to Insert button'''
    global frame_input
    global tree_view
    global conn
        # Get the current table
    table_current = table_name.get()
        # Get all the input values
    list_value = get_all_entry_widgets_text_content(frame_input)
        # Check if all the input values are nulls
    if check_input(list_value, table_current):
            # Insert into View
        insert_view(tree_view, [list_value])
            # Insert into Database
        insert_db(conn, list_value, table_current)
    return

def requst_db_all():
    '''Function to realize query all the records in database and show all in app, bound to Show All button'''
    global conn
    global tree_view
      # Get the current table
    table_current = table_name.get()
    try:
        with conn.cursor() as cur:
            sql = "SELECT * FROM " +  table_current + ";"
            cur.execute(sql)
            list_value = convert_dict_to_list(cur.fetchall())
            insert_view(tree_view, list_value)
    except Exception as e:
            print((FAIL + "{}"  + ENDC).format(e))
    return

def check_input(list_value, table_current):
    '''Function to check the input to avoid null value manipulation'''
    if all([value == ''  for value in list_value]):
        messagebox.showinfo("Errer", "Aucune valeur remplie")
        # Return the index of column not null
    index_not_null = []
    for i,value in enumerate(list_value):
        if value != '':
            index_not_null.append(i)
    return index_not_null

def delete_db(conn, list_value, table_current, index_not_null):
    '''Function to delete record in database'''
    index_key = get_index_of_key(index_not_null, table_current)
    columns = get_table_columns(table_current, return_view=False)
    try:
        with conn.cursor() as cur:
            sql = "DELETE FROM " +  table_current + " WHERE " 
            for j, index in enumerate(index_key):
                sql = sql + columns[index]  +  " = \'{}\'".format(list_value[index])
                if j < len(index_key)-1 :
                    sql = sql + " and "
                else:
                    sql = sql + ";"
            cur.execute(sql)
            if is_admin:
                conn.commit()
                print(OKGREEN + "Votre donnée a été bien supprimé dans la base de donnéese "  + ENDC)
            else:
                print(WARNING + "Suppression en échec, manque du droit Admin dans la base de données"  + ENDC)
    except Exception as e:
        print((FAIL + "{}"  + ENDC).format(e))
    return

def delete():
    '''Function to delete record in app, bound to Delete button'''
    global frame_input
    global tree_view
    global conn
    # Get the current table
    table_current = table_name.get()
        # Get all the input values
    list_value = get_all_entry_widgets_text_content(frame_input)
        # Check if all the input values are nulls
    index_not_null = check_input(list_value, table_current)
    index_key = get_index_of_key(index_not_null, table_current)
    if index_key:
        # Accurate research
        exist = search_db(conn, list_value, table_current, index_key, fuzzy=False)
        if exist: 
            confirm = messagebox.askyesno("Infomation Confirmée", "Item existe, Vous êtes sûr à supprimer?")
            if confirm:
                delete_db(conn, list_value, table_current, index_not_null)
        else:
            messagebox.showinfo("Erreur", "Item n'existe pas")
    return

def update_db(conn, list_value, table_current, index_not_null):
    '''Function to update record in database'''
    index_key, index_to_update = get_index_of_key(index_not_null, table_current, return_index_to_update=True)
    columns = get_table_columns(table_current, return_view=False)
    try:
        with conn.cursor() as cur:
            sql = "UPDATE " +  table_current + " SET " 
            for i, index in  enumerate(index_to_update):
                sql = sql + columns[index]  +  " = \'{}\'".format(list_value[index])
                if i < len(index_to_update)-1 :
                    sql = sql + ", "
                else:
                    sql = sql + " WHERE "
            for j, index in enumerate(index_key):
                sql = sql + columns[index]  +  " = \'{}\'".format(list_value[index])
                if j < len(index_key)-1 :
                    sql = sql + " and "
                else:
                    sql = sql + ";"
            cur.execute(sql)
            if is_admin:
                conn.commit()
                print(OKGREEN + "Votre donnée a été bien mise à jour dans la base de données"  + ENDC)
            else:
                print(WARNING + "Mise à jour en échec dans la base de données, manque du droit Admin"  + ENDC)
        search_db(conn, list_value, table_current, index_not_null, fuzzy=False)
    except Exception as e:
        print((FAIL + "{}"  + ENDC).format(e))
    return

def update():
    '''Function to update record in app'''
    global frame_input
    global tree_view
    global conn
    # Get the current table
    table_current = table_name.get()
        # Get all the input values
    list_value = get_all_entry_widgets_text_content(frame_input)
        # Check if all the input values are nulls
    index_not_null = check_input(list_value, table_current)
    index_key = get_index_of_key(index_not_null, table_current)
    if index_key:
        # Accurate research
        exist = search_db(conn, list_value, table_current, index_key, fuzzy=False)
        if exist: 
            confirm = messagebox.askyesno("Infomation Confirmée", "Item existe, Vous êtes sûr à mettre à jour?")
            if confirm:
                update_db(conn, list_value, table_current, index_not_null)
        else:
            messagebox.showinfo("Erreur", "Item n'existe pas")
    return

def clear():
    '''Function to clear all the content in input box'''
    global frame_input
    children_widgets = frame_input.winfo_children()
    for child_widget in children_widgets:
        if child_widget.winfo_class() == 'Entry':
            child_widget.delete(0, END)
    return

def add_user(current_user):
    '''Function to add current login user on App'''
    global frame_top
    global is_admin
    if is_admin:
        current_user = current_user + '(Admin)'
    else:
        current_user = current_user + '(Membre)'
    Label(frame_top, text=current_user, image=current_user_icon, compound=LEFT, font=("times new roman", 12, "bold"), bg='#F0F0F0').grid(row=0, column=3, padx=400)
    return

def login(event):
    '''Funtion bound to login button click event'''
    global conn
    global Login
    global App
    global username
    global password
    global login_frame
    global login_btn
    global is_admin
    current_user = username.get()
    if  username.get()== "" or  password.get()=="":
        messagebox.showerror("Erreur", "Tous les champs requis")
    else: 
        # Check in database
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM Utilisateur WHERE login=\'" + username.get() + "\' AND pwd=\'" + password.get() + "\';"
                cur.execute(sql)
                fetch_result = cur.fetchall()
                    # Assign the authority
                if fetch_result[0]['role'] == 'Admin':
                    is_admin = True
                if len(fetch_result) != 0:
                    # Hide Login window 
                    Login.withdraw()
                    # Make App window visible again
                    App.deiconify()
                    add_user(current_user)
                else:
                    messagebox.showerror("Erreur", "Nom d'utilisateur ou Mot de passe incorrecte")
        except Exception as e:
           print((FAIL + "{}"  + ENDC).format(e))
    # Recovery the button after being pressed
    login_btn = Button(login_frame, text="Login", width=8, font=("times new roman", 15, "bold"))
    login_btn.grid(row=3, column=0, pady=10, padx=25)
    login_btn.bind('<Button-1>', login)
    return

def reset(event):
    '''Function to clear content of Login Entry value'''
    global login_frame
    children_widgets = login_frame.winfo_children()
    for child_widget in children_widgets:
        if child_widget.winfo_class() == 'Entry':
            child_widget.delete(0, END)
    return

def on_closing():
    '''Allow user to quit the login interface at any time'''
    global App
    global Login
    App.destroy()

def enter_login(event):
    '''Function to login by pressing Enter key,bound to  Password Entry'''
    login(event)
    return

def show_view_statistic(conn, tree_view, App, view, sql):
    '''Function to display the result of view and statistic funciton in the Result area'''
    tree_view = create_view(App, view)
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            list_value = convert_dict_to_list(cur.fetchall())
            insert_view(tree_view, list_value)
    except Exception as e:
            print((FAIL + "{}"  + ENDC).format(e))

    # Function of view and statistic
def vExposition():
    global conn
    global tree_view
    global App
    global view_Exposition
    global vExposition_sql
    show_view_statistic(conn, tree_view, App, view_Exposition, vExposition_sql)
    return

def vOeuvreLouvreEnRestau():
    global conn
    global tree_view
    global App
    global view_OeuvreLouvreEnRestau
    global vOeuvreLouvreEnRestau_sql
    show_view_statistic(conn, tree_view, App, view_OeuvreLouvreEnRestau, vOeuvreLouvreEnRestau_sql)
    return

def vOeuvreDejaPretee():
    global conn
    global tree_view
    global App
    global view_OeuvreDejaPretee
    global vOeuvreDejaPretee_sql 
    show_view_statistic(conn, tree_view, App, view_OeuvreDejaPretee, vOeuvreDejaPretee_sql)
    return

def vOeuvreDejaEmpruntee():
    global conn
    global tree_view
    global App
    global view_OeuvreDejaEmpruntee
    global vOeuvreDejaEmpruntee_sql 
    show_view_statistic(conn, tree_view, App, view_OeuvreDejaEmpruntee, vOeuvreDejaEmpruntee_sql)
    return

def vOeuvresDejaEchangee():
    global conn
    global tree_view
    global App
    global view_OeuvresDejaEchangee
    global vOeuvresDejaEchangee_sql 
    show_view_statistic(conn, tree_view, App, view_OeuvresDejaEchangee, vOeuvresDejaEchangee_sql)
    return

def vCreneau():
    global conn
    global tree_view
    global App
    global view_Creneau
    global vCreneau_sql 
    show_view_statistic(conn, tree_view, App, view_Creneau, vCreneau_sql)
    return

def vCreneauGuide():
    global conn
    global tree_view
    global App
    global view_CreneauGuide
    global vCreneauGuide_sql 
    show_view_statistic(conn, tree_view, App, view_CreneauGuide, vCreneauGuide_sql)
    return

def vOeuvreLouvreAMettreAJour():
    global conn
    global tree_view
    global App
    global view_OeuvreLouvreAMettreAJour
    global vOeuvreLouvreAMettreAJour_sql 
    show_view_statistic(conn, tree_view, App, view_OeuvreLouvreAMettreAJour, vOeuvreLouvreAMettreAJour_sql)
    return

def vOeuvreExtAMettreAJour():
    global conn
    global tree_view
    global App
    global view_OeuvreExtAMettreAJour
    global vOeuvreExtAMettreAJour_sql 
    show_view_statistic(conn, tree_view, App, view_OeuvreExtAMettreAJour, vOeuvreExtAMettreAJour_sql)
    return

def statistic_1():
    global conn
    global tree_view
    global App
    global view_statistic_1
    global statistic_1_sql 
    show_view_statistic(conn, tree_view, App, view_statistic_1, statistic_1_sql)
    return

def statistic_2():
    global conn
    global tree_view
    global App
    global view_statistic_2
    global statistic_2_sql 
    show_view_statistic(conn, tree_view, App, view_statistic_2, statistic_2_sql)
    return

def statistic_3():
    global conn
    global tree_view
    global App
    global view_statistic_3
    global statistic_3_sql 
    show_view_statistic(conn, tree_view, App, view_statistic_3, statistic_3_sql)
    return

def statistic_4():
    global conn
    global tree_view
    global App
    global view_statistic_4
    global statistic_4_sql 
    show_view_statistic(conn, tree_view, App, view_statistic_4, statistic_4_sql)
    return

def statistic_5():
    global conn
    global tree_view
    global App
    global view_statistic_5
    global statistic_5_sql 
    show_view_statistic(conn, tree_view, App, view_statistic_5, statistic_5_sql)
    return

def statistic_6():
    global conn
    global tree_view
    global App
    global view_statistic_6
    global statistic_6_sql 
    show_view_statistic(conn, tree_view, App, view_statistic_6, statistic_6_sql)
    return
# ========================Bloc3 - END========================


# =================================== Bloc4: APP====================================
    # ========================Connection à la base de données========================
try: #ICI, on se connecte avec la BD sur PC local
    conn = pymysql.connect(host='localhost', user='root', password='XXXX', db='louvre', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    print(OKGREEN + "Connexion bien établie avec la base de données" + ENDC)

    App = Tk()
    App.resizable(width=False,height=False)
    App.geometry("880x750")
    App.title("Bienvenu à Louvre")
    App.grid_rowconfigure(1, weight=1)
    App.grid_columnconfigure(0, weight=1)
    App.withdraw()  # Cacher la fenêtre principale 'Système' 

    is_admin = False # Vérifier le role

    # ========================Interface Login========================
        # Initialiser la fênetre
    Login = Toplevel(App)
    Login.resizable(width=False,height=False)
    Login.title("NF18 - Application Python")
    Login.geometry("880x750")
        # Télécharger toutes les images
    bg_icon = ImageTk.PhotoImage(file=BG_ICON_PATH )
    user_icon = ImageTk.PhotoImage(file=USER_ICON_PATH)
    pwd_icon = ImageTk.PhotoImage(file=PWD_ICON_PATH)
    login_icon = ImageTk.PhotoImage(file=LOGIN_ICON_PATH)
    current_user_icon = ImageTk.PhotoImage(file=CURRENT_USER_ICON_PATH)
        #  Définir le titre en haut
    Label(Login, image=bg_icon).pack()
    title = Label(Login, text="Système Gestion Louvre", font=("times new roman", 40, "bold"), bg="orange", fg="blue", bd=10, relief=GROOVE)
    title.place(x=0, y=0, relwidth=1)
        # Créer un cadre de connexion pour mettre tous les wigets
    login_frame = Frame(Login, bg="white",  bd=2, relief=GROOVE)
    login_frame.place(x=538, y=250)
        # Mettez des icônes, des entrées et des boutons
    Label(login_frame, image=login_icon, bg="white").grid(row=0, columnspan=2, pady=10)
    Label(login_frame, text="Username", image=user_icon, compound=LEFT, font=("times new roman", 15, "bold"), bg="white").grid(row=1, column=0, pady=10)
    username = Entry(login_frame, bd=5, relief=GROOVE, font=("", 15))
    username.grid(row=1, column=1)
    Label(login_frame, text="Password", image=pwd_icon, compound=LEFT, font=("times new roman", 15, "bold"), bg="white").grid(row=2, column=0, pady=10)
    password = Entry(login_frame, bd=5, relief=GROOVE, font=("", 15), show='*')
    password.grid(row=2, column=1)
    password.bind('<Key-Return>', enter_login)
    login_btn = Button(login_frame, text="Login", width=8, font=("times new roman", 15, "bold"))
    login_btn.grid(row=3, column=0, pady=10, padx=25)
    login_btn.bind('<Button-1>', login)

    reset_btn = Button(login_frame, text="Reset", width=8, font=("times new roman", 15, "bold"))
    reset_btn.grid(row=3, column=1, pady=10)
    reset_btn.bind('<Button-1>', reset)

    login_footer = Label(Login, text="Crée par： Jinshan GUO / Qi XIA / Jules Yvon / Bastien LE CALVE       UTC     P20", height=30, font=("times new roman", 12, "bold"), bg="white")
    login_footer.pack(side="bottom", fill="both", expand=True)

    Login.protocol("WM_DELETE_WINDOW", on_closing)
    # ========================Interface  Login END========================

    # ========================Interface Système========================
        # Définir le style du caractère 
    ft_button = tkFont.Font(family='Times New Roman', size=12, weight=tkFont.BOLD)
    ft_label = tkFont.Font(family='Times New Roman', size=12, weight=tkFont.BOLD)
        # Créer le menu
            # Main menu
    main_menu = Menu(App)
    App.config(menu=main_menu)
            # Menu Vue
    menu_view = Menu(main_menu,tearoff=0)
    menu_view.add_command(label="1-vExposition", command=vExposition)
    menu_view.add_command(label="2-vOeuvreLouvreEnRestau", command=vOeuvreLouvreEnRestau)
    menu_view.add_command(label="3-vOeuvreDejàPrêtée", command=vOeuvreDejaPretee)
    menu_view.add_command(label="4-vOeuvreDejàEmpruntée", command=vOeuvreDejaEmpruntee)
    menu_view.add_command(label="5-vOeuvresDejàEchangee", command=vOeuvresDejaEchangee)
    menu_view.add_command(label="6-vCréneau", command=vCreneau)
    menu_view.add_command(label="7-vCréneauGuide", command=vCreneauGuide)
    menu_view.add_command(label="8-vOeuvreLouvreAMettreAJour",  command=vOeuvreLouvreAMettreAJour)
    menu_view.add_command(label="9-vOeuvreExtAMettreAJour",  command=vOeuvreExtAMettreAJour)
    main_menu.add_cascade(label="Vue",menu=menu_view)
            # Menu Statistique
    menu_statistic = Menu(main_menu,tearoff=0)
    menu_statistic.add_command(label="1-Montant des restaurations", command=statistic_1)
    menu_statistic.add_command(label="2-Prix moyen des emprunts par musée", command=statistic_2)
    menu_statistic.add_command(label="3-Montant du prix des prets par musée",  command=statistic_3)
    menu_statistic.add_command(label="4-Durée des exposittions temporaires",  command=statistic_4)
    menu_statistic.add_command(label="5-Prix moyen d'acquisition des oeuvres par exposition",  command=statistic_5)
    menu_statistic.add_command(label="6-Temps moyen des prêts avec les musées extérieur",  command=statistic_6)
    main_menu.add_cascade(label="Statistique",menu=menu_statistic)
        # Créer tous les conteneurs principaux
    frame_top = Frame(App, width=860, height=20, padx=3)
    frame_top.grid(row=0, sticky="ew")
    frame_center = Frame(App, width=860, height=800, padx=3, pady=5)
    frame_center.grid(row=1, sticky="nsew")
    frame_footer = Frame(App, width=860, height=20, padx=3)
    frame_footer.grid(row=3, sticky="ew")
        # Créer un menu d'options de la table
    list_table = ['Musee_Exterieur', 'Auteur', 'Exposition_Permanante', 'Exposition_Temporaire', 'Oeuvre_Louvre', 'Oeuvre_Ext', 'Emprunt', 'Pret','Prestataire', 'Restauration', 'Creneau', 'Guide', 'Creneau_Guide', 'Salle', 'Panneau']
    table_name= StringVar()
    table_name.set(list_table[0])
    Label(frame_top, text="Select Table: ", padx=10, font=ft_label).grid(row=0, column=0)
    table_current = OptionMenu(frame_top, table_name, *list_table, command=update_area)
    table_current.grid(row=0, column=1, padx=10)
        # Créer les widgets du centre
    frame_center.grid_rowconfigure(0, weight=1)
    frame_center.grid_columnconfigure(0, weight=1)
    center_left = Frame(frame_center, width=780, height=650, padx=10)
    center_left.grid(row=0, column=0, sticky="ns")
    center_right = Frame(frame_center, bg='orange', width=80, height=650)
    center_right.grid(row=0, column=1, sticky="ns")
        #  Créer des boutons
    center_right.grid_rowconfigure(0, weight=1)
    center_right.grid_columnconfigure(0, weight=1)
            # Bouton Insert
    button_insert = Button(center_right, text="Insert", width=10, fg="#0000CD", command=insert,font=ft_button)
    button_insert.pack(padx=5, pady=15)
            # Bouton Delete
    button_delete = Button(center_right, text="Delete", width=10, fg="#0000CD", command=delete,font=ft_button)
    button_delete.pack(padx=5, pady=15)
            # Bouton Update
    button_update = Button(center_right, text="Update", width=10, fg="#0000CD", command=update, font=ft_button)
    button_update.pack(padx=5, pady=15)
            # Bouton Accurate Search
    button_search = Button(center_right, text="Search(A)", width=10, fg="#0000CD", command=search_accurate, font=ft_button)
    button_search.pack(padx=5, pady=15)
            # Bouton Fuzzy Search
    button_search = Button(center_right, text="Search(F)", width=10, fg="#0000CD", command=search_fuzzy, font=ft_button)
    button_search.pack(padx=5, pady=15)
            # Bouton Clear
    button_exit = Button(center_right, text="Clear", width=10, fg="#0000CD", command=clear, font=ft_button)
    button_exit.pack(padx=5, pady=15)
            # Bouton Clear
    button_exit = Button(center_right, text="Show all", width=10, fg="#0000CD", command=requst_db_all, font=ft_button)
    button_exit.pack(padx=5, pady=15)
        # Créer une zone de saisie(Input area)
    center_left.grid_rowconfigure(1, weight=1)
    center_left.grid_columnconfigure(0, weight=1)
            # Définir l'étiquette de la zone de saisie
    label_input = Frame(center_left, width=780, height=25)
    label_input.grid(row=0)
    Label(label_input, text="Information Area", font=ft_label).grid(row=0)
            # Définir la zone de saisie
    frame_input = Frame(center_left, width=780, height=450, pady=5, highlightbackground="black", highlightthickness=1)
    frame_input.grid(row=1)
    frame_input.grid_rowconfigure(0, weight=1)
    frame_input.grid_columnconfigure(0, weight=1)
            # Définir l'étiquette de la zone de résulta
    label_result = Frame(center_left, width=780, height=25)
    label_result.grid(row=2)
    Label(label_result, text="Result Area", font=ft_label).grid(row=0)
        # Ajouter une étiquette d'entrée et une boîte d'entrée
    for i, column in enumerate(Musee_Exterieur.columns):
        label_name = Label(frame_input, text=column, pady=5, width=25, borderwidth=2, relief="groove")
        label_name.grid(row=i, column=0)
        input_name = Entry(frame_input, width=80)
        input_name.grid(row=i, column=1)
    # Créer une vue d'affichage des résultats
    tree_view = create_view(App, Musee_Exterieur)
    # Lancer l'application
    App.mainloop()
    # ========================Interface  Système END========================
except Exception as e:
    print((FAIL + "{}"  + ENDC).format(e))
    exit()
finally:
    print(OKGREEN + "Déconnexton avec la base de données" + ENDC)
    conn.close()
    # ========================Connection à la base de données END========================
# ========================Bloc4 - END========================