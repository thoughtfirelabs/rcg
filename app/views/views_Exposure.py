from django.http import HttpResponse
from rest_framework.decorators import api_view

import datetime
import json
import pandas as pd
from ..modules.portfolio_module import portfolio
from ..modules.fund_module import fund
from ..models.models import holdingRecord

from app.fields.fields import Fields
################################################################################
################################################################################
### Helper Functions
def getDefaultDate():
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    snapshot_date = yesterday.strftime('%m/%d/%Y')
    return snapshot_date


def validateSnapshotDate(snapshot_date):
    if type(snapshot_date) is str:
        snapshot_date = pd.to_datetime(snapshot_date)
    records = holdingRecord.objects.filter(date_held=snapshot_date).all()
    if len(records) == 0:
        return False
    return True



################################################################################
################################################################################
## Overview
@api_view(['GET'])
def get_portfolio_overview(request):


    if 'snapshot_date' in request.session:
        snapshot_date = pd.to_datetime(request.session['snapshot_date'])
    else:
        snapshot_date = pd.to_datetime(getDefaultDate())

    valid = validateSnapshotDate(snapshot_date)
    if valid:
        portfolio_id = request.session['portfolio_id']
        p = portfolio(portfolio_id, snapshot_date)
        p.restrictToSnapshot = False
        p.run()

        ### Single Number Metrics for Entire Fund ##########################
        port_details = {'market_val': p.market_val,
                        'custom_notional_exposure_gross': p.custom_notional_exposure_gross,
                        'custom_notional_exposure_net': p.custom_notional_exposure_net,
                        'custom_notional_exposure_short': p.custom_notional_exposure_short,
                        'custom_notional_exposure_long': p.custom_notional_exposure_long,
                        'num_positions': p.num_positions,
                        'beta_msci': p.beta_msci,
                        'revised_beta_msci': p.revised_beta_msci,
                        'beta_sp500': p.beta_sp500,
                        'earliestDynamicDate': p.earliestDateOfDynamicData.strftime("%Y-%m-%d")}

        error_report_details = p.createFrontEndErrorReportDetails()
        content = json.dumps({'port_details': port_details, 'error_report_details': error_report_details})
        return HttpResponse(content)


## Category Exposure Analysis
@api_view(['GET'])
def get_category_exposure_analysis(request):
    
    if 'snapshot_date' in request.session:
        snapshot_date = pd.to_datetime(request.session['snapshot_date'])
    else:
        snapshot_date = pd.to_datetime(getDefaultDate())

    valid = validateSnapshotDate(snapshot_date)
    if valid:
        
        ### Create Categorization to Pass Into Portfolio
        categoryType = str(request.GET['categoryType'])  ### Specifies Instrument, Asset Class, Geographic, etc.
        fieldObj = Fields.findStaticFieldObject(categoryType)
        categorization = fieldObj.categorization
        
        ### Create Portfolio
        portfolio_id = request.session['portfolio_id']
        p = portfolio(portfolio_id, snapshot_date)
        p.restrictToSnapshot = False
        p.run(categorization=categorization)
        
        exposure_analysis = p.categorization.retrieveAnalysis()

        ### Generate Error Report
        error_report_details = p.createFrontEndErrorReportDetails()
        workspace_details = {'snapshot_date': snapshot_date.strftime('%m/%d/%Y'), 'valid': valid,
                             'portfolio_id': p.portfolio_id, 'portfolio_name': p.portfolio_name}
        content = json.dumps({'workspace_details': workspace_details, 'exposure_analysis': exposure_analysis,
                              'error_report_details': error_report_details})
        return HttpResponse(content)


    else:
        workspace_details = {'snapshot_date': snapshot_date.strftime('%m/%d/%Y'), 'valid': valid}
        content = json.dumps({'workspace_details': workspace_details})
        return HttpResponse(content)

## Overview
@api_view(['GET'])
def get_fund_overview(request):

    if 'snapshot_date' in request.session:
        snapshot_date = pd.to_datetime(request.session['snapshot_date'])
    else:
        snapshot_date = pd.to_datetime(getDefaultDate())

    valid = validateSnapshotDate(snapshot_date)
    if valid:
        
        ### Create Portfolio
        fund_id = request.session['fund_id']
        f = fund(fund_id, snapshot_date)
        f.restrictToSnapshot = False
        f.run()
        
        ### Single Number Metrics for Entire Fund ##########################
        fund_details = {'market_val': f.market_val,
                        'custom_notional_exposure_gross': f.custom_notional_exposure_gross,
                        'custom_notional_exposure_net': f.custom_notional_exposure_net,
                        'custom_notional_exposure_short': f.custom_notional_exposure_short,
                        'custom_notional_exposure_long': f.custom_notional_exposure_long,
                        'num_positions': f.num_positions,
                        'beta_msci': f.beta_msci,
                        'revised_beta_msci': f.revised_beta_msci,
                        'beta_sp500': f.beta_sp500,
                        'earliestDynamicDate': f.earliestDateOfDynamicData.strftime("%Y-%m-%d")}

        error_report_details = f.createFrontEndErrorReportDetails()
        content = json.dumps({'fund_details': fund_details, 'error_report_details': error_report_details})
        return HttpResponse(content)

## Category Exposure Analysis for Fund
@api_view(['GET'])
def get_fund_category_exposure_analysis(request):

    if 'snapshot_date' in request.session:
        snapshot_date = pd.to_datetime(request.session['snapshot_date'])
    else:
        snapshot_date = pd.to_datetime(getDefaultDate())

    valid = validateSnapshotDate(snapshot_date)
    if valid:
        
        ### Create Categorization to Pass Into Portfolio
        categoryType = str(request.GET['categoryType'])  ### Specifies Instrument, Asset Class, Geographic, etc.
        fieldObj = Fields.findStaticFieldObject(categoryType)
        categorization = fieldObj.categorization
        
        ### Create Portfolio
        fund_id = request.session['fund_id']
        f = fund(fund_id, snapshot_date)
        f.restrictToSnapshot = False
        f.run(categorization=categorization)
        
        exposure_analysis = f.categorization.retrieveAnalysis()

        ### Generate Error Report
        error_report_details = f.createFrontEndErrorReportDetails()
        workspace_details = {'snapshot_date': snapshot_date.strftime('%m/%d/%Y'), 'valid': valid,
                             'fund_id': f.fund_id, 'fund_name': f.fund_name}
        content = json.dumps({'workspace_details': workspace_details, 'exposure_analysis': exposure_analysis,
                              'error_report_details': error_report_details})
        return HttpResponse(content)

    else:
        workspace_details = {'snapshot_date': snapshot_date.strftime('%m/%d/%Y'), 'valid': valid}
        content = json.dumps({'workspace_details': workspace_details})
        return HttpResponse(content)


