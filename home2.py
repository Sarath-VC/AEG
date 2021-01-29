import webbrowser
from fpdf import FPDF
from tkinter import filedialog, messagebox,tix
import tkinter as tk
import os
import shutil
import string
from pathlib import Path
from aegmodel import model
from flask import Flask
from tkinter.ttk import *
import json
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import sys
import fpdf

# app=Flask(__name__)

class Checkbar(tk.Frame):
   def __init__(self, parent=None, picks=[], side="left", anchor="w"):
      tk.Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         self.var = tk.IntVar()
         self.chk = tk.Checkbutton(self, text=pick, variable=self.var,font="times")
         self.chk.pack(side=side, anchor=anchor, expand="YES")
         self.vars.append(self.var)
   def state(self):
      return map((lambda var: var.get()), self.vars)

class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.__frame=None
        self.raise_frame(MainFrame)
        self.menubarstart()
    def menubarstart(master):
        menubar = tk.Menu(master)
        master['menu']=menubar
        # self.config(menu=menubar)
        homemenu = tk.Menu(menubar, tearoff=0,bg="SlateGray3",fg="white",activeforeground="black",activebackground="white",font="times")
        homemenu.add_command(label="Dash Home",command=lambda :master.raise_frame(MainFrame))
        homemenu.add_command(label="Instruction",command=lambda: master.raise_frame(InstructionFrame))
        homemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="Home", menu=homemenu)

        dictmenu = tk.Menu(menubar, tearoff=0, bg="SlateGray3", fg="white", activeforeground="black",
                             activebackground="white", font="times")
        dictmenu.add_command(label="Create Datadictionary", command=lambda: master.raise_frame(SaveDataDictFrame))
        dictmenu.add_command(label="View Datadictionary", command=lambda: master.raise_frame(ViewDataDictFrame))
        dictmenu.add_command(label="Delete Datadictionary", command=lambda: master.raise_frame(DeleteDataDictFrame))
        menubar.add_cascade(label="Dictionary", menu=dictmenu)

        historymenu = tk.Menu(menubar, tearoff=0, bg="SlateGray3", fg="white", activeforeground="black",
                              activebackground="white", font="times")
        historymenu.add_command(label="Essay Evaluation", command=lambda: master.raise_frame(ListFrame))
        # historymenu.add_command(label="Datadictionary", command=lambda: master.raise_frame(Datadictframe))
        historymenu.add_command(label="Plagiarism Checker", command=lambda: master.raise_frame(PlagiarismFrame))
        menubar.add_cascade(label="Evaluation", menu=historymenu)

        searchmenu = tk.Menu(menubar, tearoff=0,bg="SlateGray3",fg="white",activeforeground="black",activebackground="white",font="times")
        searchmenu.add_command(label="Essay Report",command=lambda: master.raise_frame(FolderFrame))
        #searchmenu.add_command(label="Plagiarism Report", command=lambda: master.raise_frame(PlagiarismReportFrame))
        menubar.add_cascade(label="Report", menu=searchmenu)




    def raise_frame(self, frame_class):
        new_frame=frame_class(self)
        if self.__frame is not None:
            self.__frame.destroy()
        self.__frame=new_frame
        self.__frame.config(bg="SlateGray4")
        self.__frame.pack(anchor="center",fill="both", expand=True)

class MainFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        updbtm = tk.Button(self, text="Upload Your Essay",bd=3, command=lambda: self.openf1(),font="times", fg="black",bg="thistle1",relief="raised")
        updbtm.pack(anchor="center",ipadx=30,pady=150)
    def openf1(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                       filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")),multiple="TRUE")

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


class InstructionFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Frame.config(self,background="white")
        insttext=tk.Text(self)
        quote="* Essay should be uploaded in pdf format." \
              "\n* The First page of essay should contain essay topic and authorname before the start of the essay." \
              "\n* Essay should contain atmost 500 words." \
              "\n* Essay file name should be in the format of REGISTERNUMBER_ESSAYNAME." \
              "\n* Essay Format is given below.\n" \
              "\n\t________________________________________________" \
              "\n\t| [Introduction]                               |" \
              "\n\t| [Content]                                    |" \
              "\n\t| [Content]                                    |" \
              "\n\t| [Content]                                    |" \
              "\n\t| [Content]                                    |" \
              "\n\t| [Content]                                    |" \
              "\n\t| [Content]                                    |" \
              "\n\t| [Content]                                    |" \
              "\n\t| [Content]                                    |" \
              "\n\t| [Content]                                    |" \
              "\n\t| [Content]                                    |" \
              "\n\t| [Conclusion]                                 |" \
              "\n\t________________________________________________"
        insttext.insert(tk.END,quote)
        insttext.pack(fill="both", expand=True, wrap=None)
        insttext.config(state=tk.DISABLED)



class ListFrame(tk.Frame):
    def __init__(self,master):
        # listessays_start
        tk.Frame.__init__(self, master)
        #listframe = Frame(master)
        #listframe.grid(row=0, column=0, sticky=W + E + S + N)
        self.labls = tk.Label(self, text="Select topic",font="times")
        self.labls.pack()
        self.lb = tk.Listbox(self,selectmode="multiple",bd=10,width=99,font="times")
        self.v = tk.Button(self, text="Evaluate", font="times",
                           command=lambda: self.evalbtncall(self.getfilenam(), self.allstates()), bd=3, fg="black",
                           bg="thistle1", relief="raised")
        self.dltbtn = tk.Button(self, text="Delete", font="times",
                           command=lambda: self.deletefile(self.getfilenam()), bd=3, fg="black",
                           bg="thistle1", relief="raised")

        fileslist = []
        fileslist2 = []
        files = (file for file in os.listdir('/AEG/Uploads/') if os.path.isfile(os.path.join('/AEG/Uploads/', file)))
        files2 = (file for file in os.listdir('/AEG/Uploads/Evaluated/') if os.path.isfile(os.path.join('/AEG/Uploads/Evaluated/', file)))
        for file in files:
            fileslist.append(file)
        for file in files2:
            fileslist2.append(file)
        n = len(fileslist)
        m=0
        for i in range(n):
            flagme = 0
            for ii in range(len(fileslist2)):
                if fileslist[i] == fileslist2[ii]:
                    m=m+1
                    break
        n=n-m
        if n==0:
            self.lb.insert(0, "No files")
            self.lb.config(state="disabled",justify="center")
            self.v.config(state="disabled")
            self.dltbtn.config(state="disabled")
        else:
            for i in range(n):
                flagme=0
                for ii in range(len(fileslist2)):
                    if fileslist[i]==fileslist2[ii]:
                        flagme=1
                        break
                #entr = tk.Label(self, bd=3, justify="right", text=fileslist[i])
                if flagme==0:
                    self.lb.insert(i, fileslist[i])
        checklist = []
        n = 1
        distros_dict = self.jsondataload()
        self.cb = []
        self.vars = []
        for i in distros_dict.keys():
            self.var = tk.IntVar()
            self.cb.append(tk.Checkbutton(self, text=i, variable=self.var))
            self.vars.append(self.var)
        self.lng = Checkbar(self, distros_dict.keys())
        wid=self.lng.winfo_width()
        # print(wid)
        self.lng.pack()
        self.labls.config(width=wid*20)
        self.labls1 = tk.Label(self, text="Choose file",width=90,font="times")
        self.labls1.pack(pady=(10,0))
        self.lb.pack()
        self.v.pack(pady=(10,0))
        self.dltbtn.pack(pady=(10,0))
        # listessays_end
    def deletefile(self,fname):
        if messagebox.askquestion("Confirm","Do you want to delete?")=="yes":
            for fn in fname:
                os.unlink("/AEG/Uploads/"+fn)
            self.master.raise_frame(ListFrame)
        else:
            pass
    def allstates(self):
        self.li = list(self.lng.state())
        return self.li
    def getfilenam(self):
        f = []
        if self.lb.curselection():
            ind = self.lb.curselection()
            for i in ind[::-1]:
                d = self.lb.get(i)
                f.append(d)
        #print(f)
        return f

    def evalbtncall(self,f, vars):
        m = len(vars)
        flag=1
        for c in range(m):
            if vars[c] == 1:
                flag=0
        if len(f)==0:
            messagebox.showinfo("Warning", "Choose any file")
        elif flag==1:
            messagebox.showinfo("Warning","Choose topic please")
        else:
            coss={}
            filesd=[]
            for filenam in f:
                stri = "D:/AEG/Uploads/" + filenam
           #     print("calling sw")
                m = len(vars)
                self.sttnew = []
                for c in range(m):
                    if vars[c] == 1:
                        st = (self.cb[c].cget('text'))
                        self.addstr(st)#str(st)
                        # print(sttnew)
                        # print (c)
                rev = model.stopword(stri)
                #filesd.append(model.tfidf(rev, self.sttnew))
                cosss={filenam:model.tfidf(rev, self.sttnew)}
                coss.update(cosss)
          #  print(coss)
            #model.plagiarism(f)
            gramdict=model.grammarcheck(f,coss)
            # save FPDF() class into
            # a variable pdf
            pdf = FPDF()

            # Add a page
            pdf.add_page()

            # set style and size of font
            # that you want in the pdf
            pdf.add_font('DejaVu', '', '/AEG/styles/font/DejaVuSansCondensed.ttf', uni=True)
            pdf.set_font('DejaVu', '', 10)
            tot = 0
            regnum=""
            topicname=""
            # open the text file in read mode
            for key,value in coss.items():
                fullname=key
                fullnam=fullname.split("_")
                regnum=fullnam[0]
                topicname=fullnam[1].split(".")[0]
                stval=self.tostr(value)
                heading="Essay name :"+topicname
                reg="Register number : "+regnum
                pdf.cell(200, 10, txt=heading, ln=1)
                pdf.cell(200, 10, txt=reg, ln=2)
                cosstr="Word Weight Value : "+stval
                pdf.cell(200, 10, txt=cosstr, ln=3)
                w = key.split(".")
                tot=tot+value
                for key2,value2 in gramdict.items():
                    if key==key2:
                        stval2=self.tostr(value2)
                        tot=tot+value2
                        gramstr="Grammatical Score : " + stval2
                        pdf.cell(200, 10, txt=gramstr, ln=4)
                        totstr = "Total Score : " + self.tostr(tot)
                        pdf.cell(200,10,txt=totstr,ln=5)
                        pdf.cell(200, 10, txt="Grammatical Errors : ", ln=6)

                        f1 = open("D:/AEG/Reports/"+w[0]+".txt", "r")

                        # insert the texts in pdf
                        for x in f1:
                            #print(x)
                            pdf.cell(200, 10, txt=x, ln=7)

                        f1.close()
                slist=self.sttnew
                lenn=len(slist)
                self.slistnew=slist[0]
                for i in range(1,lenn):
                    self.slistnew= self.slistnew + "_" + slist[i]


                directory = self.slistnew
                if not os.path.exists('/AEG/Reports/'+ self.slistnew):
                # Parent Directory path
                    parent_dir = "/AEG/Reports/"
                    path = os.path.join(parent_dir, directory)
                    os.mkdir(path)
                    path.close()
                else:
                    pass
                pdf.output("D:/AEG/Reports/" + self.slistnew + "/" + key)
                pdf.close()
                source = "D:/AEG/Uploads/"+key
                # Destination path

                if not os.path.exists('/AEG/Uploads/Evaluated/'):
                    # Parent Directory path
                    dirname="Evaluated"
                    parent_dir = "/AEG/Uploads/"
                    path = os.path.join(parent_dir, dirname)
                    os.mkdir(path)
                    path.close()
                else:
                    pass
                # Move the content of
                # source to destination
                os.remove("D:/AEG/Reports/" + w[0] + ".txt")
                destination = "D:/AEG/Uploads/Evaluated/"
                shutil.copy(source, destination)
                # destination2 = "D:/AEG/Uploads/Evaluated/PEvaluated"
                # shutil.copy(source,destination2)
                # print("D:/AEG/Uploads/" + key)
                # os.unlink(source)

            if messagebox.showinfo("Information","Essay is evaluated")=="ok":
               if len(f)==1:
                   v = 'file://D:/AEG/Reports/' + self.slistnew + "/" + f[0]
                   webbrowser.open_new(r'' + v)
                   os.unlink("D:/AEG/Uploads/"+f[0])
                   self.master.raise_frame(ListFrame)
               else:
                   self.labls.pack_forget()
                   self.lb.pack_forget()
                   self.lng.pack_forget()
                   self.labls1.pack_forget()
                   self.v.pack_forget()
                   self.dltbtn.pack_forget()
                   # for i in f:
                   #     #print(i)
                   #     os.unlink("D:/AEG/Uploads/" + i)
                   # entrename = tk.Entry(self, bd=5, justify="right", font="times")
                   # entrename.grid(row=0, column=0, sticky="nesw")
                   # entrename.insert(0, "Search Essay By Name")
                   # searchbt = tk.Button(self, text="Search", command=lambda: self.searchFile(), bd=3, font="times",
                   #                      fg="black", bg="thistle1", relief="raised")
                   # searchbt.grid(row=0, column=1, sticky="nesw")
                   self.fileslist = []
                   self.fileslist = os.listdir('/AEG/Reports/' + self.slistnew + "/")
         #          print(self.fileslist)
                   entr = tk.Entry(self, bd=3, justify="center", font="times")
                   entr.grid(row=0, column=0, sticky="nesw", pady=(10, 0))
                   entr.insert(0, "Essay Report File")
                   entr2 = tk.Entry(self, bd=3, justify="center", font="times")
                   entr2.grid(row=0, column=1, sticky="nesw", pady=(10, 0))
                   entr2.insert(0, "Action")
                   # entr3 = tk.Entry(self, bd=3, justify="center",font="times")
                   # entr3.grid(row=1, column=2, sticky="nesw")
                   # entr3.insert(0, "Details")
                   n = len(self.fileslist)
                   for i in range(0, n):
                       for j in range(2):
                           if (j == 0):
                               entrf = tk.Entry(self, bd=3, justify="right", font="times")
                               entrf.insert(0, self.fileslist[i])
                               entrf.grid(row=i + 1, column=j, sticky="nesw")
                               # k=k+1
                           elif (j == 1):
                               str = self.fileslist[i]
                               callbt = tk.Button(self, text="View", bd=3, font="times", fg="black", bg="thistle1",relief="raised")
                               callbt.grid(row=i + 1, column=j, sticky="nesw")
                               callbt.bind('<ButtonRelease-1>', self.callme)

                           else:
                               pass
                               # searchpage_end
    def callme(self, event):
        bt = event.widget
        r = bt.grid_info()['row']
        f = self.fileslist[r - 1]
        v = 'file://D:/AEG/Reports/'+self.slistnew+'/'+f
        webbrowser.open_new(r'' + v)
            # insert the texts in pdf
                # save the pdf with name .pdf
    def addstr(self,stt):
        self.sttnew.append(stt)
    def tostr(self,sv):
        return str(sv)
    def jsondataload(self):
        with open('/AEG/aegdataset/dictionary.json', 'r') as f:
            z = json.load(f)
            return (z)

class FolderFrame(tk.Frame):
    def __init__(self,master):
        # history_start
        tk.Frame.__init__(self, master)
        self.flist=[]
        self.flistn=(file for file in os.listdir('/AEG/Reports/') if os.path.isdir(os.path.join('/AEG/Reports/', file)))
        for h in self.flistn:
            self.flist.append(h)
        i=0
        #print(self.flist)
        photo = tk.PhotoImage(file=r"/AEG/styles/f1.gif")
        # btnv = tk.Button(self,text="lolo",bg=None,).pack(side="top")

        # here, image option is used to
        # set image on button
        # Button(root, text='Click Me !', image=photo).pack(side=TOP)
        for fn in self.flist:
            self.btnv = tk.Button(self, compound="top", text=fn ,justify="center",height=3)
            self.btnv.grid(row=0,column=i,sticky="news")
            self.btnv.bind('<ButtonRelease-1>', self.callme)
            i=i+1

    def callme2(self, event):
        bt = event.widget
        r = bt.grid_info()['row']
        fil = self.fileslist[r - 1]
        v = 'file://D:/AEG/Reports/' + self.f + '/' + fil
        webbrowser.open_new(r'' + v)

    def callme(self, event):
        bt = event.widget
        c = bt.grid_info()['column']
        self.f = self.flist[c]
        #self.flist.pack_forget()
        self.btnv.pack_forget()
        # entrename = tk.Entry(self, bd=5, justify="right", font="times")
        # entrename.grid(row=0, column=0, sticky="nesw")
        # entrename.insert(0, "Search Essay By Name")
        # searchbt = tk.Button(self, text="Search", command=lambda: self.searchFile(), bd=3, font="times",
        #                      fg="black", bg="thistle1", relief="raised")
        # searchbt.grid(row=0, column=1, sticky="nesw")
        self.fileslist = []
        self.fileslist = os.listdir('/AEG/Reports/' + self.f + "/")
        #print(self.fileslist)
        if len(self.fileslist)==0:
            if messagebox.showinfo("Information","No files in this directory.")=="ok":
                self.master.raise_frame(FolderFrame)
        else:
            entr = tk.Entry(self, bd=3, justify="center", font="times")
            entr.grid(row=0, column=0, sticky="nesw")
            entr.insert(0, "Essay Report File")
            entr2 = tk.Entry(self, bd=3, justify="center", font="times")
            entr2.grid(row=0, column=1, sticky="nesw")
            entr2.insert(0, "Action")
            self.backbtn=tk.Button(self, text="Back", bd=3, font="times", fg="black", bg="thistle1",
                                           relief="raised",command=lambda :self.master.raise_frame(FolderFrame),padx=10)
            # entr3 = tk.Entry(self, bd=3, justify="center",font="times")
            # entr3.grid(row=1, column=2, sticky="nesw")
            # entr3.insert(0, "Details")
            n = len(self.fileslist)
            m=0
            for i in range(0, n):
                m=i
                for j in range(2):
                    if (j == 0):
                        entrf = tk.Entry(self, bd=3, justify="right", font="times")
                        entrf.insert(0, self.fileslist[i])
                        entrf.grid(row=i + 1, column=j, sticky="nesw")
                        # k=k+1
                    elif (j == 1):
                        str = self.fileslist[i]
                        callbt = tk.Button(self, text="View", bd=3, font="times", fg="black", bg="thistle1",
                                           relief="raised")
                        callbt.grid(row=i + 1, column=j, sticky="nesw")
                        callbt.bind('<ButtonRelease-1>', self.callme2)

                    else:
                        pass
                        # searchpage_end
            self.backbtn.grid(row=m+2, column=0,columnspan=2, sticky="nesw")

class PlagiarismFrame(tk.Frame):
    def __init__(self,master):

        # listessays_start
        tk.Frame.__init__(self, master)
        #listframe = Frame(master)
        #listframe.grid(row=0, column=0, sticky=W + E + S + N)
        self.lb = tk.Listbox(self,selectmode="multiple",width=100,bd=10,font="times")
        fileslist = []
        files = (file for file in os.listdir('/AEG/Uploads/Evaluated') if os.path.isfile(os.path.join('/AEG/Uploads/Evaluated', file)))
        for file in files:
            fileslist.append(file)
        # print(fileslist)
        n = len(fileslist)
        if n==0:
            self.lb.insert(0,"No files")
            self.lb.config(state="disabled",justify="center")
        else:
            for i in range(n):
                #entr = tk.Label(self, bd=3, justify="right", text=fileslist[i],font="times")
                self.lb.insert(i, fileslist[i])
        self.labls1 = tk.Label(self, text="Choose file",font="times",width=91)
        self.labls1.pack()
        self.lb.pack()
        self.v = tk.Button(self, text="Check similarity",font="times", command=lambda: self.evalbtncall(),bd=3, fg="black",bg="thistle1",relief="raised")
        self.v.pack(pady=(10,0))
        #self.query=tk.StringVar()
        # listessays_end
    def getfilenam(self):
        f = []
        if self.lb.curselection():
            ind = self.lb.curselection()
            for i in ind[::-1]:
                d = self.lb.get(i)
                f.append(d)
        #print(f)
        return f

    def evalbtncall(self):
        #checking_plagiarism
        # print (c)
        #self.query=model.plagiarism(self.getfilenam())
        if len(self.getfilenam())==0:
            messagebox.showinfo("Warning","Choose files")
        else:
            docs=self.retdocs()
            #print("hsda",docs)
            self.labls1.pack_forget()
            self.v.pack_forget()
            self.lb.pack_forget()
            entr = tk.Entry(self, justify="center")
            entr.grid(row=0, column=0, sticky="wnes")
            entr.insert(0, "Essay Name")
            entr2 = tk.Entry(self, justify="center",width=50)
            entr2.grid(row=0, column=1, sticky="wnes")
            entr2.insert(0, "Similar Files")
            i=1
            flag=0
            #print(docs)
            for k,v in docs.items():
                if len(v)==0:
                    pass
                else:
                    flag=1
                    entr = tk.Entry(self, justify="left")
                    entr.grid(row=i, column=0,rowspan=len(v), sticky="wnes")
                    entr.insert(0, k)
                    strsimfiles=""
                    for m in range(len(v)):
                        strsimfiles=" "+v[m]+" "
                        entr2 = tk.Entry(self,justify="left",width=50)
                        entr2.grid(row=i, column=1, sticky="wnes")
                        entr2.insert(0, strsimfiles)
                        i=i+1
                        #print(k,v)
            if flag==0:
                messagebox.showinfo("Information","No Similar Files")
                self.master.raise_frame(PlagiarismFrame)
                #i=i+1
            #self.master.raise_frame(PlagiarizedDocFrame(docs,self))
    def retdocs(self):
        simdoc=model.plagiarism(self.getfilenam())
        #print("docsdict",simdoc)
        return simdoc

    def write_json2(self, data, filename='/AEG/aegdataset/plagiarism.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def jsondataload2(self):
        with open('/AEG/aegdataset/plagiarism.json', 'r') as f:
            z = json.load(f)
            return (z)

class SaveDataDictFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # savedadadict_start
        #savedatadict = Frame(master)
        # master.config(anchor="center")
        self.lab = tk.Label(self, text="Enter Word",font="times")
        self.lab.grid(row=0,column=0,sticky="wnse")
        self.entr = tk.Entry(self)
        self.entr.grid(row=0,column=1,columnspan=2,sticky="wnse")
        self.entr.var = tk.StringVar()
        self.entr['textvariable'] = self.entr.var
        self.entr.var.trace_add('write', self.toggle_state_1)
        self.addbtn = tk.Button(self, text="Add To Dictionary", command=self.addtolist, state="disabled",font="times",bd=3, fg="black",bg="thistle1",relief="raised")
        self.addbtn.grid(row=2,column=0,columnspan=3,sticky="wnse")
        self.callme()
        self.v=tk.StringVar(self,"1")
        self.values={"Best":"1","Average":"2","Common":"3"}
        i=0
        for(text,value) in self.values.items():
            tk.Radiobutton(self,text=text,variable=self.v,value=value,font="times").grid(row=1,column=i,sticky="wnse")
            i=i+1
        self.delbtn = tk.Button(self, text="Delete From List", command=self.deletefromlist,font="times",bd=3,fg="black",bg="thistle1",relief="raised")
        self.delbtn.grid(row=4,column=0,columnspan=3,sticky="wnse")
        self.datalist = tk.Listbox(self, selectmode="multiple",font="times")
        self.datalist.grid(row=3,column=0,columnspan=3,sticky="wnse",pady=(10,0))
        self.lab1 = tk.Label(self, text="Enter Index Key",font="times")
        self.lab1.grid(row=5,column=0,sticky="wnse",pady=(10,0))
        self.entr1 = tk.Entry(self)
        self.entr1.var = tk.StringVar()
        self.entr1['textvariable'] = self.entr1.var
        self.entr1.var.trace_add('write', self.toggle_state)
        self.entr1.grid(row=5,column=1,columnspan=2,sticky="wnse",pady=(10,0))
        self.savebtn = tk.Button(self, text="Save To Dictionary", command=self.savetodict, state="disabled",font="times",bd=3, fg="black",bg="thistle1",relief="raised")
        self.savebtn.grid(row=6,column=0,columnspan=3,sticky="wnse")
        self.best=[]
        self.avg=[]
        self.com=[]
    def callme(self):
        self.best = []
        self.avg = []
        self.com = []
        # savedatadict_end
    def addtolist(self):
        textlist=""
        etv = self.entr.get()
        etv = etv.lower()
        try:
            index = self.datalist.get(0, "end").index(etv)
            self.entr.delete(0, "end")
        except ValueError:
            #print(etv)
            self.selection=self.v.get()
            if self.selection=="1":
                self.best.append(etv)
                textlist=etv+" (best)"
            elif self.selection=="2":
                self.avg.append(etv)
                textlist=etv+" (average)"
            else:
                self.com.append(etv)
                textlist=etv+" (common)"
            #print(self.selection)
            self.datalist.insert("end", textlist)
            self.entr.delete(0,"end" )


    def write_json(self,data, filename='/AEG/aegdataset/dictionary.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def savetodict(self):
        etv = self.entr1.get()
        litem = list(self.datalist.get(0, "end"))
        #print(litem)
        # s = model.synonyms_find(litem)
        # for q in s:
        #     litem.append(q)
        h = {etv:{"best":list(self.best),"average":list(self.avg),"common":list(self.com)}}
        #print(h)
        z = self.jsondataload()
        z.update(h)
        flag=0
        if messagebox.askquestion("Confirm", "Are you sure want to save?") == "yes":
            if etv.isalpha():
                for i in self.jsondataload().keys():
                    if i==etv:
                        flag=1
                        break
                if flag==0:
                    self.write_json(z)
                    self.entr1.delete(0, "end")
                    self.datalist.delete(0,"end" )
                    self.callme()
                else:
                    messagebox.showinfo("Warning","'"+etv+"' Already Exists! Please Change the Index Name.")
            else:
                messagebox.showinfo("Warning", "Dictionary name only contain characters or alphabets.")

        else:
            pass
    def jsondataload(self):
        with open('/AEG/aegdataset/dictionary.json', 'r') as f:
            z = json.load(f)
            return (z)
    def deletefromlist(self):
        if self.datalist.curselection():
            if messagebox.askquestion("Confirm", "Are you sure want to delete?") == 'yes':
                ind = self.datalist.curselection()
                for i in ind[::-1]:
                    self.datalist.delete(i)
            else:
                self.datalist.selection_clear(0, "end")
                pass
        else:
            messagebox.showinfo("Warning", "Choose any item")

    def toggle_state(self,*_):
        if self.entr1.var.get():
            self.savebtn['state'] = "normal"
        else:
            self.savebtn['state'] = "disabled"

    def toggle_state_1(self,*_):
        if self.entr.var.get():
            self.addbtn['state'] = "normal"
        else:
            self.addbtn['state'] = "disabled"
class DeleteDataDictFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # deletedictionary_start
        #deletedatadict = Frame(master)
        self.labind = tk.Label(self, text="Index Name",font="times",width=91)
        self.labind.pack(anchor="center")
        self.datalistkeys = tk.Listbox(self, selectmode="multiple",font="times",width=100,bd=10)
        dictdata = self.jsondataload()
        for i in dictdata.keys():
            self.datalistkeys.insert("end", i)
            self.datalistkeys.pack(anchor="center")
        self.deldatabtn = tk.Button(self, text="Delete From Dictionary", command=self.deletefromdict,font="times",bd=3, fg="black",bg="thistle1",relief="raised")
        self.deldatabtn.pack(anchor="center", pady=(10,0))
        # deletedictionary_end
    def deletefromdict(self):
        dictdata = self.jsondataload()
        if self.datalistkeys.curselection():
            if messagebox.askquestion("Confirm", "Are you sure want to delete?") == 'yes':
                ind = self.datalistkeys.curselection()
                for i in ind[::-1]:
                    d = self.datalistkeys.get(i)
         #           print(d)
                    del dictdata[d]
                    self.datalistkeys.delete(i)
                with open('/AEG/aegdataset/dictionary.json', 'w') as f:
                    dictdata = json.dump(dictdata, f)

            else:
                self.datalistkeys.selection_clear(0, "end")
                pass
        else:
            messagebox.showinfo("Warning", "Choose any item from list")
    def jsondataload(self):
        with open('/AEG/aegdataset/dictionary.json', 'r') as f:
            z = json.load(f)
            return (z)
class ViewDataDictFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # deletedictionary_start
        #deletedatadict = Frame(master)
        self.labind = tk.Label(self, text="Available Data Dictionary",font="times",justify="center")
        self.labind.grid(row=0, column=0,columnspan=3, sticky="wens")
        dictdata = self.jsondataload()
        iname = tk.Entry(self, justify="center",font="times")
        iname.grid(row=1, column=0, sticky="wens")
        iname.insert(0,"Index Name")
        iname2 = tk.Entry(self, justify="center",font="times")
        iname2.grid(row=1, column=1, sticky="wens")
        iname2.insert(0, "Category")
        iname3 = tk.Entry(self, justify="center", font="times")
        iname3.grid(row=1, column=2, sticky="wens")
        iname3.insert(0, "Words")
        r=2
        for i in dictdata.keys():
            dic1= tk.Entry(self, justify="center",font="times")
            dic1.grid(row=r, column=0,rowspan=3, sticky="wens")
            dic1.insert(0,i)
            dic2 = tk.Entry(self, justify="center", font="times")
            dic2.grid(row=r, column=1, sticky="wens")
            dic2.insert(0, "best")
            dic3 = tk.Entry(self, justify="center", font="times")
            dic3.grid(row=r+1, column=1, sticky="wens")
            dic3.insert(0, "average")
            dic4 = tk.Entry(self, justify="center", font="times")
            dic4.grid(row=r+2, column=1, sticky="wens")
            dic4.insert(0, "common")
            strbest=" "
            n=len(dictdata[i]["best"])
            k=0
            for val in dictdata[i]["best"]:
                if(k<n-1):
                    strbest=strbest+val+", "
                else:
                    strbest = strbest + val
                k=k+1
            dic5 = tk.Entry(self, justify="left", font="times")
            dic5.grid(row=r, column=2, sticky="wens")
            dic5.insert(0, strbest)
            stravg = " "
            n = len(dictdata[i]["average"])
            k = 0
            for val in dictdata[i]["average"]:
                if (k < n - 1):
                    stravg = stravg + val + ", "
                else:
                    stravg = stravg + val
                k = k + 1
            dic6 = tk.Entry(self, justify="left", font="times")
            dic6.grid(row=r+1, column=2, sticky="wens")
            dic6.insert(0, stravg)
            strcmn = " "
            n = len(dictdata[i]["common"])
            k = 0
            for val in dictdata[i]["common"]:
                if (k < n - 1):
                    strcmn = strcmn + val + ", "
                else:
                    strcmn = strcmn + val
                k = k + 1
            dic7 = tk.Entry(self, justify="left", font="times")
            dic7.grid(row=r+2, column=2, sticky="wens")
            dic7.insert(0, strcmn)
            r=r+3
    def jsondataload(self):
        with open('/AEG/aegdataset/dictionary.json', 'r') as f:
            z = json.load(f)
            return (z)



if __name__=='__main__':
    main_app=MainApp()
    main_app.title("ESSAY AUTOMATA")
    main_app.geometry("500x400+400+150")
    main_app.config(bg="white")
    main_app.wm_iconbitmap(bitmap = "styles/iconee.ico")

    # photo=tk.PhotoImage("styles/images.png")
    # main_app.tk.call('wm','iconphoto',main_app._w,photo)
    # main_app.iconphoto(False,"styles/images.png")
    main_app.mainloop()
    # app.run(debug=False)