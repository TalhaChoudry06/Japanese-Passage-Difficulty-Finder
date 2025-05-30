from tkinter import *
import output

master = Tk()
master.title("Japanese Sentence Morphology")
master.geometry("500x300")

text_box = Text(master, height=5, width=40)
text_box.pack()

text_box.focus_set()

def retrieve_input():
    inputValue= text_box.get("1.0","end-1c")
    tokens = [output.tokenized(inputValue)]
    print(*tokens)
    output.lemma_Info(inputValue)
    

b = Button(master, text = "OK", width = 10, command = retrieve_input)
b.pack()

mainloop()
