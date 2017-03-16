import sys
sys.dont_write_bytecode = True

import json
from django.http import HttpResponse
from rest_framework.decorators import api_view

from app.models.models import staticRecord

### Gets all the static securities stored in the database.
@api_view(['GET'])
def getAllSecurities(request):

    staticModels = staticRecord.objects.all()
    desiredFields = ['id_isin', 'security_name', 'search_name', 'instrument_type','country_full_name','cntry_of_risk',
                         'gics_sector_name','bics_level_3_industry_name']

    data = {}
    for model in staticModels:
        rcg_id = model.rcg_id
        data[rcg_id] = {}

        for field in desiredFields:
            data[rcg_id][field] = getattr(model, field)

        if model.proxy_rcg_id != None:
            data[rcg_id]['proxy_rcg_id'] = model.proxy_rcg_id
        if model.underlying_rcg_id != None:
            data[rcg_id]['underlying_rcg_id'] = model.underlying_rcg_id

        if model.proxy_rcg_id != None:

            proxyModel = [findModel for findModel in staticModels if findModel.rcg_id == model.proxy_rcg_id]
            if len(proxyModel) != 0:
                proxyModel = proxyModel[0]

                data[rcg_id]['proxy_security_name'] = proxyModel.security_name
                data[rcg_id]['proxy_search_name'] = proxyModel.search_name

        if model.underlying_rcg_id != None:
            underlyingModel = [findModel for model in staticModels if findModel.rcg_id == model.underlying_rcg_id]
            if len(underlyingModel) != 0:
                underlyingModel = underlyingModel[0]
                data[rcg_id]['underlying_security_name'] = underlyingModel.security_name
                data[rcg_id]['underlying_search_name'] = underlyingModel.search_name

    jsonData = json.dumps({'securityData': data})
    return HttpResponse(jsonData)

