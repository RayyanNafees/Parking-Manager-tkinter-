
from tkinter.ttk import Button,  Label, Frame, Menubutton, Button, Entry, Scrollbar, Spinbox, Style, Treeview
from tkinter import ANCHOR, E, END, N, NE, NSEW, VERTICAL, Tk, LabelFrame, Menu, StringVar, W, Toplevel, IntVar
import csv
from uuid import uuid4
from tkinter.messagebox import showinfo
import os
#* VARS:
win = Tk()
# win.geometry('400x300')
win.title('Parking Manger')
total_frames = 3
vehicles = 'Car', 'Motorcycle', 'Scooter', "Van", 'Truck'
vtype = StringVar(value='Choose Vehicle')
cost = IntVar(value=0)
h = IntVar(value=0)
m= IntVar(value=0)
duration = IntVar(value=0)
nm = StringVar()


class Window(Toplevel):
    def __init__(root, parent):
        super().__init__(parent)

        # root.geometry('300x100')
        root.title('Toplevel Window')
        columns = ('type', 'slot', 'fee',)#'time' 'duration', 'username')

        tree = Treeview(root, columns=columns, show='headings')
        # define headings
        # type, slot, fee, time, duration, username
        tree.heading('type', text='Vehicle')
        tree.heading('slot', text='Slot ID')
        tree.heading('fee', text='Parking Fee')
        # tree.heading('time', text='Start Time')
        # tree.heading('duration', text='Duration')
        # tree.heading('username', text='Customer')

        with open('db.csv', newline='') as db:
            contacts = csv.reader(db)

            # add data to the treeview
            for contact in contacts:
                tree.insert('', END, values=contact)


        def item_selected(event):
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                record = item['values']
                # show a message
                showinfo(title='Information', message=','.join(record))


        tree.bind('<<TreeviewSelect>>', item_selected)

        tree.grid(row=0, column=0, sticky='nsew')

        # add a scrollbar
        scrollbar =Scrollbar(root, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        Button(root,
                text='Close',
                command=root.destroy).pack(expand=True)

def open_csv():
    if 'db.csv' not in os.listdir():
        with open('db.csv', 'w') as db:
            writer = csv.writer(db)
            writer.writerow('type, slot, fee, time, duration, username')
        return showinfo('No Records', 'You do not have any records yet!')
    res = os.system('start excel db.csv')
    if res !=0:
        show_records()

def add_record():
    _type, _slot, _fee, _time, _duration, _username = [vtype.get(),
                                                        uuid4(),
                                                        cost.get(),
                                                        f'{h.get()}:{m.get()}',
                                                        duration.get(),
                                                        nm.get()]
    with open('db.csv', 'a+', newline='') as db:
        writer = csv.writer(db,)
        writer.writerow([_type, _slot, _fee, _time, _duration, _username])

    showinfo('Add slot', 'Parking slot added successfully !')

def show_records():
    window = Window(win)
    window.grab_set()

#* Frame 1

# Menu button 

mb = Menubutton( text='Choose vehicle', textvariable=vtype )

menu = Menu(mb, tearoff=False)

for v in vehicles:
    menu.add_radiobutton(label=v, variable=vtype)

mb['menu'] = menu 


# Label
h1 = Label(text='Parking Manager', font=('Times New ROman', 20, 'bold'), width=20, justify='center').grid(row=0, column=1, sticky=E,pady=20)

label = Label( text="Vehicle Type: ") \
        .grid(row=1, column=0, padx=10, sticky=W, pady = 5, )

fee = Label(text='Parking Fee:') \
        .grid(row=2, column=0, padx=10, sticky=W,pady = 5, )
fee_entry = Spinbox(from_=0, increment=10, to=1000, justify='left', width=6, textvariable=cost)\
        .grid(row=2, column=1, sticky=W,pady = 5)

time = Label(text='Time:')\
        .grid(row=3, column=0, padx=10, sticky=W, pady=5)
time_hr = Spinbox(from_=00, increment=1, to=23, justify='left', width=4, textvariable=h)\
        .grid(row=3, column=1, sticky=W, pady=5, columnspan=3)
colon = Label(text=':')\
        .grid(row=3, column=1, sticky=W, pady=5, padx=43 )
time_min = Spinbox(from_=00, increment=1, to=59, justify='center', width=4, textvariable=m)\
        .grid(row=3, column=1, sticky=W, pady=5, padx=50)

dur = Label(text='Duration (hr): ')\
        .grid(row=4, column=0, padx=10, sticky=W, pady=5)
dur_entry = Spinbox(from_=0, increment=1, to=36,width=5, textvariable=duration)\
        .grid(row=4, column=1, sticky=W, pady=5)

username = Label(text='Customer:')\
        .grid(row=5, column=0, padx=10, sticky=W, pady=5 )

name = Entry(textvariable=nm)\
        .grid(row=5, column=1 ,sticky=W,pady=5)

btn = Button(text='Add Slot', command=add_record)\
        .grid(row=6, column=0, padx=10, sticky=W,pady=20,)

show = Button(text='Show all slots',command=open_csv)\
        .grid(row=6, column=3, padx=10, sticky=W,pady=20,)

#* Packing
mb.grid(row=1, column=1, sticky=W, pady=5, )


win.mainloop()
