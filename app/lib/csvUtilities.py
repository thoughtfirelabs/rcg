from django.http import HttpResponse
import csv

############# Object to construct a CSV Django response from a datatable in an array format
############## Functionality for dataframes should be built in at a later point.
class csvResponse:

    def __init__(self):
        self.delimeter = ','
        self.filename = self.reportName + '.csv'
        return

    #################################
    def writeTable(self,writer):
        if hasattr(self,'headers'):
            writer.writerow(self.headers)
        for row in self.data:
            writer.writerow(row)
        return

    #################################
    def writeToCSV(self,writer=None):
        if writer == None:
            with open(self.filename, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=self.delimeter)
                self.writeTable(writer)
        else:
            self.writeTable(writer)
        return

    #################################
    def createCSVResponse(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="'+self.filename+'"'
        response['fileName']=self.filename
        writer = csv.writer(response)
        self.writeToCSV(writer=writer)
        return response

