'''
Created on Jun 28, 2013

@author: ben

--TODO LIST--
generate a report that provides all the info that is used in slideshows
--NEXT--
check dates and notify me when we enter a month that someone needs to test in
--NEXT--
--END--
'''

import datetime as dt
import tkMessageBox as tkm

class PTRecord():
    def __init__(self, ID, name, score, date_tested, exemption=False, fip=False):
        self.ID = ID
        self.name = name
        self.score = score
        self.fip = fip
        self.exemption = exemption
        self.ONE_YEAR = dt.timedelta(days=365)
        self.SIX_MONTHS = dt.timedelta(days=180)
        self.TODAY = dt.datetime.today()
        
        try:
            self.date_tested = dt.datetime.strptime(date_tested, '%Y-%m-%d')
        except ValueError:
            tkm.showerror(title='Error', message='Make sure your date format is YYYY-MM-DD, then try again')
            
        if int(self.score) < 90:
            self.next_test = (self.date_tested + self.SIX_MONTHS)
        elif self.score >= 90:
            self.next_test = (self.date_tested + self.ONE_YEAR)
            
        self.days_til_test = self.next_test - self.TODAY
        self.dtt_int = int(str(self.days_til_test)[:3])
    
    def __str__(self):
        ''' overload default print method with custom format '''
        
        return '''Name: %s\nScore: %s\nDate Tested: %s\nNext Test Date: %s\nDays to go: %s''' % \
        (self.name, self.score, self.date_tested.strftime("%A, %d %B %Y"), 
         self.next_test.strftime("%A, %d %B %Y"), str(self.days_til_test)[:8])
        