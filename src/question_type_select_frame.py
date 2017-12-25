import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class QuestionTypeSelectFrame(tk.Frame):
    '''
    Question Creation frame in which the user is able to specify
    # of questions, due date and question type
    '''

    def __init__(self, parent, controller):
        '''
        Initializes this frame placed within parent but with
        controller as controlling window (probably QuestionCreationWindow)
        '''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        numQuestionInput = tk.StringVar()
        #for due date
        dueDate = tk.StringVar()
        # option for text questions
        classOption = tk.StringVar()      

        qtSelectLabel = ttk.Label(self, text="Select answer type for this question:")
        qtCreateBtn = ttk.Button(self, text="Create",
                               command=lambda: 
                               self.parseSettingsAndProceed(numQuestionInput.get(), dueDate.get(), classOption))
        qtCancelBtn = ttk.Button(self, text="Cancel",
                               command=lambda: self.onCancel())

        # Question Type specification widgets
        qtTypeMultipleChoice = ttk.Radiobutton(self, text="Multiple Choice", value='Multiple Choice Value', variable=classOption)
        qtTypeTextInput = ttk.Radiobutton(self, text="Text Input", value='Text Value', variable=classOption)
        qtTypeMultipleChoice.invoke()

        # questions in set prompt and field
        qtPromptQNum = tk.Label(self, text = "How many question(s) in this set?")
        mpAnsSize = tk.Entry(self, textvariable=numQuestionInput, bd=1)
        # Due date field
        qtPromptQDue = tk.Label(self, text = "What is the due date for this question set?")
        #input field
        mpAnsSizeDue = tk.Entry(self, textvariable=dueDate, bd=1)      

        # places widgets into grid
        qtSelectLabel.grid(row=0, column=0, sticky=(tk.W, tk.E))
        qtTypeMultipleChoice.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # for text input
        qtTypeTextInput.grid(row=2, column=0, sticky=(tk.W, tk.E))

        #for number of questions
        qtPromptQNum.grid(row=3, column=0, sticky=(tk.W, tk.E))
        mpAnsSize.grid(row=3, column=1, sticky=(tk.W, tk.E))

        #for due date
        qtPromptQDue.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=4)
        mpAnsSizeDue.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=4)

        qtCreateBtn.grid(row=5, column=1, sticky=(tk.W, tk.S))
        qtCancelBtn.grid(row=5, column=0, sticky=(tk.E, tk.S))

        # some global padding so UI looks less disgustingly small
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=10)

    def parseSettingsAndProceed(self, qInput, dueDate, classOption):
        ''' (String, String) -> NoneType
        Parse the given question setting inputs and iff they are valid, proceeds
        to the MultiChoiceCreation frame, set with the appropriate number of
        questions and other options
        '''
        if (not self.dueDateValid(dueDate)):
            messagebox.showerror("Due Date is empty", "Due Date cannot be empty")
            # exit early due to the error
            return

        # valid inputs are positive whole numbers
        try:
            qIntInput = int(qInput)
            if (qIntInput > 0):
                # tell our parent window to generate the specified number of frames
                self.controller.createQuestionInputFrames(qIntInput, dueDate, classOption)
                # navigate to the first of the frames
                # TODO by default is multiple choice
                self.controller.showFrame("MultiChoiceCreation 1")
            else:
                messagebox.showerror("Don't be silly",
                                 "Please only provide positive values " +
                                 "when specifying number of questions")
        except(ValueError):
            # our user gave us something stupid as input, so we yell at them
            messagebox.showerror("Invalid Number of Questions", 
                              "Please only enter integer " +
                              "values for the number of questions")

    def dueDateValid(self, dueDate):
        '''
        Perform some basic checks on the due date field
        return a boolean based on whether it looks valid
        '''
        # TODO for now, just checks if empty
        return dueDate != ""

    def onCancel(self):
        '''
        Actions to perform when the user clicks the cancel button from the
        question type page
        '''
        # if we are a child window, close return to login window on cancel
        if self.controller.parent:
            self.controller.parent.returnToLogin(self.controller.master)
        else:
            # otherwise destroy window entirely
            self.controller.master.destroy()
