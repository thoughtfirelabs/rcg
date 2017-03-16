### Functions that store the various Django models to the
### Security Models
from django.forms.models import model_to_dict
from app.models.models import dynamicRecord, staticRecord, holdingRecord
import pandas as pd

class ModelStore:

    def __init__(self):
        return

    ######################################
    def storeModel(self, model):

        ### Stores Information from a Given Model to the Fields Associated Here
        ### Store dynamic model
        if isinstance(model, dynamicRecord):
            self.storeDynamicModel(model)
        ### Store static
        elif isinstance(model, staticRecord):
            self.storeStaticModel(model)
        ### Store holding model
        elif isinstance(model, holdingRecord):
            self.storeHoldingModel(model)

        return

    ## Stores static model to the object
    def storeStaticModel(self, static_record):

        recordDict = model_to_dict(static_record)
        ### Static Model, Use Date of Portfolio Snapshot to Associate With Field Model
        date = self.snapshot_date
        for key in recordDict.keys():
            ### Loop Over Other Static Fields
            for field in self.staticFieldList:
                if key in field.alternates:
                    ### Store value is a method defined in fieldManagement.py
                    if recordDict[key] != None and str(recordDict[key]) != "":
                        field.storeValue(recordDict[key], date)
        return

    ####### Stores dynamic model to the appropriate field in this object.
    def storeHoldingModel(self, model):

        ### Store Date of Holding Model with Field
        date = pd.to_datetime(model.date_held)
        ### Loop Over Model Attributes to Store
        recordDict = model_to_dict(model)
        for key in recordDict.keys():
            ### Loop Over Field Models and Find Corresponding Model
            for field in self.holdingFieldList:
                if key in field.alternates:
                    ### Store value
                    if recordDict[key] != None and str(recordDict[key]) != "":
                        ### Pass in date for non position holding data
                        if self.holdingFieldList.index(field) != 0:
                            field.storeValue(recordDict[key], date)
                        else:
                            field.storeValue(recordDict[key], date)
        return

    ####### Stores dynamic model to the appropriate field in this object.
    def storeDynamicModel(self, model):

        measType = str(model.measurement_type)  ## Measurement Type
        value = model.value
        date = pd.to_datetime(model.date)
        ### Find Corresponding Field and Save Value
        for field in self.dynamicFieldList:
            if measType in field.alternates:
                ### More recent dynamic model, udpate value for this model.
                if field.value != None and field.date <= date:
                    field.storeValue(value, date)
                ### Value hasn't been stored yet, store value and associated date if 
                ### earlier than the previous one.
                else:
                    field.storeValue(value, date)
        return

