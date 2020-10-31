import graph
import scoring
from tkinter import *

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("AutoCorrect")
        self.root.configure(background="#121212")
        #self.root.geometry("800x500")
        self.keyAnswer = None
        self.inputAnswer = None
        self.marks = StringVar()
        self.blank = Label(self.root, bg="#121212")
        self.blank.pack()
        self.welcome = Label(
            self.root, text="Welcome to AutoCorrect!", background="#121212"
        )
        self.welcome.config(fg="#3b54ce", font=("Comfortaa", 40))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#121212")
        self.blank.pack()
        self.blank = Label(self.root, bg="#121212")
        self.blank.pack()
        self.key_answer_box = Text(self.root)
        self.key_answer_box.pack()
        self.blank = Label(self.root, bg="#121212")
        self.blank.pack()
        self.input_answer_box = Text(self.root)
        self.input_answer_box.pack()
        self.blank = Label(self.root, bg="#121212")
        self.blank.pack()
        self.grade_box = Message(
            self.root,
            textvariable=self.marks,
            bg="#121212",
            font=("Calibri"),
            fg="white",
        )
        self.grade_box.pack()
        self.blank = Label(self.root, bg="#121212")
        self.blank.pack()
        self.score_button = Button(
            self.root,
            text="GRADE",
            command=self.getMarks,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.score_button.config(height=2, width=30, borderwidth=0)
        self.score_button.pack(side=TOP, expand=1)
        self.blank = Label(self.root, bg="#121212")
        self.blank.pack()

        self.root.mainloop()

    def getMarks(self):
        self.keyAnswer = self.key_answer_box.get("1.0",END)
        self.inputAnswer = self.input_answer_box.get("1.0",END)
        if len(self.keyAnswer) == '\n':
            self.marks.set("Error in Key Answer: No answer provided.")
        elif len(self.inputAnswer) == '\n':
            self.marks.set("Error in Input Answer: No answer provided.")
        else:
            self.marks.set("GRADING...")
            key_answer_graph = graph.createGraph(self.keyAnswer.strip(), "key")
            input_answer_graph = graph.createGraph(self.inputAnswer.strip(), "ans")
            total_marks = scoring.evaluate(key_answer_graph, input_answer_graph, 4)
            self.marks.set(str(total_marks))
        

App()