import json
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseServerError
from app.reporting_modules.LimitReport.limitReportPDF import limitReportPDF
from app.reporting_modules.LimitReport.limitReport import LimitReport

## Limit Reporting
@api_view(['GET'])
def generateLimitReport(request):

    ### Error if snapshot date not in session.
    if 'snapshot_date' not in request.session:
        return HttpResponseServerError()

    snapshot_date = pd.to_datetime(request.session['snapshot_date'])
    report = LimitReport(snapshot_date)
    report.generate()
    limit_report_data = report.serialize()

    ### Store in Current Session for Easy Access in PDF
    request.session['limitReportData']=limit_report_data

    ### Leaving Out Error Report for Now : To Do
    ###error_report_details = p.createFrontEndErrorReportDetails()
    error_report_details = {}
    content = json.dumps({'report_content': {'limit_report_data':limit_report_data, 'error_report_details': error_report_details, 'error':False}})
    return HttpResponse(content)

### Check session for stored data to prepopulate limit report tables with.
@api_view(['GET'])
def retrieveLimitReportData(request):

    error = True ## Default
    limit_report_data={}
    if 'limitReportData' in request.session:
        limit_report_data = request.session['limitReportData']
        error = False

    error_report_details = {}
    content = json.dumps({'report_content': {'limit_report_data':limit_report_data, 'error_report_details': error_report_details, 'error':error}})
    return HttpResponse(content)

## Outputting Limit Report
@api_view(['GET'])
def generateLimitReportPDF(request):

    ### Error if snapshot date not in session.
    if 'snapshot_date' not in request.session or 'limitReportData' not in request.session:
        return HttpResponseServerError()

    snapshot_date = pd.to_datetime(request.session['snapshot_date'])
    limit_report_data = request.session['limitReportData']
    
    ### Generate Limit Report from Object
    pdfLimitReport = limitReportPDF(snapshot_date, limit_report_data)
    response = pdfLimitReport.generateResponse()

    ### To Do : Fix archiving function so that PDF is archived to J Drive.
    #pdfLimitReport.archive()
    return response

#####################################################
@api_view(['GET'])
def generate_single_manager_limit_report(request):
    # snapshot_date = pd.to_datetime(request.GET['snapshot_date'])
    # port_id = request.GET['port_id']

    # manager_report = ManagerLimitReport(port_id, snapshot_date)
    # manager_report.generate()

    # ### Check if Holdings Error for Current Date (i.e. Invalid Workspace)
    # if manager_report.date_error == True:
    #     print("Holdings Date Erorr in Portfolio - Missing Holdings Data for Date")
    #     content = json.dumps({'report_content': 'Error'})
    #     return Response(content)

    # manager_report.evaluate_constraints()

    # ### Get Number of Invalid Securities for Each Portfolio
    # num_removed_securities = 0
    # for position in manager_report.portfolio.positions:
    #     if position.valid == False:
    #         num_removed_securities += 1

    # ### Single Number Metrics for Entire Fund ##########################
    # report_content = {'guideline_names': manager_report.constraint_formal_names,
    #                   'constraints': manager_report.constraints,
    #                   'constraint_evaluation': manager_report.constraint_evaluation,
    #                   'constraint_table_data': manager_report.constraint_evaluation_numbers,
    #                   'all_numbers_table_data': manager_report.all_evaluation_numbers}

    #content = json.dumps({'report_content': report_content, 'num_removed_securities': num_removed_securities})
    content = json.dumps({'report_content': 'test', 'num_removed_securities': 'test'})
    return Response(content)

