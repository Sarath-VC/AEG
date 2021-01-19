class ResultFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # resultpage_start
        #resultframe = Frame(master)
        var = tk.StringVar()
        labelename = tk.Label(self, textvariable=var, relief="raised",font="times")
        var.set("Essay Name : ")
        labelename.grid(row=0, column=0, sticky="wnes")
        ename = tk.Entry(self, bd=5)
        ename.grid(row=0, column=1, sticky="wnes")
        labelewc = tk.Label(self, text="Word Count : ", relief="raised",font="times")
        labelewc.grid(row=1, column=0, sticky="wnes")
        ewc = tk.Entry(self, bd=5)
        ewc.grid(row=1, column=1, sticky="wnes")
        labelesc = tk.Label(self, text="Sentence Count : ", relief="raised",font="times")
        labelesc.grid(row=2, column=0, sticky="wnes")
        esc = tk.Entry(self, bd=5)
        esc.grid(row=2, column=1, sticky="wnes")
        labeleerr = tk.Label(self, text="Grammatical Errors : ", relief="raised",font="times")
        labeleerr.grid(row=3, column=0, sticky="wnes")
        eerror = tk.Entry(self, bd=5)
        eerror.grid(row=3, column=1, sticky="wnes")
        labelemark = tk.Label(self, text="Total Mark : ", relief="raised",font="times")
        labelemark.grid(row=4, column=0, sticky="wnes")
        emark = tk.Entry(self, bd=5)
        emark.grid(row=4, column=1, sticky="wnes")
        labelegrade = tk.Label(self, text="Grade : ", relief="raised",font="times")
        labelegrade.grid(row=5, column=0, sticky="wnes")
        egrade = tk.Entry(self, bd=5)
        egrade.grid(row=5, column=1, sticky="wnes")
        savebtn = tk.Button(self, text="Save",font="times",bd=3, fg="black",bg="thistle1",relief="raised")
        savebtn.grid(row=6, column=0, columnspan=2, sticky="wnes", pady=(10,0))
        # resultpage_end
class UploadFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        # uploadpage_start
        #uploadframe = Frame(master)
        # self.grid(row=0, column=0, sticky="wens")
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_rowconfigure(2, weight=1)
        var = tk.StringVar()
        labelaname = tk.Label(self, textvariable=var, relief="raised")
        var.set("Name Of Author : ")
        labelaname.grid(row=0, column=0, sticky="wens")
        aname = tk.Entry(self, bd=5)
        aname.grid(row=0, column=1, sticky="wens")
        labeletopic = tk.Label(self, text="Topic : ", relief="raised")
        labeletopic.grid(row=1, column=0, sticky="wens")
        etopic = tk.Entry(self, bd=5)
        etopic.grid(row=1, column=1, sticky="wens")
        updbt = tk.Button(self, text="Upload Your Essay", command=lambda: self.openf(), fg="red")
        updbt.grid(row=2, column=0, columnspan=2, sticky="wens")

        evbtn = tk.Button(self, text="Evaluate")
        evbtn.grid(row=3, column=0, columnspan=2, sticky="wens")
        # uploadpage_ends
    def openf(self):
        # print ("hlo")
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                          filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
        if not os.path.exists('/AEG/Uploads'):
            p = Path('Uploads')
            p.mkdir(exist_ok="true")
            src = filename
            dst = '/AEG/Uploads/'
            shutil.copy(src, dst)
        else:
            src = self.master.filename
            dst = "/AEG/Uploads/"
            shutil.copy(src, dst)

class HistoryFrame(tk.Frame):
    def __init__(self,master):
        # history_start
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0, sticky="wnes")
        entr = tk.Entry(self, bd=3, justify="center")
        entr.grid(row=0, column=0, sticky="wens")
        entr.insert(0, "Essay Name")
        entr2 = tk.Entry(self, bd=3, justify="center")
        entr2.grid(row=0, column=1, sticky="wnes")
        entr2.insert(0, "Grade")
        entr3 = tk.Entry(self, bd=3, justify="center")
        entr3.grid(row=0, column=2, sticky="wnes")
        entr3.insert(0, "Details")
        n = 5
        for i in range(1, n + 1):
            for j in range(3):
                entr = tk.Entry(self, bd=3, justify="right")
                entr.grid(row=i, column=j, sticky="wnes")
        # history_end
class SearchFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        self.place(anchor="center")
        # searchpage_start
        #searchframe = tk.Frame(master)
        #searchframe.grid(row=0, column=0, sticky="WESN")
        entrename = tk.Entry(self, bd=5, justify="right",font="times")
        entrename.grid(row=0, column=0, sticky="nesw")
        entrename.insert(0, "Search Essay By Name")
        searchbt = tk.Button(self, text="Search", command=lambda: self.searchFile(),bd=3,font="times", fg="black",bg="thistle1",relief="raised")
        searchbt.grid(row=0, column=1, sticky="nesw")
        self.fileslist = []
        self.fileslist = os.listdir('/AEG/Reports/')
        entr = tk.Entry(self, bd=3, justify="center",font="times")
        entr.grid(row=1, column=0, sticky="nesw",pady=(10,0))
        entr.insert(0, "Essay Report File")
        entr2 = tk.Entry(self, bd=3, justify="center",font="times")
        entr2.grid(row=1, column=1, sticky="nesw",pady=(10,0))
        entr2.insert(0, "Action")
        # entr3 = tk.Entry(self, bd=3, justify="center",font="times")
        # entr3.grid(row=1, column=2, sticky="nesw")
        # entr3.insert(0, "Details")
        n = len(self.fileslist)
        for i in range(0, n):
            for j in range(2):
                if (j==0):
                    entrf = tk.Entry(self, bd=3, justify="right",font="times")
                    entrf.insert(0, self.fileslist[i])
                    entrf.grid(row=i+2, column=j, sticky="nesw")
                    #k=k+1
                elif (j==1):
                    str= self.fileslist[i]
                    callbt = tk.Button(self, text="View",bd=3, font="times",fg="black", bg="thistle1", relief="raised")
                    callbt.grid(row=i+2, column=j, sticky="nesw")
                    callbt.bind('<ButtonRelease-1>',self.callme)
                else:
                    pass
        # searchpage_end
    def callme(self,event):
        bt=event.widget
        r=bt.grid_info()['row']
        f=self.fileslist[r-2]
        v='file://D:/AEG/Reports/'
        v=v+f
        webbrowser.open_new(r''+v)
    def searchFile(self):
        print("hjk")
