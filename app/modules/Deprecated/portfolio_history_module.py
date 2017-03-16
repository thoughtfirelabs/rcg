import numpy as np
import pandas as pd
from collections import OrderedDict
import psycopg2.extensions

from ..lib.settings import settings
#from ..lib.bug_reporting import data_report, definition_report

################################################################################
## Represents a Portfolio's History
class portfolio_history:
    
    def __init__(self,portfolio_id,snapshot_date,lookback_date,lookback_period=None):
        
        self.portfolio_id = portfolio_id
        self.snapshot_date = snapshot_date
        self.lookback_period = lookback_period
        self.lookback_date = lookback_date
        
        #self.data_report = data_report()
        #self.definition_report = definition_report()
        
        ##############################################
        ### Connection Engines
        self.DSN = "host=localhost port=5432 dbname=postgres user=postgres password=N12cholas!"
        self.conn = psycopg2.connect(self.DSN)
        self.cursor = self.conn.cursor()
        
        self.settings = settings()
        
        ##############################################
        ### Getting Description
        query = """SELECT portfolio_name, strategy, portfolio_description
                FROM public.portfolios 
                WHERE "id" = '%s'
                """ % self.portfolio_id
        

        self.cursor.execute(query)
        row = self.cursor.fetchone()

        self.portfolio_name = row[0]
        self.strategy = row[1]
        self.description = row[2]
        
        ##############################################
        ### General Data Structures Used for Storing and Operating
        self.unique_dates=[]
        self.unique_valid_security_ids = [] ## Used for Querying Static Information
        
        self.valid_security_ids = {}
        self.long_security_ids = {}
        self.short_security_ids = {}
        ##############################################
        ### Dynamic Security Level Data - Everything With Date as Primary Key     
        self.security_deltas = {}
        self.security_durations = {}
        self.underlying_security_durations = {}
        
        self.security_mult_factors = {}
        
        self.security_beta_mscis = {}
        self.security_beta_sp500s = {}
        
        self.security_weights = {}
        self.security_market_prices = {}
        
        self.security_notionals = {} ### Plain Old Gross Notional Values
        self.security_custom_notional_vals = {} ### Custom Calculation of Gross Notional
        self.security_custom_notional_weights = {}
        
        ## Only Relevant for Options
        self.security_derivative_underlying_px = {}
        
        ##############################################
        ### Position Level Data- Everything With Date as Primary Key
        self.position_designation = {}
        self.position_quantities = {}     
        self.position_market_prices = {}
        
        self.position_market_values = {}  ### Recalculated Based on Quantity and Price from SS Data
        self.ss_position_market_vals = {} ## State Streets Default Position Market Val
        
        self.position_market_prices = {}
        ##############################################
        ### Static Security Level Data - Don't Use Date as Primary Key, Sec ID is Primary Key
        self.security_ss_asset_classes = {}
        self.security_asset_groups = {}
        self.security_instrument_types = {}
        
        self.security_etf_flags = {}        
        self.security_index_flags = {}
        
        self.security_names = {}
        self.ss_security_names = {}
        
        self.security_industries = {}
        self.security_sectors = {}
        self.security_countries = {}
        self.security_regions = {}
        self.security_market_types = {}
        
        self.security_issuers = {}
        self.security_derivative_flags = {}
        self.security_rcg_geo_buckets = {}
        
        self.security_mat_dates = {}
        self.security_cpns = {}
        self.security_cpn_freq = {}
        self.security_opt_types = {}
        self.security_opt_strike_prices = {}
        
        self.exposure_excludes = {}
        self.security_custom_notional_methods = {}
        
        ##############################################
        ### Portfolio Level Data - Everything With Date as Primary Key
        self.beta_msci= {}
        self.revised_beta_msci= {}
        self.beta_sp500 = {}
        self.vol = {}
        
        self.custom_notional_exposure_long = {}
        self.custom_notional_exposure_short = {}   
        self.custom_notional_exposure_gross = {}
        self.custom_notional_exposure_net = {}
        
        self.market_val = {}
        self.num_positions = {}
        ##############################################
        ### Allocation by Market Values - Everything With Date as Primary Key
        self.asset_class_market_vals = {}
        self.instrument_market_vals = {}
        self.sector_market_vals = {}
        self.industry_market_vals = {}
        self.country_market_vals = {}
        self.strategy_market_vals = {}
        self.region_market_vals = {}
        self.market_type_market_vals = {}
        self.rcg_geo_bucket_market_vals = {}
        
        ##############################################
        ## Position Count by Category - Everything With Date as Primary Key
        self.region_position_count = {}
        self.country_position_count = {}
        self.instrument_position_count = {}
        self.asset_class_position_count = {}
        self.sector_position_count = {}
        self.industry_position_count = {}
        self.market_type_position_count = {}
        self.rcg_geo_bucket_position_count = {}
        
        ##############################################
        ## Dictionaries to Store Custom Exposures of Each Sector - Everything With Date as Primary Key
        self.sector_long_custom_notional_exposures = {}
        self.sector_short_custom_notional_exposures = {}
        self.sector_gross_custom_notional_exposures = {}
        self.sector_net_custom_notional_exposures = {}
        
        self.industry_long_custom_notional_exposures = {}
        self.industry_short_custom_notional_exposures = {}
        self.industry_gross_custom_notional_exposures = {}
        self.industry_net_custom_notional_exposures = {}
        
        ## Dictionaries to Store Custom Exposures of Each Region - Everything With Date as Primary Key
        self.region_long_custom_notional_exposures = {}
        self.region_short_custom_notional_exposures = {}
        self.region_gross_custom_notional_exposures = {}
        self.region_net_custom_notional_exposures = {}

        ## Dictionaries to Store Custom Exposures of Each Country - Everything With Date as Primary Key
        self.country_long_custom_notional_exposures = {}
        self.country_short_custom_notional_exposures = {}
        self.country_gross_custom_notional_exposures = {}
        self.country_net_custom_notional_exposures = {}

        ## Dictionaries to Store Custom Exposures of Each Instrument - Everything With Date as Primary Key
        self.instrument_long_custom_notional_exposures = {}
        self.instrument_short_custom_notional_exposures = {}
        self.instrument_gross_custom_notional_exposures = {}
        self.instrument_net_custom_notional_exposures = {}

        ## Dictionaries to Store Custom Exposures of Each Asset Class - Everything With Date as Primary Key
        self.asset_class_long_custom_notional_exposures = {}
        self.asset_class_short_custom_notional_exposures = {}
        self.asset_class_gross_custom_notional_exposures = {}
        self.asset_class_net_custom_notional_exposures = {}
        
        self.rcg_geo_bucket_long_custom_notional_exposures = {}
        self.rcg_geo_bucket_short_custom_notional_exposures = {}
        self.rcg_geo_bucket_gross_custom_notional_exposures = {}
        self.rcg_geo_bucket_net_custom_notional_exposures = {}
        
        self.market_type_long_custom_notional_exposures = {}
        self.market_type_short_custom_notional_exposures = {}
        self.market_type_gross_custom_notional_exposures = {}
        self.market_type_net_custom_notional_exposures = {}
        
        ##############################################
        ## Allocation by Gross Notional Values - Everything With Date as Primary Key
        self.instrument_custom_notional_allocation = {}
        self.sector_custom_notional_allocation = {}
        self.industry_custom_notional_allocation = {}
        self.region_custom_notional_allocation = {}
        self.country_custom_notional_allocation = {}
        self.market_type_custom_notional_allocation = {}
        self.rcg_geo_bucket_custom_notional_allocation = {} ### Need to Incorporate for Other Measures Later
        self.asset_class_custom_notional_allocation = {} ### Need to Incorporate for Other Measures Later
        
        ##############################################
        self.get_holdings()
        self.get_static_security_metrics()
        self.get_dynamic_security_metrics()
        self.calculate_general_metrics()
        return
        
    ############################
    ## Retrieves All Holdings - Security IDs, Positions and Quantities from SQL - Held on Each Day
    def get_holdings(self):
        
        self.unique_dates=[]
        query = """SELECT rcg_id, position, quantity, price, market_val, sec_name, exp_exclude, date_held
                FROM public.state_street_holdings 
                WHERE "rcg_portfolio_id" = '%s' AND "date_held" BETWEEN '%s' AND '%s'
                ORDER BY "date_held"
                """ % (self.portfolio_id, self.lookback_date, self.snapshot_date)
        

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        
        ###### Sift Through Query Results #################
        for row in rows:
            
            sec_id = str(row[0])
            udate = pd.to_datetime(row[7])
            if udate not in self.unique_dates:
                self.unique_dates.append(udate)
            
            if sec_id not in self.unique_valid_security_ids:
                self.unique_valid_security_ids.append(sec_id)
            
            ### Time Dependent Information
            if udate not in self.valid_security_ids.keys():
                
                self.valid_security_ids[udate]=[]
                self.short_security_ids[udate]=[]
                self.long_security_ids[udate]=[]
                
                self.position_quantities[udate]={}
                self.ss_position_market_vals[udate]={}
                self.security_market_prices[udate]={}
                
                self.num_positions[udate]=0
            
            self.num_positions[udate]+=1
            self.valid_security_ids[udate].append(sec_id)
            
            market_price = np.abs(float(row[3]))
            qty = float(row[2])
            
            self.position_quantities[udate][sec_id]=qty
            self.ss_position_market_vals[udate][sec_id]=float(row[4])
            self.security_market_prices[udate][sec_id]=market_price
            
            ### Static Information
            if sec_id not in self.security_names.keys():
                self.security_names[sec_id]=str(row[5])
                
            if sec_id not in self.exposure_excludes.keys():
                self.exposure_excludes[sec_id] = str(row[6])
                
            #### Position Dependent Information ######################
            if sec_id not in self.position_designation.keys():
                if str(row[1])=='L':
                    ### Store Position Information
                    self.position_designation[sec_id]='L'
                    self.long_security_ids[udate].append(sec_id)
                elif str(row[1])=='S':
                    ### Store Position Information
                    self.position_designation[sec_id]='S'
                    self.short_security_ids[udate].append(sec_id)
        return
    
    ############################
    ## Makes all calculations derived from metrics of individual securities in fund in the
    ## database responsible for storing static properties of securities
    def get_static_security_metrics(self):
        
        if len(self.unique_valid_security_ids)!=0:
            if len(self.unique_valid_security_ids) != 1:
                search = str(tuple(self.unique_valid_security_ids))
                ### Query for All Needed Historical Data
                query = """SELECT rcg_id, asset_class, ss_asset_class, sec_type, bbsec_type, gics_sector_name, gics_industry_name, country_full_name,
                            issuer, security_name, opt_strike_price, mat_date,cpn,cpn_freq,opt_type,mult_factor, etf_flag, index_flag
                            FROM public.static_securities 
                            WHERE "rcg_id" IN %s 
                            """ % search
            else:
                ### Query for All Needed Historical Data
                query = """SELECT rcg_id, asset_class, ss_asset_class, sec_type, bbsec_type, gics_sector_name, gics_industry_name, country_full_name,
                            issuer, security_name, opt_strike_price, mat_date,cpn,cpn_freq,opt_type,mult_factor, etf_flag, index_flag
                            FROM public.static_securities 
                            WHERE "rcg_id" = %s 
                            """ % self.unique_valid_security_ids[0]
                
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            region_conv = {}
            market_tp_conv = {}
            rcg_conv = {}
            
            ### Static Data ############################################################################################
            for row in rows:

                sec_id = str(row[0])

                asset_class = str(row[1])
                ss_asset_class = str(row[2])
                instrument_type = str(row[3])
                
                self.security_instrument_types[sec_id] = instrument_type
                self.security_asset_groups[sec_id] = asset_class
                self.security_ss_asset_classes[sec_id] = ss_asset_class
                
                ######################################################################
                #### Get Security Name ##################################
                if str(row[9]) != None:
                    self.security_names[sec_id]=str(row[9])
                else:
                    #self.data_report.add(sec_id,'Security Name','static_securities','Security Name Set as Missing')
                    self.security_names[sec_id]='Missing'
                
                sec_name = self.security_names[sec_id]
                
                ######################################################################
                ### Get Derivative Flag #######################
                if instrument_type in self.settings.derivative_dict.keys():
                    self.security_derivative_flags[sec_id] = self.settings.derivative_dict[instrument_type]
                else:
                    #self.definition_report.add(sec_id,sec_name,'Derivative Flag Definition',instrument_type,instrument_type+' Set as NonDerivative')
                    self.security_derivative_flags[sec_id] = False
                
                ######################################################################
                ### Get ETF Flag #######################
                if row[16] != None:
                    if str(row[16])=='True':
                        self.security_etf_flags[sec_id]=True
                    else:
                        self.security_etf_flags[sec_id]=False
                else:
                    self.security_etf_flags[sec_id]=False
                    
                ######################################################################
                ### Get Index Flag #######################
                if row[17] != None:
                    if str(row[16])=='True':
                        self.security_index_flags[sec_id]=True
                    else:
                        self.security_index_flags[sec_id]=False
                else:
                    self.security_index_flags[sec_id]=False
                    
                ######################################################################
                ### Get Mult Factor Flag #######################
                if row[15] != None:
                    self.security_mult_factors[sec_id]=float(row[15])
                else:
                    self.security_mult_factors[sec_id]=1.0
                
                ######################################################################
                ### Get Country / Region #######################
                if row[7] != None:
                    country_name = str(row[7]).title()
                    self.security_countries[sec_id]=country_name
                    ### New Found Country With No Region Definition
                    if country_name not in region_conv.keys():
                        region = self.settings.get_region(country_name)
                        if region == None:
                            region_conv[country_name] = 'Other'
                            #self.definition_report.add(sec_id,sec_name,'Region Definition',country_name,'Region Set as "Other"')
                        else:
                            region_conv[country_name] = region
                        self.security_regions[sec_id]=region_conv[country_name]
                    else:
                        ### Already Have Region Definition
                        self.security_regions[sec_id]=region_conv[country_name]
                        
                    ### New Found Country With No Market Type Definition
                    if country_name not in market_tp_conv.keys():
                        market_tp = self.settings.get_market_type(country_name)
                        if market_tp == None:
                            market_tp_conv[country_name] = 'Other'
                            #self.definition_report.add(sec_id,sec_name,'Market Type Definition',country_name,'Market Type Set as "Other"')
                        else:
                            market_tp_conv[country_name] = market_tp
                        self.security_market_types[sec_id]=market_tp_conv[country_name]
                    else:
                        ### Already Have Region Definition
                        self.security_market_types[sec_id]=market_tp_conv[country_name]
                        
                    ### New Found Country With No RCG Bucket Definition
                    if country_name not in rcg_conv.keys():
                        rcg_bucket = self.settings.get_rcg_geo_bucket(country_name)
                        if rcg_bucket == None:
                            rcg_conv[country_name] = 'Other'
                            #self.definition_report.add(sec_id,sec_name,'RCG Region/Market Definition Definition',country_name,'RCG Region/Market Type Set as "Other"')
                        else:
                            rcg_conv[country_name] = rcg_bucket
                        self.security_rcg_geo_buckets[sec_id]=rcg_conv[country_name]
                    else:
                        ### Already Have Region Definition
                        self.security_rcg_geo_buckets[sec_id]=rcg_conv[country_name]
                               
                #### Check for Missing Data - Set Value to Other if Missing ############################
                possible_required_data = {'Sector':(self.security_sectors,5),'Industry':(self.security_industries,6),'Issuer':(self.security_issuers,8)}
                
                for key in possible_required_data.keys():
                    ind = possible_required_data[key][1]
                    if row[ind] != None:
                        ### Store Data
                        possible_required_data[key][0][sec_id]=str(row[ind])
                        if key == 'Country':
                            possible_required_data[key][0][sec_id]=possible_required_data[key][0][sec_id].title()
                    else:
                        ### Data Missing - Put in Report and Set Value to 'Other'
                        #self.data_report.add(sec_id,sec_name,key,'static_securities',str(key)+' Assumed to be "Other"')
                        possible_required_data[key][0][sec_id]='Other'

        return
        
    ############################
    ## Queries Dynamic Security Database adn Gets Relevant Metrics for Valid Security IDS
    def get_dynamic_security_metrics(self):

        desired_measurements = ['beta_msci','beta_sp500','delta','opt_undl_price','duration','underlying_duration']

        if len(self.unique_valid_security_ids)!=0 and len(self.unique_dates)!=0:
            
            if len(self.unique_valid_security_ids) != 1:
                ### Query for All Needed Historical Data
                query = """SELECT rcg_id, measurement_type, value, date
                    FROM public.dynamic_securities 
                    WHERE "measurement_type" IN %s AND "rcg_id" IN %s  AND "date" BETWEEN '%s' AND '%s'
                    ORDER BY "date"
                    """  % (str(tuple(desired_measurements)),str(tuple(self.unique_valid_security_ids)),self.lookback_date,self.snapshot_date)
            else:
                ### Query for All Needed Historical Data
                query = """SELECT rcg_id, measurement_type, value, date 
                    FROM public.dynamic_securities 
                    WHERE "measurement_type" IN %s AND "rcg_id" = '%s' AND "date" BETWEEN '%s' AND '%s'
                    ORDER BY "date"
                            """ % (str(tuple(desired_measurements)),str(self.unique_valid_security_ids[0]),self.lookback_date,self.snapshot_date)
                            
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            #################### Sift Through Query Results ###################
            for row in rows:

                sec_id = str(row[0])
                meas = str(row[1]) ## Measurement Type
                value = float(row[2])
                udate = pd.to_datetime(row[3])
                
                ## Init Dictionaries for Dynamic Data Storing                
                if udate not in self.security_deltas.keys():
                    self.security_deltas[udate]={}
                if udate not in self.security_beta_mscis.keys():
                    self.security_beta_mscis[udate]={}
                if udate not in self.security_beta_sp500s.keys():
                    self.security_beta_sp500s[udate]={}
                if udate not in self.security_derivative_underlying_px.keys():
                    self.security_derivative_underlying_px[udate]={}
                if udate not in self.security_durations.keys():
                    self.security_durations[udate]={}
                if udate not in self.underlying_security_durations.keys():
                    self.underlying_security_durations[udate]={}
                    
                ## Instrument Type Static
                instrument_type = self.security_instrument_types[sec_id]
            
                ######## Handle Delta Measurements at Snapshot Date ############
                if meas == 'delta':
                    ## Check if Delta Required - Store if It Is
                    if instrument_type in self.settings.custom_exposure_dict.keys():
                        if self.settings.custom_exposure_dict[instrument_type]=='Delta Adj Exposure':
                            self.security_deltas[udate][sec_id]=value
                            
               ######## Handle Beta MSCI Measurements at Snapshot Date ############
                elif meas == 'beta_msci':
                    self.security_beta_mscis[udate][sec_id]=value
                ######## Handle Beta SP500 Measurements at Snapshot Date ###########
                elif meas == 'beta_sp500':
                    self.security_beta_sp500s[udate][sec_id]=value
                    
                ######## Handle Options Underlying Measurements at Snapshot Date ###########
                elif meas == 'opt_undl_price':
                    ## Check if Option Underyling Required/Relevant - Store if It Is
                    if instrument_type in self.settings.options:
                        self.security_derivative_underlying_px[udate][sec_id]=value
                            
                ######## Handle Options Underlying Measurements at Snapshot Date ###########
                elif meas == 'duration':
                    ## Check if Option Underyling Required/Relevant - Store if It Is
                    if instrument_type in self.settings.custom_exposure_dict.keys():
                        if self.settings.custom_exposure_dict[instrument_type]=='10yr Equiv':
                            self.security_durations[udate][sec_id]=value
                
                ######## Handle Options Underlying Measurements at Snapshot Date ###########
                elif meas == 'underlying_duration':
                    ## Check if Option Underyling Required/Relevant - Store if It Is
                    if instrument_type in self.settings.custom_exposure_dict.keys():
                        if self.settings.custom_exposure_dict[instrument_type]=='10yr Equiv': 
                            self.underlying_security_durations[udate][sec_id]=value
                            
                ######## Handle Vol Measurements at Snapshot Date ################
                elif meas == 'vol':
                    continue
                    ## Doing This Later, Fix Later
                else:
                    continue
                    ### Doing This Later, Different Dynamic Measurement Types like Vol
        
    ############################
    ## Makes general/overall calculations derived from metrics of individual securities in fund in the
    ## using data from all three core data bases
    def calculate_general_metrics(self):

        ### Loop Over Dates
        for udate in self.unique_dates:
            
            ### Store Invalid IDs for Each Round of Valid Security ID's on Date
            invalid_ids = []
            
            ### Initialize Dynamic Time Dicts with UDate Key
            if udate not in self.market_val.keys():
                
                self.position_market_values[udate]={}
                self.security_weights[udate]={}
                
                self.security_notionals[udate]={}
                
                self.security_custom_notional_weights[udate]={}
                self.security_custom_notional_vals[udate]={}
                
                self.beta_msci[udate] = 0.0
                self.beta_sp500[udate] = 0.0
                
                self.market_val[udate]=0.0
                self.custom_notional_exposure_long[udate]=0.0
                self.custom_notional_exposure_short[udate]=0.0
                self.custom_notional_exposure_gross[udate]=0.0
                self.custom_notional_exposure_net[udate]=0.0
                
            ########### Custom Exposures #######################################
            
            ### Loop Over Securities
            for sec_id in self.valid_security_ids[udate]:

                ### Static 
                sec_name = self.security_names[sec_id]
                instrument_type = self.security_instrument_types[sec_id]
                ss_asset_class = self.security_ss_asset_classes[sec_id]
                #mult_factor = self.security_mult_factors[sec_id]
                
                ### Dynamic
                qty = self.position_quantities[udate][sec_id]
                pos = self.position_designation[sec_id]
                security_price = self.security_market_prices[udate][sec_id]
                
                ###################
                if ss_asset_class =='Forward' or ss_asset_class =='Spot':
                     market_val = qty * (1.0/(security_price))
                     if pos=='S':
                       market_val=-1*market_val
                ###################
                elif ss_asset_class == 'Future' or ss_asset_class == 'Option':
                    if instrument_type == 'Bond Future':
                         market_val = qty * (1.0/(security_price/100.0))
                    else:
                         market_val = qty * security_price
                ###################
                elif ss_asset_class == 'Cash':
                    market_val = self.ss_position_market_vals[udate][sec_id]
                ###################
                elif ss_asset_class == 'Bond':
                    market_val = qty * (security_price/100.0)
                ################### WFA Cash 
                elif ss_asset_class == 'ShortTerm':
                    market_val = self.ss_position_market_vals[udate][sec_id] ## Equivalent to Saying Market Price = 1 for Dollar - Needed because WFA Cash Has Price = 3600
               
               ################### Equity, 
                else:
                    market_val = qty * security_price
                
                ### Store Calculated Position Market Value (Differs from ss_market_val in Some Cases That is Given.)
                self.position_market_values[udate][sec_id] = market_val
                self.market_val[udate] += market_val ### Update Market Value on Date
                
                ## Continue in Loop if Security is Not Included in Notional Calculations
                if self.exposure_excludes[sec_id]=='True':
                    if sec_id not in invalid_ids:
                        invalid_ids.append(sec_id)
                    continue

                ### Calculate Notional Value of Position in Security
                security_notional = np.abs(market_val)
                self.security_notionals[udate][sec_id]=security_notional

                ######### Data Required - If Not Here, Don't Include Security ####################
                required_data = [self.security_instrument_types,self.position_market_values[udate],self.position_designation]
                required_data_strings = ['Instrument','Security Market Value','Security Position Designation (L/S)']
                missing_static_data = False
                
                for i in range(len(required_data)):
                    datalist = required_data[i]
                    if sec_id not in datalist.keys():
                        missing_static_data = True
                        break
            
                if missing_static_data == True:
                    self.data_report.add(sec_id,sec_name,required_data_strings[i],'state_street_holdings','Fatal Error : Cannot Calculate Exposure of Security')
                    invalid_ids.append(sec_id)                
                    continue
                
            
                ########## Custom Exposures - Method Designation ################
                custom_exposure_method = 'Delta Adj Exposure' ## Default Value
                if instrument_type not in self.settings.custom_exposure_dict.keys():
                    self.definition_report.add(sec_id,sec_name,'Custom Exposure Method',instrument_type,'Delta Adj Exposure Used as Custom Notional')
                else:
                    custom_exposure_method = self.settings.custom_exposure_dict[instrument_type]
    
                ########### Custom Gross Exposures - Method (1) ###############
                if custom_exposure_method == 'Delta Adj Exposure':
                    self.security_custom_notional_methods[sec_id]='Delta Adj'
                    ### Check if Option First
                    if self.security_ss_asset_classes[sec_id]=='Option':
                        
                        ############ Get Delta - If Not Present - Error
                        if sec_id in self.security_deltas[udate].keys():
                            delta = self.security_deltas[udate][sec_id]
                            
                            ############ Get Underlying Price of Option - If Not Present - Remove from Calculations
                            if sec_id in self.security_derivative_underlying_px[udate].keys():
                                
                                option_underlying_px = self.security_derivative_underlying_px[udate][sec_id]
                                gross_custom_notional = np.abs(option_underlying_px*qty*delta)
                           
                            else: ## Option Underlying Px Value Missing
                                self.data_report.add(sec_id,sec_name,'Underlying Price','dynamic_securities','Cannot Calculate Exposure')
                                if sec_id not in invalid_ids:
                                    invalid_ids.append(sec_id) 
                                continue
                        
                        else: ## Delta Value Missing
                            self.data_report.add(sec_id,sec_name,'Delta','dynamic_securities','Cannot Calculate Exposure')
                            if sec_id not in invalid_ids:
                                invalid_ids.append(sec_id) 
                            continue
                        
                    ### Check if Future Next
                    elif self.security_ss_asset_classes[sec_id]=='Future':
                        delta = 1.0
                        gross_custom_notional = security_notional*delta
                    
                    else:
                        ############ Get Delta - If Not Present - Error
                        delta = self.security_deltas[udate][sec_id]
                        gross_custom_notional = security_notional*delta
    
                ############# Custom Gross Exposures - Method (2) ###############
                elif custom_exposure_method == 'Market Value':
                    gross_custom_notional = security_notional
                    self.security_custom_notional_methods[sec_id]='Market Val'
                ## Custom Gross Exposures - Method (3) ###############
                elif custom_exposure_method == '10yr Equiv':
                    self.security_custom_notional_methods[sec_id]='10yr Equiv'
                    ############ Get Duration - If Not Present - Remove from Calculations
                    if sec_id in self.security_durations[udate].keys():
                        sec_duration = self.security_durations[udate][sec_id]
                        if sec_id not in self.underlying_security_durations[udate].keys():
                            duration_ratio = sec_duration / self.settings.ten_year_duration
                        else:
                            ## Uncommment Below Duration Ratio to Use Local 10yr Equiv Bond Duration
                            ##duration_ratio = sec_duration / self.underlying_security_durations[sec_id]
                            duration_ratio = sec_duration / self.settings.ten_year_duration
                    else:
                        self.data_report.add(sec_id,sec_name,'Duration','dynamic_securities','Cannot Calculate Exposure')
                        if sec_id not in invalid_ids:
                            invalid_ids.append(sec_id) 
                        continue
                    
                    gross_custom_notional = security_notional*duration_ratio
    
                ## Store Info Depending on Position
                self.security_custom_notional_vals[udate][sec_id] = gross_custom_notional
                if pos == 'L': ### Long Positions
                    self.custom_notional_exposure_long[udate] += gross_custom_notional
                else:  ### Short Positions
                    self.custom_notional_exposure_short[udate] += gross_custom_notional
            
            ### Update Invalid Sec IDS for Date Batch
            for sec_id in invalid_ids:
                if sec_id in self.valid_security_ids[udate]:   
                    self.valid_security_ids[udate].remove(sec_id)
            
            ### Congolomerate Total Delta Adj Notional Values, Gross and Net
            self.custom_notional_exposure_gross[udate] = self.custom_notional_exposure_long[udate] + self.custom_notional_exposure_short[udate]
            self.custom_notional_exposure_net[udate] = self.custom_notional_exposure_long[udate] - self.custom_notional_exposure_short[udate]
            
            ### Security Market Values Already Take Into Account Quantity of Each Security
            ## Want Security Weights as Abs(MarketValue)/Sum(AbsValMarketVals)
            abs_market_vals = {}
            for sec_id in self.position_market_values[udate].keys():
                abs_market_vals[sec_id]=np.abs(self.position_market_values[udate][sec_id])
                    
            #################### Conglomerate Security Weights by Market Val and Notional
            for sec_id in self.valid_security_ids[udate]:
                self.security_weights[udate][sec_id]=np.abs(abs_market_vals[sec_id])/sum(abs_market_vals.values())
                ### Weights By Custom Notional Vals
                if self.exposure_excludes[sec_id]=='False':
                    self.security_custom_notional_weights[udate][sec_id]=self.security_custom_notional_vals[udate][sec_id]/self.custom_notional_exposure_gross[udate]
    
            #################### Congolmerate Beta's and Vols for Portfolio 
            for sec_id in self.valid_security_ids[udate]:
                
                sec_name = self.security_names[sec_id]
                
                if sec_id not in self.security_beta_mscis[udate].keys():
                    None
                    #self.data_report.add(sec_id,sec_name,'Beta MSCI','dynamic_securities','Not Included in Calculation')
                else:
                    if pos == 'L': ### Long Positions
                        self.beta_msci[udate] += self.security_weights[udate][sec_id]*self.security_beta_mscis[udate][sec_id]
                    else:
                        self.beta_msci[udate] -= self.security_weights[udate][sec_id]*self.security_beta_mscis[udate][sec_id]
                
                ### Need to Do : Revised Beta MSCI
                if sec_id not in self.security_beta_sp500s[udate].keys():
                    None
                    #self.data_report.add(sec_id,sec_name,'Revised Beta SP500','dynamic_securities','Not Included in Calculation')
                else:
                    if pos == 'L': ### Long Positions
                        self.beta_sp500[udate] += self.security_weights[udate][sec_id]*self.security_beta_sp500s[udate][sec_id]
                    else:
                        self.beta_sp500[udate] -= self.security_weights[udate][sec_id]*self.security_beta_sp500s[udate][sec_id]
                    
        return
        
    ###############################################################################################
    ###############################################################################################
    def calculate_position_count(self):
        
        ### Loop Over Dates
        for udate in self.unique_dates:
            
            ### Initialize Dynamic Time Dicts with UDate Key
            if udate not in self.country_position_count.keys():
                
                self.country_position_count[udate]={}
                self.region_position_count[udate]={}
                self.instrument_position_count[udate]={}
                self.asset_class_position_count[udate]={}
                self.sector_position_count[udate]={}
                self.industry_position_count[udate]={}
                self.market_type_position_count[udate]={}
                self.rcg_geo_bucket_position_count[udate]={}
                
            ### Loop Over Securities
            for sec_id in self.valid_security_ids[udate]:
                
                sec_name = self.security_names[sec_id]
    
                ###### Make Sure Required Data Present #################
                required_data = [self.security_asset_groups,self.security_instrument_types,
                                 self.security_sectors,self.security_countries,self.security_regions]
                required_data_strings = ['Asset Class','Instrument','Sector','Country','Region']
                missing_static_data = False
                for i in range(len(required_data)):
                    datalist = required_data[i]
                    if sec_id not in datalist.keys():
                        #self.data_report.add(sec_id,sec_name,required_data_strings[i],'static_securities','Cannot Be Used to Calculate Position Counts - Security ID From Calculation Pool ')
                        missing_static_data = True
                        break
                if missing_static_data == True:
                    continue
                    
                ## Static Data, Irrelevant of Date
                asset_group = self.security_asset_groups[sec_id]
                instrument_type = self.security_instrument_types[sec_id]
                sector = self.security_sectors[sec_id] 
                country = self.security_countries[sec_id] 
                industry = self.security_industries[sec_id]
                region = self.security_regions[sec_id]
                market_type = self.security_market_types[sec_id]
                rcg_geo_bucket = self.security_rcg_geo_buckets[sec_id]
                
                #################
                if region in self.region_position_count[udate].keys():
                    self.region_position_count[udate][region]+=1
                else:
                    self.region_position_count[udate][region]=1
                #################
                if country in self.country_position_count[udate].keys():
                    self.country_position_count[udate][country]+=1
                else:
                    self.country_position_count[udate][country]=1
                #################
                if instrument_type in self.instrument_position_count[udate].keys():
                    self.instrument_position_count[udate][instrument_type]+=1
                else:
                    self.instrument_position_count[udate][instrument_type]=1
        
                #################
                if asset_group in self.asset_class_position_count[udate].keys():
                    self.asset_class_position_count[udate][asset_group]+=1
                else:
                    self.asset_class_position_count[udate][asset_group]=1
        
                #################
                if sector in self.sector_position_count[udate].keys():
                    self.sector_position_count[udate][sector]+=1
                else:
                    self.sector_position_count[udate][sector]=1
                
                #################
                if industry in self.industry_position_count[udate].keys():
                    self.industry_position_count[udate][industry]+=1
                else:
                    self.industry_position_count[udate][industry]=1
                    
                #################
                if market_type in self.market_type_position_count[udate].keys():
                    self.market_type_position_count[udate][market_type]+=1
                else:
                    self.market_type_position_count[udate][market_type]=1
                    
                #################
                if rcg_geo_bucket in self.rcg_geo_bucket_position_count[udate].keys():
                    self.rcg_geo_bucket_position_count[udate][rcg_geo_bucket]+=1
                else:
                    self.rcg_geo_bucket_position_count[udate][rcg_geo_bucket]=1



    ############################
    ## Organizes Query Results to Show Total Market Values for Each Category
    def calculate_market_vals(self):
        
        ### Loop Over Dates
        for udate in self.unique_dates:
            
            ### Initialize Dynamic Time Dicts with UDate Key
            if udate not in self.country_market_vals.keys():
                
                self.country_market_vals[udate]={}
                self.region_market_vals[udate]={}
                self.instrument_market_vals[udate]={}
                self.asset_class_market_vals[udate]={}
                self.sector_market_vals[udate]={}
                self.industry_market_vals[udate]={}
                self.market_type_market_vals[udate]={}
                self.rcg_geo_bucket_market_vals[udate]={}
                
            ### Loop Over Securities
            for sec_id in self.valid_security_ids[udate]:
                

                sec_name = self.security_names[sec_id]
                
                ###################################################################
                ###### Make Sure Required Data Present #################
                required_data = [self.security_asset_groups,self.security_instrument_types,
                                 self.security_sectors,self.security_countries,self.security_regions]
                required_data_strings = ['Asset Class','Instrument','Sector','Country','Region']
                missing_static_data = False
                for i in range(len(required_data)):
                    datalist = required_data[i]
                    if sec_id not in datalist.keys():
                        #self.data_report.add(sec_id,sec_name,required_data_strings[i],'static_securities','Cannot Be Used to Calculate Market Values - Security ID From Calculation Pool ')
                        missing_static_data = True
                        break
                if missing_static_data == True:
                    continue
                
                required_data = [self.position_market_values[udate]]
                required_data_strings = ['Security Market Value']
                missing_static_data = False
                for i in range(len(required_data)):
                    datalist = required_data[i]
                    if sec_id not in datalist.keys():
                        self.data_report.add(sec_id,required_data_strings[i],'state_street_holdings','Cannot Be Used to Calculate Market Values - Security ID From Calculation Pool ')
                        missing_static_data = True
                        break
                if missing_static_data == True:
                    continue
                
                ###################################################################
                ## Static Data, Irrelevant of Date
                asset_group = self.security_asset_groups[sec_id]
                instrument_type = self.security_instrument_types[sec_id]
                sector = self.security_sectors[sec_id] 
                country = self.security_countries[sec_id] 
                region = self.security_regions[sec_id]   
                market_type = self.security_market_types[sec_id]
                rcg_geo_bucket = self.security_rcg_geo_buckets[sec_id]
                industry = self.security_industries[sec_id]
                ### Short Securities Already Have Negative Market Value
     
                ## Asset Class
                if asset_group in self.asset_class_market_vals[udate].keys():
                    self.asset_class_market_vals[udate][asset_group]+=self.position_market_values[udate][sec_id]
                else:
                    self.asset_class_market_vals[udate][asset_group]=self.position_market_values[udate][sec_id]
                ## Instrument Type
                if instrument_type in self.instrument_market_vals[udate].keys():
                    self.instrument_market_vals[udate][instrument_type]+=self.position_market_values[udate][sec_id]
                else:
                    self.instrument_market_vals[udate][instrument_type]=self.position_market_values[udate][sec_id]
                ## Sector
                if sector in self.sector_market_vals[udate].keys():
                    self.sector_market_vals[udate][sector]+=self.position_market_values[udate][sec_id]
                else:
                    self.sector_market_vals[udate][sector]=self.position_market_values[udate][sec_id]
                ## Industry
                if industry in self.industry_market_vals[udate].keys():
                    self.industry_market_vals[udate][sector]+=self.position_market_values[udate][sec_id]
                else:
                    self.sector_market_vals[udate][sector]=self.position_market_values[udate][sec_id]
                ## Country
                if country in self.country_market_vals[udate].keys():
                    self.country_market_vals[udate][country]+=self.position_market_values[udate][sec_id]
                else:
                    self.country_market_vals[udate][country]=self.position_market_values[udate][sec_id]
                ## Region
                if region in self.region_market_vals[udate].keys():
                    self.region_market_vals[udate][region]+=self.position_market_values[udate][sec_id]
                else:
                    self.region_market_vals[udate][region]=self.position_market_values[udate][sec_id]
                ## Market Types
                if market_type in self.market_type_market_vals[udate].keys():
                    self.market_type_market_vals[udate][market_type]+=self.position_market_values[udate][sec_id]
                else:
                    self.market_type_market_vals[udate][market_type]=self.position_market_values[udate][sec_id]
                ## RCG Geo Bucket
                if rcg_geo_bucket in self.rcg_geo_bucket_market_vals[udate].keys():
                    self.rcg_geo_bucket_market_vals[udate][rcg_geo_bucket]+=self.position_market_values[udate][sec_id]
                else:
                    self.rcg_geo_bucket_market_vals[udate][rcg_geo_bucket]=self.position_market_values[udate][sec_id]

        return


    ############################
    ## Organizes Query Results for Exposures Into Dictionaries for Future Use
    def calculate_exposures(self):
        
        ### Loop Over Dates
        for udate in self.unique_dates:
            
            ### Initialize Dynamic Time Dicts with UDate Key
            if udate not in self.asset_class_long_custom_notional_exposures.keys():
                
                self.asset_class_long_custom_notional_exposures[udate]={}
                self.asset_class_short_custom_notional_exposures[udate]={}
                self.asset_class_gross_custom_notional_exposures[udate]={}
                self.asset_class_net_custom_notional_exposures[udate]={}
                
                self.instrument_short_custom_notional_exposures[udate]={}
                self.instrument_long_custom_notional_exposures[udate]={}
                self.instrument_gross_custom_notional_exposures[udate]={}
                self.instrument_net_custom_notional_exposures[udate]={}
                
                self.sector_short_custom_notional_exposures[udate]={}
                self.sector_long_custom_notional_exposures[udate]={}
                self.sector_gross_custom_notional_exposures[udate]={}
                self.sector_net_custom_notional_exposures[udate]={}
                
                self.industry_short_custom_notional_exposures[udate]={}
                self.industry_long_custom_notional_exposures[udate]={}
                self.industry_gross_custom_notional_exposures[udate]={}
                self.industry_net_custom_notional_exposures[udate]={}
                
                self.region_short_custom_notional_exposures[udate]={}
                self.region_long_custom_notional_exposures[udate]={}
                self.region_gross_custom_notional_exposures[udate]={}
                self.region_net_custom_notional_exposures[udate]={}
                
                self.country_short_custom_notional_exposures[udate]={}
                self.country_long_custom_notional_exposures[udate]={}
                self.country_gross_custom_notional_exposures[udate]={}
                self.country_net_custom_notional_exposures[udate]={}
                
                self.rcg_geo_bucket_short_custom_notional_exposures[udate]={}
                self.rcg_geo_bucket_long_custom_notional_exposures[udate]={}
                self.rcg_geo_bucket_gross_custom_notional_exposures[udate]={}
                self.rcg_geo_bucket_net_custom_notional_exposures[udate]={}
                
                self.market_type_short_custom_notional_exposures[udate]={}
                self.market_type_long_custom_notional_exposures[udate]={}
                self.market_type_gross_custom_notional_exposures[udate]={}
                self.market_type_net_custom_notional_exposures[udate]={}

            ### Loop Over Securities
            for sec_id in self.valid_security_ids[udate]:
                
                sec_name = self.security_names[sec_id]
                
                ###################################################################
                ###### Make Sure Required Data Present #################
                required_data = [self.security_asset_groups,self.security_instrument_types,
                                 self.security_sectors,self.security_countries,self.security_regions,self.security_issuers]
                required_data_strings = ['Asset Class','Instrument','Sector','Country','Region','Issuer']
                missing_static_data = False
                for i in range(len(required_data)):
                    datalist = required_data[i]
                    if sec_id not in datalist.keys():
                        #self.data_report.add(sec_id,sec_name,required_data_strings[i],'static_securities','Cannot Be Used to Calculate Market Values - Security ID From Calculation Pool ')
                        missing_static_data = True
                        break
                if missing_static_data == True:
                    continue
    
                required_data = [self.security_custom_notional_vals[udate]]
                required_data_strings = ['Security Custom Notional Value']
                missing_static_data = False
                for i in range(len(required_data)):
                    datalist = required_data[i]
                    if sec_id not in datalist.keys():
                        #self.data_report.add(sec_id,sec_name,required_data_strings[i],'state_street_holdings','Cannot Be Used to Calculate Exposure Values - Security ID From Calculation Pool ')
                        missing_static_data = True
                        break
                if missing_static_data == True:
                    continue
                
                ########### Static Data, Irrelevant of Date #######################
                asset_group = self.security_asset_groups[sec_id]
                instrument_type = self.security_instrument_types[sec_id]
                sector = self.security_sectors[sec_id] 
                country = self.security_countries[sec_id] 
                region = self.security_regions[sec_id]
                
                market_type = self.security_market_types[sec_id]
                rcg_geo_bucket = self.security_rcg_geo_buckets[sec_id]            
                industry = self.security_industries[sec_id]
                
                ########### Security Notional Values #######################
                sec_custom_notional_val = self.security_custom_notional_vals[udate][sec_id]
                
                ########## LONG POSITIONS ######################
                if self.position_designation[sec_id] == 'L':
                
                    ## Asset Class ###################################################
                    if asset_group in self.asset_class_long_custom_notional_exposures[udate].keys():
                        self.asset_class_long_custom_notional_exposures[udate][asset_group]+=sec_custom_notional_val
                    else:
                        self.asset_class_long_custom_notional_exposures[udate][asset_group]=sec_custom_notional_val
                    
                    ## Instrument Type ###################################################
                    if instrument_type in self.instrument_long_custom_notional_exposures[udate].keys():
                        self.instrument_long_custom_notional_exposures[udate][instrument_type]+=sec_custom_notional_val
                    else:
                        self.instrument_long_custom_notional_exposures[udate][instrument_type]=sec_custom_notional_val
                        
                    ## Sector ###################################################
                    if sector in self.sector_long_custom_notional_exposures[udate].keys():
                        self.sector_long_custom_notional_exposures[udate][sector]+=sec_custom_notional_val  
                    else:
                        self.sector_long_custom_notional_exposures[udate][sector]=sec_custom_notional_val
    
                    ## Industry ###################################################
                    if industry in self.industry_long_custom_notional_exposures[udate].keys():
                        self.industry_long_custom_notional_exposures[udate][industry]+=sec_custom_notional_val     
                    else:
                        self.industry_long_custom_notional_exposures[udate][industry]=sec_custom_notional_val
                        
                    ## Country ###################################################
                    if country in self.country_long_custom_notional_exposures[udate].keys():
                        self.country_long_custom_notional_exposures[udate][country]+=sec_custom_notional_val
                    else:
                        self.country_long_custom_notional_exposures[udate][country]=sec_custom_notional_val
                    
                    ## Region ###################################################
                    if region in self.region_long_custom_notional_exposures[udate].keys():
                        self.region_long_custom_notional_exposures[udate][region]+=sec_custom_notional_val
                    else:
                        self.region_long_custom_notional_exposures[udate][region]=sec_custom_notional_val
                        
                    ## Market Type ###################################################
                    if market_type in self.market_type_long_custom_notional_exposures[udate].keys():
                        self.market_type_long_custom_notional_exposures[udate][market_type]+=sec_custom_notional_val
                    else:
                        self.market_type_long_custom_notional_exposures[udate][market_type]=sec_custom_notional_val
    
                    ## RCG Geo Bucket ###################################################
                    if rcg_geo_bucket in self.rcg_geo_bucket_long_custom_notional_exposures[udate].keys():
                        self.rcg_geo_bucket_long_custom_notional_exposures[udate][rcg_geo_bucket]+=sec_custom_notional_val
                    else:
                        self.rcg_geo_bucket_long_custom_notional_exposures[udate][rcg_geo_bucket]=sec_custom_notional_val
                
                ########## SHORT POSITIONS ######################
                elif self.position_designation[sec_id] == 'S':
                    
                    ## Asset Class ###################################################
                    if asset_group in self.asset_class_short_custom_notional_exposures[udate].keys():
                        self.asset_class_short_custom_notional_exposures[udate][asset_group]+=sec_custom_notional_val                  
                    else:
                        self.asset_class_short_custom_notional_exposures[udate][asset_group]=sec_custom_notional_val
                        
                    ## Instrument Type ###################################################
                    if instrument_type in self.instrument_short_custom_notional_exposures[udate].keys():
                        self.instrument_short_custom_notional_exposures[udate][instrument_type]+=sec_custom_notional_val                        
                    else:
                        self.instrument_short_custom_notional_exposures[udate][instrument_type]=sec_custom_notional_val
                        
                    ## Sector ###################################################
                    if sector in self.sector_short_custom_notional_exposures[udate].keys():
                        self.sector_short_custom_notional_exposures[udate][sector]+=sec_custom_notional_val    
                    else:
                        self.sector_short_custom_notional_exposures[udate][sector]=sec_custom_notional_val
    
                    ## Industry ###################################################
                    if industry in self.industry_short_custom_notional_exposures[udate].keys():
                        self.industry_short_custom_notional_exposures[udate][industry]+=sec_custom_notional_val  
                    else:
                        self.industry_short_custom_notional_exposures[udate][industry]=sec_custom_notional_val
                        
                    ## Country ###################################################
                    if country in self.country_short_custom_notional_exposures[udate].keys():
                        self.country_short_custom_notional_exposures[udate][country]+=sec_custom_notional_val
                    else:
                        self.country_short_custom_notional_exposures[udate][country]=sec_custom_notional_val
                    
                    ## Region ###################################################
                    if region in self.region_short_custom_notional_exposures[udate].keys():
                        self.region_short_custom_notional_exposures[udate][region]+=sec_custom_notional_val
                    else:
                        self.region_short_custom_notional_exposures[udate][region]=sec_custom_notional_val
                        
                    ## Market Type ###################################################
                    if market_type in self.market_type_short_custom_notional_exposures[udate].keys():
                        self.market_type_short_custom_notional_exposures[udate][market_type]+=sec_custom_notional_val
                    else:
                        self.market_type_short_custom_notional_exposures[udate][market_type]=sec_custom_notional_val
    
                    ## RCG Geo Bucket ###################################################
                    if rcg_geo_bucket in self.rcg_geo_bucket_short_custom_notional_exposures[udate].keys():
                        self.rcg_geo_bucket_short_custom_notional_exposures[udate][rcg_geo_bucket]+=sec_custom_notional_val
                    else:
                        self.rcg_geo_bucket_short_custom_notional_exposures[udate][rcg_geo_bucket]=sec_custom_notional_val
                        
                #############################################################################
                ## Conglomerate Short and Long Exposures to Gross and Net for Each Type
                short_dict_custom_exposures = [self.asset_class_short_custom_notional_exposures[udate], self.instrument_short_custom_notional_exposures[udate],
                                        self.sector_short_custom_notional_exposures[udate], self.country_short_custom_notional_exposures[udate],
                                        self.region_short_custom_notional_exposures[udate],self.industry_short_custom_notional_exposures[udate],self.rcg_geo_bucket_short_custom_notional_exposures[udate],
                                        self.market_type_short_custom_notional_exposures[udate]]
                long_dict_custom_exposures = [self.asset_class_long_custom_notional_exposures[udate], self.instrument_long_custom_notional_exposures[udate],
                                        self.sector_long_custom_notional_exposures[udate], self.country_long_custom_notional_exposures[udate],
                                        self.region_long_custom_notional_exposures[udate],self.industry_long_custom_notional_exposures[udate],self.rcg_geo_bucket_long_custom_notional_exposures[udate],
                                        self.market_type_long_custom_notional_exposures[udate]]
                gross_dict_custom_exposures = [self.asset_class_gross_custom_notional_exposures[udate], self.instrument_gross_custom_notional_exposures[udate],
                                        self.sector_gross_custom_notional_exposures[udate], self.country_gross_custom_notional_exposures[udate],
                                        self.region_gross_custom_notional_exposures[udate],self.industry_gross_custom_notional_exposures[udate],self.rcg_geo_bucket_gross_custom_notional_exposures[udate],
                                        self.market_type_gross_custom_notional_exposures[udate]]
                net_dict_custom_exposures = [self.asset_class_net_custom_notional_exposures[udate], self.instrument_net_custom_notional_exposures[udate],
                                        self.sector_net_custom_notional_exposures[udate], self.country_net_custom_notional_exposures[udate],
                                        self.region_net_custom_notional_exposures[udate],self.industry_net_custom_notional_exposures[udate],self.rcg_geo_bucket_net_custom_notional_exposures[udate],
                                        self.market_type_net_custom_notional_exposures[udate]]
                
                            
                #############################################################################
                ## Custom Exposures  - Combine Long/Short for Each Type into Gross/Net Exposures
                for i in range(len(long_dict_custom_exposures)):
                    longdict = long_dict_custom_exposures[i]
                    shortdict = short_dict_custom_exposures[i]
                    unique_keys = list(set(list(longdict.keys())+list(shortdict.keys())))
         
                    for key in unique_keys:
          
                        if key in longdict.keys() and key in shortdict.keys():
                            gross_dict_custom_exposures[i][key]=longdict[key]+shortdict[key]
                            net_dict_custom_exposures[i][key]=longdict[key]-shortdict[key]
                        elif key in longdict.keys():
                            gross_dict_custom_exposures[i][key]=longdict[key]
                            net_dict_custom_exposures[i][key]=longdict[key]
                        elif key in shortdict.keys():
                            gross_dict_custom_exposures[i][key]=shortdict[key]
                            net_dict_custom_exposures[i][key]= -1 * shortdict[key]

        return
    ############################
    ## Gets Historical Prices for All Dates in Range and All Held Securities
    ## Returns as Data Frame
    def get_historical_security_prices(self):
        
        self.historical_security_prices = OrderedDict()
        
        if len(self.unique_security_ids) != 0:
            
            query = """SELECT date, security_id, value
                    FROM public.historical_data 
                    WHERE "measurement_type" = 'market_val' AND "security_id" IN %s AND "date" BETWEEN '%s' AND '%s'
                    ORDER BY date
                    """ % (str(tuple(self.unique_security_ids)), self.start_date, self.end_date)
            
            ## Returned As Dataframe
            self.historical_security_prices_df = pd.read_sql(query,self.conn)
            for unique_date in self.unique_dates:
                find_date = pd.to_datetime(unique_date)
                
                prices_subdf = self.historical_security_prices_df[self.historical_security_prices_df['date']==find_date]
                prices_subdf = prices_subdf.drop('date',axis=1)
                
                self.historical_security_prices[find_date] = prices_subdf.set_index('security_id').squeeze().to_dict()

        return
    
    ############################
    ## Gets Returns for Each Security on Each Trading Day in Portfolio and Combined
    ## To Get Returns for Portfolio on Each Trading Day
    def get_historical_returns(self):
        
        ## Get Allocations to Each Security on Each Day
        self.get_historical_security_allocations()
        
        self.historical_security_returns = OrderedDict()
        self.historical_returns = OrderedDict()
        self.historical_returns_string_format = OrderedDict()
            
        if len(self.unique_security_ids) != 0:
            
            dates = self.historical_holdings.keys()
            for i in range(1,len(dates)):
                ## Aggregate Returns in Dictionary for All Securities
                after_agg_prices = self.historical_security_prices[dates[i]]
                before_agg_prices = self.historical_security_prices[dates[i-1]]
     
                ## Weighting Occurs by Day Before (To Make Inflows/Outflows Irrelevant)
                agg_wts = self.historical_security_allocations[dates[i-1]]
               
                ### NEED TO DO : ACCOUNT FOR SHORT/LONG DIFFERENCE HERE
                sec_rtn_temp_dict = {}
                wt_rtns = 0.0
                for sec_key in after_agg_prices.keys():
                    
                    
                    sec_rtn = after_agg_prices[sec_key]/before_agg_prices[sec_key]-1.0
                    sec_rtn_temp_dict[sec_key]=sec_rtn
                    wt_rtns += sec_rtn * agg_wts[sec_key]
                
                ## Store Weighted Return Value for Portfolio by Indexed Date for Historical Sec Returns
                self.historical_returns[dates[i]]=wt_rtns
                self.historical_returns_string_format[dates[i].strftime('%Y-%m-%d')]=wt_rtns
                ## Store Dictionary by Indexed Date for Historical Sec Returns
                self.historical_security_returns[dates[i]]=sec_rtn_temp_dict

        return

    ############################
    ## Gets Returns for Each Security on Each Trading Day in Portfolio and Combines
    ## To Get Returns for Portfolio on Monthly Basis
    def get_historical_monthly_returns(self):
        
        ## Gets Daily Returns Between Two Dates        
        self.get_historical_returns()
        
        self.historical_monthly_returns_string_format = {}
        
        ## Group Daily Returns by Month
        monthly_return_series = {}
        
        for dttime in self.historical_returns.keys():
            month_time = int(dttime.month)
            year_time = int(dttime.year)
            
            ## Count First Day Month as Grouping into Previous Month 
            if dttime.day == 1:
                month_time = month_time - 1
                ## January 1 Back One Day is December
                if month_time == 1:
                    month_time = 12
                    year_time = year_time-1
            
            month_year_string = str(month_time)+'-'+str(year_time)
            
            if month_year_string not in monthly_return_series.keys():
                monthly_return_series[month_year_string] = []
            monthly_return_series[month_year_string].append(self.historical_returns[dttime])

        ## For All Grouped Month Series, Convert List of Returns to Single Monthly Return
        for month in monthly_return_series.keys():
            self.historical_monthly_returns_string_format[month] = self.convert_to_singular_return(monthly_return_series[month])

        return 

#p=portfolio_history('9604','9/28/2016','9/28/2016')
#p.calculate_position_count()
#p.calculate_market_vals()
#p.calculate_exposures()
