// Functions that communicate to the back end asynchronously and retreive data
// which is then used to populate the HTML fields/tables.
function get_fund_overview(dataHandler){

    $.ajax({
         url:'get_fund_overview/',
         type: "get",
         success: function(response) {
            var overview_data = JSON.parse(response)['fund_details']
            var error_data = JSON.parse(response)['error_report_details']
            dataHandler(overview_data,error_data)
         }
      })   
}

///////////////////////////////////////////////////////////////////////////////
// Gets the exposure of a portfolio to a certain category breakdown (region, instrument, etc.)
function get_fund_overview_exposure(categoryType,callback){

    $.ajax({
        url:"get_fund_category_exposure_analysis/",
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



///////////////////////////////////////////////////////////////////////////////
// Draws Polar Chart and instrument Exposure Table
function get_specific_fund_exposure(exposure_type){
    
    $('#exposure_type_header').html('% of Total Gross Exposure')

    // Get fund ID and Snapshot Date from Local Storage
    var snapshot_date = localStorage.getItem("snapshot_date");
    var fund_id = localStorage.getItem("fund_id");

    ////////////////////////
    $.ajax({
        url:'get_category_exposure_analysis/',
         type: "get",
         data: {'fund_id':fund_id,'snapshot_date':snapshot_date,'type':'region'},
         success: function(response) {
            
            var overview_data1 = JSON.parse(response)['exposure_analysis']

            /// Data for Handling Errors and Missing Securities
            var error_data = JSON.parse(response)['error_report_details']
            /// Handle All Other Data
            var position_count1 = overview_data1['position_count']
            if (exposure_type=='Gross'){
                exposures1 = overview_data1['gross_exposures']
                exposure_nav1 = overview_data1['gross_notional_nav']
            }
            else if (exposure_type=='Net'){
                exposures1 = overview_data1['net_exposures']
                exposure_nav1 = overview_data1['net_notional_nav']
            }
            else if (exposure_type=='Long'){
                exposures1 = overview_data1['long_exposures']
                exposure_nav1 = overview_data1['long_notional_nav']
            }
            else if (exposure_type=='Short'){
                exposures1 = overview_data1['short_exposures']
                exposure_nav1 = overview_data1['short_notional_nav']
            }
            ////////////////////////
            $.ajax({
                url:'get_category_exposure_analysis/',
                 type: "get",
                 data: {'fund_id':fund_id,'snapshot_date':snapshot_date,'type':'country'},
                 success: function(response) {

                    var overview_data2 = JSON.parse(response)['exposure_analysis']
                    var position_count2 = overview_data2['position_count']
                    if (exposure_type=='Gross'){
                        exposures2 = overview_data2['gross_exposures']
                        exposure_nav2 = overview_data2['gross_notional_nav']
                    }
                    else if (exposure_type=='Net'){
                        exposures2 = overview_data2['net_exposures']
                        exposure_nav2 = overview_data2['net_notional_nav']
                    }
                    else if (exposure_type=='Long'){
                        exposures2 = overview_data2['long_exposures']
                        exposure_nav2 = overview_data2['long_notional_nav']
                    }
                    else if (exposure_type=='Short'){
                        exposures2 = overview_data2['short_exposures']
                        exposure_nav2 = overview_data2['short_notional_nav']
                    }
                    ////////////////////////
                    $.ajax({
                        url:'get_category_exposure_analysis/',
                         type: "get",
                         data: {'fund_id':fund_id,'snapshot_date':snapshot_date,'type':'market_type'},
                         success: function(response) {

                            var overview_data3 = JSON.parse(response)['exposure_analysis']
                            var position_count3 = overview_data3['position_count']
                            if (exposure_type=='Gross'){
                                exposures3 = overview_data3['gross_exposures']
                                exposure_nav3 = overview_data3['gross_notional_nav']
                            }
                            else if (exposure_type=='Net'){
                                exposures3 = overview_data3['net_exposures']
                                exposure_nav3 = overview_data3['net_notional_nav']
                            }
                            else if (exposure_type=='Long'){
                                exposures3 = overview_data3['long_exposures']
                                exposure_nav3 = overview_data3['long_notional_nav']
                            }
                            else if (exposure_type=='Short'){
                                exposures3 = overview_data3['short_exposures']
                                exposure_nav3 = overview_data3['short_notional_nav']
                            }
                            ////////////////////////
                            $.ajax({
                                url:'get_category_exposure_analysis/',
                                 type: "get",
                                 data: {'fund_id':fund_id,'snapshot_date':snapshot_date,'type':'rcg_geo_bucket'},
                                 success: function(response) {

                                    var overview_data4 = JSON.parse(response)['exposure_analysis']
                                    var position_count4 = overview_data4['position_count']
                                    if (exposure_type=='Gross'){
                                        exposures4 = overview_data4['gross_exposures']
                                        exposure_nav4 = overview_data4['gross_notional_nav']
                                    }
                                    else if (exposure_type=='Net'){
                                        exposures4 = overview_data4['net_exposures']
                                        exposure_nav4 = overview_data4['net_notional_nav']
                                    }
                                    else if (exposure_type=='Long'){
                                        exposures4 = overview_data4['long_exposures']
                                        exposure_nav4 = overview_data4['long_notional_nav']
                                    }
                                    else if (exposure_type=='Short'){
                                        exposures4 = overview_data4['short_exposures']
                                        exposure_nav4 = overview_data4['short_notional_nav']
                                    }


                                    ////////////////////////////////////////////////////////////////////////
                                    var dataTable1 = create_specific_exposure_table('#exposure_table1',position_count1,exposures1,exposure_nav1)
                                    var dataTable2 = create_specific_exposure_table('#exposure_table2',position_count2,exposures2,exposure_nav2)
                                    var dataTable3 = create_specific_exposure_table('#exposure_table3',position_count3,exposures3,exposure_nav3)
                                    dataTable1.draw()
                                    dataTable2.draw()
                                    dataTable3.draw()
                                    
                                    ////////////////////////////////////////////////////////////////////////
                                    // Create All Polar Charts
                                    exposures = [exposures1,exposures2,exposures3]
                                    chart_divs = ['#chart1 svg','#chart2 svg','#chart3 svg']
                                    legend_divs = ['#legend1 svg','#legend2 svg','#legend3 svg']
                                    for(var i = 0; i<exposures.length; i++){

                                        var donut_pieces = create_donut_chart(350,350,exposures[i])
                                        var chart = donut_pieces[0]
                                        var chart_data = donut_pieces[1]
                                        legend = donut_pieces[2]
                                        legend = legend.padding(25)
                                        legend = legend.width(400)
                                        legend = legend.height(600)

                                        var legend_data = donut_pieces[3]

                                        d3.select(chart_divs[i])
                                            .datum([chart_data])
                                            .transition().duration(500)
                                            .call(chart);


                                        d3.select(legend_divs[i])
                                            .datum(legend_data)
                                            .call(legend);

                                        handle_data_report(error_data,false)
                                        $('#specific_exposure_div').show();
                                        nv.addGraph(chart)
                                    }
                                }})
                            }})
                        }})
                    }})
}