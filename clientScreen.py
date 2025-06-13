from tkinter import *
from scripts import featureEnginering

master = Tk()
master.title("Japanese Sentence Morphology")
master.geometry("500x300")

text_box = Text(master, height=5, width=40)
text_box.pack()

text_box.focus_set()

def retrieve_input():
    inputValue= text_box.get("1.0","end-1c")
    tokens = [featureEnginering.tokenize(inputValue)]
    print(*tokens)
    print(len(*tokens))
    #output.lemma_Info(inputValue)
    

b = Button(master, text = "OK", width = 10, command = retrieve_input)
b.pack()

mainloop()
