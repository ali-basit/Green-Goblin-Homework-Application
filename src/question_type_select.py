import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os.path
import multi_choice_question as mcq
import login_windows as loginW
import question_file_save_dialog as filesave
import question_type_select_frame as typeselect_frame
import question_create_mult_choice_frame as multichoice_frame
import question_create_text_input_frame as textinput_frame
# note, ttk offers some prettier widgets than tk
# TODO - I am not convinced we are laying these classes out correctly... talk later

class QuestionCreationWindow():
   '''
   Base window object which will hold and manage frames related to question creation
   '''
   
   def __init__(self, master, parent):
      self.parent = parent
      self.master = master
      self._multipleChoiceQuestionSize = 0
      self._answerType = ""
      self._visibleFrameName = ""
      # all of our other frames go into this one
      self._mainframe = ttk.Frame(master, padding="3 3 3 3")
      self._mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
      self._mainframe.columnconfigure(0, weight=1)
      self._mainframe.rowconfigure(0, weight=1) 
      self.init_type_window()
      
   def init_type_window(self):
      '''
      Initialize the subframes dictionary which we use to navigate through different pages
      '''
      # specify what other frames we might show in this window
      self.subframes={}
      # initial frame to show
      self.subframes["TypeSpecify"] = typeselect_frame.QuestionTypeSelectFrame(
         parent=self._mainframe, controller=self)
      self.subframes["TypeSpecify"].grid(
         row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
      
      # set the frame shown initially
      self.showFrame("TypeSpecify")
      
   def createQuestionInputFrames(self, numFrames, dueDate, classOption):
      ''' (QuestionCreationWindow, int) -> NoneType
      Creates the specified number of question frames and places them
      into  the subframe list. Be sure to destroy these subframes when complete
      '''
      
      # create the required number of frames and number them
      for i in range(1, numFrames + 1):
         # TODO Can we do java style lambda expressions here?
         # Determine which position the frame is in for display purposes
         final = False
         first = False
         if (i == 1):
            first = True
         if (i == numFrames):
            final = True
         # this format is VERY important, other functions rely on it
         # TODO make an enum for this so we're not guessing
         if (classOption.get() == 'Multiple Choice Value'):
            self.subframes["MultiChoiceCreation " + str(i)] = multichoice_frame.MultiChoiceQuestionFrame(
               self._mainframe, self, final, first, i, dueDate)
            self.subframes["MultiChoiceCreation " + str(i)].grid(
               row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S)) 
         elif (classOption.get() == 'Text Value'):
            self.subframes["MultiChoiceCreation " + str(i)] = textinput_frame.TextQuestionFrame(
               self._mainframe, self, final, first, i, dueDate)
            self.subframes["MultiChoiceCreation " + str(i)].grid(
               row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))             
      
   def showFrame(self, pageName):
      ''' (QuestionCreationWindow, String) -> NoneType
      Uses the given pagename to locate a corresponding frame
      and raise it to top level visibility
      '''
      # TODO in the future this also handles navigating
      # to the correct question type
      frame = self.subframes[pageName]
      frame.tkraise()
      self._visibleFrameName = pageName
      
   def _shiftFrame(self, value):
      '''
      Shift currently visible frame by value and displays the frame found
      '''
      curFrameName = self._visibleFrameName
      # change the frame name to one with specified number at the end
      splitIndex = curFrameName.index(' ') + 1
      pageName = curFrameName[:splitIndex]
      pageNumTarget = int(curFrameName[splitIndex:]) + value
      self.showFrame(pageName + str(pageNumTarget))
      
   def nextQuestionFrame(self):
      '''
      When called from a Question set frame, shows the next frame
      in the subframe array
      '''
      self._shiftFrame(1)
   
   def prevQuestionFrame(self):
      '''
      When called from a Question set frame, shows the previous frame
      in the subframe array
      '''
      self._shiftFrame(-1)  
   
   def destroyQuestionFrames(self):
      ''' (self) -> noneType
      Removes all question frames from the subframe array.
      Use only when the user cancels or finishes 
      their question creating operation.
      '''
      # Good practice to destroy all frames before going ahead
      for frame in self.subframes:
         # going through the keys in the dictionary to destroy the frames
         self.subframes[frame].destroy()
            
      # re initialize subframes with just the specification frame
      self.init_type_window()
   
   def collectWriteAllQuestions(self, dueDate):
      ''' (self, str) -> NoneType
      Loop through each question frame in the our subframe dict and
      compile each one's information into a list.
      Aftewards, write out the questions to file after prompting for name
      '''
      questionList = []
      # TODO possibly screws up the ordering of questions. Investigate
      for frame in self.subframes:
         if (frame != 'TypeSpecify'):
            questionList.append(self.subframes[frame].compileQuestionInfo())
      self.writeOutQuestion(questionList, dueDate)
      
   def writeOutQuestion(self, mcq, dueDate):
      '''(self, List(multiChoiceQuestion), str) -> NoneType
      REQ: multiChoiceQuestion has correct answer at last index
      Writes information contained in the given window's textboxes to file after
      prompting the user for a name
      '''
      # prompt for a file name
      dialogBox = filesave.fileNameDialog(self.master)
      # wait for our called dialog box to complete its actions
      self.master.wait_window(dialogBox)
      # get the filename the user wanted
      fileName = dialogBox.getFileNameResult()
      
      # sanitize the filename a bit
      fileNameClean = fileName.replace(".", "").strip()
      # an empty string in the result means either the user didn't listen
      # or they cancelled the operation. Either way we do not continue      
      if fileNameClean != '':
         openFile = "Question Sets/" + fileNameClean + ".txt"
         with open(openFile, "w") as file:
            # writeout the number of questions in this set
            file.write(str(len(mcq)) + "\n")
            # write due date
            file.write(dueDate + "\n")
            # write out question/answer information
            for nextQuestion in mcq: 
               file.write(nextQuestion.getQuestionBody())
               for possibleAns in nextQuestion.getPossibleAnswers():
                  # auto newlines attached by list
                  file.write(possibleAns)
                  # TODO could program to be smarter about finding correct answer but I'm lazy
               # explicitly specify the correct answer out of the given
               file.write(nextQuestion.getPossibleAnswers()[-1])
               # Write out the instant feedback.
               file.write("Feedback: " + nextQuestion.getInstantFeedback() + "\n")
        
         messagebox.showinfo("Set Saved", 
                             "Saved question set as \'" + fileNameClean + ".txt\'")
         self.destroyQuestionFrames()
         
      else:
         # inform user that nothing was saved
         messagebox.showinfo("Save Operation Cancelled", 
                                   "Question Set has not been saved.")  
def generateMainWindow(oldWindow):
   '''
   Withdraw the given window handle and display the main window of this class
   '''
   # set behaviour on close
   oldWindow.master.withdraw()
   top = tk.Toplevel()
   top.title("Question Creation")
   top.minsize(320, 150)
   top.resizable(False, False)
   qTypeSelect = QuestionCreationWindow(top, oldWindow)
   qTypeSelect.master.protocol('WM_DELETE_WINDOW', lambda: oldWindow.returnToLogin(top))

if __name__ == "__main__":
   rootQ = tk.Tk()
   rootQ.title("Question Creation")
   rootQ.minsize(320, 150)
   rootQ.resizable(False, False)
   qTypeSelect = QuestionCreationWindow(rootQ, None)
   rootQ.mainloop()