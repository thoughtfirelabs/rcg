from app.fields.underlyingFields import UnderlyingFields

############################################################################################################################
class UnderlyingSecurity(UnderlyingFields):

    def __init__(self,staticModel,dynamicModels):

        self.valid = True
        UnderlyingFields.__init__(self)

        self.staticModel = staticModel
        self.dynamicModels = dynamicModels

        self.rcg_id = None
        self.search_name = None
        self.security_name = None

        self.id_cusip = None
        self.id_isin = None
        self.id_sedol1 = None

        self.ss_asset_class = None
        self.asset_class = None
        self.instrument_type = None

        self.crncy_adj_mkt_cap = None
        self.volatility_162w = None
        return

    ################################
    ### Stores Data from Models to Proxy and then Validates the Use of Proxy
    def setup(self):

        ### Missing Static Model Immediately Invalidates Proxy
        if self.staticModel == None:
            self.valid = False
            return
        ### Store Static Data
        self.staticModel.attributeToSecurity(self)
        ### Store Dynamic Data
        if self.dynamicModels != None:
            for model in self.dynamicModels:
                model.attributeToSecurity(self)

        ### Validate Fields to Determine if Proxy Can Be Used (This only looks for the most
        ### basic level of information, security name, id and instrument type, it doesn't care about
        ### missing data because if data is missing it will simply not be used to supplement the main security)
        self.validateFields()

        return