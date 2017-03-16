///////////////////////////////////////////////////////////////////////////////////////
function get_portfolio_holdings(callback){
    $.ajax({
      url:'/holding_level/get_portfolio_holdings/',
       type: "get",
       success: function(response) {
        
          var holdings_content = JSON.parse(response)['holdings_content']
          var error_data = JSON.parse(response)['error_report_details']
          callback(holdings_content,error_data)
      }
    })
}
