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
    var splited_url = splited_urls[0] + splited_urls[1];
    splited_url = splited_url.split('&');
    var url = "";
    for (var i = 0; i < splited_url.length; i++){
        if (i == 0 && (splited_url[i])){
            url = splited_url[i];
        }
        else{
            console.log(splited_url[i])
            if (splited_url[i] && splited_url.indexOf('=') != -1){
                console.log('novo_filtro', splited_url[i]);
                url += '&' + splited_url[i];
            }
        }
    }
    url += '/'
    console.log('urlk', url);
    window.location.href = url;
};

function replaceAll(string, token, newtoken) {
    while (string.indexOf(token) != -1) {
        string = string.replace(token, newtoken);
    }
    return string;
}
