#!/usr/bin/env python
import re,signal,sys,time,argparse, uuid, datetime, json, pprint 
from transaction import Transaction, Expense, Income, Transfer , Account 
from user import User 

def void () :
    print("the aim of the projet is to make a small account management")
    return

def serialize_account(acc):
    if isinstance(acc, Account):
        return acc.serializeMe()
    raise TypeError(repr(acc) + " n'est pas sérialisable !")

def serialize_user(user):
    if isinstance(user, User):
        return user.serializeMe()
    raise TypeError(repr(user) + " n'est pas sérialisable !")

def serialize_obj(obj):
    if isinstance(obj, User):
        return obj.serializeMe()
    if isinstance(obj, Account):
        return obj.serializeMe()
    if isinstance(obj,Transaction):
        return obj.serializeMe()
    raise TypeError(repr(obj) + " n'est pas sérialisable !")
    
def deserialize_account(obj_dict):
    if "__class__" in obj_dict:
        if obj_dict["__class__"] == "Account":
            acc= Account(obj_dict["owner_id"],obj_dict["libelle"],obj_dict["solde"],obj_dict["currency"])
            acc.id_account= obj_dict["id_account"]
            acc.history = obj_dict["history"]
            return acc 
               
def deserialize_obj(obj_dict):
    if "__class__" in obj_dict:
        if obj_dict["__class__"] == "User":
            user = User(obj_dict["name"],obj_dict["lastname"])
            user.id=obj_dict["id"]
            return user 
    if "__class__" in obj_dict:
        if obj_dict["__class__"] == "Account":
            acc= Account(obj_dict["owner_id"],obj_dict["libelle"],obj_dict["solde"],obj_dict["currency"])
            acc.id_account= obj_dict["id_account"]
            return acc 

def deserialize_transaction(obj_dict):
    print("ici")
    if "__class__" in obj_dict:
        if obj_dict["__class__"] == "Transfer":
            print('Transfer')
            transfer = Transfer(None,None,obj_dict["amount"],obj_dict["currency_code"],obj_dict["date"],obj_dict["desc"])
            return transfer 
        if obj_dict["__class__"] == "Expense":
            print('Expense')
            expense = Expense(obj_dict["amount"],obj_dict["currency_code"],obj_dict["date"],obj_dict["desc"])
            return expense 
        if obj_dict["__class__"] == "Income":
            print('Income')
            income = Income(obj_dict["amount"],obj_dict["currency_code"],obj_dict["date"],obj_dict["desc"])
            return income 
  
def write_inJson(filename,list_obj,serialize_methode):
     with open(filename, "w", encoding="utf-8") as fichier:
        json.dump(list_obj, fichier, default=serialize_methode)
        
def read_Json(filename,deserialize_methode):
    with open(filename, "r", encoding="utf-8") as fichier:
        list_obj = json.load(fichier, object_hook=deserialize_methode)
        return list_obj

def initial():
    lucile = User("Lucile","Jeanneret")
    compte1_lucile = Account(str(lucile.id),"compte1_lucile",15000,'EUR')
    income = Income(100,'EUR','18/12/2018','test')
    income2 = Income(300,'EUR','18/12/2018','test')
    compte1_lucile.ledger.append(income)
    compte1_lucile.ledger.append(income2)
    compte1_lucile.history = 2 
    compte1_lucile.printLedger()
    compte2_lucile = Account(str(lucile.id),"compte2_lucile",25000,'USD')
    lucile.addAccount(compte1_lucile)
    lucile.addAccount(compte2_lucile)
    
    melanie = User("Melanie","Jeanneret")
    compte1_melanie = Account(str(melanie.id),"compte1_melanie",25000,'EUR')
    melanie.addAccount(compte1_melanie)

    registre_user = []
    registre_user.append(lucile)
    registre_user.append(melanie)

    registre_acc=[]
    registre_acc.append(compte1_lucile)
    registre_acc.append(compte2_lucile)
    registre_acc.append(compte1_melanie) 
    write_inJson('data/users.json',registre_user,serialize_user)
    write_inJson('data/account.json',registre_acc,serialize_account)

# Main #
def mainMenu():
    list_obj = read_Json("data/users.json",deserialize_obj)
    list_acc2 = read_Json("data/account.json",deserialize_account)
    
    for usr in list_obj : 
        if isinstance(usr, User) :
            for acc in list_acc2 :
                if isinstance(acc,Account): 
                    if usr.id == acc.owner_id:
                        usr._tabAccount.append(acc)
                        
    user  = menu_user(list_obj)                      
    user = menu_acc(user)
    nv_list_acc = []
    for usr in list_obj : 
        if isinstance(usr, User) :
            if usr.id == user.id:
                usr._tabAccount = user._tabAccount
            for acc in usr._tabAccount: 
                 nv_list_acc.append(acc)

    write_inJson('data/users.json',list_obj,serialize_user)
    write_inJson('data/account.json',nv_list_acc,serialize_account)
 
# Le menu qui gere la partie user 
def menu_user(user_list) :
    print("Welcome to you Bank Account Management \n What do you want to do ? ")
    choice= input ("    1) Log in\n    2) Create your space  \n ") 
    while not isinstance(choice,int):
        try :
            choice =int(choice)
        except Exception as e :
            print(" Choice must be 1 or 2 !  ")
            choice = input("Select new choice : ")
    if choice == 1 : #login  by id 
        found = False 
        n_id = input("Please enter your id : ")
        for n_user in user_list : 
            if isinstance(n_user,User):
                print(str(n_user.id))
                if str(n_user.id)== n_id :
                    found = True 
                    return n_user # on retourne l'user pour se connecter
        if found == False : 
            print("Wrong ID")
            menu_user(user_list)
    elif choice == 2   :  #create user 
        print("Create")
        name = input ( "Please enter your name : " )
        lastname = input ("Please enter your lastname :")
        user = User(name,lastname)
        print(" This is your personal ID keep it in order to login \n ID : "+str( user.id))
        user_list.append(user) # on ajoute le nvx user à la liste 
        write_inJson("data/users.json",user_list,serialize_user) # on maj le fichier user json 
        return user # on retourne l'user pour se connecter 
    return None 

# le menu qui gere les account d'un user      
def menu_acc(user):
    if not isinstance(user,User):
        print("error")
    else  : 
        print(" _______________________________________________________________________________ ")
        print( "\n        Welcome " , user.name, user.lastname)
        print(" you have "+str(user.getTotalAccount()) + " account : ")
        print("\n") 
        choose_acount = True  
        while(choose_acount):
            print(" 1. CHOOSE AN ACCOUNT ") 
            print(" 2. CREATE AN ACCOUNT")

            choice1 = input("\nEnter a choice : ")
            while not isinstance(choice1,int):   
                try :
                    choice1 =int(choice1)
                except Exception as e :
                    print(" Choice must be 1 or 2 !  ")
                    choice1 = input("Select new choice : ")  
            
            # Choix du compte 
            if user.getTotalAccount() == 0  or choice1 == 2 : 
                print("Create a new account ")
                acc = user.createAccount()      
            elif choice1 == 1  : 
                print("Choose an account ")
                print(str(user))
                acc = user.getAccount() 
                if not isinstance(acc,Account):
                    acc =user.getAccount()
            else :
                choice1 = input("Enter a choice : ")
            # on verifie l'historic 
            choose_action = True 
            print(acc.history)
            if acc.history >0 : 
                tab_ledger = read_Json(acc.path,deserialize_transaction)
                acc.ledger = tab_ledger
            while(choose_action):
                print(" What do you want to do ")
                print("\n    1) CHECK AN ACCOUNT HISTORY \n    2) TRANSFER\n    3) EXPENSE\n    4) INCOME\n    5) RETURN\n    6) QUIT \n") 
                choice= input("Made a choice : ")
                while not isinstance(choice,int):
                    try :
                        choice =int(choice)
                    except Exception as e : 
                        print(" Choice must be between 1 and 5  ")
                        choice = input("Select new choice : ")
                if choice == 1 :
                    print("--------------- ACCOUNT HISTORY ---------------------") 
                    acc.printLedger()
                    print("     Do you want to save your history in json ?")
                    choice2=input( "    1. Yes \n    2. No \n") 
                    try : 
                        choice2=int(choice2)
                    except Exception as e :
                        choice2 = input("    1. Yes \n    2. No \n")
                    if choice2 == 1 :
                        print("save")
                        write_inJson(acc.path,acc.ledger,serialize_obj)
                    elif choice2 == 2 : 
                        print("don't save")
                    else : 
                        print("ici")
                if choice == 2 : 
                    print("                MADE A TRANSFER BETWEEN ACCOUNT     ")
                    if len(user._tabAccount) < 2:
                        print("You need to have minimum 2 acounts ")
                    else :
                        acc.manageTransaction('transfer',user)
                if choice == 3 : 
                    print("                MADE A EXPENSE FROM AN ACCOUNT     ")
                    acc.manageTransaction('expense',user)
                if choice == 4 : 
                    print("                MADE AN ICOME TO AN ACCOUNT     ")
                    acc.manageTransaction('income',user)
                if choice == 5 : 
                    write_inJson(acc.path,acc.ledger,serialize_obj)
                    for account in user._tabAccount :
                        if account.id_account == acc.id_account :
                            account = acc 
                    choose_action = False 
                if choice == 6 : 
                    write_inJson(acc.path,acc.ledger,serialize_obj)
                    for account in user._tabAccount :
                        if account.id_account == acc.id_account :
                            account = acc 
                    choose_action = False 
                    choose_acount = False 

    # on sauvegarde les modification 
    for acc in user._tabAccount :
        if isinstance(acc,Account):
            write_inJson(acc.libelle+'.json',acc.ledger,serialize_obj)
    
    return user


mainMenu()    

