// Functions that communicate to the back end asynchronously and retreive data
// which is then used to populate the HTML fields/tables.

///////////////////////////////////////////////////////////////////////////////
function get_portfolio_overview(dataHandler){

    $.ajax({
         url:'get_portfolio_overview/',
         type: "get",
         success: function(response) {

            var overview_data = JSON.parse(response)['port_details']
            var error_data = JSON.parse(response)['error_report_details']
            dataHandler(overview_data,error_data)
         }
      })   
}

///////////////////////////////////////////////////////////////////////////////
// Gets the exposure of a portfolio to a certain category breakdown (region, instrument, etc.)
function get_portfolio_overview_exposure(categoryType,callback){

    $.ajax({
        url:"get_category_exposure_analysis/",
         type: "get",
         data: {'categoryType':categoryType},
         success: function(response) {
            var overview_data = JSON.parse(response)['exposure_analysis']
            var error_data = JSON.parse(response)['error_report_details']
            callback(overview_data,error_data);
            return 
         }
     });

};
