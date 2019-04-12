"""
A simple Calendar-Event list-manager.
"""

import tkinter
import pickle
from os import getcwd
from os import sep
from os import path
from enum import Enum
import datetime

#----------------------------------------------PRE--------------------------------------------------

pathfile = str(getcwd() + sep + "TRICKYdata.pk")
today = datetime.datetime.now().date()
fontstyle = ("ms sans serif",11)

rootwindow = tkinter.Tk()
rootwindow.title("TRICKYcalendar")
rootwindow.geometry("-200+80")

class Genre(Enum) :
    """Types of events:
    - ONETIMERs are events which require no prepatation (like doctors appointment, ...)
    - COUNTDOWNs are events which are waited (like university exams, ...)"""
    ONETIMER = 0
    COUNTDOWN = 1

def wtfisgoinon(s) :
    """Function that prints a simple log statement to console"""
    print(" > " + s)

class Agenda_Event() :
    """Class representing an event which has:
    a date (day,month,current year)
    a name
    a description
    a genre"""
    def __init__(self,day=1,month=1,genre=Genre.ONETIMER,name="nd",description="no info") :
        self.date = (day,month)
        self.genre = genre
        self.name = name
        self.description = description 

    @property
    def date(self) :
        """The date on which the event take place (as a datetime object)"""
        return self._data

    @date.setter
    def date(self,timecoordinates) :
        day,month = timecoordinates
        try :
            self._data = datetime.date(today.year,month,day) #data
        except Exception as e :
            var_message.set("error : invalid date")
            raise e

    @property
    def day(self) :
        """The day of the event"""
        return int(self._data.day)

    @property
    def month(self) :
        """The month of the event"""
        return int(self._data.month)

    @property
    def genre(self) :
        """The nature/genere of the event, 
        which could be a one-time-only event (onetimer) or something that is waited for (countdown)"""
        return self._genere

    @genre.setter
    def genre(self,value) :
        if isinstance(value,Genre) :
            self._genere = value
        else :
            self._genere = Genre.ONETIMER

    @property
    def name(self) :
        """The name of the event"""
        return self._nome.get()

    @name.setter
    def name (self,value) :
        self._nome = tkinter.StringVar()
        self._nome.set(value)

    @property
    def description(self) :
        """The description of the event"""
        return self._info.get()

    @description.setter
    def description(self,value) :
        self._info = tkinter.StringVar()
        self._info.set(value)

    def show(self,container) :
        """Return an event as a group of widgets compatible with tkinter"""
        w = 30 #widget width
        f = tkinter.Frame(container)
        #data
        tkinter.Label(f,text=str(self.day) + '/' + str(self.month),bg='red',font=fontstyle,relief=tkinter.GROOVE,width=int(w*0.2)).grid(rowspan=2,sticky=tkinter.N+tkinter.S)
        #name
        if self.genre == Genre.COUNTDOWN :
            namebar = tkinter.Frame(f)
            tkinter.Entry(namebar,text=self._nome,bg='green',font=fontstyle,relief=tkinter.FLAT,width=int(w*0.8*0.7)).grid(row=0)
            #TODO coundown giorni
            tkinter.Label(namebar,text='-' + str((self.date-today).days) + ' giorni',bd=1,bg='red',font=fontstyle,padx=2,width=int(w*0.8*0.29)).grid(column=2,row=0)
            namebar.grid(column=2,row=0)
        else :
            tkinter.Entry(f,text=self._nome,bg='green',font=fontstyle,relief=tkinter.FLAT,width=int(w*0.8)).grid(column=2,row=0)
        #description
        tkinter.Entry(f,text=self._info,bg='blue',font=fontstyle,relief=tkinter.FLAT,width=int(w*0.8)).grid(column=2,row=1)
        return f

    def __str__(self) :
        if(isinstance(self, dict)) :
            return "(dict) " + str(self)
        else :
            return "(Event) " + str(self.date) + '\t|' + self.name + '\t|' + self.description
    
    def asdict(self) :
        return { 'giorno' : self.day , 'mese' : self.month , 'tipo' : self.genre , 'nome' : self.name , 'info' : self.description }

class Agenda(list) :
    """A list of events"""
    def __init__(self,name="") :
        self._nome = name
        list.__init__([])

    @property
    def name(self) :
        """The name of the list of event"""
        return self._nome

    def insertEvent(self,event) :
        """Insert an event in a list in cronological order"""
        #wtfisgoinon("sono in lista " + self.getnome())
        if self == [] :
            self.append(event) #the Agenda is empty, inizialize it with the Event passed
            return
        else :
            c = 0
            for e in self :
                if event.date >= e.date : #until there is a later Event, continue
                    c+=1
                else :
                    #put the event as the c-element
                    self.insert(c,event)
                    return
            #reached the end of the Agenda, put the Event as last
            self.append(event)

    def removeEvent(self,index) :
        """Remove an element in position index"""
        #wtfisgoinon("rimozione di " + str(self.geteventi()[index]))
        del self[index]

    def depklize(self) :
        """Restore the Agenda to before it was pickled (with tkinter variables)"""
        a = Agenda(self.name)
        for e in self :
            #wtfisgoinon("depickelizing " + str(e) + "\n\tdi tipo " + str(type(e)) + "\tin " + self.getnome())
            a.insertEvent(Agenda_Event(e['giorno'],e['mese'],e['tipo'],e['nome'],e['info']))
        return a

    def pklize(self) :
        """return the Agenda as a pickelizable object (every event is a dict)"""
        a = Agenda(self.name)
        for e in self :
            #wtfisgoinon("pickelizing:\t" + str(e) + "\n\tdi tipo " + str(type(e)) + "\tin " + self.name)
            a.append(e.asdict())
        return a

    def show(self,container) :
        """Return an Agenda as a list of events as widgets compatible with tkinter"""
        f = tkinter.LabelFrame(container,font=fontstyle,text=self.name)
        for r , e in enumerate(self) :
            e.show(f).grid(column=0,row=r)
        return f

    def __repr__(self) :
        s = "Agenda: " + self.name + '\n\t'
        for e in self :
            s += str(e) + '\n'
        return s

def clear(container) :
    for w in container.winfo_children() :
        w.destroy()

#----------------------------------------------------MAIN----------------------------------------------------------------

if path.exists(pathfile) and path.getsize(pathfile) > 0 :
    try :
        with open(pathfile,"rb") as  readfile:
            calendar = [ a.depklize() for a in pickle.load(readfile) ]
        #wtfisgoinon("read 'STRICKYlist.pk' in 'listaEventi'")
    except Exception as e :
        raise e
else :
    #default
    calendar=[Agenda("test")]
    calendar[0].insertEvent(Agenda_Event())

#structure of the main window
row_messages = tkinter.Frame(rootwindow)
row_commands = tkinter.Frame(rootwindow)
row_display = tkinter.Frame(rootwindow)

"""Status messages for the user"""
#column=0   row=0
var_message = tkinter.StringVar()

def clearmsg() :
    clear(row_messages)
    label_message = tkinter.Label(row_messages,textvariable=var_message)
    label_message.grid(column=0,row=0)
clearmsg()

var_message.set("Welcome, use the various entries and menus to insert the event data, then click 'INSERT' to commit.")
row_messages.grid(column=0,row=0,sticky=tkinter.W)

"""Buttons and entry to insert new events"""
#column=0   row=1
#preparing the OptionMenu widget to select the agenda in which to insert the new event
var_agendas = tkinter.StringVar()

def updateagendas() :
    list_agendas = [] #list of agendas name

    list_agendas = [a.name for a in calendar]
    option_agendas = tkinter.OptionMenu(row_commands,var_agendas,*list_agendas)

    def newagenda() :
        var_message.set("Insert new Agenda name -> ")
        entry_newagenda = tkinter.Entry(row_messages,font=fontstyle,width=20,text=var_agendas)
        entry_newagenda.grid(column=1,row=0)

    option_agendas['menu'].add_command(label="-new-",command=newagenda)
    option_agendas.grid(column=0,row=0)
updateagendas()
var_agendas.set(calendar[0].name)

#column=1   row=1
var_genre = tkinter.StringVar()
var_genre.set('Onetimer')
option_genre = tkinter.OptionMenu(row_commands,var_genre,'Onetimer','Countdown')
option_genre.grid(column=1,row=0)

#column=2   row=1
#data
frame_data = tkinter.Frame(row_commands,bg='red')
var_day = tkinter.IntVar()
var_day.set(1)
var_month = tkinter.IntVar()
var_month.set(1)
tkinter.Label(frame_data,text='DD',bg='red',font=fontstyle).grid(column=0,row=0)
tkinter.Entry(frame_data,text=var_day,bg='red',font=fontstyle,justify="right",relief=tkinter.GROOVE,width=2).grid(column=0,row=1)
tkinter.Label(frame_data,text='/\n/',bg='red',font=fontstyle).grid(column=1,row=0,rowspan=2)
tkinter.Label(frame_data,text='MM',bg='red',font=fontstyle).grid(column=2,row=0)
tkinter.Entry(frame_data,text=var_month,bg='red',font=fontstyle,justify="right",relief=tkinter.GROOVE,width=2).grid(column=2,row=1)
frame_data.grid(column=2,row=0)

#column=3   row=1
#event name
frame_info = tkinter.Frame(row_commands,bg='green')
var_name = tkinter.StringVar()
var_name.set("Nome Evento")
tkinter.Entry(frame_info,text=var_name,bd=2,bg='green',font=fontstyle,relief=tkinter.FLAT).grid(column=2,row=0)
#event description
var_desc = tkinter.StringVar()
var_desc.set("Descrizione")
tkinter.Entry(frame_info,text=var_desc,bd=2,bg='blue',font=fontstyle,relief=tkinter.FLAT).grid(column=2,row=1)
frame_info.grid(column=3,row=0)

#column=4   row=1
def insert() :
    a = var_agendas.get()
    index_agenda = None
    msg_insert = "Added Event."

    for i , c in enumerate(calendar) :
        if c.name == a :
            index_agenda = i

    if index_agenda is None :
        calendar.append(Agenda(var_agendas.get()))
        updateagendas()
        index_agenda = -1
        msg_insert = "Added Event in new Agenda"

    calendar[index_agenda].insertEvent(Agenda_Event(var_day.get() ,
                                        var_month.get() ,
                                        {'Onetimer' : Genre.ONETIMER,'Countdown' : Genre.COUNTDOWN}[var_genre.get()] ,
                                        var_name.get() ,
                                        var_desc.get() ) )

    clearmsg()
    var_message.set("Added event.")
    show(row_display,calendar)

button_add = tkinter.Button(row_commands,font=fontstyle,text="INSERT",command=insert)
button_add.grid(column=4,row=0)

#column=5   row=0
def remove() :
    clear(row_display)

    indexes = [] #mirros calendar

    for c , a in enumerate(calendar) :
        indexes.append([])
        frame_agenda = tkinter.LabelFrame(row_display,font=fontstyle,text=a.name)
        for r , e in enumerate(a) :
            indexes[c].append(tkinter.IntVar()) #one for every event
            tkinter.Checkbutton(frame_agenda,variable=indexes[c][r]).grid(column=0,row=r)
            e.show(frame_agenda).grid(column=1,row=r)
        frame_agenda.grid(column=c,row=0,sticky=tkinter.N)

    row_display.grid(column=0,row=2)

    def confirmremove() :
        for c in range(len(indexes)) :
            offset = 0
            for r in range(len(indexes[c])) :
                if indexes[c][r].get() == 1 :
                    calendar[c].removeEvent(r-offset) #remove the event from the agenda
                    offset+=1

        for i in range(len(calendar)) : #delete all agendas which are empty
            if i < len(calendar) and not calendar[i]:
                del calendar[i]
                i-=1
        updateagendas()

        clearmsg()
        var_message.set("The selected element were removed.")
        show(row_display,calendar)

    var_message.set("Select which event are to be removed, then press -> ")
    button_confirmremove = tkinter.Button(row_messages,font=fontstyle,text="CONFIRM",command=confirmremove)
    button_confirmremove.grid(column=5,row=0)


button_remove = tkinter.Button(row_commands,font=fontstyle,text="REMOVE",command=remove)
button_remove.grid(column=5,row=0)

row_commands.grid(column=0,row=1)

"""Agendas"""
#column=0   row=2
def show(container,calendar) :
    clear(container)

    for c , a in enumerate(calendar) :
        a.show(container).grid(column=c,row=0,sticky=tkinter.N)

show(row_display,calendar)

row_display.grid(column=0,row=2)

rootwindow.mainloop()

try :
    with open(pathfile,"wb") as savefile:
        pickle.dump([ a.pklize() for a in calendar ] , savefile)
    #wtfisgoinon("saved 'listaEventi' to 'STRICKYlist.pk'")
except Exception as e :
    raise e
