### Functions to safely read valid data from model or row attributes and then return
### None for invalid data and the value for valid data.
import pandas as pd


################### Safely Reads Float Data from Model Based on Field Name
def safeReadInt(field_name,model=None,row=None):

    ##### Read Field Name from Model
    if model != None:
        ### Check if Alternate Form of Model Attribute Exists if Model Doesn't Have Field
        if hasattr(model, field_name):

            try:
                value = getattr(model,field_name)
                if value != None and str(value) != "" and 'N/A' not in str(value) and pd.isnull(value) == False:
                    try:
                        value = int(value)
                        return value
                        
                    except:
                        print 'Value : ',value,'for Field : ',field_name,' Cannot be Converted to Integer'
                        return None
                else:
                    return None
            except:
                print "Reading Model :",type(model),"Does Not Have Field Name : ",field_name
                return None
        else:
            print "Reading Model :",type(model),"Does Not Have Field Name : ",field_name
            return None
    
    ##### Read Field Name from Row
    else:
        ### Check if Alternate Form of Model Attribute Exists if Model Doesn't Have Field
        if field_name in row.keys():

            try:
                value = row[field_name]
                if value != None and str(value) != "" and 'N/A' not in str(value) and pd.isnull(value) == False:
                    try:
                        value = int(value)
                        return value
                    except:
                        print 'Value : ',value,'for Field : ',field_name,' Cannot be Converted to Integer'
                        return None
                else:
                    return None
            except:
                print 'Row Does Not Have Attribute: ',field_name
                return None
        else:
            print 'Row Does Not Have Attribute: ',field_name
            return None
            
    return
    
################### Safely Reads Float Data from Model Based on Field Name
def safeReadBool(field_name,model=None,row=None):
    
    ##### Read Field Name from Model
    if model != None:
        ### Check if Alternate Form of Model Attribute Exists if Model Doesn't Have Field
        if hasattr(model, field_name):

            try:
                value = getattr(model,field_name)
                if value != None and str(value) != "" and 'N/A' not in str(value) and pd.isnull(value) == False:
                    try:
                        value = bool(value)
                        return value
                        
                    except:
                        print 'Value : ',value,'for Field : ',field_name,' Cannot be Converted to Boolean'
                        return None
                else:
                    return None
            except:
                print "Reading Model :",type(model),"Does Not Have Field Name : ",field_name
                return None
        else:
            print "Reading Model :",type(model),"Does Not Have Field Name : ",field_name
            return None
    
    ##### Read Field Name from Row
    else:
        ### Check if Alternate Form of Model Attribute Exists if Model Doesn't Have Field
        if field_name in row.keys():

            try:
                value = row[field_name]
                if value != None and str(value) != "" and 'N/A' not in str(value) and pd.isnull(value) == False:
                    try:
                        value = bool(value)
                        return value
                    except:
                        print 'Value : ',value,'for Field : ',field_name,' Cannot be Converted to Boolean'
                        return None
                else:
                    return None
            except:
                print 'Row Does Not Have Attribute: ',field_name
                return None
        else:
            print 'Row Does Not Have Attribute: ',field_name
            return None
            
    return
    
################### Safely Reads Float Data from Model Based on Field Name
def safeReadFloat(field_name,model=None,row=None):
    
    ##### Read Field Name from Model
    if model != None:
        ### Check if Alternate Form of Model Attribute Exists if Model Doesn't Have Field
        if hasattr(model, field_name):

            try:
                value = getattr(model,field_name)
                if value != None and str(value) != "" and 'N/A' not in str(value) and pd.isnull(value) == False:
                    try:
                        value = float(value)
                        return value
                        
                    except:
                        print 'Value : ',value,'for Field : ',field_name,' Cannot be Converted to Float'
                        return None
                else:
                    return None
            except:
                print "Reading Model :",type(model),"Does Not Have Field Name : ",field_name
                return None
        else:
            print "Reading Model :",type(model),"Does Not Have Field Name : ",field_name
            return None
    
    ##### Read Field Name from Row
    else:
        ### Check if Alternate Form of Model Attribute Exists if Model Doesn't Have Field
        if field_name in row.keys():

            try:
                value = row[field_name]
                if value != None and str(value) != "" and 'N/A' not in str(value) and pd.isnull(value) == False:
                    try:
                        value = float(value)
                        return value
                        
                    except:
                        print 'Value : ',value,'for Field : ',field_name,' Cannot be Converted to Float'
                        return None
                else:
                    return None
            except:
                print 'Row Does Not Have Attribute: ',field_name
                return None
        else:
            print 'Row Does Not Have Attribute: ',field_name
            return None
            
    return
    
####################### Safely Reads Data from Model Based on Field Name
def safeReadString(field_name,model=None,row=None):
    
    validField = True

    ##### Read Field Name from Model
    if model != None:
        ### Check if Alternate Form of Model Attribute Exists if Model Doesn't Have Field
        if hasattr(model, field_name) == False:
    
            newFieldName = None
            validField = False
            
            nameAlternatives = ['sec_name','security_name']
            if field_name in nameAlternatives:
                for tempField in nameAlternatives:
                    if hasattr(model, tempField):
                        newFieldName = tempField
                        break
                        
            idAlternatives = ['sec_id','rcg_id']
            if field_name in idAlternatives:
                for tempField in idAlternatives:
                    if hasattr(model, tempField):
                        newFieldName = tempField
                        break
                        
            instrumentAlternatives = ['instrument_type','sec_type']
            if field_name in instrumentAlternatives:
                for tempField in instrumentAlternatives:
                    if hasattr(model, tempField):
                        newFieldName = tempField
                        break
        
            sectorAlternatives = ['gics_sector_name','sector']
            if field_name in sectorAlternatives:
                for tempField in sectorAlternatives:
                    if hasattr(model, tempField):
                        newFieldName = tempField
                        break
        
            industryAlternatives = ['bics_industry_subgroup','industry']
            if field_name in industryAlternatives:
                for tempField in industryAlternatives:
                    if hasattr(model, tempField):
                        newFieldName = tempField
                        break
        
            countryAlternatives = ['country_full_name','country']
            if field_name in countryAlternatives:
                for tempField in countryAlternatives:
                    if hasattr(model, tempField):
                        newFieldName = tempField
                        break
                        
            if newFieldName != None:
                validField = True
                field_name = newFieldName
            
        ### Successfully Found Alternative Valid Field for Model
        if validField:
            try:
                value = getattr(model,field_name)
                if value != None and str(value) != "" and 'N/A' not in str(value) and pd.isnull(value) == False:
                    try:
                        value = str(value)
                        return value
                        
                    except:
                        print 'Value : ',value,'for Field : ',field_name,' Cannot be Converted to String'
                        return None
                else:
                    return None
            except:
                print "Reading Model :",type(model),"Does Not Have Field Name : ",field_name
                return None
        else:
            print "Reading Model :",type(model),"Does Not Have Field Name : ",field_name
            return None
    
    ##### Read Field Name from Dataframe Row
    else:
        
        ### Check if Alternate Form of Row Attribute Exists if Row Doesn't Have Field
        if field_name not in row.keys():
    
            newFieldName = None
            validField = False
            
            nameAlternatives = ['sec_name','security_name']
            if field_name in nameAlternatives:
                for tempField in nameAlternatives:
                    if tempField in row.keys():
                        newFieldName = tempField
                        break
                        
            idAlternatives = ['sec_id','rcg_id']
            if field_name in idAlternatives:
                for tempField in idAlternatives:
                    if tempField in row.keys():
                        newFieldName = tempField
                        break
                        
            instrumentAlternatives = ['instrument_type','sec_type']
            if field_name in instrumentAlternatives:
                for tempField in instrumentAlternatives:
                    if tempField in row.keys():
                        newFieldName = tempField
                        break
        
            sectorAlternatives = ['gics_sector_name','sector']
            if field_name in sectorAlternatives:
                for tempField in sectorAlternatives:
                    if tempField in row.keys():
                        newFieldName = tempField
                        break
        
            industryAlternatives = ['bics_industry_subgroup','industry']
            if field_name in industryAlternatives:
                for tempField in industryAlternatives:
                    if tempField in row.keys():
                        newFieldName = tempField
                        break
        
            countryAlternatives = ['country_full_name','country']
            if field_name in countryAlternatives:
                for tempField in countryAlternatives:
                    if tempField in row.keys():
                        newFieldName = tempField
                        break
                        
            if newFieldName != None:
                validField = True
                field_name = newFieldName
                
        ### Successfully Found Alternative Valid Field for Model
        if validField:
            try:
                value = row[field_name]
                if value != None and str(value) != "" and 'N/A' not in str(value) and pd.isnull(value) == False:
                    try:
                        value = str(value)
                        return value
                        
                    except:
                        print 'Value : ',value,'for Field : ',field_name,' Cannot be Converted to String'
                        return None
                else:
                    return None
            except:
                print 'Row Does Not Have Attribute: ',field_name
                return None
        else:
            print 'Row Does Not Have Attribute: ',field_name
            return None
    return
