from app.fields.standardization.standardizeMethods import SectorStandardization, GeoStandardization, InstrumentStandardization
from app.fields.standardization.currencyStandards import CurrencyStandards

###### Base standardization class that all other standardizations flow through.
class Standardize(GeoStandardization,SectorStandardization):
    
    ### These are performed on holding models before they are transformed into static models.
    holdingModelStandards = [CurrencyStandards]
    currencyStandardizationTechniques = []
    staticStandardizationTechniques = [SectorStandardization,GeoStandardization,InstrumentStandardization]
    
    def __init__(self):
        GeoStandardization.__init__(self)
        SectorStandardization.__init__(self)
    
    ####### Standardized during State Street Holdings Update
    @staticmethod
    def standardizeHoldingModel(holdingModel):
        ### Standardize holding model for each standardization technique.
        for std in Standardize.holdingModelStandards:
            holdingModel = std.standardizeHoldingModel(holdingModel)
        return holdingModel
    
    ###### Standardized during a data update from Bloomberg or other editing security method in front end.
    @staticmethod
    def standardizeStaticModel(staticModel):
        
        ### Standardize holding model for each standardization technique.
        for technique in Standardize.staticStandardizationTechniques:
            staticModel = technique.standardizeStaticModel(staticModel)
        return staticModel

    ###### Standardized Live on Application Run
    
    ### This is inherited by individual field models - this standardization is done live, during app run,
    ### unlike the previous two methods which are done during updates/refreshses of the data.
    def standardize(self):
        
        fieldName = self.__class__.__name__
        
        ### Geography Security Standardizations
        if fieldName == 'CountryFullName':
            self.standardizeCountryFullName()

        elif fieldName == 'CountryOfRisk':
            self.standardizeCountryOfRisk()
            
        elif fieldName == 'Region': 
            self.standardizeRegion()
            
        elif fieldName == 'MarketType':
            self.standardizeMarketType()
            
        elif fieldName == 'RCGGeoBucket':
            self.standardizeRCGGeoBucket()
        
        elif fieldName == 'Country':
            self.standardizeCountry()

        ### Sector/Industry Stnadardizations
        elif fieldName == 'Sector':
            self.standardizeSector()
        
        return 
        
    
