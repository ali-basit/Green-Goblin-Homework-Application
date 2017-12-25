import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import account_types
import account
import question_type_select as instrWindow
import question_set_panel as studentWindow
from tkinter import *
from winsound import * # This breaks on any non-windows platform

class LoginWindow(tk.Frame):
    '''A class to represent a login window; toplevel window which contains UI for logging in as users.'''

    def __init__(self, master):
        '''(LoginWindow, Tk) -> NoneType
        Initialize a new login window with the given parameters.
        '''
        super(LoginWindow, self).__init__()      
        self.master = master
        self.parent = self.master
        # Initial mainframe in which we place all other frames into.
        self._mainframe = ttk.Frame(root, padding="3 3 3 3")
        self._mainframe.grid(column=0, row=4, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._mainframe.columnconfigure(100, weight=1)
        self._mainframe.rowconfigure(100, weight=1) 
        self.initUserLoginFrames()
        
        self._miscframe = ttk.Frame(root, padding="3 3 3 3")
        self._miscframe.grid(column=0, row=5, sticky=(tk.N, tk.W, tk.E, tk.S), columnspan=1)
        
        # for music
        play = lambda: PlaySound('sound/shrek_2_all_star_theme_song.wav', SND_FILENAME)
        button = ttk.Button(root, text = 'Play Green Goblin Theme Song', command = play)
        button.grid(row=5, column=0, sticky=(tk.E, tk.W), columnspan=2)

        # for logo
        logo_filepath = "graphics/green_goblin_symbol.gif"
        img = tk.PhotoImage(file = logo_filepath)
        logo = tk.Label(root, image=img)
        logo.photo = img
        logo.grid(row=1, column=0, rowspan=1, columnspan=1)

        
        # for title with image
        logo_filepath = "graphics/green-goblin-title.gif"
        img = tk.PhotoImage(file = logo_filepath)
        logo = tk.Label(root, image=img)
        logo.photo = img
        logo.grid(row=0, column=0, rowspan=1, columnspan=1)        
        
        # Button for exiting out (with fancy effect)
        fadebutton = tk.Button(root, text="Exit Application", command=self.fade_away)
        fadebutton.grid(row=6, column=0, sticky=(tk.E, tk.W), columnspan=3)

    # the function following is for the fade effect/button
    def fade_away(self):
        alpha = self.parent.attributes("-alpha")
        if alpha > 0:
            alpha -= .15
            self.parent.attributes("-alpha", alpha)
            self.after(100, self.fade_away)
        else:
            self.parent.destroy()         

    def initUserLoginFrames(self):
        '''(LoginWindow) -> NoneType
        Initialize the intro frame, as well as student and instructor login 
        frames.
        '''
        # Dict to store the frames.
        self._subframes = {}

        # Create all frames and store them in a dict so we can grab them when
        # we need them.
        self._subframes["intro"] = IntroFrame(self._mainframe, self)
        self._subframes["intro"].grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._subframes["loginStudent"] = LoginFrame(self._mainframe, self, account_types.Account_type.S)
        self._subframes["loginStudent"].grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self._subframes["loginInstructor"] = LoginFrame(self._mainframe, self, account_types.Account_type.I)
        self._subframes["loginInstructor"].grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        # This is the initially shown frame.
        self.showFrame("intro")

    def showFrame(self, frameName):
        '''(LoginWindow, str) -> NoneType
        Raises the frame mapping from the given name to top level visibility.
        '''
        frame = self._subframes[frameName];
        frame.tkraise()

    def returnToLogin(self, oldWindow):
        '''(LoginWindow, Frame) -> NoneType
        This is used by child classes to prompt a logout, then cleanup and
        return to this login screen.
        '''
        # Warn the user that they are logging out.
        if messagebox.askyesno("Logging Out", 
                               "Are you sure you want to log out?"):    
            oldWindow.destroy()
            self.master.deiconify()

class IntroFrame(tk.Frame):
    '''A class to represent an intro frame that asks users to specify what type of user they are logging in as.'''

    def __init__(self, parent, controller):
        '''(IntroFrame, parent, controller) -> NoneType
        Initialize a new intro frame with the given parameters.
        '''        
        tk.Frame.__init__(self, parent, relief='raised', borderwidth=10, background="green")
        self.controller = controller

        # Widget declaration.
        userSelectLabel = ttk.Label(self, text="Are you signing in as an Instructor or Student?", font=("Tahoma", 12), 
                                    background="green", foreground="white")
        logoLabel = ttk.Label(self, text="Green Goblins Software Solutions 2017 Ltd.", font=("Tahoma", 6), 
                              background="green", foreground="white")
        introSeparator = ttk.Separator(self, orient=tk.HORIZONTAL)
        studentLoginBtn = ttk.Button(self, text="Login as a Student", 
                                     command=lambda: self.controller.showFrame("loginStudent"))
        instrLoginBtn = ttk.Button(self, text="Login as an Instructor", 
                                   command=lambda: self.controller.showFrame("loginInstructor"))

        # Grid management for widgets.
        userSelectLabel.grid(row=2, column=0, sticky=(tk.N, tk.S), columnspan=2)
        introSeparator.grid(row=3, column=0, sticky=(tk.E, tk.W), columnspan=2)
        studentLoginBtn.grid(row=4, column=0, sticky=(tk.E, tk.W))
        instrLoginBtn.grid(row=4, column=1, sticky=(tk.E, tk.W))
        logoLabel.grid(row=5, column=0, columnspan=2)    

        # Global padding so widgets aren't too close.
        for child in self.winfo_children():
            child.grid_configure(padx=3, pady=9)        

class LoginFrame(tk.Frame):
    '''A class to represent a frame dynamically containing and redirecting users to correct windows based on login credentials and user type. 
    Also handles login verification logic.'''

    def __init__(self, parent, controller, userType):
        '''(LoginFrame, parent, controller, account_type Enum) -> NoneType
        Initialize a new login frame with the given parameters.
        '''
        tk.Frame.__init__(self, parent, relief='raised', borderwidth=10, background="green")
        self.controller = controller  
        self.username = tk.StringVar()
        password = tk.StringVar()
        
        # for input field colour change
        self.username.trace(mode="w", callback=self.command_user)
        password.trace(mode="w", callback=self.command_pass)

        #the above sets up a callback if the variable containing
        #the value of the entry gets updated
        
        # entry for username
        self.username_entry = Entry(self, textvariable = self.username)
        self.username_entry.grid(row=1, column=1, sticky=(tk.E, tk.W))
        # entry for password
        self.password_entry = Entry(self, textvariable = password)
        self.password_entry.grid(row=2, column=1, sticky=(tk.E, tk.W))

        # Shave off the 's' when we display the enum so it looks nicer.
        userTypeLabel = ttk.Label(self, text=(userType.value[:-1] + " Login"), font=("Tahoma", 14), background="green", foreground="white")
        namePromptLabel = ttk.Label(self, text="Username :", background="green", foreground="white")
        passPromptLabel = ttk.Label(self, text="Password :", background="green", foreground="white")
        
        # for checkbox show password feature
        self.checkCmd = IntVar()
        self.checkCmd.set(0)
        checkbox = Checkbutton(self, variable=self.checkCmd, onvalue=1, offvalue=0, 
                               text="Toggle Show Password", background="green", foreground="white", command=self.showPassword)
        checkbox.grid(row=2, column=2, sticky=(tk.E, tk.W))      

        # for hiding password upon entry
        self.password_entry.config(show="*")

        # Buttons which redirect to appropriate toplevels or frames.
        backBtn = ttk.Button(self, text="Return to Menu", command=lambda: self.controller.showFrame("intro"))
        loginBtn = ttk.Button(self, text="Login", command=lambda: self.try_login(self.username.get(),
                                                                                 password.get(),
                                                                                 userType))
        registBtn = ttk.Button(self, text="Register as New User",
                               command=lambda: self.try_register_account(self.username.get(),
                                                                         password.get(),
                                                                         userType))

        # Grid management.
        userTypeLabel.grid(row=0, column=0, sticky=(tk.E, tk.W), columnspan=2)
        namePromptLabel.grid(row=1, column=0, sticky=(tk.E))
        passPromptLabel.grid(row=2, column=0, sticky=(tk.E))
        backBtn.grid(row=3, column=0, sticky=(tk.E, tk.W))
        loginBtn.grid(row=3, column=1, sticky=(tk.E, tk.W))
        registBtn.grid(row=4, column=0, sticky=(tk.E, tk.W), columnspan=2)

        # More global padding.
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=5)
            
    # method for showing password feature
    def showPassword(self):
        if self.checkCmd.get() == 1:
            # for hiding password upon entry
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    # the below two methods are for the input field colour change feature
    def command_user(self, *args):
            try: #trys to update the background to the entry contents
                self.username_entry.config({"background": self.username_entry.get()})
            except: #if the above fails then it does the below
                self.username_entry.config({"background": "green", "foreground": "white"})

    def command_pass(self, *args):
            try: #trys to update the background to the entry contents
                self.password_entry.config({"background": self.password_entry.get()})
            except: #if the above fails then it does the below
                self.password_entry.config({"background": "green", "foreground": "white"})            
            
    def try_login(self, givenName, givenPass, userType):
        '''(LoginFrame, str, str, account_type Enum) -> NoneType
        Use given userType and given information currently in the username and
        password boxes and try to match a record.
        If they do, open the relevant user window. Otherwise, display a message
        box with explanation.
        '''
        potentialAccount = account.Account()
        # Check if account exists at all.
        if potentialAccount.readAccountInfo(givenName, userType):
            # Check if account credentials are valid.
            if potentialAccount.auth(givenPass):
                # Pass along the right user window to open.
                self.openUserWindow(userType)
            else:
                messagebox.showerror("Incorrect Password Combination", 
                                     "Invalid User/Password Combination")
        else:
            messagebox.showerror("No such account", 
                                 "Couldn't find an account with that username")

    def try_register_account(self, givenName, givenPass, userType):
        '''(LoginFrame, str, str, account_type Enum) -> NoneType
        Try to write out a new account with the given information.
        Display a messagebox describing whether writing succeeded.
        '''
        accountOut = account.Account(givenName, givenPass, userType)
        if accountOut.writeAccountInfo():
            messagebox.showinfo("Created new account", 
                                "New account registered\nYou may now log in")
        else:
            messagebox.showerror("Could not register", 
                                 "Given username or password is invalid"
                                 + " or account of same name already exists")

    def openUserWindow(self, userType):
        '''(LoginFrame, account_type Enum) -> NoneType
        Given a user type as account_type Enum, open the appropriate top level
        window for them.
        '''
        # TODO: Umm, code smells we can strategy pattern this instead.
        if userType == account_types.Account_type.I:
            sourceFile = instrWindow.generateMainWindow(self.controller)
        elif userType == account_types.Account_type.S:
            sourceFile = studentWindow.questionSetPanel(self.username.get())
        self.clearInfo()

    def clearInfo(self):
        '''(LoginFrame) -> NoneType
        Clears login info that exists within the username/password fields.
        '''
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

if __name__ == "__main__":      
    root = tk.Tk()
    root.title("Welcome to your Homework App!")
    root.minsize(320, 150)
    root.resizable(False, False)
    loginWindow = LoginWindow(root)
    loginWindow.grid(row=8, column=0, sticky=(tk.E, tk.W))
    root.mainloop() 
