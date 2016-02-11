__author__ = 'truba'

from Tkinter import *
from tkFileDialog import askopenfilename
import presenter
import tkMessageBox

class App:

    def __init__(self, master):
        master.title("Classifying the time period of text")

        frame = Frame(master, padx=10, pady=10)
        frame.pack()

        tf_frame = Frame(frame)
        tf_frame.pack(side=LEFT)

        frame_right = Frame(frame)
        frame_right.pack(side=RIGHT)

        frame_right_up = Frame(frame_right)
        frame_right_up.pack(side=TOP)
        frame_right_down = Frame(frame_right, pady=70)
        frame_right_down.pack(side=BOTTOM)


        self.tf = Text(tf_frame)
        self.tf.pack()

        label = Label(frame_right_up, text="Select granularity")
        label.pack()

        self.v_text = StringVar()
        radio_btn = Radiobutton(frame_right_up, text="Fine", variable=self.v_text, value="F")
        radio_btn.pack(anchor = W)
        radio_btn = Radiobutton(frame_right_up, text="Medium", variable=self.v_text, value="M")
        radio_btn.pack(anchor = W)
        radio_btn = Radiobutton(frame_right_up, text="Course", variable=self.v_text, value="C")
        radio_btn.pack(anchor = W)

        btn = Button(frame_right_down, text="Import from file", command=self.import_from_file)
        btn.pack()
        btn = Button(frame_right_down, text="Classify", command=self.evaluate)
        btn.pack()

    def import_from_file(self):
        filename = askopenfilename()
        with open (filename, "r") as file:
            data = file.read()
            self.tf.delete("1.0", END)
            self.tf.insert(INSERT, data)

    def evaluate(self):
        gran = self.v_text.get()
        text = self.tf.get("1.0",END)
        year = presenter.evaluate(gran, text)
        result = "Given text was written in: " + str(year)
        tkMessageBox.showinfo("Classification result", result)

root = Tk()

app = App(root)

root.mainloop()
root.destroy()
