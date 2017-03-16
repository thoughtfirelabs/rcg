////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Utility Functions


////////////////////////////
// Formatting Function for Turning Float into Dollar Formatted String
Number.prototype.formatMoney = function(c, d, t){
var n = this, 
    c = isNaN(c = Math.abs(c)) ? 2 : c, 
    d = d == undefined ? "." : d, 
    t = t == undefined ? "," : t, 
    s = n < 0 ? "-" : "", 
    i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
    j = (j = i.length) > 3 ? j % 3 : 0;
   return '$ ' + s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
 };
////////////////////////////
String.prototype.formatCountry = function(){

    var invalid_names = ['Eu European Union']
    var renames = ['Europe']

    var str = this
    str_low = str.toLowerCase()
    str_format=str_low.replace(/\b./g, function(m){ return m.toUpperCase(); })

    if (str_format == 'Eu European Union'){
        str_format = 'Europe'
    }
    return str_format
}
////////////////////////////
function get_index_of_array(search_index_name,array){

    var found_index=-1
    for (var i = 0; i<array.length; i++){
        if (array[i]==search_index_name){
            found_index = i
        }
    }
    return found_index
}
////////////////////////////
function indexOfMax(arr) {
    if (arr.length === 0) {
        return -1;
    }
    var max = arr[0];
    var maxIndex = 0;

    for (var i = 1; i < arr.length; i++) {
        if (arr[i] > max) {
            maxIndex = i;
            max = arr[i];
        }
    }
    return maxIndex;
}
function hexToRgb(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}
////////////////////////////
function consolidate_country_exposure(countries,amounts){

    // Consolidate Countries to Show Max 5 Countries, Bin Others 
    if (countries.length >=5){

        new_countries = new Array()
        new_amts = new Array()
        for (var i = 0; i<5; i++){
            current_max_index = indexOfMax(amounts)
            new_countries.push(countries[current_max_index])
            new_amts.push(amounts[current_max_index])

            // Remove Max Index
            amounts.splice(current_max_index, 1);
        }
        // Put Leftovers Into New Bin
        sum=0
        for(var j = 0; j<amounts.length; j++){
            sum=sum+amounts[j]
        }
        new_amts.push(sum)
        new_countries.push('Other')
    }
    else{
        new_countries = countries
        new_amts = amounts
    }
    return [new_countries,new_amts]
}
////////////////////////////
// Calculates Percentage for Each Label Based on Dollar amounts
function calculate_percentages(label_names,amounts){

    temp_sum=0
    for(var i=0; i<amounts.length; i++){
        temp_sum=temp_sum+amounts[i]
    }

    pct_arr = new Array()
    for (var i = 0; i<label_names.length; i++){
        pct_arr[label_names[i]]=(100*amounts[i]/temp_sum).toFixed(2)
    }
    return pct_arr
}

////////////////////////////
// Calculates Percentage for Long and Short Based on List of Amounts and Long/Short Designation
function calculate_long_short_pcts(long_shorts,amounts){

    temp_sum_long=0
    temp_sum_short=0
    temp_sum = 0
    for(var i=0; i<amounts.length; i++){
        temp_sum=temp_sum+amounts[i]
        if (long_shorts[i]=='Long'){
            temp_sum_long=temp_sum_long+amounts[i]
        }
        else{
            temp_sum_short=temp_sum_short+amounts[i]
        }
    }

    pct_arr = new Array()
    pct_arr['Long']=(100*temp_sum_long/temp_sum).toFixed(2)
    pct_arr['Short']=(100*temp_sum_short/temp_sum).toFixed(2)

    return pct_arr
}
