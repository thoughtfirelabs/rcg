////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Chart Utility Functions

function filter_values(values_to_plot){

    var min_value = values_to_plot[0][0]
    var max_value = values_to_plot[0][0]

    new_values_to_plot = new Array()
    for (var i = 0; i<values_to_plot.length; i++){

        if(values_to_plot[i][1]<min_value){
           min_value = values_to_plot[i][1]
        }
        if(values_to_plot[i][1]>max_value){
          max_value = values_to_plot[i][1]
        }
    }
    return [min_value,max_value]
}

////////////////////////////////////////////////////////
function create_portfolio_table(div_name,portfolio_data){

   var dataTable = $(div_name).DataTable({"pageLength": 8, "searching":false, "retrieve": true,"sDom": 'rt'});
   dataTable.clear();

   // Create Table Rows
    for(var i = 0; i<portfolio_data.length; i++){
        var new_row = []
       
        new_row.push(portfolio_data[i].id)
        new_row.push(portfolio_data[i].portfolio_name)
        new_row.push(portfolio_data[i].strategy)

        new_row.push(portfolio_data[i].portfolio_description)
        new_row.push(portfolio_data[i].fund_id)
        new_row.push(portfolio_data[i].fund_name)

        dataTable.row.add(new_row)

    }
    return dataTable
}
////////////////////////////////////////////////////////
function create_missing_data_table(div_name,fatal_data_report){

   var dataTable = $(div_name).DataTable({"pageLength": 12, "searching":false, "retrieve": true});
   dataTable.clear();

   // Create Table Rows
    for(var i = 0; i<fatal_data_report.length; i++){
        var new_row = []
        var row = fatal_data_report[i]
        for(var j = 0; j<row.length; j++){
            new_row.push(row[j])
        }
        dataTable.row.add(new_row)
    }
    return dataTable
}

////////////////////////////////////////////////////////
function create_reporting_portfolio_table(div_name,portfolio_ids,portfolio_names,region_constraints,market_constraints,instrument_constraints){

   var dataTable = $(div_name).DataTable({"pageLength": 8, "searching":false, "retrieve": true,"sDom": 'rt'});
   dataTable.clear();

   // Create Table Rows
    for(var i = 0; i<portfolio_ids.length; i++){
        var new_row = []
        var port_id = portfolio_ids[i]

        new_row.push(portfolio_ids[i])
        new_row.push(portfolio_names[i])

        if (typeof(region_constraints[portfolio_ids[i]]) != "undefined"){
            new_row.push(region_constraints[portfolio_ids[i]])
        }
        else{
            new_row.push("")
        }

        if (typeof(market_constraints[portfolio_ids[i]]) != "undefined"){
            new_row.push(market_constraints[portfolio_ids[i]])
        }
        else{
            new_row.push("")
        }

        if (typeof(instrument_constraints[portfolio_ids[i]]) != "undefined"){
            new_row.push(instrument_constraints[portfolio_ids[i]])
        }
        else{
            new_row.push("")
        }
        dataTable.row.add(new_row)

    }
    return dataTable
}
////////////////////////////////////////////////////////
function create_fund_table(div_name,fund_data){

   var dataTable = $(div_name).DataTable({"pageLength": 8, "searching":false, "retrieve": true,"sDom": 'rt'});
   dataTable.clear();
   for (var i = 0; i<fund_data.length; i++){

        var new_row = []
        new_row.push(fund_data[i].id)
        new_row.push(fund_data[i].fund_name)
        new_row.push(fund_data[i].fund_description)
        
        dataTable.row.add(new_row)
    }
    return dataTable
}
////////////////////////////
function create_manager_table(div_name,manager_data){

   var dataTable = $(div_name).DataTable({"pageLength": 8, "searching":false, "retrieve": true});
   dataTable.clear();
   for (var i = 0; i<manager_data.length; i++){

        var new_row = []
        new_row.push(manager_data[i].id)
        new_row.push(manager_data[i].portfolio_name)
        new_row.push(manager_data[i].strategy)
        new_row.push(manager_data[i].portfolio_description)
        
        dataTable.row.add(new_row)
    }
    return dataTable
}
////////////////////////////
function create_bar_chart(height,width,plot_data,filter){

    dates = Object.keys(plot_data)

    values_to_plot=new Array()
    for (var i = 0; i<dates.length; i++){
        values_to_plot.push([dates[i],plot_data[dates[i]]])
    }

    if(filter == true){
        min_value = filter_values(values_to_plot)[0]
        max_value = filter_values(values_to_plot)[1]
    }
    chart_data=new Array()
    chart_data.push({'key':'Gross','values':values_to_plot})

    var chart = nv.models.multiBarChart()

    // Chart Formatting/Displaying Options
    chart.height = height
    chart.width = width
    chart.color(d3.scale.category10().range())
    chart.x(function(d) { return d[0]; })
    chart.y(function(d) { return d[1]; })

    chart.xAxis.tickFormat(function(d) { return d3.time.format('%b %d %y')(new Date(d)) });
    chart.yAxis.tickFormat(d3.format(',.3f'));
    chart.yAxis.tickPadding(25);
    
    chart.forceY([min_value,max_value])

  return [chart,chart_data]
}
////////////////////////////
function create_donut_chart(height,width,plot_data){
    
    // Put Data in Right Format
    var chart_data = new Array()
    var legend_data = new Array()

    keys = Object.keys(plot_data)
    for(var i = 0; i<keys.length; i++){
        chart_data.push([keys[i],plot_data[keys[i]]])
        legend_data.push({key:keys[i]})
    }

    var chart = nv.models.pie()
        .x(function(d) { return d[0]; })
        .y(function(d) { return d[1]; })
        .width(width)
        .height(height)
        .labelType('percent')
        .valueFormat(d3.format('%'))
        .donut(true)
        .showLabels(true);

    var legend = nv.models.legend()
        .align('center')
        .padding(20)
        .width(350);

    return [chart,chart_data,legend,legend_data]

}
////////////////////////////
// Name of Cateegory, Num Positions, Market Val, Weight by Market val, Gross Exp, % Total Gross Exp
function create_overview_table(div_name,position_count, market_vals, gross_exposures, gross_allocations, additional_col){
    
    var dataTable = $(div_name).DataTable({"pageLength": 8, "searching":false, "retrieve": true});
   dataTable.clear();
   categories = Object.keys(position_count)

    for (var i = 0; i<categories.length; i++){

        var new_row = []
        new_row.push(categories[i])
        if (typeof additional_col !== 'undefined'){
            new_row.push(additional_col[categories[i]])
        }
        new_row.push(position_count[categories[i]])
        ///////////////////////////
        if (typeof(market_vals[categories[i]]) != "undefined"){
            string_data = market_vals[categories[i]].formatMoney(2)
            new_row.push(string_data)
        }
        else{
            string_data = "$ 0.00"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(gross_exposures[categories[i]]) != "undefined"){
            string_data = gross_exposures[categories[i]].formatMoney(2)
            new_row.push(string_data)
        }
        else{
            string_data = "$ 0.00"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(gross_allocations[categories[i]]) != "undefined"){
            string_data = String((100*gross_allocations[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }
        dataTable.row.add(new_row)
    }
    return dataTable
}   
////////////////////////////
// Name of Cateegory, Num Positions, Market Val, Weight by Market val, Gross Exp, % Total Gross Exp
function create_fund_overview_table(div_name,position_count, market_vals, market_allocations, gross_exposures, gross_allocations, additional_col){
    
   var dataTable = $(div_name).DataTable({"pageLength": 8, "searching":false, "retrieve": true});
   dataTable.clear();
   categories = Object.keys(position_count)

    for (var i = 0; i<categories.length; i++){

        var new_row = []
        new_row.push(categories[i])
        if (typeof additional_col !== 'undefined'){
            new_row.push(additional_col[categories[i]])
        }
        new_row.push(position_count[categories[i]])
        ///////////////////////////
        if (typeof(market_vals[categories[i]]) != "undefined"){
            string_data = market_vals[categories[i]].formatMoney(2)
            new_row.push(string_data)
        }
        else{
            string_data = "$ 0.00"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(market_allocations[categories[i]]) != "undefined"){
            string_data = String((100*market_allocations[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(gross_exposures[categories[i]]) != "undefined"){
            string_data = gross_exposures[categories[i]].formatMoney(2)
            new_row.push(string_data)
        }
        else{
            string_data = "$ 0.00"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(gross_allocations[categories[i]]) != "undefined"){
            string_data = String((100*gross_allocations[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }
        dataTable.row.add(new_row)
    }
    return dataTable
}   


////////////////////////////
// Name of Cateegory, Gross Exp and % Nav, Long Exp and % Nav, Short Exp and % Nav, Net Exp and % Nav,
function create_overview_table2(div_name, gross_exposures, gross_allocations, long_exposures, long_allocations, short_exposures, short_allocations,net_exposures, net_allocations, additional_col){
    
   var dataTable = $(div_name).DataTable({"pageLength": 8, "searching":false, "retrieve": true});
   dataTable.clear();
   categories = Object.keys(gross_exposures)

   for (var i = 0; i<categories.length; i++){

        var new_row = []
        new_row.push(categories[i])

        if (typeof additional_col !== 'undefined'){
            new_row.push(additional_col[categories[i]])
        }

        ///////////////////////////
        if (typeof(gross_exposures[categories[i]]) != "undefined"){
            string_data = gross_exposures[categories[i]].formatMoney(2)
            new_row.push(string_data)
        }
        else{
            string_data = "$ 0.00"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(gross_allocations[categories[i]]) != "undefined"){
            string_data = String((100*gross_allocations[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(long_exposures[categories[i]]) != "undefined"){
            string_data = long_exposures[categories[i]].formatMoney(2)
            new_row.push(string_data)
        }
        else{
            string_data = "$ 0.00"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(long_allocations[categories[i]]) != "undefined"){
            string_data = String((100*long_allocations[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(short_exposures[categories[i]]) != "undefined"){
            string_data = short_exposures[categories[i]].formatMoney(2)
            new_row.push(string_data)
        }
        else{
            string_data = "$ 0.00"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(short_allocations[categories[i]]) != "undefined"){
            string_data = String((100*short_allocations[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(net_exposures[categories[i]]) != "undefined"){
            string_data = net_exposures[categories[i]].formatMoney(2)
            new_row.push(string_data)
        }
        else{
            string_data = "$ 0.00"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(net_allocations[categories[i]]) != "undefined"){
            string_data = String((100*net_allocations[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }
        dataTable.row.add(new_row)
    }
    return dataTable

}   
////////////////////////////////////////////////////
function create_specific_exposure_table(div_name,num_positions,exposure,exposure_allocation, additional_col){
    
    var dataTable = $(div_name).DataTable({"pageLength": 8, "searching":false, "retrieve": true,"sDom": 'rt'});
    dataTable.clear();
    
    categories = Object.keys(exposure)
    // Create Table Rows
    for(var i = 0; i<categories.length; i++){

        var new_row = []
        new_row.push(categories[i])

        if (typeof additional_col !== 'undefined'){
            new_row.push(additional_col[categories[i]])
        }
        new_row.push(num_positions[categories[i]])
        ///////////////////////////
        if (typeof(exposure[categories[i]]) != "undefined"){
            string_data = exposure[categories[i]].formatMoney(2)
            new_row.push(string_data)
        }
        else{
            string_data = "$ 0.00"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(exposure_allocation[categories[i]]) != "undefined"){
            string_data = String((100*exposure_allocation[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }

        dataTable.row.add(new_row)
    }
    return dataTable
}
////////////////////////////////////////////////////
function create_beta_table(div_name,beta_sp,beta_msci, revised_beta_msci, additional_col){
        
    var dataTable = $(div_name).DataTable({"pageLength": 8, "searching":false, "retrieve": true});
    dataTable.clear();
    
    categories = Object.keys(beta_sp)
    // Create Table Rows

    for (var i = 0; i<categories.length; i++){

        var new_row = []
        new_row.push(categories[i])

        if (typeof additional_col !== 'undefined'){
            new_row.push(additional_col[categories[i]])
        }
        ///////////////////////////
        if (typeof(beta_msci[categories[i]]) != "undefined"){
            string_data = String((100*beta_msci[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(revised_beta_msci[categories[i]]) != "undefined"){
            string_data = String((100*revised_beta_msci[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }
        ///////////////////////////
        if (typeof(beta_sp[categories[i]]) != "undefined"){
            string_data = String((100*beta_sp[categories[i]]).toFixed(2))+' %'
            new_row.push(string_data)
        }
        else{
            string_data = "0.00 %"
            new_row.push(string_data)
        }
        dataTable.row.add(new_row)

    }
    return dataTable
}
