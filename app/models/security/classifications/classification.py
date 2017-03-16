### This object is inherited by the security model so that it can classify several
### different fields.
from app.fields.classifications.geoClassifyDefinitions import GeoClassificationDefinitions

class Classification:

    def __init__(self):
        return
    
    def defaultEurope(self):
        self.MarketType.value = 'Developed Market'
        self.Region.value = 'Europe'
        self.RCGGeoBucket.value = 'Europe'
        self.Country.value = 'Europe'
        return
    ###############################
    ## Uses country of risk and country full name from bloomberg to make other geographic
    ## classifications and determinations
    def classifyGeography(self):
        
        ######################
        def findCountryNameBasedOn(search,basedOn):
            geoConversion = GeoClassificationDefinitions.conversion
            for row in geoConversion:
                if row[basedOn]==search:
                    return row['name']
            print 'Cannot Classify Country Name Based on ',basedOn,' = ',search
            return None
            
        ######################
        def findRegionNameBasedOn(search,basedOn):
            geoConversion = GeoClassificationDefinitions.conversion
            for row in geoConversion:
                if row[basedOn]==search:
                    return row['region']
            print 'Cannot Classify Region Based on ',basedOn,' = ',search
            return None
        
        ######################
        def findRCGGeoBucketBasedOn(search,basedOn):
            geoConversion = GeoClassificationDefinitions.conversion
            for row in geoConversion:
                if row[basedOn]==search:
                    return row['rcg_geo_bucket']
            print 'Cannot Classify Region Based on ',basedOn,' = ',search
            return None
        
        ######################
        def findMarketTypeBasedOn(search,basedOn):
            geoConversion = GeoClassificationDefinitions.conversion
            for row in geoConversion:
                if row[basedOn]==search:
                    return row['market_tp']
            print 'Cannot Classify Market Type Based on ',basedOn,' = ',search
            return None
        
                
        ### Check for Europe First ##########################
        if self.CountryFullName.value != None:
            if 'europe' in self.CountryFullName.value.lower():
                self.defaultEurope()
                return
        
        if self.CountryOfRisk.value != None:
            if self.CountryOfRisk.value.lower() == 'eu':
                self.defaultEurope()
                return
        
        ### Classify Using Country of Risk First       
        if self.CountryOfRisk.value != None:
            if len(self.CountryOfRisk.value)==2:
                countryName = findCountryNameBasedOn(self.CountryOfRisk.value,'alpha2')
            else:
                countryName = findCountryNameBasedOn(self.CountryOfRisk.value,'alpha3')
            if countryName != None:
                self.Country.value = countryName
                ### Use country from the conversion to classify other attributes
                self.Region.value = findRegionNameBasedOn(self.Country.value,'name')
                
                self.MarketType.value = findMarketTypeBasedOn(self.Country.value,'name')
                self.RCGGeoBucket.value = findRCGGeoBucketBasedOn(self.Country.value,'name')

        ### Try classifying based on country full name                
        elif self.CountryFullName.value != None:
            ## Try to find standardized version
            self.Country.value = self.CountryFullName.value.title()
            
            ### Try to use country from the conversion to classify other attributes
            self.Region.value = findRegionNameBasedOn(self.Country.value,'name')
            self.MarketType.value = findMarketTypeBasedOn(self.Country.value,'name')
            self.RCGGeoBucket.value = findRCGGeoBucketBasedOn(self.Country.value,'name')
        
        #### Check for Weird ETF Instances Last Thing
        if self.SecurityName.value != None:
            if 'emerging' in self.SecurityName.value.lower() and 'ishares' in self.SecurityName.value.lower():
                    self.RCGGeoBucket.value = 'Emerging Market'
                    self.MarketType.value = 'Emerging Market'
                    return
                    
        return 


    ###########################################################
    ### Classifies Security as WF Govt Cash Security
    def classifyWFCash(self):
        if self.SecurityName.value != None:
            if 'wells fargo govt' in self.SecurityName.value.lower():
                self.WFCash.activate()
        return


    ##############################################################
    ### Determines if Security is Classified as Restricted or Not
    def classifyRestricted(self):
        if self.WFCash.value == False:
            if self.Issuer.value != None:
                if 'wells' in self.Issuer.value and 'fargo' in self.Issuer.value:
                    self.Restricted.activate()
                    return


    ##############################################################
    ### Determines if self.security is Classified as Index
    def classifyIndex(self):
        
        if self.SearchName.value != None:
            if 'index' in self.SearchName.value.lower():
                self.IndexFlag.activate()
                return

        if self.SecurityName.value != None:
            name_cases = ['idx', 'index', 's+p', 'spdr', 'spi', 'topix', 'hang seng', 'cac40', 'dax', 'stoxx',
                          'ftse','msci', 'eafe']
            for name in name_cases:
                if name in self.SecurityName.value.lower():
                    self.IndexFlag.activate()
                    return
        return


    ##############################################################
    ### Determines if self.self.security is Classified as ETF
    def classifyETF(self):
        if self.SSAssetClass.value != None and self.InstrumentType.value != None:

            if 'equity' in self.InstrumentType.value.lower() or 'equity' in self.SSAssetClass.value.lower():
                if 'etf' in self.SecurityName.value.lower():
                    self.ETFFlag.activate()
                    return

        if self.SecurityName.value != None:
            if 'ishares' in self.SecurityName.value.lower():
                self.ETFFlag.activate()
                return
        return


        