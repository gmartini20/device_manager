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

    if ($("input[name='password']")){
        $("input[type=submit]").click(function(event){
            event.preventDefault();
            event.stopPropagation();
            var pass = $("input[name='password']").val();
            console.log("pass ", pass);
            var confirmed_pass = $("input[name='confirmed_password']").val();
            if (pass != confirmed_pass){
                alert("senhas informadas são diferentes")
            }
            else{
                var url = "http://localhost:8080" + $($('form')[0]).attr('action');
                var crypted_pass = criptografar(pass);
                var username = $("input[name='username']").val();
                var person = $("select[name='person']").val();
                var data = {"username": username, "password": crypted_pass, "confirmed_password": crypted_pass, "person": person};
                console.log("pass crypted ", crypted_pass);
                $.ajax({
                  type: "POST",
                  url: url,
                  data: data,
                  success: function(data){ window.location.href = url.replace('edit', 'list')}
                });
            }
        });
    }
    
})
