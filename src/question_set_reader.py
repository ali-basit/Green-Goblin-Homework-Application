from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import os.path
import shutil


class questionSetReader:

    def __init__(self, panel, set_name, student_id):
        """(questionSetReader, Tk, str, str) -> None
        Initializing a questionSetReader object that reads a question
        set (.txt file), outputs file contents as labels and buttons.
        """
        self.master = panel
        self.master.panel.withdraw()
        self.reader = Toplevel()
        self.reader.title(set_name)
        self.set_name = set_name
        self.student = student_id
        self.fcontent = []
        self.questions = []
        self.mark = 0
        self.get_file_content()
        self.create_labels_and_buttons()

    def get_file_content(self):
        """(questionSetReader) -> list
        checking if file exist in student's own folder, if it does, prompt
        message box to ask if student wants to resume the saved work.
        """
        try:
            fdir = "Students/" + self.student + "/" + self.set_name + ".txt"
            fp = open(fdir, "r")
            self.fcontent = fp.read().splitlines()
            self.fcontent[2]
            self.reader.update()
            if messagebox.askyesno("Progress Found",
                                   "Would you like to resumeyour work?"):
                self.mark = int(self.fcontent[1])
                self.fcontent = self.fcontent[2:]
            else:
                raise FileNotFoundError
        except (FileNotFoundError, IndexError, TypeError):
            fdir = "Question Sets/" + self.set_name + ".txt"
            fp = open(fdir, "r")
            self.fcontent = fp.read().splitlines()[2:]
            pass

    def create_labels_and_buttons(self):
        """(questionSetReader) -> None
        Creating all buttons and labels, link them with corresponding function
        i.e. each button for answer is binding to check_ans
        """
        save_progress_button = Button(self.reader, text="Save progress",
                                      command=self.save_progress)
        save_progress_button.grid(row=0, column=1, sticky='WNSE')
        student_id_label = Label(self.reader, text=self.student)
        student_id_label.grid(row=0, column=0, sticky='WNSE')
        self.answer_buttons = list()
        # creating question label
        try:
            self.question_label = Label(self.reader, text=self.fcontent[0])
            self.question_label.grid(row=1, column=0, sticky='WNSE')
            # creating answer buttons
            for i in range(1, 5):
                answer = Button(self.reader, text=self.fcontent[i],
                                command=lambda student_ans=self.fcontent[i]: self.check_ans(student_ans))
                answer.grid(row=i+1, column=0, sticky='WNSE')
                self.answer_buttons.append(answer)
            # creating feedback label
            self.correct_ans = self.fcontent[5]
            self.feedback = self.fcontent[6]
        except IndexError:
            self.save_progress()
            pass

    def save_progress(self):
        """(questionSetReader) -> None
        Save progress to folder under student's id, if a file already
        exist, update file content.
        """
        des_dir = "Students/" + self.student + "/"
        messagebox.showinfo("result", "You got " + str(self.mark) +
                            " question(s) correct.")
        try:
            # try to open question set within student folder
            fp = open(des_dir + self.set_name + '.txt', 'r')
            highest_mark = int(fp.readlines()[0].strip())
        # if file does not exist in student folder, that means student haven't
        # attemp this set before, so set highest mark as current mark
        except (FileNotFoundError, IndexError, TypeError):
            highest_mark = self.mark
            pass
        fp = open(des_dir + self.set_name + '.txt', 'w')
        # update highest mark if current mark is higher
        if highest_mark < self.mark:
            highest_mark = self.mark
        fp.write(str(highest_mark) + '\n')
        fp.write(str(self.mark) + '\n')
        for line in self.fcontent:
            fp.write(line + "\n")
        messagebox.showinfo("Save Progress",
                            "Your progress has been saved to folder: " +
                            des_dir)
        fp.close()
        self.quit()

    def check_ans(self, student_ans):
        '''(QuestionSetGridview, event, str) -> int
        Checking if student has choosen the correct answer, update window after
        checking, if student reach the end of question set, call save_progress.
        '''
        # clear window
        self.disable_buttons()
        if str(student_ans) == str(self.correct_ans):
            res = "correct"
            self.mark += 1
        else:
            res = "wrong"
        messagebox.showinfo("result", "Your answer is " +
                            res + ".\n" + self.feedback)
        # self.master.withdraw()
        self.reader.withdraw()
        self.reader = Toplevel()
        try:
            self.fcontent = self.fcontent[7:]
            self.create_labels_and_buttons()
        except IndexError:
            self.save_progress(event)
            pass

    def disable_buttons(self):
        """(questionSetReader) -> None
        Disable all answer bottons
        """
        for button in self.answer_buttons:
            button.config(state=DISABLED)

    def quit(self):
        """(questionSetReader) -> None
        Remove all widgets in current Tk window, close window after removing.
        """
        self.reader.destroy()
        self.master.update_status()
