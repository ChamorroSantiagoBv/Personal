from tkinter import *
from tkinter.ttk import *
from time import strftime

def actualiza_reloj():
    etiquta_hm.config(text=strftime ("%H:%M"))
    etiquta_s.config(text=strftime ("%S"))
    etiquta_fecha.config(text=strftime ("%A, %d/%m/%Y"))
    etiquta_s.after(1000, actualiza_reloj)

app = Tk()
app.title("Reloj digital")


frame_hora = Frame(app)
frame_hora.pack()
etiquta_hm=Label(frame_hora, font=("digitalk, 100"), text="H:M")
etiquta_hm.grid(row=0, column=0)

etiquta_s=Label(frame_hora, font=("digitalk, 50"), text="s")
etiquta_s.grid(row=0, column=1, sticky="n")

etiquta_fecha=Label(font=("digitalk", 50), text=" dia d/m/aaaa")
etiquta_fecha.pack(anchor="center")

actualiza_reloj()

app.mainloop()