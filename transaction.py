#!/usr/bin/env python
import requests
import re,signal,sys,time,argparse, uuid, datetime, json, pprint
list_currency = ['EUR','USD',"HRK","HUF","IDR",
"PHP","TRY","RON","ISK","SEK","THB","PLN",
"GBP","CAD","AUD","MYR","NZD","CHF","DKK",
"SGD","CNY","BGN","CZK","BRL","JPY","KRW",
"INR","MXN","RUB","HKD","ZAR","ILS","NOK" ]

### Class Transaction // amount, date, and a short description
class Transaction(object):
    def __init__(self,*args): 
                self.amount = args[0]
                self.currency_code = args[1]
                self.date = args[2]
                self.desc = args[3]

    @property
    def amount(self):
        return self.__amount
    @amount.setter
    def amount(self,value):
        if not isinstance(value,float):
            try :
                value = float(value)
            except Exception as e :
                raise TypeError('choose a valid amount')
        self.__amount = value
    
    @property
    def currency_code (self):
        return self.__currency_code 
    @currency_code .setter
    def currency_code (self,value):
        if not isinstance(value,str) :
            raise TypeError('muste be a real currency')
        self.__currency_code  = value

    @property
    def date (self):
        return self.__date
    @date.setter
    def date(self,value):
        if not isinstance(value,str):
            raise TypeError('unvalid dateTime')
        self.__date = value

    @property
    def desc(self):
        return self.__desc
    @desc.setter
    def desc(self,value):
        if not isinstance(value,str):
            try :
                value = str(value)
            except Exception as e:
                raise TypeError('invalid description')
        self.__desc = value

    ## Methode ##

    ## Methode qui retourne le str d'une Transaction 
    def __str__(self):
        return '  Amount :' + str(self.amount) + self.currency_code  + '              \n  Date : ' + str(self.date) + '\n  Description : ' + str(self.desc)

### Fin classe Transaction ###

### Classe Transfer : Herite de la classe Transaction

class Transfer(Transaction):  
    def __init__(self,acc1,acc2,*args):
        super(Transfer,self).__init__(*args)
        self.transmitter= acc1
        self.receiver = acc2 

    @property
    def transmitter(self):
        return self.__transmitter
    @transmitter.setter
    def transmitter(self,value):
        if not isinstance(value,Account)and value is not None:
            raise TypeError('muste be an account') 
        self.__transmitter = value

    @property
    def receiver(self):
        return self.__receiver
    @receiver.setter
    def receiver(self,value):
        if not isinstance(value,Account) and value is not None:
            raise TypeError('muste be an account')
        self.__receiver = value

    def serializeMe(self) :
        return {'__class__': 'Transfer','amount': self.amount,'currency_code':self.currency_code,'date':str(self.date),'desc':self.desc }

### Fin Classe Transfer ###

### Classe Expense Herite de la classe Transaction ###

class Expense(Transaction):
    def __init__(self,*args):
        super(Expense,self).__init__(*args)

    def serializeMe(self) :
        return {'__class__': 'Expense','amount': self.amount,'currency_code':self.currency_code,'date':str(self.date),'desc':self.desc }

### Fin Classe Expense ###

### Classe Income : herite de la classe Transaction ###

class Income(Transaction):
    def __init__(self,*args):
        super(Income,self).__init__(*args)

    def serializeMe(self) :
        return {'__class__': 'Income','amount': self.amount,'currency_code':self.currency_code,'date':str(self.date),'desc':self.desc }
### Fin class Income 

### Class Account ###

class Account(object):
    def __init__(self,*args):
        self.owner_id = args[0]
        self.libelle = args[1]
        self.solde = args[2]
        self.currency=args[3]
        self.id_account = uuid.uuid4()
        self.ledger = []
        self.history = 0
        self.path = self.libelle + '.json'


    @property
    def owner_id (self):
        return self.__owner_id
    @owner_id.setter
    def owner_id(self,value):
        if not isinstance(value,str) and value is not None:
            try:
                value=str(value)
            except Exception as e :
                raise TypeError('Unknow owner_id')
        self.__owner_id= value

    @property
    def libelle (self): 
        return self.__libelle
    @libelle.setter
    def libelle(self,value):
        if not isinstance(value,str):
            try :
                value = str(value)
            except Exception as e :
                raise TypeError('Unknow libelle')
        self.__libelle = value 

    @property
    def solde(self):
        return self.__solde
    @solde.setter
    def solde(self,value):
        if not isinstance(value,float) and value is not None:
            try :
                value= float(value)
            except Exception as e :
                raise TypeError('invalid solde')
        self.__solde = value

    @property
    def currency(self):
        return self.__currency
    @currency.setter
    def currency(self,value):
        if not isinstance(value,str) :
            raise TypeError('choose a real currency')
        else :
            self.__currency= value
    
    @property
    def id_account(self):
        return self.__id_account
    @id_account.setter
    def id_account(self,value):
        self.__id_account=value

    @property
    def ledger(self):
        return self.__ledger
    @ledger.setter
    def ledger(self,value):
        self.__ledger = value 

    @property
    def history(self):
        return self.__history
    @history.setter
    def history(self,value):
        self.__history = value 

    @property
    def path(self):
        return self.__path
    @path.setter
    def path(self,value):
        if not isinstance(value,str):
            try: 
                value = str(value)
            except Exception as e : 
                print('error')
        self.__path = value 



    ## Methode

    # Methode qui retourne le taux de convertion d'une devise à l autre 
    def getDailyRate(self,base, target):
        # https://api.exchangeratesapi.io/latest?symbols
        href ="https://api.exchangeratesapi.io/latest?symbols="+target+"&base="+base
        r = requests.get(href).json() # on recuperer un dico 
        return r['rates'][target]

    # Methode qui verifie qu'une currency exist 
    def checkCurrency(self,currency): 
        for code in list_currency : 
                if code == currency :
                        return True 
        return False 

    # Methode qui retourne le boolean de la comparaison de 2 Account 
    def __eq__(self,other):
        if not isinstance(other,Account):
            raise TypeError('can only comparate 2 account')
        else :
            if self.id_account==other.id_account :
                return True
            else :
                return False
    
    #Methode qui retourn le str d'un Account 
    def __str__(self):
        return 'id :' + str(self.id_account) +'\n owner_id : ' + str(self.owner_id) + '\n solde : ' + str(self.solde)
    
    #methode qui serialize un account / retourne un dictionnaire 
    def serializeMe(self):
        return {'__class__': 'Account', 'owner_id': self.owner_id,'libelle':self.libelle,'solde':self.solde ,'currency' :self.currency,'id_account':str(self.id_account),'history':self.history} 
  
    # Methode qui retourne la transaction créer
    def createTransaction(self,nature,user):
        date = str(datetime.datetime.now())
        desc = input('    - DESCRIPTION : ')
        amount = input('    - AMOUNT : ' )
        while not isinstance(amount,float):
            try :
                 amount = float(amount)
            except Exception as e :
                print(' Amount must be a valid float ')
                amount = input('Select new Amount : ')
        if nature == 'expense' :
            # create currency
            currency = input('    - CURRENCY CODE : ')
            while(self.checkCurrency(currency) != True):
                currency = input('    - ENTER A VALID CURRENCY CODE : ')
            rate = self.getDailyRate(self.currency,currency)
            print(amount,self.currency + ' = ',amount*rate,currency)
            transaction = Expense(amount * rate ,currency,date,desc)
            return transaction
         
        elif nature =='income':
            transaction = Income(amount,'EUR',date,desc)
            return transaction
           
        elif nature =='transfer':
            #acc = user.getAccount()
            print('\n---- SELECT THE ACCOUNT YOU WANT TO TRANSFER MONEY TO ----')
            to_acc = user.getAccount()
            while to_acc.id_account ==self.id_account:
                print(" You must choose a different account ")
                to_acc = user.getAccount()
            if to_acc.currency != self.currency : 
                rate = self.getDailyRate(self.currency,to_acc.currency)
                print(" The Account you transfer money to use",to_acc.currency," The dalay rate is ", rate,to_acc.currency )
                print(amount,self.currency + ' = ', amount * rate ,to_acc.currency)
            transaction = Transfer(self,to_acc,amount*rate,to_acc.currency,date,desc)
            # on rajoute le transfere à l'autre compte 
            desc_income= 'Transfer from account n°' + to_acc.id_account
            inc = Income(amount,'Eur',date,desc_income)
            to_acc.solde += amount 
            to_acc.addTransaction(inc)
            return transaction
        else : 
            return None 

    # Methode qui retourne le boolean de la sauvegarde de la transaction dans le ledger 
    def addTransaction(self,transaction):
        if not isinstance(transaction,Transaction):
            print('Must be a valid transaction')
            return False 
        else :
            self.ledger.append(transaction)
            self.history +=1 
            return True 

    # Methode qui retourne le boolean de l'execution la transaction 
    def runTransaction(self,user,transaction):
        if not isinstance(transaction,Transaction):
            print('Must be a valid transaction')
            return False
        else :
            if isinstance(transaction,Expense) :
                self.solde-= transaction.amount
            elif isinstance(transaction,Income) :
                self.solde+= transaction.amount
            elif isinstance(transaction,Transfer):     
                for acc in user._tabAccount:
                    if acc == transaction.receiver :
                       
                        self.solde-=transaction.amount
                        acc.solde+= transaction.amount
                        acc.ledger.append(transaction)
                        
            else :
                return False
        return True  
    
    # Methode qui gere tout le management de la transaction / celle qu'on utilise dans notre programe 
    def manageTransaction(self,nature,user):
        t =  self.createTransaction(nature,user)
        if(self.runTransaction(user,t)):
            if (self.addTransaction(t)):
                self.history += 1
                print(nature + ' done and add to your history ') 
            else:
                print(nature + ' done but not in your history ')
        else: 
            print(nature + ' didn t work')

    # Methode qui affiche le Ledger dans la console 
    def printLedger(self):
        cmp_exp = 1
        cmp_inc =1
        cmp_tra = 1 
        print(" _______________________________________" )
        print('         History of  the Account   ')
        for transaction in self.ledger :
            if isinstance(transaction,Expense):
                print('  Expense n° ',str(cmp_exp),' :')
                cmp_exp +=1
            if isinstance(transaction,Income):
                print('  Income n° ',str(cmp_inc),' :')
                cmp_inc +=1
            if isinstance(transaction,Transfer):
                print('  Transfer n° ',str(cmp_tra),' :')
                cmp_tra +=1
            print(str(transaction),'\n')
        print(" ______________________________________" )
                                                                     

### fin class Account  ###
