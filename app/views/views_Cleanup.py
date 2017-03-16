from django.http import HttpResponse
from rest_framework.decorators import api_view
from app.models.models import staticRecord, dynamicRecord
from django.forms.models import model_to_dict
import pandas as pd
from app.fields.standardization.standardize import Standardize
from app.fields.standardization.standardizeMethods import GeoStandardization
from app.fields.standardization.currencyStandards import CurrencyStandards


### Looks at all of the referenced proxies and underlyings for all securities, if the proxy or underlying doesn't exist
### in the database, the reference is removed.
@api_view(['GET'])
def cleanupProxiesUnderlyings(request):

    all_models = staticRecord.objects.all()
    for model in all_models:

        ### Check if Proxy Not Referenced
        if model.proxy_rcg_id != None:
            if model.proxy_rcg_id not in [loopModel.rcg_id for loopModel in all_models]:
                model.proxy_rcg_id = None
                model.save()

        ### Check if Underlying Not Referenced
        if model.underlying_rcg_id != None:
            if model.underlying_rcg_id not in [loopModel.rcg_id for loopModel in all_models]:
                model.underlying_rcg_id = None
                model.save()
    return HttpResponse('Finished')


### Sifts through static data and removes all empty space strings, "Other" values or things that might
### have accidentally slipped through the cracks and saved.
@api_view(['GET'])
def cleanupStatic(request):


    #### Standardize Currency Static Models
    all_models = staticRecord.objects.all()
    for model in all_models:


        defn = CurrencyStandards.findDefinition(model.security_name)
        if model.rcg_id == "RCG930SCB908":
            print defn
        if defn != None:

            ## Completely new model, remove old one and add new one
            if defn.rcg_id != model.rcg_id : 

                print 'New Model Definition Different - Removing old model and replacing with new model.'
                model.delete()
                newmodel = defn.generateStaticModel()
                newmodel.save()
            ### Update existing model
            else:
                ## Restandardize Model
                model = defn.standardizeStaticModel(model)
                model.save()

    for model in all_models:

        securityData = model_to_dict(model)
        updated = False
        ### Remove Null or Missing Data
        for key, value in securityData.iteritems():
            ### Set invalid strings to null
            if str(value).strip() == '' or str(value).strip().lower() == 'other':
                setattr(model, key, None)
                updated = True

        if updated: model.save()

    ### Cleanup 3 Digit Country Codes by Converting to 2 Digit
    for model in all_models:
        if model.cntry_of_risk != None and model.cntry_of_risk != "Suppress":
            cntry_of_risk = str(model.cntry_of_risk)
            if len(cntry_of_risk)>2:
                alpha2 = GeoStandardization.convertAlpha3Alpha2(cntry_of_risk)
                if alpha2 == None:
                    print 'Cannot Convert Alpha 3 : ',cntry_of_risk,' to Alpha 2'
                else:
                    model.cntry_of_risk = alpha2
                    model.save()
                
    return HttpResponse('Finished')

### Sifts through dynamic data and removes all duplicates that might have occured accidnetally
### during any phase of the update or development process.
@api_view(['GET'])
def cleanupDynamic(request):

    ### Sift Throuhg Models and Organize by RCGID
    currentDynamicModels = dynamicRecord.objects.all()

    modelDict = {}
    for model in currentDynamicModels:
        if model.rcg_id not in modelDict.keys():
            modelDict[model.rcg_id] = []
        modelDict[model.rcg_id].append(model)

    numDuplicatesRemoved = 0
    ### Sift Through Security Dynamic Models - Delete Extra Models
    for rcg_id in modelDict.keys():

        models = modelDict[rcg_id]
        dateFieldPairs = []
        for model in models:
            dateField = (pd.to_datetime(model.date), str(model.measurement_type))

            if dateField in dateFieldPairs:
                model.delete()  ### Remove Extra Model
                numDuplicatesRemoved += 1
                print 'Removed Duplicate : ', numDuplicatesRemoved
            else:
                dateFieldPairs.append(dateField)

    return HttpResponse(str(numDuplicatesRemoved) + ' Duplicates Found and Removed')


### Sifts through static models and reclassifies instrument types based on security names
### given.
@api_view(['GET'])
def smartInstrumentClassifier(request):
    
    reclassifiedInstruments = 0
    all_models = staticRecord.objects.all()
    for model in all_models:
        
        securityName = str(model.security_name)
        if securityName != None:
            
            ### Check for FX Instruments
            if 'cash' in securityName.lower() and 'collateral' in securityName.lower():
                model.instrument_type = 'FX'
                model.save()
                reclassifiedInstruments += 1 
                continue
            
            ### Check for Currency Futures
            checks = [['curr','fut'],['currency','fut'],['curr','future'],['currency','future']]
            foundNewInstrumentType=False
            for check in checks:
                if check[0] in securityName.lower() and check[1] in securityName.lower():
                        
                    model.instrument_type = 'Currency Future'
                    model.save()
                    
                    foundNewInstrumentType = True
                    reclassifiedInstruments += 1 
                    break
                
            if foundNewInstrumentType:
                continue
            
            ### Check for FX Forwards
            checks = [['fx','forward']]
            foundNewInstrumentType=False
            for check in checks:
                if check[0] in securityName.lower() and check[1] in securityName.lower():
                        
                    model.instrument_type = 'FX Forward'
                    model.search_name = None
                    model.save()
                    
                    foundNewInstrumentType = True
                    reclassifiedInstruments += 1 
                    break
                
            if foundNewInstrumentType:
                continue
            
    return HttpResponse(str(reclassifiedInstruments) + ' Instrument Types Reclassified')
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    
    