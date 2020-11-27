from tkinter import Tk, PhotoImage, Frame, Entry, RIGHT, LEFT, Button, INSERT, Label, StringVar
from pathlib import Path
from filesReducerGPSMT import reduceFiles
from tkinter import filedialog
import threading

def selectDirAction(labelText,entry):
    labelText.set("Carregando...")
    entrada = entry.get().replace(',', '.')
    try:
        float(entrada)
    except:
        labelText.set("Digite um numero como medida")
        return
    file_path = filedialog.askdirectory()

    if reduceFiles(file_path, float(entrada)):
        labelText.set("Imagens salvas em "+file_path+"/resultsFileReducer")
    else:
        labelText.set("Selecione um diretorio com SOMENTE imagens georeferenciadas")

if __name__ == '__main__':
    instance = Tk()
    labelText = StringVar()
    #Window(instance)
    instance.geometry("800x300+50+50")
    logoPath = Path('imgs/wendy-logo.png')
    instance.iconphoto(instance, PhotoImage(file=logoPath.as_posix()))
    instance.title("")

    instance.configure(background='#b2c1ff')

    img = PhotoImage(file=logoPath.as_posix())
    my_image = Label(instance, image=img)
    my_image.pack()
    my_image.configure(background='#b2c1ff')

    label = Label(instance, text="Distância(metros)")
    label.pack()
    label.configure(background='#b2c1ff')

    entry = Entry(instance)
    entry.pack()
    entry.insert(INSERT, '')
    entry.configure(width=200)

    # Print the contents of entry widget to console
    def select_dir():
       t = threading.Thread(target=selectDirAction, args=(labelText,entry,))    
       t.start()

    # Create a button that will print the contents of the entry
    button = Button(instance, text='Selecionar diretorio', command=select_dir)
    button.configure(width=200, background='#c6b6e0')
    button.pack()
    #instance.eval('tk::PlaceWindow %s center' % instance.winfo_pathname(instance.winfo_id()))
    instance.resizable(False, False)

    label2 = Label(instance, textvariable=labelText)
    label2.pack()
    label2.configure(background='#cccccc')

    instance.mainloop()

