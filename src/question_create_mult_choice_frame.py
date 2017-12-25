import tkinter as tk
from tkinter import ttk
import multi_choice_question as mcq
import question_create_text_input_frame as textframe

class MultiChoiceQuestionFrame(textframe.TextQuestionFrame):
    '''
    Representation of a standard 4 option multiple choice question frame
    '''

    # TODO we could maybe use a null object instead of this isfinal.isfirst stuff
    def __init__(self, parent, controller, isFinal=False, isFirst=False, pos=1,
                dueDate='No Due Date'):
        # parent constructor takes care of placing most widgets...
        textframe.TextQuestionFrame.__init__(
            self, parent, controller, isFinal, isFirst, pos, dueDate, 4)

        # we mostly worry just about placing and gridding our extra widgets
        mcqAnswerLabel = ttk.Label(self, text="Enter Possible Incorrect Answers:")
        mcqAnswerLabel.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # place one potential answer entrybox for each extra possible answer
        for i in range(self._numPossibleAnswers - 1):
            self.mcqPossibleAnswerText.append(tk.Text(self, height=1, width=50))
            self.mcqPossibleAnswerText[i].grid(row=(i+3), column=1, columnspan=2)