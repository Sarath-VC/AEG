from tkinter import filedialog, messagebox
from tkinter import *
import json
deletedatadict = Tk()
deletedatadict.title("ESSAY AUTOMATA")
deletedatadict.geometry("500x400+10+20")


def deletefromdict():
    with open('/AEG/aegdataset/datajson.json', 'r') as f:
        dictdata = json.load(f)
    if datalist.curselection():
        if messagebox.askquestion("Confirm","Are you sure want to delete?")=='yes':
            ind=datalist.curselection()
            for i in ind[::-1]:
                d=datalist.get(i)
                print(d)
                del dictdata[d]
                datalist.delete(i)
            with open('/AEG/aegdataset/datajson.json', 'w') as f:
                dictdata = json.dump(dictdata, f)

        else:
            datalist.selection_clear(0,END)
            pass
    else:
        messagebox.showinfo("Warning","Choose any item from list")
    #datalist.remove(entr.get())

labind=Label(deletedatadict, text="INDEX NAME ")
labind.pack(anchor=N+W,pady=5,padx=25)
datalist=Listbox(deletedatadict, selectmode="multiple")
with open('/AEG/aegdataset/datajson.json', 'r') as f:
    dictdata = json.load(f)
for i in dictdata.keys():
    datalist.insert(END,i)
datalist.pack(anchor=N+W,padx=5,pady=10)
deldatabtn=Button(deletedatadict, text="DELETE FROM DICTIONARY", command=deletefromdict)
deldatabtn.pack(anchor=N+W,padx=5,pady=10)
deletedatadict,mainloop()