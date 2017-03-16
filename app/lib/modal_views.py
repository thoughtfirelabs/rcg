from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render_to_response

import pandas as pd
import json
from ..modules.portfolio_module import portfolio
from ..settings import settings

##########################################################################
### Explore Modal Views
@api_view(['GET'])
def explore_modal_base(request):
    return render_to_response('other/explore_modal.html')

@api_view(['GET'])
def explore_region(request):
    
    snapshot_date = pd.to_datetime(request.GET['snapshot_date'])
    portfolio_id = request.GET['portfolio_id']
    region_name = request.GET['region_name']
    
    p = portfolio(portfolio_id,snapshot_date)
    data = p.explore_region(region_name)
    
    return Response(json.dumps(data))

    
    
##########################################################################
### Geo Modal Views
@api_view(['GET'])
def geo_modal_base(request):
    return render_to_response('other/geo_modal.html')
    
@api_view(['GET'])
def geo_modal_data(request):
    
    snapshot_date = pd.to_datetime(request.GET['snapshot_date'])
    portfolio_id = request.GET['portfolio_id']
    
    p = portfolio(portfolio_id,snapshot_date)
    p.calculate_position_count()
    p.calculate_exposures()
    
    market_type_dict = settings().market_type_dict
    
    country_notional_codes = {}
    for key in p.country_gross_custom_notional_exposures.keys():
        code = settings().get_country_code(key)
        print(key, code)
        if code != None:
            country_notional_codes[code]=p.country_gross_custom_notional_exposures[key]
                
    em_markets = []
    frontier_markets = []
    dev_markets = []
    for key in market_type_dict.keys():
        if market_type_dict[key]=='Emerging Market':
            code = settings().get_country_code(key)
            if code != None:
                em_markets.append(code)
        elif market_type_dict[key]=='Developed Market':
            code = settings().get_country_code(key)
            if code != None:
                dev_markets.append(code)
        elif market_type_dict[key]=='Frontier Market':
            code = settings().get_country_code(key)
            if code != None:
                frontier_markets.append(code)
    
    content = json.dumps({'gross_exposure':country_notional_codes,'emerging_markets':em_markets,
                            'frontier_markets':frontier_markets,'dev_markets':dev_markets})
    return Response(content)