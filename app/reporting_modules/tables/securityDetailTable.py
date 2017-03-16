from app.lib.csvUtilities import csvResponse

################################################################################
## Used to Organize and Output All Calculations and Data of Securities Used in General Notional and Market Value Calculations
class SecurityDetailTable(csvResponse):
    def __init__(self, portfolio = None, portfolios = [],name = None):

        self.portfolio = portfolio
        self.portfolios = portfolios
        self.name = name

        if self.portfolio != None:
            self.portfolios = [self.portfolio]

        if self.name == None:
            self.reportName = self.portfolio.portfolio_name + '_' + 'SecurityDetails'
        else:
            self.reportName = self.name + '_' + 'SecurityDetails'
        csvResponse.__init__(self)

        self.data = []
        self.fields = ['rcg_id','security_name', 'portfolio_name', 'market_val', 'gross_custom_notional',
                        'gross_delta_notional', 'net_delta_notional',
                        'search_name',
                        'ss_asset_class', 'instrument_type', 'position_designation',
                        'issuer', 'market_tp', 'region', 'country', 'country_full_name', 'cntry_of_risk',
                        'rcg_geo_bucket',
                        'rcgCustomInstrument', 'rcgCustomAssetClass',
                        'industry', 'sector', 'asset_class', 'derivative', 'restricted', 'wf_cash',
                        'beta_msci', 'beta_sp500', 'quantity', 'px_pos_mult_factor', 'volume', 'numContracts',
                        'illiquid', 'crncy_adj_mkt_cap', 'volatility_162w', 'delta', 'duration',
                        'option_underlying_price']
        self.headers = self.fields

    ######### Generate table by looping over each security, create CSV Response and return
    def generate(self):

        ### Loop over portfolios
        for port in self.portfolios:

            ### Loop over securities in each portfolio
            for security in port.securities:

                data_row = []
                for fieldName in self.fields:
                    
                    addValue = ""
                    ### Field Not Associated with Field Obj Right Now
                    if fieldName in ['rcg_id','market_val', 'gross_custom_notional','gross_delta_notional', 'net_delta_notional','crncy_adj_mkt_cap','volatility_162w']:
                        value = getattr(security,fieldName)
                        if value!= None:
                            addValue = value
                        data_row.append(addValue)
                        continue
                    
                    else:
                        ### Get Associated Field Obj
                        fieldObj = security.findField(fieldName)
                        addValue = ""
                        if fieldObj.value != None:
                            addValue = fieldObj.value

                        data_row.append(addValue)
                        
                self.data.append(data_row)
        return


