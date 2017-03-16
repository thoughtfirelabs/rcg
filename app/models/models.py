import sys
sys.dont_write_bytecode = True
from django.db import models


#######################################################################
class Portfolio(models.Model):
    db_table = 'portfolios'

    id = models.BigIntegerField(primary_key=True, unique=True)
    portfolio_name = models.CharField(max_length=50, null=False)
    strategy = models.CharField(max_length=50, null=True)
    portfolio_description = models.CharField(max_length=50, null=True)
    fund_id = models.CharField(max_length=10, null=False)
    fund_name = models.CharField(max_length=20, null=False)

    class Meta:
        managed = True
        db_table = 'portfolios'

    def __repr__(self):
        return "<Portfolio(id='%s', portfolio_name='%s', portfolio_description='%s', fund_name='%s')>" % (
            self.id, self.portfolio_name, self.portfolio_description, self.fund_name)


#######################################################################
class Fund(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=50, null=True)

    class Meta:
        managed = True
        db_table = 'funds'

    def __repr__(self):
        return "<Fund(id='%s', name='%s', description='%s')>" % (
            self.id, self.name, self.description)


#######################################################################
class holdingRecord(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    rcg_id = models.CharField(max_length=50, null=False)
    ssid = models.CharField(max_length=50, null=True)
    date_held = models.DateField(null=False)
    rcg_portfolio_id = models.CharField(max_length=50, null=False)
    ss_portfolio_id = models.CharField(max_length=50, null=True)

    port_name = models.CharField(max_length=50, null=True)
    sec_name = models.CharField(max_length=50, null=False)

    sdl = models.CharField(max_length=50, null=True)
    isin = models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=50, null=False)
    ss_asset_class = models.CharField(max_length=50, null=True)

    price = models.FloatField(null=True)
    market_val = models.FloatField(null=True)
    unrealized_gains_losses = models.FloatField(null=True)
    quantity = models.FloatField(null=True)

    #################################
    class Meta:
        managed = True
        db_table = 'state_street_holdings'

    #################################
    def __repr__(self):
        return "<holdingRecord(id='%s', date='%s', rcg_id='%s', position='%s')>" % (
            self.id, self.date_held, self.rcg_id, self.position)

    #################################
    @property
    def portfolio_name(self):
        return self.port_name

    #################################
    @property
    def market_price(self):
        return self.market_price

    #################################
    @property
    def position_designation(self):
        return self.position

    #################################
    @property
    def ss_market_val(self):
        return self.market_val

    #################################
    @property
    def id_isin(self):
        return self.isin

    #################################
    @property
    def id_sedol1(self):
        return self.sdl

    #################################
    @property
    def id_cusip(self):
        return self.ssid

    #################################
    @property
    def security_name(self):
        return self.sec_name

    #################################
    @property
    def portfolio_id(self):
        return self.rcg_portfolio_id


#######################################################################
class dynamicRecord(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    rcg_id = models.CharField(max_length=50, null=False)
    date = models.DateField(null=False)
    measurement_type = models.CharField(max_length=50, null=False)
    value = models.FloatField(null=False)

    class Meta:
        managed = True
        db_table = 'dynamic_securities'

    ####################################################################
    def __repr__(self):
        return "<dynamicRecord(id='%s', date='%s', rcg_id='%s', measurement_type='%s')>" % (
            self.id, self.date, self.rcg_id, self.measurement_type)

##############################################################################
class staticRecord(models.Model):
    rcg_id = models.CharField(primary_key=True, max_length=50, unique=True)
    id_cusip = models.CharField(max_length=50, null=True)
    id_isin = models.CharField(max_length=50, null=True)
    id_sedol1 = models.CharField(max_length=50, null=True)

    security_name = models.CharField(max_length=50, null=True)
    ss_asset_class = models.CharField(max_length=50, null=True)
    search_name = models.CharField(max_length=50, null=True)

    ###### Proxy Information
    proxy_rcg_id = models.CharField(max_length=50, null=True)

    #### Underlying Information
    underlying_rcg_id = models.CharField(max_length=50, null=True)

    ##### Classification Information
    instrument_type = models.CharField(max_length=50, null=True)
    security_typ = models.CharField(max_length=50, null=True)
    security_typ2 = models.CharField(max_length=50, null=True)
    market_sector_des = models.CharField(max_length=50, null=True)
    bpipe_reference_security_class = models.CharField(max_length=50, null=True)

    ####### Detail Information
    gics_sector = models.BigIntegerField(null=True)
    gics_sector_name = models.CharField(max_length=50, null=True)

    issuer = models.CharField(max_length=50, null=True)
    country_full_name = models.CharField(max_length=50, null=True)
    cntry_of_risk = models.CharField(max_length=50, null=True)

    px_pos_mult_factor = models.FloatField(null=True)
    bics_level_3_industry_name = models.CharField(max_length=50, null=True)


    ####################################################################
    class Meta:
        managed = True
        db_table = 'static_securitiesV2'
    ####################################################################
    def __repr__(self):
        return "<staticRecord(rcg_id='%s', security_name='%s', instrument_type='%s', search_name='%s')>" % (
            self.rcg_id, self.security_name, self.instrument_type, self.search_name)

    ### Stores the contents of a field object to the static record
    def saveField(self,fieldObj):

        setSuccessful = False
        for possibleName in fieldObj.alternates:
            if hasattr(self,possibleName):
                setattr(self,possibleName,fieldObj.value)
                setSuccessful = True

        if not setSuccessful:
            print 'Cannot Attribute : ', fieldObj.internalFieldName, ' to Static Record'


        return
