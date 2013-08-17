$(document).ready(
function(){
    var $date_element = $('.datepicker')
    if($date_element && $date_element.length > 0){
        $date_element.datepicker({
            format: 'dd/mm/yyyy'
        });
    }

    var $time_element = $('.time')
    if($time_element && $time_element.length > 0){
        $time_element.timepicker();
    }
    
})
