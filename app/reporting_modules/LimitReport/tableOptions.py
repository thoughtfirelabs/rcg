import locale
from reportlab.platypus import Table
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet

##########################################################################
class TableOptions:
    
    stylesheet = getSampleStyleSheet()
    styleN = stylesheet['Normal']
    styleH = stylesheet['Heading1']
    styleS = stylesheet['Normal']
    vspace = Spacer(8.5*inch,0.15*inch)

    ##### Spacing Parameters
    pageSize = A4
    pageHeight=pageSize[1]; pageWidth=pageSize[0]
    imageMarginX = 10
    imageHeight = 0.5*inch
    imageWidth = pageWidth - 2*imageMarginX
    marginXOffset = 30
        
        
    @staticmethod
    def standardRCGTable(data, headings, colwidths=None, colFormats=None, colMultipliers=None):
        
        locale.setlocale(locale.LC_ALL, '')
        if colFormats != None and colMultipliers != None:
            for i in range(len(data)):
                for j in range(1, len(data[i])):
                    if j >= len(colFormats):
                        format = colFormats[-1]
                    else:
                        format = colFormats[j - 1]
                
                if j >= len(colMultipliers):    
                    mult = colMultipliers[-1]   
                else:
                    mult = colMultipliers[j - 1]
                try:
                    if data[i][j] == 'Insignificant':
                        data[i][j] = ''
                    elif mult == 100:
                        data[i][j] = locale.format(format, data[i][j]*mult)  + '%'
                    else:
                        data[i][j] = locale.format(format, data[i][j], grouping=True)
                except:
                    data[i][j] = locale.format('%s', data[i][j])
         
        data.insert(0, headings)
        style = TableOptions.standardRCGTableStyle2()
        return Table(data, colWidths=colwidths, style=style)
     
    @staticmethod
    def standardRCGFooterStyle():
        font = 'Times-Roman'
        fontSize=7
        style = ParagraphStyle('default',fontName=font,fontSize=fontSize)
        style.leading = 8
        return style

    @staticmethod
    def standardRCGTableStyle(fontSize=7, padding=0.5):
        
        font = 'Times-Roman'
        rcgblue2 = colors.Color(0.33, 0.30, 0.55)
        lightgrey = colors.Color(0.7, 0.7, 0.7)
        return [('FONT', (0, 0), (-1, -1), font, fontSize),

            ('TOPPADDING', (0, 0), (-1, -1), padding),
            ('BOTTOMPADDING', (0, 0), (-1, -1), padding),
             ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
             ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
             ('LINEABOVE', (0, 1), (-1, 1), 1, rcgblue2),
             ('FONT', (0, 0), (-1, 0), font),
             ('ROWBACKGROUNDS', (0, 1), (-1, -1), [lightgrey, None]),
             ('FONT', (0, -1), (-1, -1), font)]

    @staticmethod
    def standardRCGTableStyle2(fontSize=7):
        padding=0.5
        font = 'Times-Roman'

        return [('FONT', (0, 0), (-1, -1), font, fontSize), ('TOPPADDING', (0, 0), (-1, -1), 0.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 0.5),
            ('TOPPADDING', (0, 0), (-1, -1), padding),
             ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOTTOMPADDING', (0, 0), (-1, -1), padding),
             ('INNERGRID', (0,0), (-1,-1), 0.25, colors.lightgrey),
             ('OUTERGRID', (0,0), (-1,-1), 0.25, colors.black),
             ('ALIGN', (1, 0), (-1, -1), 'CENTER'), ('ALIGN', (1, 1), (1, -1), 'CENTER'), ('LINEABOVE', (0, 1), (-1, 1), 1, colors.black),
             ('FONT', (0, 0), (-1, 0), font), 
             ('LINEBEFORE', (1, 0), (1, -1), 0.25, colors.black), ('FONT', (0, -1), (-1, -1), font)]


