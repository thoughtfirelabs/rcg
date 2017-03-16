from django.http import HttpResponse

#########################################################
### Inherited by PDF Objects to Create Downloadable PDF Response
class pdfResponse:
    def __init__(self):
        self.delimeter = ','
        self.filename = self.reportName + '.pdf'

        self.response = HttpResponse(content_type='application/pdf')
        self.response['Content-Disposition'] = 'attachment; filename="'+self.filename+'"'

        self.response['fileName'] = self.filename
        return


