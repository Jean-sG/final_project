 #!/usr/bin/env python
import re,signal,sys,time,argparse, uuid, datetime, json, pprint 
from transaction import Transaction, Expense, Income, Transfer , Account 
list_currency = ['EUR','USD',"HRK","HUF","IDR",
"PHP","TRY","RON","ISK","SEK","THB","PLN",
"GBP","CAD","AUD","MYR","NZD","CHF","DKK",
"SGD","CNY","BGN","CZK","BRL","JPY","KRW",
"INR","MXN","RUB","HKD","ZAR","ILS","NOK" ]

## Class User ##

class User(object):
    def __init__(self,*args):
        if len(args)==2 :
            self.name = args[0]
            self.lastname = args[1]
            self.id = uuid.uuid4()
            self._tabAccount= [] # un user peut avoir 1 ou plusieurs compte

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,value) :
        if not isinstance(value,str):
            try :
                value = str(value)
                #faire une verif sur le format ( 1er lettre en maj pas de caractere speciaux )
            except Exception as e :
                raise TypeError( 'must be a valid string ')
        self.__name = value

    @property
    def lastname(self):
        return self.__lastname
    @lastname.setter
    def lastname(self,value) :
        if not isinstance(value,str):
            try :
                value = str(value)
                #faire une verif sur le format ( 1er lettre en maj pas de caractere speciaux )
            except Exception as e :
                raise TypeError( 'must be a valid string ')
        self.__lastname = value

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,value):
        self.__id=value


    ###  Methode ###
    #methode qui ajoute un Account à la liste d'Account du User
    def addAccount(self,n) :
        if not isinstance(n,Account):
            return False #si erreur
        else :
            self._tabAccount.append(n)
            return True  # si ok

    #methode qui supprime un Account à la liste d'Account du User
    def deleteAccount(self,n):
        if not isinstance(n,Account):
            return False
        else :
            # cherche
            for i in self._tabAccount :
                if i == n :
                    #del(i)
                    return  True
        return False

    #methode qui creer un nv Account 
    def createAccount(self):
        owner_id = self.id
        libelle  = self.name + ' ' + self.lastname
        solde    = 0
        res = ' List of currency : '
        print("Choose the currency of your account :")
        for cur in list_currency : 
            res += cur + '  ' 
        print(res)
        currency = None 
        while currency == None : 
            currency_code= input("input a currency code : ")
            for cur in list_currency : 
                if cur == currency_code:
                    currency = cur 
        
        new_acc=Account(owner_id,libelle,solde,currency)
        if self.addAccount(new_acc) :
            print(" New account created ")
            return new_acc
        else : 
            print(" Error creating the new account ")

    #methode qui retourne la taille de la liste d'Account du User
    def getTotalAccount(self):
        return len(self._tabAccount)

    #methode qui retourne un Account choisi de la liste d'Account du User
    def getAccount(self):
        t = self.getTotalAccount()
        print ('    Enter an account number ')
        index=input ( '    - NUMBER : ')
        while not isinstance(index,int):
            try :
               index = int(index)
            except Exception as e :
               print ('    Enter a valid account number ')
               index = input('    NUMBER : ')
            if index > t:
                print("    Enter a valid account number ")
                index = input('    NUMBER : ')

        return self._tabAccount[index-1]

    #methode qui serialise un User en retournant un dieco 
    def serializeMe(self):
        return {'__class__': 'User', 'name': self.name, 'lastname' : self.lastname,'id':str(self.id)}

    #methode qui retourne un str de User      
    def __str__(self):
        l = self.getTotalAccount()
        res = '\n TOTAL OF ACCOUNT : ' + str(l) +'\n ----------------------- \n'
        n=1
        if l >0 :
            for i in self._tabAccount :
                res +='\n ACCOUNT '+ str(n) + ' :  ' + str(i.solde) +' ' + i.currency 
                n +=1
        return res

###  Fin class User  ###