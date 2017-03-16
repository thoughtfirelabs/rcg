from app.models.models import staticRecord

#############################################################################################
class StandardizedCurrency:
    def __init__(self):
        self.sector = 'Suppress'
        self.ss_asset_class = 'Spot'
        self.instrument_type = 'FX'
        self.gics_sector_name = 'Suppress'
        self.gics_industry_name = 'Suppress'
        self.issuer = 'Suppress'
        self.bics_level_3_industry_name = 'Suppress'
        return

#############################################################################################
class CurrencyDef(StandardizedCurrency):

    ###Currency name: Dollar, Pound, Ringit, Etc.##Country Desc Name: euro, brazilian, etc.
    def __init__(self, code = None, name = None, country = None, country_desc_name = None):
        self.code = code
        self.name = name
        self.country = country
        self.country_desc_name = country_desc_name
        return

    ### Standardized Properties Based on Currency Definition
    @property
    def rcg_id(self):
        return "RCG" + self.code.upper() + "999999"
    @property
    def search_name(self):
        return self.code.upper() + " Curncy"
    @property
    def security_name(self):
        return self.country_desc_name.title() + " " + self.name.title()

    @staticmethod
    def nameMeetsRequirementList(name, requirementList):
        for req in requirementList:
            if req not in name.lower():
                return False
        return True

    def fitsName(self, name):
        if 'forward' in name.lower() or 'fut' in name.lower():
            return False
        requirements = self.possibleRequirements
        for requirementSet in requirements:
            if CurrencyDef.nameMeetsRequirementList(name, requirementSet):
                return True
        return False

    def fitsID(self, rcg_id):
        if self.rcg_id == rcg_id or(self.code.upper() in rcg_id and '999' in rcg_id):
            return True
        return False

    @property
    def possibleRequirements(self):
    
        requirements = []### The appends with only one element in the list mean that the security name will have to almost equal### the string exactly.
        requirements.append([self.security_name.lower()])##['chilean peso']
        requirements.append([self.security_name.lower()])##['us dollar']
        
        requirements.append([self.code.lower()[: 2] + " " + self.name.lower()])#['usd dollar']
        requirements.append([self.code.lower() + " cash"])##['jpy cash']
        requirements.append([self.code.lower() + " collateral"])
        
        ### Multi element list appends mean the security name will have to contain all of the separate sub parts.
        requirements.append([self.code.lower(), "cash", "collateral"])
        requirements.append([self.code.lower(), "broker", "cash"])
        return requirements
    
    ### Restandardizes an already existing static model
    def standardizeHoldingModel(self, model):
    
        StandardizedCurrency.__init__(self)
    
        model.rcg_id = self.rcg_id
        model.sec_name = self.security_name.title()### Inherited
        model.ss_asset_class = self.ss_asset_class
        return model
    
    ### Restandardizes an already existing static model
    def standardizeStaticModel(self, model):
    
        StandardizedCurrency.__init__(self)
    
        model.rcg_id = self.rcg_id
        model.security_name = self.security_name.title()
        model.country_full_name = self.country.title()
        model.search_name = self.search_name
        
        ### Inherited
        model.ss_asset_class = self.ss_asset_class
        model.bics_level_3_industry_name = self.bics_level_3_industry_name
        model.issuer = self.issuer
        model.gics_industry_name = self.gics_industry_name
        model.instrument_type = self.instrument_type
        model.gics_sector_name = self.gics_sector_name
        
        return model

    ### Generates a new static model that is standardized
    def generateStaticModel(self):
    
        StandardizedCurrency.__init__(self)
        model = staticRecord()
        model = self.standardizeStaticModel(model)
    
        return model

#############################################################################################
class CurrencyStandards:

###Names that aren 't programatically determined to be associated with currencies but instead### hardcoded in .

    defaults = {
        'pound sterling': 'gbp'
    }
    
    currencyDefinitions = [
    
        CurrencyDef(code = 'aud', name = 'dollar', country = 'australia', country_desc_name = "australian"),
        CurrencyDef(code = 'usd', name = 'dollar', country = 'united states', country_desc_name = "united states"),
        CurrencyDef(code = 'cad', name = 'dollar', country = 'canada', country_desc_name = "canadian"),
    
        CurrencyDef(code = 'clp', name = 'peso', country = 'chile', country_desc_name = "chilean"),
        CurrencyDef(code = 'dkk', name = 'krone', country = 'denmark', country_desc_name = "danish"),
        CurrencyDef(code = 'hkd', name = 'dollar', country = 'hong kong', country_desc_name = "hong kong"),
        CurrencyDef(code = 'eur', name = 'currency', country = 'europe', country_desc_name = "euro"),
    
        CurrencyDef(code = 'brl', name = 'real', country = 'brazil', country_desc_name = "brazilian"),
        CurrencyDef(code = 'jpy', name = 'yen', country = 'japan', country_desc_name = "japanese"),
        CurrencyDef(code = 'idr', name = 'rupiah', country = 'indonesia', country_desc_name = "indonesian"),
        CurrencyDef(code = 'myr', name = 'ringgit', country = 'malaysia', country_desc_name = "malaysian"),
    
        CurrencyDef(code = 'nzd', name = 'dollar', country = 'new zealand', country_desc_name = "new zealand"),
        CurrencyDef(code = 'nok', name = 'krone', country = 'norway', country_desc_name = "norweigian"),
        CurrencyDef(code = 'gbp', name = 'pound', country = 'united kingdom', country_desc_name = "british"),
    
        CurrencyDef(code = 'sgd', name = 'dollar', country = 'singapore', country_desc_name = "singapore"),
        CurrencyDef(code = 'krw', name = 'won', country = 'south korea', country_desc_name = "south korean"),
        CurrencyDef(code = 'sek', name = 'krona', country = 'sweden', country_desc_name = "swedish"),
    
        CurrencyDef(code = 'chf', name = 'franc', country = 'switzerland', country_desc_name = "swiss"),
        CurrencyDef(code = 'twd', name = 'dollar', country = 'taiwan', country_desc_name = "taiwanese"),
        CurrencyDef(code = 'mxn', name = 'peso', country = 'mexico', country_desc_name = "mexican"),
    ]

    @staticmethod
    def findDefinitionForCode(code):
        for defn in CurrencyStandards.currencyDefinitions:
            if defn.code == code.lower():
                return defn
        return None
    
    @staticmethod
    def findDefinition(rcg_id, security_name):
    
        for defn in CurrencyStandards.currencyDefinitions:
            if defn.fitsName(security_name) or defn.fitsID(rcg_id):
                return defn
        return None
    
    @staticmethod
    def standardizeHoldingModel(holding_model):
    
        newHoldingModel = holding_model### Try Default First
        if holding_model.sec_name.lower() in CurrencyStandards.defaults.keys():
            code = CurrencyStandards.defaults[holding_model.sec_name.lower()]
            defn = CurrencyStandards.findDefinitionForCode(code)
            newHoldingModel = defn.standardizeHoldingModel(newHoldingModel)
            return newHoldingModel
    
        if holding_model.rcg_id != None and holding_model.sec_name != None:
            defn = CurrencyStandards.findDefinition(holding_model.rcg_id, holding_model.sec_name)
            if defn != None:
                newHoldingModel = defn.standardizeHoldingModel(newHoldingModel)
    
        return newHoldingModel