import tkinter as tk
from tkinter import ttk

class fileNameDialog(tk.Toplevel):
    '''
    Dialog prompt to be used with the question set creation panels.
    Asks for file names and can return given file name on completion
    '''

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        # link this dialog to the parent
        self.transient(parent)
        self.title("Saving Question Set")
        self.parent = parent
        # This is what we use to communicate the result with parent windows
        self.fileNameResult = ""
        # Local storage of filename variable
        fileNameInput = tk.StringVar()

        fndPromptWarn = ttk.Label(self, text=
                                "Enter the name this question set will be saved as:" + 
                                "\nEmpty names are not allowed.\nAny existing file with " + 
                                "the same name will be overwritten.", font=("Tahoma", 11))
        fndPromptWarn.grid(row=0, column=0, sticky=(tk.E, tk.W))

        fndTextInput = ttk.Entry(self, textvariable=fileNameInput, width=20)
        fndTextInput.grid(row=0, column=1, columnspan=2)

        fndBtnCancel = ttk.Button(self, text="Cancel",
                                command=lambda: self.closeDialog())
        fndBtnOk = ttk.Button(self, text="Accept and Save", 
                            command=lambda: self.pressedOk(fileNameInput.get()))
        fndBtnCancel.grid(row=1, column=1, sticky=(tk.N))
        fndBtnOk.grid(row=1, column=2, sticky=(tk.N))
        # disables the parent's window and focuses on this
        self.grab_set()

    def pressedOk(self, fileName):
        ''' (fileNameDialog, String) -> NoneType
        Handles all events which should occur when ok is pressed on this
        dialog box e.g. finalizing values and cleaning up focus
        '''
        self.withdraw()
        self.fileNameResult = fileName
        self.closeDialog()

    def closeDialog(self):
        '''(fileNameDialog) -> NoneType
        Handles events which should occur when the dialog is closed via typical means
        '''
        self.parent.focus_set()
        self.destroy()
        
    def getFileNameResult(self):
        '''
        Returns the file name which has been finalized by this dialog.
        Behaviour is not defined when called while dialog still has focus
        '''
        return self.fileNameResult
