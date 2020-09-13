import tkinter as tk
import logging
from TreeBuilder import TreeBuilder
from TreeDrawer import TreeDrawer

class myGUI(tk.Frame):

    # This class defines the graphical user interface 

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.build_gui()    
        self.config()
        self.root.mainloop()
    def config(self):
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (self.w, self.h))

    def build_gui(self):
        canvas1 = tk.Canvas(self.root, width = 1024, height = 600)
        canvas1.pack()
        

        label1 = tk.Label(self.root, text= 'Enter number of vertices', fg='green', font=('helvetica', 12, 'bold'))

        input1 = tk.Entry(self.root, bg='white')

        button1 = tk.Button(text='Generate')
        button1.bind("<ButtonPress-1>", lambda data: TreeDrawer.generateAndDraw(input1.get())) 
    
    
        tex = tk.Text(master=self.root)

        bop = tk.Frame()
        canvas1.create_window(512, 500, window=tex)
        canvas1.create_window(512, 200, window=button1)
        canvas1.create_window(512, 120, window=label1)
        canvas1.create_window(512, 150, window=input1)

        # Create textLogger
        text_handler = TextHandler(tex)

        # Logging configuration
        logging.basicConfig(filename='test.log',
            level=logging.INFO, 
            format='%(message)s')       

        # Add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(text_handler)


class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        self.text.delete('1.0', tk.END)
        msg = self.format(record)
        def append():
            self.text.insert(tk.END, msg + '\n')
            # Autoscroll to the bottom
            self.text.see(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)
