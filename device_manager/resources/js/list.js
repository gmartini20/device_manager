function linkTo(url, id){
    window.location.href=url + id + '/';
}

$(document).ready(
function(){
elements = document.getElementsByClassName('wide')
for (var i=0;i< elements.length; i++){
    elements[i].parentNode.style.width = '100%';
}
})
