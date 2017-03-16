///////////////////////////////////////////////////////////////////////////////
function downloadSecurityDetails(referenceID,selection){

  // Snapshot date will be grabbed from session on back end.

  /// AJAX Call to Download Exposure Report
  getFile = $.ajax({
        url:'download_security_details/',
         type: "get",
         data: {'referenceID':referenceID, 'selection':selection},
         success: function(response) {
            
            var fileName = getFile.getResponseHeader('fileName')

            var blob=new Blob([response]);
            var link=document.createElement('a');
            link.href=window.URL.createObjectURL(blob);
            link.download=fileName
            link.click();
         }
    })

}
///////////////////////////////////////////////////////////////////////////////
function downloadExposureReport(referenceID,selection){
  
  /// AJAX Call to Download Exposure Report
  getFile = $.ajax({
        url:'download_exposure_report/',
         type: "get",
         data: {'referenceID':referenceID, 'selection':selection},
         success: function(response) {
            
            var fileName = getFile.getResponseHeader('fileName')

            var blob=new Blob([response]);
            var link=document.createElement('a');
            link.href=window.URL.createObjectURL(blob);
            link.download=fileName
            link.click();
         }
    })
}


