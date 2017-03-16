from reportlab.platypus import Paragraph, Frame, Table,SimpleDocTemplate, PageBreak, Spacer, PageTemplate, NextPageTemplate
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from reportlab.lib.units import inch
import pandas as pd
from io import BytesIO

from django.http import HttpResponse
from app.settings import settings
from reportlab.lib.utils import ImageReader

from app.reporting_modules.LimitReport.tableOptions import TableOptions

######################################################################################################
class limitReportPDF:
    
    categoryFormalNames = {'geo':'Geographical Exposures',
                            'instrument':'Instrument and Asset Class Exposures','misc':'Other Constraints',
                            'misc':'Other Constraints','sector_industry':'Sector and Industry Concentration',
                            'beta':'Portfolio Betas','concentration':'Portfolio Concentrations','general':'Overview Exposures'}
    
    categoryOrder = ['general','concentration','beta','geo','instrument','sector_industry','misc']
    
    def __init__(self,date, limit_report_data):

        self.date = date
        self.baseData = limit_report_data
        
        if type(self.date) == str:
            self.date = pd.to_datetime(self.date)
        self.date = self.date.strftime("%Y-%m-%d") 
        self.filename = "LimitReport_"+self.date+".pdf"
        self.report_download_dir_ext = "/Reporting/LimitReports/LimitReport_"+self.date+".pdf"

        ### Hosted Online
        self.imageUrl = 'https://s3.postimg.org/epto6jhub/RCGLogo.jpg'

        ### Local and J Drive Archive Directories
        self.settings = settings()
        self.server_total_download_dir = str(self.settings.server_archive_directory+self.report_download_dir_ext)
        self.local_total_download_dir = str(self.settings.local_archive_directory+self.report_download_dir_ext)

        self.all_table_data = None
        self.applicable_table_data = None
        self.guidelines = None
        self.headers = None
        self.highlightedInds = None

        self.response = None
        return
    
    #################################
    def generateResponse(self):

        ### Create Response for PDF
        self.response = HttpResponse(content_type='application/pdf')
        self.response['Content-Disposition'] = 'attachment; filename="'+self.filename+'"'
        self.response['fileName'] = self.filename

        buff = BytesIO()
        doc = SimpleDocTemplate(buff, rightMargin=72, leftMargin=72, topMargin=30,
                                bottomMargin=72, pagesize=TableOptions.pageSize)
        c = canvas.Canvas(self.response)
        c = self.draw(c,doc)

        pdf = buff.getvalue()
        buff.close()

        self.response.write(pdf) 
        return self.response
        
    #######################################
    ### Generate set of applicable and non applicable tables for a single grouping
    def generateTable(self,tableData):
        
        constraintIDs = tableData.keys()
        
        applicableTableData = []
        nonApplicableTableData = []
        breaches = []
        
        ### Add Manager Headers First
        headerRow = [""]
        for i in range(len(self.portIDs)):
            headerRow.append(self.managerNameConv[str(self.portIDs[i])])
        
        applicableTableData.append(headerRow)
        nonApplicableTableData.append(headerRow)

        ### Populate Table Data
        for i in range(len(constraintIDs)):
            constraintID = constraintIDs[i]
            
            applicableRowData = []
            nonApplicableRowData = []
            rowJson = tableData[constraintID]
            formalConstraintName = self.formalConstraintNameConv[constraintID]
           
            ### Add Constraint Name 
            applicableRowData.append(formalConstraintName)
            nonApplicableRowData.append(formalConstraintName)
            
            ### Loop Over Managers for Each Column
            for j in range(len(self.portIDs)): 
                port_id=str(self.portIDs[j])
                constraintData = rowJson[port_id]
                
                val = str(round(100.0*constraintData['value'],2))+' %'

                nonApplicableRowData.append(val) ### Always Include
                applicable = constraintData['applicable']
                
                if not applicable:
                    applicableRowData.append("")
                    
                if applicable:
                    applicableRowData.append(val)
                    breached = constraintData['breached']
                    if breached:
                        breaches.append((i,j))
            
            applicableTableData.append(applicableRowData)
            nonApplicableTableData.append(nonApplicableRowData)
        
        ### Table Styling
        style = TableOptions.standardRCGTableStyle2()
        for i in range(len(breaches)):
            tup = (breaches[i][1]+1,breaches[i][0]+1)
            style.append(('BACKGROUND', tup, tup,colors.yellow))
        
        from reportlab.lib.units import mm
        colWidths=(68*mm, 16*mm, 16*mm, 16*mm, 16*mm, 16*mm, 16*mm, 16*mm)
        
        applicableTable = Table(applicableTableData, colWidths=colWidths, style=style,hAlign='CENTER')
        nonApplicableTable = Table(nonApplicableTableData, colWidths=colWidths, style=style,hAlign='CENTER')
        return applicableTable, nonApplicableTable
    
    #################################
    ### Creates the canvas on either  the directory for archive or the respnose object.
    def draw(self,canvas,doc):
        
        self.createTables()
        
        ##########
        def firstPage(canvas, doc):
            canvas.saveState()
            cumHeight = self.drawHeaderOnCanvas(canvas, doc)

            ### Unique to Page 1
            pPage1 = Paragraph("Only Applicable Limits Shown:", TableOptions.styleN)
            w, h = pPage1.wrap(doc.width, doc.topMargin)
            pPage1.drawOn(canvas, doc.leftMargin - TableOptions.marginXOffset, TableOptions.pageHeight - cumHeight - 30)

            self.drawFooterOnCanvas(canvas, doc)
            canvas.restoreState()

        ##########
        def mySecondPage(canvas, doc):

            canvas.saveState()
            cumHeight = self.drawHeaderOnCanvas(canvas, doc)

            ### Unique to Page 2
            pPage2 = Paragraph("All Calculations Shown:", TableOptions.styleN)
            w, h = pPage2.wrap(doc.width, doc.topMargin)
            pPage2.drawOn(canvas, doc.leftMargin - TableOptions.marginXOffset, TableOptions.pageHeight - cumHeight - 30)

            self.drawFooterOnCanvas(canvas, doc)
            canvas.restoreState()

        templateFrame = Frame(0.5 * inch, 1.0 * inch, 7.5 * inch, 8.5 * inch, id='templateFrame')
        pageTemplate1 = PageTemplate(id='pageTemplate1', frames=[templateFrame], onPage=firstPage)
        pageTemplate2 = PageTemplate(id='pageTemplate2', frames=[templateFrame], onPage=mySecondPage)

        Story = []
        
        tableheaderStyle = TableOptions.styleH
        tableheaderStyle.fontSize = 10
        for i in range(len(self.applicableTables)):
            
            table = self.applicableTables[i]
            
            ### Create Grouping Header Paragraph
            grouping = self.categoryOrder[i]
            formalGrouping = limitReportPDF.categoryFormalNames[grouping]
            categoryParagraph = Paragraph(formalGrouping, tableheaderStyle)
            
            Story.append(categoryParagraph)
            Story.append(table)
            Story.append(TableOptions.vspace)

        Story.append(NextPageTemplate('pageTemplate2'))
        Story.append(PageBreak())
        
        for i in range(len(self.nonApplicableTables)):
            table = self.nonApplicableTables[i]
            
            ### Create Grouping Header Paragraph
            grouping = self.categoryOrder[i]
            formalGrouping = limitReportPDF.categoryFormalNames[grouping]
            categoryParagraph = Paragraph(formalGrouping, tableheaderStyle)
            
            Story.append(categoryParagraph)
            Story.append(table)
            Story.append(TableOptions.vspace)
            
        Story.append(PageBreak())
        
        doc.addPageTemplates([pageTemplate1, pageTemplate2])
        doc.build(Story)

        return canvas
        
    ### Loop through groupings and create all of the tables
    def createTables(self):
        
        self.portIDs = self.baseData['portIDs']
        self.groupingNames = self.baseData['groupingNames']
        self.formalConstraintNameConv = self.baseData['formalConstraintNameConv']
        self.managerNameConv = self.baseData['managerNameConv']
        self.categoryFormalNames = self.baseData['table_settings']['categoryFormalNames']
        
        self.categoryOrder = self.baseData['table_settings']['categoryOrder']
        tables = self.baseData['tables']
        
        self.applicableTables = []
        self.nonApplicableTables = []
        
        ### Loop Over Different Tables
        for grouping in self.categoryOrder:
            
            tableData = tables[grouping]
            applicableTable, nonApplicableTable = self.generateTable(tableData)
            self.applicableTables.append(applicableTable)
            self.nonApplicableTables.append(nonApplicableTable)
    
        return
        
    #########################################
    def drawFooterOnCanvas(self,canvas,doc):
        footerText = """Data as of the date indicated above.
                This information contains confidential and proprietary information that cannot be disclosed to any third parties or used for any purpose unrelated to the investor's investment in the fund or the
                account referenced herein.
                You agree that you will not distribute any information herein without the express
                written approval of Rock Creek.
                Past performance of the referenced managers and their funds is not indicative of future results.
                The analysis herein is based on available data and information prepared and reported
                by the referenced managers.
                Rock Creek has not verified and is not liable or responsible for the
                completeness or accuracy of such information and
                information about the referenced managers.
                As such, there can be no assurances that this material is
                a complete and accurate depiction of, among other things,
                the applicable manager's exposures to the guidelines listed herein."""

        footer = Paragraph(footerText, style=TableOptions.standardRCGFooterStyle())

        w, h = footer.wrap(doc.width + 80, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin - 40, doc.bottomMargin - 60)
        return

    #########################################
    def drawHeaderOnCanvas(self,canvas,doc):
        mainHeaderStyle = TableOptions.styleH
        mainHeaderStyle.fontSize = 14
        ### Base Paragraphs
        pgraphs = []
        p1 = Paragraph("Rock Creek Investment Guidelines Report",mainHeaderStyle)
        pgraphs.append(p1)

        p2 = Paragraph("Wells Fargo Alternative Strategies Fund",TableOptions.styleN)
        pgraphs.append(p2)

        p3 = Paragraph(self.date,TableOptions.styleN)
        pgraphs.append(p3)

        ### Header Logo
        logo = ImageReader(self.imageUrl)
        canvas.drawImage(logo, TableOptions.imageMarginX, TableOptions.pageHeight - 50, width=TableOptions.imageWidth, height=TableOptions.imageHeight,
                         mask='auto')

        cumHeight = 1.0 * inch
        for pgraph in pgraphs:
            w, h = pgraph.wrap(doc.width, doc.topMargin)
            cumHeight += h
            pgraph.drawOn(canvas, doc.leftMargin - TableOptions.marginXOffset, TableOptions.pageHeight - cumHeight-0.5)

        return cumHeight

    #################################################
    #### Writes PDF Generated to Directory in J Drive to Archive PDF
    def archive(self):

        buff = BytesIO()
        doc = SimpleDocTemplate(buff, rightMargin=72, leftMargin=72, topMargin=30,
                                bottomMargin=72, pagesize=TableOptions.pageSize)
        c = canvas.Canvas(self.response)
        c = self.draw(c, doc)

        pdf = buff.getvalue()

        file = open(self.local_total_download_dir, 'w')
        file.write(pdf)
        file.close()

        buff.close()

        return



