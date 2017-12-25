from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import os
import os.path
import shutil
from question_set_reader import *

class questionSetPanel():
    '''A class to represent a question set panel.'''    

    def __init__(self, student_id):
        '''(questionSetPanel, str) -> NoneType
        Initialize a new questionSetPanel with the given directory that contains
        question sets.
        '''
        self.qs_dir = "Question Sets"
        self.panel = Tk()
        self.panel.title("Student Question Grid")
        self.question_sets = list()
        self.labels = list()
        self.student = student_id
        self.fill_question_sets_list()
        self.create_labels_and_buttons()
        self.panel.update()
        self.panel.mainloop()

    def fill_question_sets_list(self):
        '''(questionSetPanel) -> NoneType
        Permeate question_sets with information of question sets within the
        given directory (self.qs_dir) in the format:
        [[set_name, size, due, highest_mark, status], [set_name,...]...]
        '''
        for file in os.listdir(self.qs_dir):
            set_info = []
            try:
                fp = open(self.qs_dir + "/" + file, "r")
                fcontent = fp.read().splitlines()
                if ((len(fcontent) - 2) % 7) != 0:
                    raise IndexError
                set_info = [file.rsplit('.', 1)[0], int(fcontent[0]),
                            fcontent[1]]
                try:
                    fp2 = open("Students/" + self.student + "/" + file, "r")
                    set_info.append(int(fp2.readline()))
                    set_info.append("Attempted")
                except FileNotFoundError:
                    set_info.append("")
                    set_info.append("New")
                    pass
                except ValueError:
                    print(file + " invalid format, one of the following element(s) missing: size, due day, feedback, correct answer\n")
                    set_info.clear()
                    pass
            except (ValueError, IndexError):
                # if such condition meets, this is not an valid file
                # either the due day or size not correct
                print(file + " invalid format, one of the following element(s) missing: size, due day, feedback, correct answer\n")
                set_info.clear()
                pass
            except FileNotFoundError:
                print(file + " wrong file name\n")
                set_info.clear()
                pass
            self.question_sets.append(set_info)
        for i in range(self.question_sets.count([])):
            self.question_sets.remove([])

    def create_labels_and_buttons(self):
        '''(questionSetPanel) -> NoneType
        Create labels and buttons based on information in question_sets.
        '''
        topic_label = ["Homework Set", "Set size", "Due Date",
                           "Highest Mark", "Status", "Attempt"]
        # Lay down topic labels in grid.
        for i in range(len(topic_label)):
            topic_label[i] = Label(self.panel, text=topic_label[i])
            topic_label[i].grid(row=0, column=i)

        # Create labels and buttons for each unique question set.
        for i in range(len(self.question_sets)):
            current_set = self.question_sets[i]

            for j in range(len(current_set)):
                label = Label(self.panel, text=current_set[j])
                label.grid(row=i+1, column=j)
                self.labels.append(label)
            button = Button(self.panel, text=current_set[0],
                            command=lambda set_name=current_set[0]:
                            self.read_question_set(set_name))

            # If the due date has passed, disable the ability to attempt the question set.
            try:
                if datetime.now() >= datetime.strptime(current_set[2], '%m/%d/%y %I:%M%p'):
                    button.configure(text = "Due Date Has Passed")
                    button.configure(state = DISABLED)
            except ValueError:
                pass

            button.grid(row=i+1, column=len(current_set))

        quit_button = Button(self.panel, text="Quit", command=self.close_window)
        quit_button.grid(row=0, column=len(topic_label))

    def read_question_set(self, set_name):
        '''(questionSetPanel, str) -> NoneType
        Open a question set reader (questionSetReader), get mark from student,
        and update panel information.
        '''
        qsr = questionSetReader(self, set_name, self.student)
        self.panel.deiconify()
        self.update_status()

    def update_status(self):
        '''(questionSetPanel) -> NoneType
        Update the information of the question sets.
        '''
        for label in self.labels:
            label.grid_forget()
        self.labels.clear()
        self.question_sets.clear()
        self.fill_question_sets_list()
        self.create_labels_and_buttons()

    def close_window(self):
        '''(questionSetPanel) -> NoneType
        Clean all widgets and close the window.
        '''
        self.panel.destroy()
        self.panel.quit()
