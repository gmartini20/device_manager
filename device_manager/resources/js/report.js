function linkTo(url, id){
    window.location.href=url + id + '/';
}

$(document).ready(
function(){
$("#list_table").tablesorter(); 
var acumulatedValeu = $("#acumulatedFilter").val();
var filters = acumulatedValeu.split("&");
console.log(filters);
var html = "<li class='filter'><a class='filters' onClick='deleteFilter(this)' href='#'>{0}</a></li>";
for (var i = 0; i < filters.length; i++){
    $("#choosen_filters").append(html.replace("{0}", filters[i]));
}



elements = document.getElementsByClassName('wide')
for (var i=0;i< elements.length; i++){
    elements[i].parentNode.style.width = '100%';
}

$('#filterButton').click(function(){
    var acumulatedValeu = $("#acumulatedFilter").val();
    var textFilter = $("#filterText").val();
    var selectedOption = $("#filterKind").find(":selected").val();
    var url = getUrl();
    if(textFilter && selectedOption){
        if(!acumulatedValeu || acumulatedValeu == ""){
            acumulatedValeu = "";
        }
        else{
            acumulatedValeu += "&";
        }
        acumulatedValeu += selectedOption + "=" + textFilter;
        window.location.href = url + acumulatedValeu + '/';
    }
})

$('#reportButton').click(function(){
    var acumulatedValeu = $("#acumulatedFilter").val();
    var url = document.URL;
    var report_url = $("#reportUrl").val();
    url = url.split("/reports/")[0] + "/reports/";
    url = url + report_url + "/";
    url = url + acumulatedValeu;
    if (acumulatedValeu && acumulatedValeu != "")
        url = url + '/';
    window.location.href = url;
})
})

function deleteFilter(e){
    var text = e.innerHTML;
    var acumulated_filter = $('#acumulatedFilter').val();
    var filters = acumulated_filter.split(text);
    var filter = filters[0] + filters[1];
    separated_filter = filter.split('&');
    var new_filter = '';
    var is_first = true;
    for (var i = 0; i < separated_filter.length; i++){
        if (i == 0 && (separated_filter[i] && separated_filter[i] != "")){
            new_filter = separated_filter[i];
            is_first = false;
        }
        else{
            if (separated_filter[i]){
                if(is_first){
                    console.log('novo_filtro', separated_filter[i]);
                    new_filter += separated_filter[i];
                    is_first = false;
                }
                else{
                    new_filter += '&' + separated_filter[i];
                }
            }
        }
    }
    var url = getUrl() + new_filter;
    e.parentNode.removeChild(e);
    $("#acumulatedFilter").val(new_filter);
    if (url.indexOf('/', url.length -1) === -1){
        url += '/';
    }
    else if(url.indexOf('//', url.length -2) !== -1){
        url = url.substring(0, url.length - 1);
    }
    window.location.href = url;
};

function getUrl(){
    var splited_url = document.URL.split("/reports/");
    return splited_url[0] + "/reports/" + splited_url[1].split("/")[0] + '/'
}

function replaceAll(string, token, newtoken) {
    while (string.indexOf(token) != -1) {
        string = string.replace(token, newtoken);
    }
    return string;
}
