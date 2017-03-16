import json
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from app.lib.jsonBytified import json_loads_byteified
from app.models.models import staticRecord, dynamicRecord

from app.modules.securityFactory import SecurityFactory

### Takes a static model and creates a json response containing its data for the front end.
def createSecurityDetailResponse(staticModel):

    securityData = model_to_dict(staticModel)
    outputData = {}
    ### Remove Null or Missing Data
    for key, value in securityData.iteritems():
        if value != None and str(value) != "":
            outputData[key] = str(value)

        ### Update to Keep Securities in Line
        if str(value) == "":
            setattr(staticModel,key,None)
            staticModel.save()

    return outputData


### Views to retrieve data, edit data or analyze a single security.

### Get static details for a given security id.
@api_view(['GET'])
def get_security_details(request):

    security_id = str(request.GET['security_id'])
    staticModel = staticRecord.objects.filter(rcg_id__iexact = security_id).first()
    if staticModel == None:
        outputJson = json.dumps({'error':'Error : Cannot find static record for given id.','security_details': {}})
        return HttpResponse(outputJson)
    
    security = SecurityFactory.generateFromStaticModel(staticModel)
    data = security.retrieveData()
    data['rcg_id']=security.rcg_id

    outputJson = json.dumps({'security_details': data})
    response = HttpResponse(outputJson)
    return response


### Saves static details for a given security id.
@api_view(['GET'])
def save_security_details(request):

    security_id = str(request.GET['security_id'])
    securityData = str(request.GET['data'])

    staticModel = staticRecord.objects.filter(rcg_id__iexact = security_id).first()
    if staticModel == None:
        return HttpResponseServerError('Error : Cannot find static record for given id.')

    ### Use bytify load to load JSON as String representations
    saveData = json_loads_byteified(securityData)
    if 'undefined' in saveData.keys():
        del saveData['undefined']

    ### Loop Over
    for key in saveData.keys():
        if key != "index":
            if str(saveData[key]).lower() != 'none':

                ### Make sure not to save empty data as empty string, but None instead.
                saveVal = saveData[key]
                if str(saveData[key]) == "":
                    saveVal = None

                setattr(staticModel, key, saveVal)

    staticModel.save()
    return HttpResponse('Success')


### Remove Static Security and Dynamic Security References for Static Security
### Removes the entire security from the database and removes any references to the security in other places.
@api_view(['GET'])
def removeSecurity(request):

    updateResponse = {}
    security_id = str(request.GET['security_id'])

    ### Remove Static Model
    staticModel = staticRecord.objects.filter(rcg_id__iexact=security_id).first()
    if staticModel == None:
        return HttpResponseServerError('Error : Cannot find static record for given id.')

    staticModel.delete()

    ### Remove Dynamic Models
    dynamicRecord.objects.filter(rcg_id__iexact = security_id).delete()

    ### Remove All References to Security Used as Underlying or Proxy
    for model in staticRecord.objects.all():

        if model.proxy_rcg_id == security_id:
            model.proxy_rcg_id = None
            model.save()

        if model.underlying_rcg_id == security_id:
            model.underlying_rcg_id = None
            model.save()


    updateResponse['updateSuccess'] = True
    return HttpResponse(json.dumps({'updateResponse': updateResponse}))

### Remove Underlyings and Proxies - Only removes reference  to the underlying, but doesn't remove the security iteslf.
def removeProxy(request):

    security_id = str(request.GET['security_id'])
    staticModel = staticRecord.objects.filter(rcg_id__iexact=security_id).first()
    if staticModel == None:
        return HttpResponseServerError('Error : Cannot find static record for given id.')

    staticModel.proxy_rcg_id = None
    staticModel.save()

    outputData = createSecurityDetailResponse(staticModel)
    outputJson = json.dumps({'security_details': outputData})
    response = HttpResponse(outputJson)
    return response

### Remove Underlyings and Proxies - Only removes reference  to the underlying, but doesn't remove the security iteslf.
@api_view(['GET'])
def removeUnderlying(request):

    security_id = str(request.GET['security_id'])
    staticModel = staticRecord.objects.filter(rcg_id__iexact=security_id).first()
    if staticModel == None:
        return HttpResponseServerError('Error : Cannot find static record for given id.')

    staticModel.underlying_rcg_id = None
    staticModel.save()

    outputData = createSecurityDetailResponse(staticModel)
    outputJson = json.dumps({'security_details': outputData})
    response = HttpResponse(outputJson)
    return response


### Given either a ticker or ID, this will see if we already have the specified security stored as underlying
@api_view(['GET'])
def checkIfUnderlyingExists(request):

    underlyingTickerOrID = str(request.GET['underlyingTickerOrID'])
    responseData = {}

    check = staticRecord.objects.filter(rcg_id__iexact=underlyingTickerOrID).first()
    if check == None:
        check = staticRecord.objects.filter(search_name__iexact=underlyingTickerOrID).first()
        if check == None:
            responseData['exists']=False

    if check != None:
        responseData['exists'] = True
        responseData['rcg_id'] = check.rcg_id
        responseData['search_name'] = check.search_name
        responseData['security_name'] = check.security_name
        responseData['instrument_type'] = check.instrument_type

    return HttpResponse(json.dumps({'data':responseData}))

### Given either a ticker or ID, this will see if we already have the specified security stored as proxy
@api_view(['GET'])
def checkIfProxyExists(request):

    proxyTickerOrID = str(request.GET['proxyTickerOrID'])
    responseData = {}

    check = staticRecord.objects.filter(rcg_id__iexact=proxyTickerOrID).first()
    if check == None:
        check = staticRecord.objects.filter(search_name__iexact=proxyTickerOrID).first()
        if check == None:
            responseData['exists']=False

    if check != None:
        responseData['exists'] = True
        responseData['rcg_id'] = check.rcg_id
        responseData['search_name'] = check.search_name
        responseData['security_name'] = check.security_name
        responseData['instrument_type'] = check.instrument_type

    return HttpResponse(json.dumps({'data':responseData}))

### Updates Proxy Based on Ticker Value by Checking if Proxy Already Exists
@api_view(['GET'])
def updateProxy(request):

    securityID = str(request.GET['securityID'])
    proxyID = str(request.GET['proxyID'])
    proxyTicker = str(request.GET['proxyTicker'])
    proxyName = str(request.GET['proxyName'])
    proxyInstrumentType = str(request.GET['proxyInstrumentType'])

    responseData = {}

    if str(securityID) == "":
        responseData['error'] = 'Internal Error : Missing security ID to update proxy for.'
        return HttpResponse(json.dumps({'data': responseData}))

    if str(proxyID) != "" and str(proxyTicker) != "" and str(proxyName) != "" and str(proxyInstrumentType) != "":

        ### Make Sure Proxy ID Doesn't Already Exist, If it does, don't create it, just attribute to security.
        proxyModel = staticRecord.objects.filter(rcg_id__iexact=proxyID).first()
        if proxyModel == None:
            proxyModel = staticRecord()
            proxyModel.rcg_id = proxyID
            proxyModel.search_name = proxyTicker
            proxyModel.security_name = proxyName
            proxyModel.instrument_type = proxyInstrumentType

            proxyModel.save()

        ### Attribute Created Proxy Security to Static Model
        staticModelToUpdate = staticRecord.objects.filter(rcg_id__iexact=securityID).first()
        staticModelToUpdate.proxy_rcg_id = str(proxyID)

        staticModelToUpdate.save()

        responseData['success'] = 'success'
        return HttpResponse(json.dumps({'data': responseData}))

    else:
        responseData['error'] = 'Invalid/Missing Data for Proxy'
        return HttpResponse(json.dumps({'data': responseData}))



### Updates Proxy Based on Ticker Value by Checking if Proxy Already Exists
@api_view(['GET'])
def updateUnderlying(request):

    securityID = str(request.GET['securityID'])
    underlyingID = str(request.GET['underlyingID'])
    underlyingTicker = str(request.GET['underlyingTicker'])
    underlyingName = str(request.GET['underlyingName'])
    underlyingInstrumentType = str(request.GET['underlyingInstrumentType'])

    responseData = {}

    if str(securityID) == "":
        responseData['error'] = 'Internal Error : Missing security ID to update underlying for.'
        return HttpResponse(json.dumps({'data': responseData}))

    if str(underlyingID) != "" and str(underlyingTicker) != "" and str(underlyingName) != "" and str(underlyingInstrumentType) != "":

        ### Make Sure Underlying ID Doesn't Already Exist, If it does, don't create it, just attribute to security.
        underlyingModel = staticRecord.objects.filter(rcg_id__iexact=underlyingID).first()
        if underlyingModel == None:
            underlyingModel = staticRecord()
            underlyingModel.rcg_id = underlyingID
            underlyingModel.search_name = underlyingTicker
            underlyingModel.security_name = underlyingName
            underlyingModel.instrument_type = underlyingInstrumentType

            underlyingModel.save()

        ### Attribute Created Underlying Security to Static Model
        staticModelToUpdate = staticRecord.objects.filter(rcg_id__iexact=securityID).first()
        staticModelToUpdate.underlying_rcg_id = str(underlyingID)

        staticModelToUpdate.save()

        responseData['success'] = 'success'
        return HttpResponse(json.dumps({'data': responseData}))


    else:
        responseData['error'] = 'Invalid/Missing Data for Underlying'
        return HttpResponse(json.dumps({'data': responseData}))

### Suppresses a field for a given security and returns the security details
@api_view(['GET'])
def suppressField(request):
    
    securityID = str(request.GET['securityID'])
    fieldName = str(request.GET['fieldName'])
    
    ### Get Security

    staticModel = staticRecord.objects.filter(rcg_id = securityID).first()  
    if staticModel == None:
        return HttpResponseServerError('Static record for security ID does not exist.')
    
    if fieldName == 'sector':
        staticModel.gics_sector_name = 'Suppress'
        staticModel.save()
    elif fieldName == 'industry':
        staticModel.bics_level_3_industry_name = 'Suppress'
        staticModel.save()
    elif fieldName == 'country':
        staticModel.country_full_name = 'Suppress'
        staticModel.save()
    elif fieldName == 'cntry_of_risk':
        staticModel.cntry_of_risk = 'Suppress'
        staticModel.save()
    
    ### Get Updated Security Details
    outputData = createSecurityDetailResponse(staticModel)
    outputJson = json.dumps({'security_details': outputData})
    response = HttpResponse(outputJson)
    return response

### Unsuppresses a field for a given security and returns the security details
@api_view(['GET'])
def unsuppressField(request):
    
    
    securityID = str(request.GET['securityID'])
    fieldName = str(request.GET['fieldName'])
    
    ### Get Security

    staticModel = staticRecord.objects.filter(rcg_id = securityID).first()  
    if staticModel == None:
        return HttpResponseServerError('Static record for security ID does not exist.')
    
    if fieldName == 'sector':
        staticModel.gics_sector_name = None
        staticModel.save()
    elif fieldName == 'industry':
        staticModel.bics_level_3_industry_name = None
        staticModel.save()
    elif fieldName == 'country':
        staticModel.country_full_name = None
        staticModel.save()
    elif fieldName == 'cntry_of_risk':
        staticModel.cntry_of_risk = None
        staticModel.save()
    
    ### Get Updated Security Details
    outputData = createSecurityDetailResponse(staticModel)
    outputJson = json.dumps({'security_details': outputData})
    response = HttpResponse(outputJson)
    return response
    
    
    return