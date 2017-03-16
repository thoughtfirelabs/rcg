import pandas as pd

######## Functions designed to read a specific field name from a row of a dataframe
#### imported frome xcel and only load valid data

############################################
def excelBoolSafeLoad(dataRow, fieldName):

    data = dataRow[fieldName] 

    error = True
    ### Check for Excel Errors
    if data != None and str(data) != "" and 'N/A' not in str(data) and pd.isnull(data) == False and str(data.lower())!='other':
        ### Check for BB Errors
        if str(data) != '#N/A Field Not Applicable' and str(data)!='#N/A N/A' and str(data) != '#N/A Invalid Security' and '#' not in str(data):
            ### First Try to Convert Directly to Bool
            try:
                data=bool(data)   
                error = False
            except ValueError:
                ### First Try to Convert to String and Then Bool
                try:
                    data=str(data)   
                    if data.lower() == 'true':
                        data=True
                        error = False
                    elif data.lower()=='false':
                        data=False
                        error = False
                ### No Help - Boolean Field is Not Valid
                except ValueError:
                    print 'Invalid Format for : ',fieldName

    if error:
        return None
    else:
        return data

############################################
def excelIntSafeLoad(dataRow, fieldName):

    data = dataRow[fieldName]

    error = True
    ### Check for Excel Errors
    if data != None and str(data) != "" and 'N/A' not in str(data) and pd.isnull(data) == False and str(data.lower())!='other':
        ### Check for BB Errors
        if str(data) != '#N/A Field Not Applicable' and str(data) != '#N/A N/A' and str(
                data) != '#N/A Invalid Security' and '#' not in str(data):
            try:
                data = int(data)
                error = False
            except ValueError:
                print 'Invalid Format for : ', fieldName

    if error:
        return None
    else:
        return data

############################################
def excelFloatSafeLoad(dataRow, fieldName):
    
    data = dataRow[fieldName] 

    error = True
    ### Check for Excel Errors
    if data != None and str(data) != "" and 'N/A' not in str(data) and pd.isnull(data) == False and str(data.lower())!='other':
        ### Check for BB Errors
        if str(data) != '#N/A Field Not Applicable' and str(data)!='#N/A N/A' and str(data) != '#N/A Invalid Security' and '#' not in str(data):
            try:
                data=float(data)   
                error = False
            except ValueError:
                print 'Invalid Format for : ',fieldName

    if error:
        return None
    else:
        return data
    
############################################
def excelStringSafeLoad(dataRow, fieldName):

    data = dataRow[fieldName] 
    error = True
    ### Check for Excel Errors
    if data != None and str(data) != "" and 'N/A' not in str(data) and pd.isnull(data) == False and str(data.lower())!='other':
        ### Check for BB Errors
        if str(data) != '#N/A Field Not Applicable' and str(data)!='#N/A N/A' and str(data) != '#N/A Invalid Security' and '#' not in str(data):
            try:
                data=str(data)   
                error = False
            except ValueError:
                print 'Invalid Format for : ',fieldName
                error = True
    
    if error:
        return None
    else:
        return data

############################################
def excelDateSafeLoad(dataRow, fieldName):
    
    data = dataRow[fieldName] 
    error = True
    ### Check for Excel Errors
    if data != None and str(data) != "" and 'N/A' not in str(data) and pd.isnull(data) == False and str(data.lower())!='other':
        ### Check for BB Errors
        if str(data) != '#N/A Field Not Applicable' and str(data)!='#N/A N/A' and str(data) != '#N/A Invalid Security' and '#' not in str(data):
            try:
                data=pd.to_datetime(data)   
                error = False
            except ValueError:
                print 'Invalid Format for : ',fieldName
                error = True
    
    if error:
        return None
    else:
        return data
                