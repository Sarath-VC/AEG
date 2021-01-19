from tkinter import filedialog, messagebox
import tkinter as tk
import os
import shutil
from pathlib import Path
from aegmodel import model
from flask import Flask
import json
import sys

app=Flask(__name__)
sys.setrecursionlimit(1000)

class Checkbar(tk.Frame):
   def __init__(self, parent=None, picks=[], side="LEFT", anchor="W"):
      tk.Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = tk.IntVar()
         chk = tk.Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand="YES")
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)

class MainApp(tk.Tk):
    def __init__(self,master):
        tk.Tk.__init__(self)
        self.__frame=None
        self.menubarstart()
        # self.frames={}
        # for frame in (MainFrame, ListFrame, SearchFrame, ResultFrame, HistoryFrame, SaveDataDictFrame, DeleteDataDictFrame):
        #     f = frame(container,self)
        #     self.frames[frame]=f
        #     f.grid(row=0, column=0, sticky=W + N + E + S)

        self.raise_frame(MainFrame)
    def menubarstart(self):
        menubar = tk.Menu(self)
        homemenu = tk.Menu(menubar, tearoff=0)
        homemenu.add_command(label="Dash Home")
        homemenu.add_command(label="Exit", command=self.quit)
        # homemenu.config(state="active")
        menubar.add_cascade(label="Home", menu=homemenu)

        searchmenu = tk.Menu(menubar, tearoff=0)
        searchmenu.add_command(label="Search")
        menubar.add_cascade(label="Search", menu=searchmenu)

        historymenu = tk.Menu(menubar, tearoff=0)
        historymenu.add_command(label="Essays")
        historymenu.add_command(label="Report")
        historymenu.add_command(label="Create Datadictionary")
        historymenu.add_command(label="Delete Datadictionary")
        menubar.add_cascade(label="Management", menu=historymenu)
        self.config(menu=menubar)

    def raise_frame(self, frame):
        # frame=self.frames[fr]
        # frame.tkraise()
        new_frame=frame(self)
        if self.__frame is not None:
            self.__frame.destroy()
        self.__frame=new_frame
        self.__frame.pack()

class MainFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        updbt = tk.Button(master, text="Upload Your Essay", command=lambda: master.raise_frame(UploadFrame), fg="red")
        updbt.pack()
        updbtm = tk.Button(master, text="Upload Multiple Essays", command=lambda: self.openf1(), fg="red")
        updbtm.pack()
    def openf1(self):
        #print ("hlo")
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                       filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")),multiple=TRUE)

        li= self.master.splitlist(filename)
        filePath=[]
        if not os.path.exists('/AEG/Uploads'):
            p = Path('Uploads')
            p.mkdir(exist_ok="TRUE")
            for f in li:
                src = f
                dst = '/AEG/Uploads/'
                shutil.copy(src, dst)
        else:
            for f in li:
                src = f
                dst = "/AEG/Uploads/"
                shutil.copy(src, dst)


    def raise_frame(self, frame):
        new_frame=frame(self)
        if self.__frame is not None:
            self.__frame.destroy()
        self.__frame=new_frame
        self.__frame.pack()
class SearchFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # searchpage_start
        searchframe = Frame(master)
        searchframe.grid(row=0, column=0, sticky=W + E + S + N)
        entrename = Entry(searchframe, bd=3, justify=RIGHT)
        entrename.grid(row=0, column=0, sticky=W + N + E + S)
        entrename.insert(0, "SEARCH ESSAY BY NAME")
        searchbt = Button(searchframe, text="SEARCH", command=lambda: self.searchFile(), fg="red")
        searchbt.grid(row=0, column=1, sticky=W + N + E + S)

        entr = Entry(searchframe, bd=3, justify=CENTER)
        entr.grid(row=1, column=0, sticky=W + N + E + S)
        entr.insert(0, "ESSAY NAME")
        entr2 = Entry(searchframe, bd=3, justify=CENTER)
        entr2.grid(row=1, column=1, sticky=W + N + E + S)
        entr2.insert(0, "GRADE")
        entr3 = Entry(searchframe, bd=3, justify=CENTER)
        entr3.grid(row=1, column=2, sticky=W + N + E + S)
        entr3.insert(0, "DETAILS")
        n = 5
        for i in range(2, n + 2):
            for j in range(3):
                entr = Entry(searchframe, bd=3, justify=RIGHT)
                entr.grid(row=i, column=j, sticky=W + N + E + S)
        # searchpage_end

    def searchFile(self):
        print("hjk")
class ListFrame(tk.Frame):
    def __init__(self,master):
        # listessays_start
        tk.Frame.__init__(self, master)
        listframe = Frame(master)
        listframe.grid(row=0, column=0, sticky=W + E + S + N)
        lb = Listbox(listframe)
        fileslist = []
        fileslist = os.listdir('/AEG/Uploads/')
        # print(fileslist)
        n = len(fileslist)
        for i in range(n):
            entr = Label(listframe, bd=3, justify=RIGHT, text=fileslist[i])
            lb.insert(i, fileslist[i])
        checklist = []
        n = 1
        distros_dict = self.jsondataload()
        cb = []
        vars = []
        for i in distros_dict.keys():
            var = IntVar()
            cb.append(Checkbutton(listframe, text=i, variable=var))
            vars.append(var)
        lng = Checkbar(listframe, distros_dict.keys())
        lng.pack()
        lb.pack()
        v = Button(listframe, text="Evaluate", command=lambda: self.evalbtncall(lb.get(ACTIVE), self.allstates()))
        v.pack()
        p = Button(listframe, text="UPDATE FRAME", command=listframe.update())
        p.pack()
        # listessays_end
    def allstates(self):
        li = list(self.lng.state())
        return li
    def upframe(self):
        self.listframe.update()
        self.raise_frame(self.listframe)

    def evalbtncall(self,f, vars):
        stri = "D:/AEG/Uploads/" + f
        print("calling sw")
        m = len(vars)
        sttnew = []
        for c in range(m):
            if vars[c] == 1:
                st = (self.cb[c].cget('text'))
                self.addstr(str(st))
                # print(sttnew)
                # print (c)
        rev = model.stopword(stri)
        model.tfidf(rev, sttnew)
        # return str

    def addstr(self,stt):
        self.sttnew.append(stt)

    def jsondataload(self):
        with open('/AEG/aegdataset/datajson.json', 'r') as f:
            z = json.load(f)
            return (z)
class HistoryFrame(tk.Frame):
    def __init__(self,master):
        # history_start
        tk.Frame.__init__(self, master)
        historyframe = Frame(master)
        historyframe.grid(row=0, column=0, sticky=W + E + S + N)
        entr = Entry(historyframe, bd=3, justify=CENTER)
        entr.grid(row=0, column=0, sticky=W + N + E + S)
        entr.insert(0, "ESSAY NAME")
        entr2 = Entry(historyframe, bd=3, justify=CENTER)
        entr2.grid(row=0, column=1, sticky=W + N + E + S)
        entr2.insert(0, "GRADE")
        entr3 = Entry(historyframe, bd=3, justify=CENTER)
        entr3.grid(row=0, column=2, sticky=W + N + E + S)
        entr3.insert(0, "DETAILS")
        n = 5
        for i in range(1, n + 1):
            for j in range(3):
                entr = Entry(historyframe, bd=3, justify=RIGHT)
                entr.grid(row=i, column=j, sticky=W + N + E + S)
        # history_end
class SaveDataDictFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # savedadadict_start
        savedatadict = Frame(master)
        lab = Label(savedatadict, text="ENTER WORD ")
        lab.pack(anchor=N + W, pady=5, padx=25)
        entr = Entry(savedatadict)
        entr.pack(anchor=N + W, side=TOP, pady=5, padx=25)
        entr.var = StringVar()
        entr['textvariable'] = entr.var
        entr.var.trace_add('write', self.toggle_state_1)
        addbtn = Button(savedatadict, text="ADD TO DICTIONARY", command=self.addtolist, state=DISABLED)
        addbtn.pack()
        delbtn = Button(savedatadict, text="DELETE FROM LIST", command=self.deletefromlist)
        delbtn.pack()
        datalist = Listbox(savedatadict, selectmode="multiple")
        datalist.pack(anchor=N + E)
        lab1 = Label(savedatadict, text="ENTER INDEX KEY ")
        lab1.pack(anchor=S + W)
        entr1 = Entry(savedatadict)
        entr1.var = StringVar()
        entr1['textvariable'] = entr1.var
        entr1.var.trace_add('write', self.toggle_state)
        entr1.pack(anchor=S + W)
        savebtn = Button(savedatadict, text="SAVE TO DICTIONARY", command=self.savetodict, state=DISABLED)
        savebtn.pack()
        # savedatadict_end
    def addtolist(self):
        etv = self.entr.get()
        etv = etv.lower()
        try:
            index = self.datalist.get(0, "end").index(etv)
            self.entr.delete(0, END)
        except ValueError:
            self.datalist.insert(END, etv)
            self.entr.delete(0, END)

    def write_json(self,data, filename='/AEG/aegdataset/datajson.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def savetodict(self):
        etv = self.entr1.get()
        litem = list(self.datalist.get(0, END))
        s = model.synonyms_find(litem)
        for q in s:
            litem.append(q)
        h = {etv: litem}
        z = self.jsondataload()
        z.update(h)
        if messagebox.askquestion("Confirm", "Are you sure want to save?") == "yes":
            self.write_json(z)
            self.entr1.delete(0, END)
            self.datalist.delete(0, END)
        else:
            pass
    def jsondataload(self):
        with open('/AEG/aegdataset/datajson.json', 'r') as f:
            z = json.load(f)
            return (z)
    def deletefromlist(self):
        if self.datalist.curselection():
            if messagebox.askquestion("Confirm", "Are you sure want to delete?") == 'yes':
                ind = self.datalist.curselection()
                for i in ind[::-1]:
                    self.datalist.delete(i)
            else:
                self.datalist.selection_clear(0, END)
                pass
        else:
            messagebox.showinfo("WARNING", "CHOOSE ANY ITEM")

    def toggle_state(self,*_):
        if self.entr1.var.get():
            self.savebtn['state'] = NORMAL
        else:
            self.savebtn['state'] = DISABLED

    def toggle_state_1(self,*_):
        if self.entr.var.get():
            self.addbtn['state'] = NORMAL
        else:
            self.addbtn['state'] = DISABLED

class DeleteDataDictFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # deletedictionary_start
        deletedatadict = Frame(master)
        labind = Label(deletedatadict, text="INDEX NAME ")
        labind.pack(anchor=N + W, pady=5, padx=25)
        datalistkeys = Listbox(deletedatadict, selectmode="multiple")
        dictdata = self.jsondataload()
        for i in dictdata.keys():
            datalistkeys.insert(END, i)
        datalistkeys.pack(anchor=N + W, padx=5, pady=10)
        deldatabtn = Button(deletedatadict, text="DELETE FROM DICTIONARY", command=self.deletefromdict)
        deldatabtn.pack(anchor=N + W, padx=5, pady=10)
        # deletedictionary_end
    def deletefromdict(self):
        dictdata = self.jsondataload()
        if self.datalistkeys.curselection():
            if messagebox.askquestion("Confirm", "Are you sure want to delete?") == 'yes':
                ind = self.datalistkeys.curselection()
                for i in ind[::-1]:
                    d = self.datalistkeys.get(i)
                    print(d)
                    del dictdata[d]
                    self.datalistkeys.delete(i)
                with open('/AEG/aegdataset/datajson.json', 'w') as f:
                    dictdata = json.dump(dictdata, f)

            else:
                self.datalistkeys.selection_clear(0, END)
                pass
        else:
            messagebox.showinfo("Warning", "Choose any item from list")
    def jsondataload(self):
        with open('/AEG/aegdataset/datajson.json', 'r') as f:
            z = json.load(f)
            return (z)
class UploadFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # uploadpage_start
        uploadframe = Frame(master)
        uploadframe.grid(row=0, column=0, sticky=W + E + N + S)
        uploadframe.grid_columnconfigure(0, weight=1)
        uploadframe.grid_columnconfigure(1, weight=1)
        uploadframe.grid_rowconfigure(0, weight=1)
        uploadframe.grid_rowconfigure(1, weight=1)
        uploadframe.grid_rowconfigure(2, weight=1)
        var = StringVar()
        labelaname = Label(uploadframe, textvariable=var, relief=RAISED)
        var.set("NAME OF AUTHOR : ")
        labelaname.grid(row=0, column=0, sticky=W + E + N + S)
        aname = Entry(uploadframe, bd=5)
        aname.grid(row=0, column=1, sticky=W + E + N + S)
        labeletopic = Label(uploadframe, text="TOPIC : ", relief=RAISED)
        labeletopic.grid(row=1, column=0, sticky=W + E + N + S)
        etopic = Entry(uploadframe, bd=5)
        etopic.grid(row=1, column=1, sticky=W + E + N + S)
        updbt = Button(uploadframe, text="Upload Your Essay", command=lambda: self.openf(), fg="red")
        updbt.grid(row=2, column=0, columnspan=2, sticky=W + E + N + S)

        evbtn = Button(uploadframe, text="EVALUATE")
        evbtn.grid(row=3, column=0, columnspan=2, sticky=W + E + N + S)
        # uploadpage_ends
    def openf(self):
        # print ("hlo")
        self.master.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                          filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
        if not os.path.exists('/AEG/Uploads'):
            p = Path('Uploads')
            p.mkdir(exist_ok=TRUE)
            src = self.master.filename
            dst = '/AEG/Uploads/'
            shutil.copy(src, dst)
        else:
            src = self.master.filename
            dst = "/AEG/Uploads/"
            shutil.copy(src, dst)


class ResultFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # resultpage_start
        resultframe = Frame(master)
        resultframe.grid(row=0, column=0, sticky=W + E + S + N)
        resultframe.grid_columnconfigure(0, weight=1)
        resultframe.grid_columnconfigure(1, weight=1)
        resultframe.grid_rowconfigure(0, weight=1)
        resultframe.grid_rowconfigure(1, weight=1)
        resultframe.grid_rowconfigure(2, weight=1)
        resultframe.grid_rowconfigure(3, weight=1)
        resultframe.grid_rowconfigure(4, weight=1)
        resultframe.grid_rowconfigure(5, weight=1)
        resultframe.grid_rowconfigure(6, weight=1)
        var = StringVar()
        labelename = Label(resultframe, textvariable=var, relief=RAISED)
        var.set("ESSAY NAME : ")
        labelename.grid(row=0, column=0, sticky=W + N + E + S)
        ename = Entry(resultframe, bd=5)
        ename.grid(row=0, column=1, sticky=W + N + E + S)
        labelewc = Label(resultframe, text="WORD COUNT : ", relief=RAISED)
        labelewc.grid(row=1, column=0, sticky=W + N + E + S)
        ewc = Entry(resultframe, bd=5)
        ewc.grid(row=1, column=1, sticky=W + N + E + S)
        labelesc = Label(resultframe, text="SENTENCE COUNT : ", relief=RAISED)
        labelesc.grid(row=2, column=0, sticky=W + N + E + S)
        esc = Entry(resultframe, bd=5)
        esc.grid(row=2, column=1, sticky=W + N + E + S)
        labeleerr = Label(resultframe, text="GRAMMATICAL ERRORS : ", relief=RAISED)
        labeleerr.grid(row=3, column=0, sticky=W + N + E + S)
        eerror = Entry(resultframe, bd=5)
        eerror.grid(row=3, column=1, sticky=W + N + E + S)
        labelemark = Label(resultframe, text="TOTAL MARK : ", relief=RAISED)
        labelemark.grid(row=4, column=0, sticky=W + N + E + S)
        emark = Entry(resultframe, bd=5)
        emark.grid(row=4, column=1, sticky=W + N + E + S)
        labelegrade = Label(resultframe, text="YOUR GRADE : ", relief=RAISED)
        labelegrade.grid(row=5, column=0, sticky=W + N + E + S)
        egrade = Entry(resultframe, bd=5)
        egrade.grid(row=5, column=1, sticky=W + N + E + S)
        savebtn = Button(resultframe, text="SAVE")
        savebtn.grid(row=6, column=0, columnspan=2, sticky=W + N + E + S)
        # resultpage_end


if __name__=='__main__':
    window=tk.Tk()
    main_app=MainApp(window)
    main_app.title("ESSAY AUTOMATA")
    main_app.geometry("500x400+10+20")
    main_app.mainloop()
    app.run(debug=True)