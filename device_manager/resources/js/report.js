function linkTo(url, id){
    window.location.href=url + id + '/';
}

$(document).ready(
function(){
var acumulatedValeu = $("#acumulatedFilter").val();
var filters = acumulatedValeu.split("&");
console.log(filters);
var html = "<li class='filter'><a class='filters' onClick='deleteFilter(this)' href='#'>{0}</a></li>";
for (var i = 0; i < filters.length; i++){
    console.log("Filtro", filters[i]);
    console.log($('#choosen_filters'))
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
    var url = ""
    if(textFilter && selectedOption){
        if(!acumulatedValeu || acumulatedValeu == ""){
            acumulatedValeu = "";
            url = document.URL
        }
        else{
            url = document.URL.split(replaceAll(acumulatedValeu, ' ', '%20'))[0]
            acumulatedValeu += "&";
        }
        acumulatedValeu += selectedOption + "=" + textFilter;
        window.location.href = url + acumulatedValeu + '/';
    }
})
})

function deleteFilter(e){
    var text = e.innerHTML;
    var acumulated_filter = $('#acumulatedFilter').val();
    var filters = acumulated_filter.split(text);
    var filter = filters[0] + filters[1];
    separated_filter = filter.split('&');
    var new_filter = '';
    for (var i = 0; i < separated_filter.length; i++){
        if (i == 0 && (separated_filter[i])){
            new_filter = separated_filter[i];
        }
        else{
            if (separated_filter[i]){
                console.log('novo_filtro', separated_filter[i]);
                new_filter += '&' + separated_filter[i];
            }
        }
    }
    e.parentNode.removeChild(e);
    $("#acumulatedFilter").val(new_filter);
    var splited_urls = document.URL.split(text);
    if(splited_urls[1])
        var splited_url = splited_urls[0] + splited_urls[1];
    else
        var splited_url = splited_urls[0];
    splited_url = splited_url.split('&');
    var url = "";
    var is_first = true;
    for (var i = 0; i < splited_url.length; i++){
        if (i == 0 && (splited_url[i] && splited_url[i] != "")){
            url = splited_url[i];
            if(splited_url[i].indexOf('=') != -1)
                is_first = false;
        }
        else{
            if (splited_url[i] && splited_url[i].indexOf('=') != -1){
                if (is_first){
                    url += splited_url[i];
                    is_first = false;
                }
                else{
                    url += '&' + splited_url[i];
                }
            }
        }
    }
    if (url.indexOf('/', url.length -1) === -1){
        url += '/'
    }
    else if(url.indexOf('//', url.length -2) !== -1){
        url = url.substring(0, url.length - 1);
    }
    window.location.href = url;
};

function replaceAll(string, token, newtoken) {
    while (string.indexOf(token) != -1) {
        string = string.replace(token, newtoken);
    }
    return string;
}
