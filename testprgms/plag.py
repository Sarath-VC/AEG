z = self.jsondataload2()
h = z

if len(h) == 0:
    newkindex = {k: v}
    h.update(newkindex)
else:


    for indexplag in h.keys():
        flag = 0
        if indexplag == k:
            for vii in v:
                h[indexplag].append(vii)
                flag = 1
            break
        else:
            for vi in h[indexplag]:
                if vi == k:
                    for vii in v:
                        h[indexplag].append(vii)
                        flag = 1
                    break
        for viii in v:
            if indexplag == viii:
                h[indexplag].append(k)
                h[indexplag].append(v)
                flag = 1
                break
        for viiii in h[indexplag]:
            for viiiii in v:
                if viiiii == viiii:
                    h[indexplag].append(k)
                    h[indexplag].append(v)
                    flag = 1
                    break
        if flag == 0:
            newkindex = {k: v}
            print("polo")
            print(newkindex)
            h.update(newkindex)
            self.write_json2(h)
print(h)
z.update(h)
self.write_json2(z)



///////
        self.scrollbar = tk.Scrollbar(self.datalistkeys, orient="vertical",command=self.datalistkeys.yview)
        self.scrollbar.pack(side="right",fill="y")
        dictdata = self.jsondataload()
        for i in dictdata.keys():
            self.datalistkeys.insert("end", i)
        self.datalistkeys.pack(anchor="center",fill="both",expand=1)
        self.datalistkeys.config(yscrollcommand=self.scrollbar.set)

scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
self.scrollable_frame = ttk.Frame(canvas)

self.scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all"), width=495
    )
)

canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set, scrollregion=canvas.bbox("all"), height=800)

canvas.pack(side="left", fill="both", expand=True)
# scrollbar2.pack(side="bottom", fill="x")
scrollbar.pack(side="right", fill="y")

///////
frame = ScrollableFrame(self)
self.labind = tk.Label(frame.scrollable_frame, text="Available Data Dictionary", font="times", justify="center")
self.labind.grid(row=0, column=0, columnspan=3, sticky="wens")
dictdata = self.jsondataload()
iname = tk.Entry(frame.scrollable_frame, justify="center", font="times")
iname.grid(row=1, column=0, sticky="wens")
iname.insert(0, "Index Name")
iname2 = tk.Entry(frame.scrollable_frame, justify="center", font="times")
iname2.grid(row=1, column=1, sticky="wens")
iname2.insert(0, "Category")
iname3 = tk.Entry(frame.scrollable_frame, justify="center", font="times")
iname3.grid(row=1, column=2, sticky="wens")
iname3.insert(0, "Words")
r = 2
for i in dictdata.keys():
    dic1 = tk.Entry(frame.scrollable_frame, justify="center", font="times")
    dic1.grid(row=r, column=0, rowspan=3, sticky="wens")
    dic1.insert(0, i)
    dic1.config(state="disabled")
    dic2 = tk.Entry(frame.scrollable_frame, justify="center", font="times")
    dic2.grid(row=r, column=1, sticky="wens")
    dic2.insert(0, "best")
    dic2.config(state="disabled")
    dic3 = tk.Entry(frame.scrollable_frame, justify="center", font="times")
    dic3.grid(row=r + 1, column=1, sticky="wens")
    dic3.insert(0, "average")
    dic3.config(state="disabled")
    dic4 = tk.Entry(frame.scrollable_frame, justify="center", font="times")
    dic4.grid(row=r + 2, column=1, sticky="wens")
    dic4.insert(0, "common")
    dic4.config(state="disabled")
    strbest = " "
    n = len(dictdata[i]["best"])
    k = 0
    for val in dictdata[i]["best"]:
        if (k < n - 1):
            strbest = strbest + val + ", "
        else:
            strbest = strbest + val
        k = k + 1
    dic5 = tk.Text(frame.scrollable_frame, font="times", wrap="word", height=5, width=5)
    dic5.grid(row=r, column=2, sticky="wens")
    dic5.insert("insert", strbest)
    dic5.config(state="disabled")
    stravg = " "
    n = len(dictdata[i]["average"])
    k = 0
    for val in dictdata[i]["average"]:
        if (k < n - 1):
            stravg = stravg + val + ", "
        else:
            stravg = stravg + val
        k = k + 1
    dic6 = tk.Text(frame.scrollable_frame, font="times", wrap="word", height=5, width=5)
    dic6.grid(row=r + 1, column=2, sticky="wens")
    dic6.insert("insert", stravg)
    dic6.config(state="disabled")
    strcmn = " "
    n = len(dictdata[i]["common"])
    k = 0
    for val in dictdata[i]["common"]:
        if (k < n - 1):
            strcmn = strcmn + val + ", "
        else:
            strcmn = strcmn + val
        k = k + 1
    dic7 = tk.Text(frame.scrollable_frame, font="times", wrap="word", height=5, width=5)
    dic7.grid(row=r + 2, column=2, sticky="wens")
    dic7.insert("insert", strcmn)
    dic7.config(state="disabled")
    r = r + 3
frame.pack()