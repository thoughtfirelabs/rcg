import json
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..modules.portfolio_module import portfolio
from django.http import HttpResponseServerError

############################################################################
@api_view(['GET'])
def get_portfolio_holdings(request):

    if 'snapshot_date' not in request.session or 'portfolio_id' not in request.session:
        return HttpResponseServerError()

    snapshot_date = pd.to_datetime(request.session['snapshot_date'])
    portfolio_id = str(request.session['portfolio_id'])

    p = portfolio(portfolio_id, snapshot_date)
    p.restrictToSnapshot = False

    p.run()

    instrument_dict = {}

    sec_name_dict = {}
    search_name_dict = {}

    issuer_dict = {}
    sector_dict = {}
    country_dict = {}

    region_dict = {}
    market_dict = {}
    industry_dict = {}

    pos_dict = {}
    mkt_val_dict = {}
    gross_custom_notional_dict = {}
    gross_delta_notional_dict = {}

    for security in p.securities:
        sec_id = security.rcg_id

        instrument_dict[sec_id] = security.InstrumentType.value
        sec_name_dict[sec_id] = security.SecurityName.value
        search_name_dict[sec_id] = security.SearchName.value

        issuer_dict[sec_id] = security.Issuer.value
        sector_dict[sec_id] = security.Sector.value
        country_dict[sec_id] = security.Country.value
        region_dict[sec_id] = security.Region.value
        market_dict[sec_id] = security.MarketType.value
        industry_dict[sec_id] = security.Industry.value

        pos_dict[sec_id] = security.PositionDesignation.value

        mkt_val_dict[sec_id] = security.market_val
        gross_custom_notional_dict[sec_id] = security.gross_custom_notional
        gross_delta_notional_dict[sec_id] = security.gross_delta_notional

    holdings_content = {'instrument_type': instrument_dict,
                        'security_name': sec_name_dict,
                        'search_name':search_name_dict,
                        'sector': sector_dict,
                        'industry': industry_dict,
                        'issuer': issuer_dict,
                        'country': country_dict,
                        'market_tp':market_dict,
                        'region':region_dict,
                        'position_designation': pos_dict,
                        'market_val': mkt_val_dict,
                        'gross_custom_notional': gross_custom_notional_dict,
                        'gross_delta_notional': gross_delta_notional_dict}

    error_report_details = p.createFrontEndErrorReportDetails()
    content = json.dumps({'holdings_content': holdings_content, 'error_report_details': error_report_details})
    return Response(content)


