import requests
import tkinter as tk
from tkinter import ttk, Label, Button, Entry, messagebox
import re

#local
#from frames import CreateAccount
#from frames import Login
#from new_gui import main

BASE = "http://127.0.0.1:5000/"

#response = requests.get(BASE + "login")
#print(response.json())

#response = requests.post(BASE + "login", {'username':'neil', 'password':'password'})
#print(response.json())



class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        
        self.geometry('720x720')
  
        # initializing frames to an empty array
        self.frames = {} 
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Login, CreateAccount, SubmitData):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(Login)
  
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Login(tk.Frame):

    global token_value

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        #self.pageElemets(controller)

        login_label = Label(self, text="Login")
        login_label.grid(column=1, row=0)

        username_title = Label(self, text="Username:")
        username_title.grid(column=0, row=1)

        username_box = Entry(self, width=20)
        username_box.grid(column=1,row=1)

        password_title = Label(self, text="Password:")
        password_title.grid(column=0, row=2)

        password_box = Entry(self, show="*", width=20)
        password_box.grid(column=1, row=2)

    #needs username_box password_box token_text controller

        #token box
        token_label = Label(self, text="Token: ")
        token_label.grid(column=0, row=5)

        #this is the text we change for the token
        token_text = Label(self, text="No Token")
        token_text.grid(column=1, row=5)


        #user id
        user_id_label = Label(self, text="User ID: ")
        user_id_label.grid(column=0, row=6)
        user_id_text = Label(self, text="No Token")
        user_id_text.grid(column=1, row=6)


        def login_clicked():
            username = username_box.get()
            password = password_box.get()

            #get token
            response = requests.post(BASE + "login", {'username':username, 'password':password})
            print(response.json())
            token_text.configure(text=response.json())
            
            token_value = response.json()

            #get userID with token
            response2 = requests.post(BASE + "user", {'token':token_value,})
            print(response2.json())
            user_id_text.configure(text=response2.json())
            
            user_id = response2.json()
            print("User ID: " + str(user_id[0]))

            #this is fucking stupid
            #WE SHOULD NOT BE DOING THIS
            f = open("token.txt", "w")
            f.write(token_value)

            u = open("userid.txt", "w")
            u.write(str(user_id[0]))

            print("TOKEN VALUE: " + str(token_value))


            controller.show_frame(SubmitData)
            #self.state(newstate='iconic')
            #main()

        login_button = Button(self, text="Login", command= login_clicked)
        login_button.grid(column=1, row=3)

        login_create_account_button = Button(self, text="Create Account", command= lambda : controller.show_frame(CreateAccount))
        login_create_account_button.grid(column=1, row=4)

    

# second window frame page1
class CreateAccount(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        create_account_label = Label(self, text="Create Account")
        create_account_label.grid(column=1, row=0)

        #username
        username_title = Label(self, text="Username:")
        username_title.grid(column=0, row=1)

        username_box = Entry(self, width=20)
        username_box.grid(column=1,row=1)

        #email
        email_label = Label(self, text="Email:")
        email_label.grid(column=0, row=2)

        email_box = Entry(self, width=20)
        email_box.grid(column=1,row=2)

        #confirm email
        confirm_email_label = Label(self, text="Confirm Email:")
        confirm_email_label.grid(column=0, row=3)

        confirm_email_box = Entry(self, width=20)
        confirm_email_box.grid(column=1,row=3)

        #password
        password_title = Label(self, text="Password:")
        password_title.grid(column=0, row=4)

        password_box = Entry(self, show="*",width=20)
        password_box.grid(column=1, row=4)

        #confirm password
        confirm_password_title = Label(self, text="Confirm Password:")
        confirm_password_title.grid(column=0, row=5)

        confirm_password_box = Entry(self, show="*", width=20)
        confirm_password_box.grid(column=1, row=5)

        #create account checks
        def check_creds():
            username = username_box.get()
            password = password_box.get()
            confirm_password = confirm_password_box.get()
            email = email_box.get()
            confirm_email = confirm_email_box.get()

            #check username length and valid characters
            if len(username) < 4:
                    messagebox.showerror('Error', 'Error: Username is too short!')
            else:
                #check if emails match
                if str(email) != str(confirm_email):
                    messagebox.showerror('Error', 'Error: Emails do not match!')
                else:
                    #check if passwords match
                    if str(password) != str(confirm_password):
                        messagebox.showerror('Error', 'Error: Passwords do not match!')
                    else:
                        #check if valid email address
                        email_pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
                        if email_pattern.match(email) == None:
                            messagebox.showerror('Error', 'Error: Invalid email!')
                        #create account
                        else:
                            response = requests.post(BASE + "createaccount", {'username':username, 'email':email,'confirm_email':confirm_email, 'password':password, 'confirm_password':confirm_password})
                            print(response.json())
                            if response.json() == "Success. Please Login.":
                                #success
                                messagebox.showinfo(title="Info", message=response.json())
                                #go to login page
                                controller.show_frame(Login)
                            else:
                                messagebox.showerror(title="Error", message=response.json())


        #create account button
        create_account_button = Button(self, text="Create Account", command= check_creds)
        create_account_button.grid(column=1, row=6)

# third window frame page2
class SubmitData(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #this is fucking stupid
        #this is incredibly BAD
        f = open("token.txt", "r")
        token_value = f.read()

        #get the user id
        u = open("userid.txt", "r")
        user_id_value = u.read()

        token_text = Label(self, text=f"Entering data with token: {token_value}")
        token_text.grid(column=1, row=0)

        user_id_text = Label(self, text=f"Entering data with user id: {user_id_value}")
        user_id_text.grid(column=1, row=2)


# Driver Code
if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()