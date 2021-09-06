#Write a GUI application to manage a phone book using the classes Contact and
#PhoneBook in seminar 2.ppt, reproduced here:

from tkinter import *
from tkinter.scrolledtext import *

class Contact:
    '''Contact class for getter, setter name and phone'''
    def __init__(self, name, phone):
        self._name = name
        self._phone = phone
        
    @property
    def name(self):
        return self._name
    
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, phone):
        self._phone = phone
        
    def __str__(self):
        return 'Name: {} Phone: {}'.format(self._name, self._phone)


class PhoneBook:
    '''Phone class to search, add, remove the contact into list'''  
    def __init__(self, name):
        self._name = name
        self._contacts = []
        
    def addContact(self, contact):
        self._contacts.append(contact)
        
    def searchContact(self, name):
        for c in self._contacts:
            if c.name == name: return c
        return None
    
    def removeContact(self, name):
        c = self.searchContact(name)
        if c is None: return False
        self._contacts.remove(c)
        return True
    
    def updateContact(self, name, phone):
        c = self.searchContact(name)
        if c is None: return False
        c.phone = phone
        return True
    
    def __str__(self):
        contacts = [str(c) for c in self._contacts]
        contacts.sort()
        return 'Phone Book Owner Name: {}\n{}' .format(self._name, '\n'.join(contacts))
    

''''GUI CLASS START FROM LINE 59'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''        
class DemoGUI:
    def __init__(self, title):
        self._myFriends = PhoneBook('Jim')
        self._myFriends.addContact(Contact('Peter', 9123123))
        self._myFriends.addContact(Contact('Joe', 8123123))
        self._myFriends.addContact(Contact('Amy', 6123231))
        
        self._tk = Tk()
        self._tk.title(title)
        self._tk.resizable(False, False)
        self._tk.geometry('600x250') 
        self.initWidgets()
        self._tk.mainloop()
        
    def initWidgets(self):
        '''Arrange the label and text components for name, phone in one frame'''
        lblTxtFrame = Frame(self._tk)
        self._lblName = Label(lblTxtFrame, text = "Name:")
        self._txtName = Entry(lblTxtFrame, width = 20)
        self._lblPhone = Label(lblTxtFrame, text = "Phone:")
        self._txtPhone = Entry(lblTxtFrame, width = 20)
        self._lblName.grid(row =0, column =1, pady=3)
        self._txtName.grid(row =0, column =2)
        self._lblPhone.grid(row =1, column =1)
        self._txtPhone.grid(row =1, column =2) 
        
        '''Arrange the button components in one frame'''
        btnFrame = Frame(self._tk)
        self._btnSearch = Button(btnFrame, text = "Search", width = 10, command= self.btnSearchClick)
        self._btnUpdate = Button(btnFrame, text = "Update", width = 10, command = self.btnUpdateClick)
        self._btnRemove = Button(btnFrame, text = "Remove", width = 10, command = self.btnRemoveClick)
        self._btnAdd = Button(btnFrame, text = "Add", width = 10, command = self.btnAddClick)
        self._btnShow = Button(btnFrame, text = "Show", width = 10, command = self.btnShowClick)
        self._btnClean = Button(btnFrame, text = "Clean", width = 10, command = self.btnCleanClick)
        self._btnSearch.grid(row =0, column =0)
        self._btnUpdate.grid(row =0, column =1)
        self._btnRemove.grid(row =0, column =2)
        self._btnAdd.grid(row =0, column =3)
        self._btnShow.grid(row =0, column =4)
        self._btnClean.grid(row =0, column =5)
         
        '''Declare output components'''
        self._sclOutput = ScrolledText(self._tk, width = 70, height = 9, state = DISABLED)
        
        '''Arrange the position of lblTxtFrame, btnFrame, outputFrame at main frame''' 
        lblTxtFrame.grid(row = 0, column = 0, pady=5)
        btnFrame.grid(row = 1, column = 0, padx = 25)
        self._sclOutput.grid(row =2, column= 0, columnspan = 2, pady = 5, padx = 5)
        
    
    def setText(self, txt):
        self._sclOutput.config(state = NORMAL) 
        self._sclOutput.insert('end', txt +'\n')
        self._sclOutput.config(state = DISABLED)    
    
    def btnSearchClick(self):
        nameInput = self._txtName.get()
        phoneInput = self._txtPhone.get()
        if self._myFriends.searchContact(nameInput):
            self.setText("Retrieved: " + str(self._myFriends.searchContact(nameInput)))
        else:
            self.setText(f"No entry for {nameInput}")
                    
    def btnUpdateClick(self):
        nameInput = self._txtName.get()
        phoneInput = self._txtPhone.get()
        if self._myFriends.updateContact(nameInput, phoneInput):
            self.setText("Updated: " + str(self._myFriends.searchContact(nameInput)) + '\n' + str(self._myFriends))
        else:
            self.setText(f"No entry for {nameInput}")    
    
    def btnRemoveClick(self):
        nameInput = self._txtName.get()
        phoneInput = self._txtPhone.get()
        if self._myFriends.searchContact(nameInput):
            self.setText("Remove: " + str(self._myFriends.searchContact(nameInput)))
            if self._myFriends.removeContact(nameInput):
                self.setText(str(self._myFriends))     
        else:
            self.setText(f"No entry for {nameInput}")       
    
    def btnAddClick(self):
        nameInput = self._txtName.get()
        phoneInput = self._txtPhone.get()
        if self._myFriends.searchContact(nameInput) is None:
            c = Contact(nameInput, phoneInput)
            self._myFriends.addContact(c)
            self.setText("Added: " + str(self._myFriends.searchContact(nameInput)) + '\n' + str(self._myFriends))
        else:
            self.setText(f"Existing entry for {nameInput}") 
            
    def btnShowClick(self):
        nameInput = self._txtName.get()
        phoneInput = self._txtPhone.get()
        if self._myFriends.searchContact(nameInput):
            self.setText(str(self._myFriends))
        else:
            self.setText(f"No entry for name: {nameInput} with phone:{phoneInput}")
    
    def btnCleanClick(self):
        '''clear the txt entry'''
        self._txtName.delete(0,END)
        self._txtPhone.delete(0,END)
        
        '''clear the scroll ouput entry'''
        self._sclOutput.config(state = NORMAL) 
        self._sclOutput.delete(1.0,END)
        self._sclOutput.config(state = DISABLED)  
        
        
def main():
    
    DemoGUI("Phone Book Management System")
main()  
