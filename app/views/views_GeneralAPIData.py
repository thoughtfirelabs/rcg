from app.fields.standardization.standardizeMethods import InstrumentStandardization, SectorStandardization
from app.fields.classifications.geoClassifyDefinitions import GeoClassificationDefinitions
import json
from django.http import HttpResponse
from rest_framework.decorators import api_view

### Contains general views for getting data from the database that the front end uses at various times.

#### Gets All Possible Discrete Options for Instrument Type
@api_view(['GET'])
def get_all_instrument_types(request):

    instrumentTypes = InstrumentStandardization.discreteOptions ### Include All Instrument Types
    outputJson = json.dumps({'instrument_types': instrumentTypes})
    return HttpResponse(outputJson)


#### Gets All Possible Discrete Options for Sector
@api_view(['GET'])
def get_all_sectors(request):

    sectors = SectorStandardization.discreteOptions
    ## Formalize
    formattedSectors = []
    for sector in sectors:
        formattedSectors.append(sector.title())
    outputJson = json.dumps({'sectors': formattedSectors})
    return HttpResponse(outputJson)
    
#### Gets All Possible Discrete Options for Sector
@api_view(['GET'])
def get_all_country_names(request):

    lookup = GeoClassificationDefinitions.conversion
    countryNames = []
    for look in lookup:
        countryNames.append(look['name'])

    outputJson = json.dumps({'countryNames': countryNames})
    return HttpResponse(outputJson)
    

#### Gets All Possible Discrete Options for Sector
@api_view(['GET'])
def get_all_country_codes(request):

    lookup = GeoClassificationDefinitions.conversion
    countryCodes = []
    for look in lookup:
        countryCodes.append(look['alpha2'])

    outputJson = json.dumps({'countryCodes': countryCodes})
    return HttpResponse(outputJson)
    