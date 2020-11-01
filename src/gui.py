import graph
import scoring
import utils
from tkinter import *


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("AutoCorrect")
        self.root.configure(background="#d2d2c9")
        self.root.geometry("480x640")
        self.keyAnswer = None
        self.inputAnswer = None
        self.marks = StringVar()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.root, text="AutoCorrect", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 80))
        self.welcome.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.root, text="Key Answer", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.key_answer_box = Text(self.root, height=15)
        self.key_answer_box.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.welcome = Label(self.root, text="Test Answer", background="#d2d2c9")
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 30))
        self.welcome.pack()
        self.input_answer_box = Text(self.root, height=15)
        self.input_answer_box.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.pack()
        self.grade_box = Message(
            self.root,
            textvariable=self.marks,
            bg="#d2d2c9",
            font=("Calibri", 25),
            fg="#6d031c",
        )
        self.grade_box.pack()
        self.blank = Label(self.root, bg="#d2d2c9")
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
        self.blank = Label(self.root, bg="#d2d2c9")
        self.openie_client = utils.getOpenieClient()
        self.openie_client.annotate("This is to initialize the client")
        self.blank.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.root.mainloop()

    def getMarks(self):
        self.keyAnswer = self.key_answer_box.get("1.0", END)
        self.inputAnswer = self.input_answer_box.get("1.0", END)
        if len(self.keyAnswer) == "\n":
            self.marks.set("Error in Key Answer: No answer provided.")
        elif len(self.inputAnswer) == "\n":
            self.marks.set("Error in Input Answer: No answer provided.")
        else:
            self.marks.set("GRADING...")
            key_answer_graph = graph.createGraph(
                self.keyAnswer.strip(), "key", self.openie_client
            )
            input_answer_graph = graph.createGraph(
                self.inputAnswer.strip(), "ans", self.openie_client
            )
            # graph.displayGraph(key_answer_graph)
            # graph.displayGraph(input_answer_graph)
            total_marks = scoring.evaluate(key_answer_graph, input_answer_graph, 4)
            self.marks.set(f"Score: {utils.roundMarks(total_marks)}")

    def onClose(self):
        self.openie_client.__del__()
        self.root.destroy()


App()
