function linkTo(url, id){
    window.location.href=url + id + '/';
}

$(document).ready(
function(){
elements = document.getElementsByClassName('wide')
for (var i=0;i< elements.length; i++){
    elements[i].parentNode.style.width = '100%';
}

$('#filterButton').click(function(){
    var acumulatedValeu = $("#acumulatedFilter").val();
    var textFilter = $("#filterText").val();
    var selectedOption = $("#filterKind").find(":selected").text();
    var url = ""
    if(textFilter && selectedOption){
        if(!acumulatedValeu || acumulatedValeu == ""){
            acumulatedValeu = "";
            url = document.URL
        }
        else{
            url = document.URL.split(acumulatedValue)[0]
            acumulatedValeu += "&";
        }
        console.log(selectedOption);
        console.log(textFilter);
        acumulatedValeu = selectedOption + "=" + textFilter;
        console.log("url", url);
        console.log("filtro", acumulatedValeu);
        window.location.href = url + acumulatedValeu + '/';
    }
})

})
