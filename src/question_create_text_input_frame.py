import tkinter as tk
from tkinter import ttk
import multiChoiceQuestion as mcq

class TextQuestionFrame(tk.Frame):
    '''
    Template for a generic question which has one correct answer and 
    some number (possibly none) of provided possible answers
    '''
    
    # TODO this is a clone of the multi choice frame, should be reworked using OOP
    def __init__(self, parent, controller, isFinal=False, isFirst=False, pos=1,
                dueDate='No Due Date', possible_ans=1):
        tk.Frame.__init__(self, parent)
        self.controller = controller   
        self.shouldGenerateAnswer = tk.BooleanVar()
        self._numPossibleAnswers = possible_ans
        self.dueDate = dueDate
        self.mcqPossibleAnswerText = []

        mcqQuestionNumber = ttk.Label(self, text="Question #" + str(pos), 
                                    font=("Tahoma", 12, "bold italic"))
        mcqQuestionLabel = ttk.Label(self, text="Enter Question Body:")
        self.mcqQuestionText = tk.Text(self, height=4, width=50)
        mcqAutoGenCheckbox = ttk.Checkbutton(self, text="Auto-generate answers", 
                                           variable=self.shouldGenerateAnswer, 
                                           command=self.checkAndDisableAnswer,
                                           onvalue=tk.TRUE, offvalue=tk.FALSE)

        mcqCorrectAnswerLabel = ttk.Label(self, text="Enter The Correct Answer:")
        self.mcqCorrectAnswerText = tk.Text(self, height=1, width=50)

        # Create the instant feedback entry box.
        self.instantFeedbackEntry = tk.Entry(self, width = 60, bg = 'white')
        self.instantFeedbackEntry.grid(row = self._numPossibleAnswers + 5, column = 1, columnspan = 2, sticky = 'W')

        #Create the instant feedback toggle checkbox.
        instantFeedbackVar = tk.IntVar(value = 1)
        instantFeedbackCheckbox = ttk.Checkbutton(self, 
                                            text = 'Enable Question Feedback', 
                                            variable = instantFeedbackVar, 
                                            state = tk.NORMAL, 
                                            command = lambda entry = self.instantFeedbackEntry, 
                                            variable = instantFeedbackVar: self.toggleInstantFeedback(entry, variable))
        instantFeedbackCheckbox.grid(row = self._numPossibleAnswers + 5, column = 0, sticky = 'W')      

        # specify what cancel should do
        mcqCancelBtn = ttk.Button(self, text="Cancel and Return", 
                                command=lambda: self.controller.destroyQuestionFrames())

        # places widgets into grid
        mcqQuestionNumber.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        mcqQuestionLabel.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.mcqQuestionText.grid(row=1, column=1, columnspan=2)
        mcqCorrectAnswerLabel.grid(row=(self._numPossibleAnswers + 2), column=0, sticky=(tk.W, tk.E))
        self.mcqCorrectAnswerText.grid(row=(self._numPossibleAnswers + 3), column=1, 
                                     columnspan=2, sticky=(tk.W, tk.E))
        mcqAutoGenCheckbox.grid(row=(self._numPossibleAnswers + 4), column=0, sticky=tk.E)
        mcqCancelBtn.grid(row=(self._numPossibleAnswers + 6), column=0, sticky=(tk.E, tk.S))

        # based on question position in the set, show differing buttons
        if (isFinal):
            mcqSaveBtn = ttk.Button(self, text="Save and Finalize Set",
                                 command=lambda: 
                                    self.controller.collectWriteAllQuestions(self.dueDate))   
            mcqSaveBtn.grid(row=(self._numPossibleAnswers + 6), column=2, sticky=(tk.W, tk.S))
        else:
            mcqSaveBtn = ttk.Button(self, text="Continue to Next Question",
                                 command=lambda: 
                                       self.controller.nextQuestionFrame())      
            mcqSaveBtn.grid(row=(self._numPossibleAnswers + 6), column=2, sticky=(tk.W, tk.S))

        if(not (isFirst)):
            mcqBackBtn = ttk.Button(self, text="Back to Previous Question",
                                 command=lambda: 
                                       self.controller.prevQuestionFrame())
            mcqBackBtn.grid(row=(self._numPossibleAnswers + 6), column=1, sticky=(tk.S))

        # MORE PADDING
        for child in self.winfo_children():
            child.grid_configure(padx=3, pady=3)

    def getPossibleAnswersFromInput(self, numAns):
        '''
        Goes through numAns-1 many entries in this page's list of
        textboxes for possible answers and returns a list of the
        string values of each, in order
        '''
        retList = []
        for i in range(numAns - 1):
            retList.append(self.mcqPossibleAnswerText[i].get('1.0', 'end'))
        return retList

    def checkAndDisableAnswer(self):
        '''(TextQuestionFrame) -> NoneType
        Disables answer related textboxes when AutoGenerate answers is ticked off
        '''      
        if (self.shouldGenerateAnswer.get()):
            targetState = "disabled"
        else:
            targetState= "normal"
        for textbox in self.mcqPossibleAnswerText:
            textbox.config(state=targetState)

    def toggleInstantFeedback(self, entry, var):
        '''(TextQuestionFrame, Entry, IntVar) -> NoneType
        Enables or disables the instant feedback entry box.
        '''
        if var.get() == 0:
            entry.configure(state = tk.DISABLED)
        else:
            entry.configure(state = tk.NORMAL)         

    def compileQuestionInfo(self):
        ''' (self) -> mChoiceQuestion
        Wrapper class which converts this frame's raw data into an object accepted
        by the writeOutQuestion function
        '''
        # Configure instant feedback appropriately depending on its state.
        instantFeedback = self.instantFeedbackEntry.get()
        if (self.instantFeedbackEntry.cget('state') == tk.DISABLED) or (self.instantFeedbackEntry.get() == ''):
            instantFeedback = 'N/A'

        # a handle for one question only, writeOutQuestion does this for all
        mcQuestion = mcq.mChoiceQuestion(self.mcqQuestionText.get('1.0', 'end'), 
                                       self.getPossibleAnswersFromInput(
                                           self._numPossibleAnswers), 
                                       self.mcqCorrectAnswerText.get('1.0', 'end'),
                                       instantFeedback)
        return mcQuestion
