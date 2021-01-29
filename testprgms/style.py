from tkinter.ttk import *
def TButton():
    style = Style()
    style.configure('TButton', font=('calibri', 20, 'bold'), borderwidth='4')

    # Changes will be reflected
    # by the movement of mouse.
    style.map('TButton', foreground=[('active', '! disabled', 'green')],
              background=[('active', 'black')])
    return style