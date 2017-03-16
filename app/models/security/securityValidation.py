################################################################################
### Missing Data Fields for Single security (i.e. assortment of fields associated with invalid
### data points for a single security Object)
class SecurityDataRecords:
    def __init__(self):
        self.missingRecords = []
        self.missingUnderlyingRecords = []
        self.missingProxyRecords = []
        return

###############################################################################
### Handles validation or invalidation of security fields.
class SecurityValidation(SecurityDataRecords):
    
    def __init__(self):
        SecurityDataRecords.__init__(self)
        return
        
    ### Validation of Static Fields - Common to All Security Models
    def validateStaticFields(self):
        
        return
        
    #####################################
    ### Notes a Missing Underlying
    def invalidateUnderlying(self):
        self.missingUnderlying = True
        return

    #####################################
    ### Notes a Missing Underlying
    def invalidateProxy(self):
        self.missingUnderlying = True
        return

    #####################################
    def invalidateProxyField(self, field_name):

        return

    #####################################
    def invalidateUnderlyingField(self, field_name):

        return
        
    #####################################
    def invalidateField(self, fieldObject):

        ### Invalidate if Field is Required for Different Calculations and is Applicable for This Security
        ### This is just a safety block, only applicable fields should be invalidated from the get go.
        if fieldObject.applicable:

            ### Create a New Data Record to Keep Track of Missign Data - Pass in Security as Self
            newDataRecord = missingDataRecord(self, fieldObject)
            newDataRecord.generateRecordID()
            ### Make Sure Record Not Already Existing in Missing Data Records
            if newDataRecord.id not in [record.id for record in self.missingDataRecords]:
                self.missingDataRecords.append(newDataRecord)

        return