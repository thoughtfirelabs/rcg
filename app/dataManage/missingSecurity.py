from app.models.models import staticRecord

####################################################
class MissingSecurity:
    ### Initialize missing security from the holding model.
    def __init__(self,rcg_id):

        self.rcg_id = rcg_id
        self.security_name = None
        self.instrument_type = None
        self.ss_asset_class = None
        self.id_isin = None
        self.search_name = None
        self.proxy_rcg_id = None
        self.underlying_rcg_id = None

        self.proxyMissing = False
        self.underlyingMissing = False
        return

    ### Check if Security is Completely Missing from Static DB
    @staticmethod
    def isCompletelyMissing(rcg_id,allStaticModels):
        for model in allStaticModels:
            if model.rcg_id == rcg_id:
                return False
        return True

    ### Determine if static model is missing any required data, and if the static model
    ### has a proxy that is either missing or missing any static data.
    @staticmethod
    def isMissingData(staticModel):

        ### Check if Security is Completely Missing from Static DB
        ### Check if Missing Vital Attributes
        requiredAttributes = ['instrument_type','security_name']
        for attr in requiredAttributes:
            if getattr(staticModel,attr) == None:
                return True
        return False

    ### Store data to MissingSecurity if the staticModel is missing vital information
    def storeDataFromStatic(self, staticModel):

        if staticModel.security_name != None:
            self.security_name = str(staticModel.security_name)

        if staticModel.ss_asset_class != None:
            self.ss_asset_class = str(staticModel.ss_asset_class)

        if staticModel.id_isin != None:
            self.id_isin = str(staticModel.id_isin)

        if staticModel.rcg_id != None:
            self.rcg_id = str(staticModel.rcg_id)

        if staticModel.proxy_rcg_id != None:
            self.proxy_rcg_id = str(staticModel.proxy_rcg_id)

        if staticModel.underlying_rcg_id != None:
            self.underlying_rcg_id = str(staticModel.underlying_rcg_id)

        if staticModel.search_name != None:
            self.search_name = str(staticModel.search_name)

        if staticModel.instrument_type != None:
            self.instrument_type = str(staticModel.instrument_type)

        return

    ### Store data to MissingSecurity model associated with the holding model.
    def storeDataFromHolding(self, holdingModel):

        if holdingModel.security_name != None:
            self.security_name = str(holdingModel.security_name)

        if holdingModel.ss_asset_class != None:
            self.ss_asset_class = str(holdingModel.ss_asset_class)

        if holdingModel.isin != None:
            self.id_isin = str(holdingModel.isin)

        if holdingModel.rcg_id != None:
            self.rcg_id = str(holdingModel.rcg_id)

        return
