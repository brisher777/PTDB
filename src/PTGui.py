'''
Created on Jun 28, 2013

@author: ben

--IDEA--
when a record is built, last_name.lower() will be the records name on disk
--END--

--LAYOUT--
    --tab 1--
        5 user input fields
        1 button to generate a record
        2 entry fields with default values and checkboxes to turn them on and off
    --popup--
        if exemptions are present, popup window with details
--END--
'''
import Tkinter as tk
import ttk
import tkMessageBox as tkm
import shelve
from PTDatabase import PTRecord

class PTGui(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent             
        self.initialize()
        self.db = shelve.open('PT_Shelve')
        
    def initialize(self):
        self.parent.title('PT Database')
        
        '''                Labels and Entries                '''
        
        self.norm_fields = ('ID', 'Name', 'Score', 'Date Tested')
        self.false_fields = ('Exemptions', 'FIP')
        self.entries = {}
        label_frame = tk.LabelFrame(self.parent, bd=2)
        for (i, label) in enumerate(self.norm_fields):         
            field_label = tk.Label(label_frame, text=label, pady=3)
            field_entry = tk.Entry(self.parent, bd=2)
            field_label.grid(row=i, column=0, sticky='w')
            field_entry.grid(row=i, column=1)
            self.entries[label] = field_entry
        
        spacer = ttk.Separator(label_frame, orient=tk.HORIZONTAL)
        spacer.grid(row=4, column=0, sticky='news')
        
        for (i, label) in enumerate(self.false_fields):
            i += 5
            entry = tk.Entry(self.parent, bd=2)
            entry.grid(row=i, column=1, sticky='we')
            self.entries[label] = entry
            self.entries[label].insert(0, 'False')
            self.entries[label].config(state='disabled')
            
            int_var = tk.IntVar()
            check = tk.Checkbutton(label_frame, text=label, anchor=tk.S)
            check.config(variable=int_var, onvalue=1, offvalue=0,
                         anchor='w', command=lambda e=entry, 
                         v=int_var: self.entry_check(e, v))
            check.grid(row=i, column=0, sticky='wes')
        
        label_frame.grid(row=0, column=0, rowspan=7, sticky='ns')
        self.entries['Date Tested'].insert(0, 'YYYY-MM-DD')
        
        fetch_button = tk.Button(self.parent, text='Fetch', width=7,
                                 command=self.fetch)
        fetch_button.grid(row=7, column=1, sticky='w')
        
        update_button = tk.Button(self.parent, text='Update', width=7,
                                  command=self.shelve_it)
        update_button.grid(row=7, column=1, sticky='e')
        
        report_button = tk.Button(self.parent, text='Report',
                                  command=self.report)
        report_button.grid(row=7, column=0, sticky='we')
    
    def fetch(self):
        ''' display the pt record of an individual '''
        
        sid = self.entries['ID'].get()
        try:
            self.db[sid]
        except:
            tkm.showerror(title='Error', message='No such ID!')
        else:
            for field in self.norm_fields + self.false_fields:
                self.entries[field].delete(0, tk.END)
                
            self.entries['ID'].insert(0, self.db[sid].ID)
            self.entries['Name'].insert(0, self.db[sid].name)
            self.entries['Score'].insert(0, self.db[sid].score)
            self.entries['Date Tested'].insert(0, self.db[sid].date_tested.strftime("%Y-%m-%d"))
            self.entries['Exemptions'].insert(0, self.db[sid].exemption)
            self.entries['FIP'].insert(0, self.db[sid].fip)
                
    def shelve_it(self):
        ''' add a record to the shelve database '''
        
        record = PTRecord(self.entries['ID'].get(), self.entries['Name'].get(),
                          self.entries['Score'].get(), self.entries['Date Tested'].get())
        self.db[record.ID] = record
        
    def report(self): 
        ''' generate a report on all individuals '''
        
        total_people = len(self.db)
        goods = {}
        excellents = {}
        sats = {}
        percent = lambda part, whole: 100 * float(part)/float(whole)
        
        for sid in self.db:
            if int(self.db[sid].score) >= 90:
                excellents[sid] = self.db[sid]
            elif int(self.db[sid].score) < 90 and int(self.db[sid].score) > 80:
                goods[sid] = self.db[sid]
            elif int(self.db[sid].score) <= 80 and int(self.db[sid].score) >= 75:
                sats[sid] = self.db[sid]
            
            if self.db[sid].dtt_int <= 31:
                print self.db[sid].name, 'needs to test this month'
                
        
        print str(percent(len(excellents), total_people)) + '% of the det is above 90%'
        print str(percent(len(goods), total_people)) + '% of the det is between 80% and 90%'
        print str(percent(len(sats), total_people)) + '% of the det is below 80%'
          
    def entry_check(self, entry, checked):
        ''' disables and enables the entries associated with a checkbox '''
        
        if checked.get() == 0:
            entry.configure(state = 'disabled')
        else:
            entry.configure(state = 'normal')
        
if __name__ == '__main__':
    root = tk.Tk()
    app = PTGui(root)
    root.mainloop()