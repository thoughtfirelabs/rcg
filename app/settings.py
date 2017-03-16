import os

###################################################################################
###################################################################################
class settings:

    ### The maximum number of days to look backwards in time for dynamic data without
    ### removing security and treating as invaild
    maximumLookbackDays = 3

    local_archive_directory = 'J:/HFOF/RCG/RISK/Transparency/portfolioApp'
    server_archive_directory = '/mnt/samba/transparency/portfolioApp'
    download_directory = os.path.expanduser("~") + "/Downloads/"

    ten_year_duration = 9.133
    dynamicFieldsToRetrieve = ['beta_msci','beta_sp500','delta','option_underlying_price','duration','underlying_duration',
                               'volume_avg_30d','crncy_adj_mkt_cap','volatility_162w']

    holding_type_dict = {'date_held': 'date', 'market_val': 'float',
                         'unrealized_gains_losses': 'float', 'quantity': 'float', 'price': 'float'}

    holding_headers = ['id', 'date_held', 'rcg_id', 'ssid', 'rcg_portfolio_id', 'ss_portfolio_id',
                       'port_name', 'sec_name', 'sdl', 'isin', 'position', 'price', 'market_val',
                       'unrealized_gains_losses',
                       'ss_asset_class', 'quantity']
    
    staticMasterHeaders = ['rcg_id','id_cusip','id_isin','id_sedol1','security_name','ss_asset_class','search_name',
                   'proxy_rcg_id','underlying_rcg_id','instrument_type',
                   'security_typ','security_typ2','market_sector_des','bpipe_reference_security_class','gics_sector',
                   'gics_sector_name','issuer','country_full_name','cntry_of_risk',
                   'px_pos_mult_factor','bics_level_3_industry_name']
                   
    port_name_mapping ={9731:'Chilton Sub-Adviser 40 Act',
                           9591:'Passport Sub-Adviser 40 Act',
                           9512:'Sirios Sub-Adviser 40 Act',
                           9408:'Wellington Sub-Adviser 40 Act',
                           9604:'Canyon Sub-Adviser 40 Act',
                           9740:'AQR Sub-Adviser 40 Act',
                           9733:'Mellon Capital Sub-Adviser 40 Act',
                           10008:'Pine River Sub-Adviser 40 Act'}

    port_id_mapping = {'WBRF':9731,'WBRH':9591,'WBRL':9512,'WBRM':9408,'WBRJ':9604,
                           'WBRE':9740,'WBRG':9733,'WBRI':10008}
    automatic_constant_pull_dynamic_fields = ['beta_sp500', 'beta_msci']
    asset_class_mapping = {'B':'Bond','C':'ShortTerm','F':'Future','M':'Cash','O':'Option',
                                    'P':'Spot','S':'Equity','W':'Forward'}

###################################################################################
###################################################################################
class MissingDataReportSettings:
    def __init__(self):
        ######## Dynamic Report Fields
        self.desiredFieldsForReport_Dynamic = ['date', 'rcg_id', 'id_cusip', 'id_isin', 'id_sedol1', 'security_name','ss_asset_class', 'search_name']
        self.missingDynamicDataReportHeaders = ['date', 'rcg_id', 'id_cusip', 'id_isin', 'id_sedol1', 'security_name','ss_asset_class', 'search_name',
                                                'missing_field','missing_value']

        self.allApplicableStaticSearchFields = ['instrument_type', 'bpipe_reference_security_class', 'gics_sector_name',
                                                'gics_industry_name', 'issuer', 'country_full_name', 'cntry_of_risk',
                                                'px_pos_mult_factor', 'bics_level_3_industry_name']

        ######## Static Report Fields
        self.desiredFieldsForReport_Static = ['rcg_id', 'id_cusip', 'id_isin', 'id_sedol1', 'security_name','ss_asset_class', 'search_name']
        self.missingStaticDataReportHeaders = ['rcg_id', 'id_cusip', 'id_isin', 'id_sedol1', 'security_name','ss_asset_class', 'search_name',
                                               'missing_field','missing_value']

        self.allApplicableDynamicSearchFields = ['beta_msci', 'beta_sp500', 'delta', 'opt_undl_price', 'duration',
                                                 'volume_avg_30d', 'crncy_adj_mkt_cap', 'volatility_162w']


###################################################################################
###################################################################################
class ExposureReportSettings:
    def __init__(self):
        self.assetClassExhaustiveCategories = ['Equity', 'Fixed Income', 'Commodities', 'Currency', 'Other']
        self.instrumentExhaustiveCategories = ['Equities', 'Fixed Income', 'Derivatives', 'Other']
        self.geoExhaustiveCategories = ['North America', 'Emerging Market', 'Japan', 'Other Asia', 'Europe', 'Other']
        self.sectorExhaustiveCategories = ['Consumer Staples', 'Consumer Discretionary', 'Energy', 'Financials',
                                           'Health Care', 'Industrials', 'Materials', 'Information Technology',
                                           'Telecommunication Services', 'Utilities', 'Other']
        self.strategyExhaustiveCategories = ['Equity Hedged', 'Relative Value', 'Global Macro', 'Event Driven',
                                             'Rock Creek Group']

        self.exhaustiveCategories = {'RCGGeoBucket': self.geoExhaustiveCategories,
                                     'RCGCustomAssetClass': self.assetClassExhaustiveCategories,
                                     'RCGCustomInstrument': self.instrumentExhaustiveCategories,
                                     'Sector': self.sectorExhaustiveCategories,
                                     'PortfolioStrategy': self.strategyExhaustiveCategories}

        self.managerIDOrder = ['10008', '9408', '9604', '9731', '9733', '9591', '9512', '9740', 'RCG40Act']

        self.strategyTableColumnLabels = ['Strategy', 'Allocation (%)', "Long Exposure", 'Short Exposure',
                                          'Gross Exposure', 'Net Exposure']

        ### Categories to be included in the report
        self.categoryNames = ['RCGGeoBucket', 'RCGCustomAssetClass', 'RCGCustomInstrument', 'Sector']
        self.categoryTableColumnLabels = ["% Gross Exposure", "Long Exposure", 'Short Exposure', 'Gross Exposure',
                                          'Net Exposure']
        self.digitsToRound = 2
        return



