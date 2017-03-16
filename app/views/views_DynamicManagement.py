import sys
sys.dont_write_bytecode = True
import pandas as pd

from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import View

from app.lib.excelSafeRead import excelStringSafeLoad, excelDateSafeLoad, excelFloatSafeLoad

from app.connections import Connection
from app.settings import settings
from app.models.models import dynamicRecord
from app.lib.errorLog import ErrorLog
import json

from app.views.dataUpdateBase import DataUpdate
from app.fields.fields import Fields

from app.directoryUtilities import importDF

########################################################################
class DynamicUpdateView(View,Connection,DataUpdate):

    def __init__(self):

        Connection.__init__(self)
        DataUpdate.__init__(self)

        self.portfolios = []
        self.missingSecurityResponse = {}

        self.portIDMappings = settings.port_id_mapping
        self.portNameMapping = settings.port_name_mapping
        self.assetClassMapping = settings.asset_class_mapping

        self.errors = ErrorLog()
        return

    #### Directs the process of the view based on the request data
    def get(self, request):

        response = self.update()
        return response

    ### Updates the dynamic data from CSV file stored in J Drive
    def update(self):

        dynamic_update_data = importDF('dynamic_update', 'data', subdirPath='update_data')
        dynamic_update_data = dynamic_update_data.fillna('')

        count = 0
        ############ Loop Over Securities
        for i in range(len(dynamic_update_data.index)):

            count += 1
            row = dynamic_update_data.iloc[i, :]

            #### Safeload Date
            date = excelDateSafeLoad(row, 'date')
            if date == None or self.validateDate(date) == False:
                self.errors.add('Found Invalid Format for Date at Row : ' + str(i) + ' -> Removed from Update')
                continue

            #### Safeload RCG ID
            rcg_id = excelStringSafeLoad(row, 'rcg_id')
            if rcg_id == None:
                self.errors.add('Found Invalid Format for ID at Row : ' + str(i) + ' -> Removed from Update')
                continue

            updateString = "Security : " + rcg_id + "... " + str(count) + "/" + str(len(dynamic_update_data.index))
            print updateString

            ### (1) #### Update Dynamic Record if New Field Specified #################################################################
            missing_field = excelStringSafeLoad(row, 'missing_field')
            if missing_field == None:
                self.errors.add('Found Invalid Field Name at Row : ' + str(i) + ' -> Removed from Update')
                continue
            
            ### Get Field Obj Associated with Missing Field
            fieldObj = Fields.findStaticFieldObject(missing_field)
            if fieldObj == None:
                self.errors.add('Invalid Field Name : ' + str(missing_field) + ' at Row : '+str(i))
                continue

            ### Value will only be stored to record if it is valid
            internalFieldName = fieldObj.modelFieldName
            if internalFieldName == None:
                self.errors.add('No Model Field for  : ' + str(fieldObj.internalFieldName))
                continue
    
            ### Get Server Data Field Name
            missing_field_formatted = internalFieldName

            ### Store Dynamic Data in Record Model ##########################################################################
            dynamic_record = dynamicRecord.objects.filter(rcg_id=rcg_id, date=pd.to_datetime(date), measurement_type=missing_field_formatted).first()
            if dynamic_record == None:
                dynamic_record = dynamicRecord(rcg_id=rcg_id) ### Create New object

            ### Save Information for Dynamic Data Update if Data Valid
            update_val = excelFloatSafeLoad(row, 'missing_value')
            if update_val != None:
                dynamic_record.value = update_val
                dynamic_record.rcg_id = rcg_id
                dynamic_record.date = date
                dynamic_record.measurement_type = missing_field_formatted
                dynamic_record.save()

        self.errors.noteSuccess('Dynamic Update Successful with : ' + str(self.errors.numErrors) + ' Errors')
        responseData = self.errors.createResponseJson()
        responseData = json.dumps({'response': responseData})
        return HttpResponse(responseData)

