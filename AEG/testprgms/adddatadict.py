from tkinter import filedialog, messagebox
from tkinter import *
import json
savedatadict = Tk()
savedatadict.title("ESSAY AUTOMATA")
savedatadict.geometry("500x400+10+20")

def addtolist():
    etv=entr.get()
    try:
        index=datalist.get(0, "end").index(etv)
        entr.delete(0, END)
    except ValueError:
        datalist.insert(END,etv)
        entr.delete(0,END)
def write_json(data, filename='/AEG/aegdataset/datajson.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)
def savetodict():
    #for i in range(datalist.size()):
    etv=entr1.get()
    litem=list(datalist.get(0,END))
    h={etv:litem}
    with open('/AEG/aegdataset/datajson.json', 'r') as f:
        z = json.load(f)
    z.update(h)
    if messagebox.askquestion("Confirm","Are you sure want to save?")=="yes":
        write_json(z)
        entr1.delete(0, END)
        datalist.delete(0,END)
    else:
        pass
    print(json.dumps(z))
    print(litem)
def deletefromlist():
    if datalist.curselection():
        if messagebox.askquestion("Confirm","Are you sure want to delete?")=='yes':
            ind=datalist.curselection()
            for i in ind[::-1]:
                datalist.delete(i)
        else:
            datalist.selection_clear(0,END)
            pass
    else:
        messagebox.showinfo("WARNING","CHOOSE ANY ITEM")
    #datalist.remove(entr.get())
def toggle_state(*_):
    if entr1.var.get():
        savebtn['state']=NORMAL
    else:
        savebtn['state']=DISABLED
def toggle_state_1(*_):
    if entr.var.get():
        addbtn['state']=NORMAL
    else:
        addbtn['state']=DISABLED
lab=Label(savedatadict, text="ENTER WORD ")
lab.pack(anchor=N+W,pady=5,padx=25)
entr = Entry(savedatadict)
entr.pack(anchor=N+W,side=TOP,pady=5,padx=25)
entr.var=StringVar()
entr['textvariable']=entr.var
entr.var.trace_add('write',toggle_state_1)
addbtn=Button(savedatadict, text="ADD TO DICTIONARY", command=addtolist, state=DISABLED)
addbtn.pack()
delbtn=Button(savedatadict, text="DELETE FROM LIST", command=deletefromlist)
delbtn.pack()
#addbtn.pack(anchor=W,side=TOP,pady=5,padx=25)
datalist=Listbox(savedatadict, selectmode="multiple")
datalist.pack(anchor=N+E)
lab1=Label(savedatadict, text="ENTER INDEX KEY ")
lab1.pack(anchor=S+W)
entr1 = Entry(savedatadict)
entr1.var=StringVar()
entr1['textvariable']=entr1.var
entr1.var.trace_add('write',toggle_state)
entr1.pack(anchor=S+W)
savebtn=Button(savedatadict, text="SAVE TO DICTIONARY", command=savetodict, state=DISABLED)
savebtn.pack()

savedatadict.mainloop()