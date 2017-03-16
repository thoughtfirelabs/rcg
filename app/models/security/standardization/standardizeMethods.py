from app.fields.standardization.standards import GeoStandards
from app.fields.classifications.geoClassifyDefinitions import GeoClassificationDefinitions

#############################################################################################
#### Standardizes the instrument type for each security - this is only done from the update point
#### or from an admin refresh of the data.
class InstrumentStandardization:
    
    discreteOptions = ['Bond','Bond Future','Bond Option','Callable Floater','Cash','Credit Default Swap',
                    'Currency Future','Curve','Defaulted Fixed Income','Equity','Equity ADR','Equity Future',
                       'Equity Option','Equity Warrants','FX','FX Forward','Index','Internal Equity','Preferred Stock',
                       'RMBS - Non Agency','Structured Product - Fixed','TRS']
    discreteConversion = {'Bond Future':['bond future','bond futures'],
                          'Bond Option':['bond option','bond options'],
                          'Bond':['bond'],

                          'Callable Floater':['callable floater','call floater','callable float'],
                          'Cash':['cash','dollar','usd','us dollar'],
                          'Credit Default Swap':['cds','credit default swap'],
                          'Currency Future':['currency future','fx future','currency futures','fx futures'],
                          'Curve':['curve'],
                          'Defaulted Fixed Income':['defaulted fixed income','default fixed income'],
                          
                          'Equity ADR':['equity adr','adr'],
                          'Preferred Stock':['preferred equity','preferred stock'],
                          'Equity Future':['equity future', 'equities futures', 'equities future', 'equity futures'],
                          'Equity Option':['equity option', 'equities options', 'equities option', 'equity options'],
                          'Equity Warrants':['equity warrant','equities warrant','equities warrant','equity warrants'],
                          'Internal Equity':['internal equity'],
                          'Equity':['equity','common stock','stock','equities'],

                          'FX Forward':['fx forward','currency forward','fx forwards','currency forwards'],
                          'FX':['fx','currency','spot currency','foreign exchange'],

                          'Index':['index'],
                          
                          'RMBS - Non Agency':['rmbs','abs','rmbs non agency'],
                          'Structured Product - Fixed':['structured product','structured products','structured'],
                          'TRS':['total return swap','equity swap','trs']}
    def __init__(self):
        return
    
    ### Dont need a dynamic method here that would otherwise be inherited by field object - only 
    ### standardizing instrument types on updates, not live - doesn't need to be inherited.
    @staticmethod
    def standardizeStaticModel(staticModel):
        value = staticModel.instrument_type
        if value != None:
            staticModel.instrument_type = InstrumentStandardization.standardizeInstrumentValue(value)
        return staticModel
        
    ### Called by both the static method and inherited method.
    @staticmethod
    def standardizeInstrumentValue(value):
        
        ### Value should never be suppressed or other
        if value == None:
            return value

        ## Check Directly Equal to Any Options
        for option in InstrumentStandardization.discreteConversion.keys():
            ### Check against possible sets of words
            words = InstrumentStandardization.discreteConversion[option]
            for word in words:
                if word == value.lower():
                    standardizedInstrument = option
                    return standardizedInstrument
          
        return value
                       
#############################################################################################
#### Standardizes the sector for each security.
class SectorStandardization:

    discreteOptions = ['consumer staples','consumer discretionary','energy','financials','health care',
                        'industrials','materials','information technology','telecommunication services','utilities']
    def __init__(self):
        return
        
    @staticmethod
    def standardizeStaticModel(staticModel):
        value = staticModel.gics_sector_name
        if value != None:
            staticModel.gics_sector_name = SectorStandardization.standardizeSectorValue(value)
        return staticModel
        
    ### Inherited by sector field so this references value directly.
    def standardizeSector(self):
        if self.value != None and self.value.lower() != 'suppress':
            self.value = SectorStandardization.standardizeSectorValue(self.value)
            
    ### Called by both the static method and inherited method.
    @staticmethod
    def standardizeSectorValue(value):
        
        if value.lower() == 'other' or value.lower() == 'suppress':
            return value
            
        ## Check Directly Equal to Any Options
        for option in SectorStandardization.discreteOptions:
            if option == value.lower():
                value = value.title()
                return value
                    
        
        ### Weird Exceptions - Real Estate in Financials
        if 'real' in value.lower() and 'estate' in value.lower():
            value = 'financials'.title()
            return value

        ### Non & Consumer Consumer, Multi Word Option
        for option in SectorStandardization.discrete_options:
            if 'consumer' not in option and len(option.split(' '))>1:
                firstWord = option.split(' ')[0]
                if firstWord in value.lower():
                    value = option.title()
                    return value

            elif 'consumer' in option:
                secondWord = option.split(' ')[1]
                if secondWord in value.lower():
                    value = option.title()
                    return value

        print 'Cannot Standardize Sector for : ',value
        return None

#############################################################################################
### Standardizes the Geographic Field Attributes of the Security
class GeoStandardization(GeoStandards):

    countryStandards = GeoStandards.countryStandards
    def __init__(self):
        return
    
    ### Note inherited but instead is called from the GeoStandardization static class during an update
    ### of the static data.
    @staticmethod
    def standardizeStaticModel(staticModel):
        staticModel.country_full_name = GeoStandardization.standardizeCountryFullNameValue(staticModel.country_full_name)
        return staticModel
    
    ### Static methods that allow functionality for both inherited and static classes.
    ### Called by both the static method and inherited method.
    @staticmethod
    def standardizeCountryFullNameValue(value):
        
        if value == None:
            return None
            
        if value.lower() == 'other' or value.lower() == 'suppress':
            return value
    
        for key in GeoStandardization.countryStandards.keys():
            if value.lower() == key or value.lower() in GeoStandardization.countryStandards[key]:
                value = key

        if value.lower() == 'europe':
            value = 'EU European Union'

        ### Remove Republic of and Province of Formatting
        if ',' in value:
            if 'republic of' in value.lower() or 'province of' in value.lower():
                value = value.split(',')[0].strip().title()
                
        value = value.title()
        return value
    
    ### Converts an Alpha 3 country code to alpha 2 by looking at GeoClassificationDefinitions
    @staticmethod
    def convertAlpha3Alpha2(alpha3):
        
        conv = GeoClassificationDefinitions.conversion
        for row in conv:
            if row['alpha3'].lower() == alpha3.lower():
                return row['alpha2']
        return None
        
    #######################################
    ### Inherited methods used by the fields subclassed 
    
    #####################
    ### Both live and during static update.
    def standardizeCountryFullName(self):
                    
        if self.value != None:
            if not self.suppressable:
                self.value = GeoStandardization.standardizeCountryFullNameValue(self.value)
            elif not self.suppressed:
                self.value = GeoStandardization.standardizeCountryFullNameValue(self.value)
        return
    
