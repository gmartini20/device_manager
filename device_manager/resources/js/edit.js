$(document).ready(
function(){
    var $date_element = $('.date')
    if($date_element && $date_element.length > 0){
        $date_element.datepicker({
            dateFormat: 'dd/mm/yy'
        });
    }

    var $time_element = $('.time')
    if($time_element && $time_element.length > 0){
        $time_element.timepicker();
    }
    
})
