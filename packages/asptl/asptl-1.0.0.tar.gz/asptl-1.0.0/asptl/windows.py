from tkinter import*
def msgwin(caption='',ExitButton='OK',MainLabel='please...',buttons=[],labels=[],loop=True):
    def Exit():
        root.destroy()
    root=Tk(caption)
    root.title(caption)
    label=Label(root,text=MainLabel).pack()
    button=Button(root,text=ExitButton,command=Exit).pack()
    labellst=[]
    for l in labels:
        labellst.append(Label(root,text=l).pack())
    buttonlst=[]
    for b in buttons:
        buttonlst.append(Button(root,text=b).pack())
    if loop:
        root.mainloop()

def printxt(button):
        print(button.txt)
    
def eventwin(caption='',ExitButton='OK',label='please...',eventButton='event',command=msgwin,geometry=None,loop=True):
    root=Tk()
    root.title(caption)
    root.geometry(geometry)
    class button(Button):
        def __init__(self,master,text,command):
            super().__init__(root,text=text,command=lambda:command())
            self.txt=text
    def Exit():
        root.destroy()
    Exit=Button(root,text=label,command=Exit).pack()
    Main=button(root,eventButton,command).pack()
    if loop:
        root.mainloop()
