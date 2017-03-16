import datetime as dt
import pandas as pd

#### Defines the base functionality that is inherited by the different data updating and reporting views so that
#### the functinos can be accessed by multiple views.
class DataUpdate:

    def __init__(self):

        self.prepared = False

        self.refreshType = None
        self.rangeUpdate = None

        self.singleDate = None
        self.endDate = None
        self.startDate = None

        self.unique_dates = []
        self.error = False
        self.responseMessage = None
        return

    ## Determines whether or not a date given in a format is valid to be converted
    def validateDate(self, date):
        if type(date) == str:
            try:
                date = pd.to_datetime(date)
            except:
                return False
        if int(date.year) < 2016:
            return False
        return True

    #### Generates dates to loop over
    def generateLoopDates(self):

        ### Get Unique Dates Between Start and End Date
        self.unique_dates = []
        if not self.prepared:
            self.prepare()

        if self.rangeUpdate:

            delta = self.endDate - self.startDate
            for i in range(delta.days + 1):
                nextDate = self.startDate + dt.timedelta(days=i)
                self.unique_dates.append(nextDate)

        else:
            self.unique_dates = [self.singleDate]

        return

    #####################################################
    ##### Prepares the view to generate data according to the request's data
    def prepare(self):

        self.prepared = True

        self.error = False
        self.responseMessage = None

        ### Determine Range or Single Date Update
        if self.refreshType == 'single_date':
            if self.singleDate != "":
                self.rangeUpdate = False
                self.singleDate = pd.to_datetime(self.singleDate)
            else:
                self.responseMessage = 'Error : Invalid Dates'
                self.error = True
                return

        ### Update Between Dates
        elif self.refreshType == 'between_dates':
            if self.endDate != "" and self.startDate != "":

                self.endDate = pd.to_datetime(self.endDate)
                self.startDate = pd.to_datetime(self.startDate)

                if self.endDate < self.startDate:
                    self.responseMessage = 'Error : Ending Date Must be Before Start Date'
                    self.error = True
                    return

                elif self.endDate == self.startDate:
                    self.rangeUpdate = False
                    self.singleDate = self.startDate
                    return

                else:
                    self.rangeUpdate = True
                    self.generateLoopDates()
                    return
            else:
                self.responseMessage = 'Error : Invalid Dates'
                self.error = True
                return

        else:
            self.responseMessage = 'Error : Invalid Dates'
            self.error = True
            return