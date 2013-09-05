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

    if ($("input[name='password']") && $("input[name='password']").length > 0){
        $("input[type=submit]").click(function(event){
            event.preventDefault();
            event.stopPropagation();
            var pass = $("input[name='password']").val();
            var confirmed_pass = $("input[name='confirmed_password']").val();
            if (pass != confirmed_pass){
                setErrorMessage("senhas informadas são diferentes")
            }
            else{
                var href = window.location.href;
                href = href.split("/user")[0]
                var url = href + $($('form')[0]).attr('action');
                var crypted_pass = criptografar(pass);
                var username = $("input[name='username']").val();
                var id = $("input[name='id']").val();
                var person = $("select[name='person']").val();
                var profile = $("select[name='profile']").val();
                if (!username){
                    setErrorMessage("Username é um campo obrigatório")
                }
                else if(!person){
                    setErrorMessage("Pessoa é um campo obrigatório")
                }
                else if (!pass){
                    setErrorMessage("Senha é um campo obrigatório")
                }
                else if (!confirmed_pass){
                    setErrorMessage("Confirmação de Senha é um campo obrigatório")
                }
                else if(!profile){
                    setErrorMessage("Perfil é um campo obrigatório")
                }
                else{
                    var data = {"id": id, "username": username, "password": crypted_pass, "confirmed_password": crypted_pass, "person": person, "profile": profile};
                    console.log("pass crypted ", crypted_pass);
                    $.ajax({
                      type: "POST",
                      url: url,
                      data: data,
                      success: function(data){ window.location.href = url.replace('edit', 'list')},
                      error: function(jqXHR, textStatus, errorThrown) {
                        if(jqXHR.responseText){
                            setErrorMessage(jqXHR.responseText);
                        }
                        else{
                            setErrorMessage("Ocorreu um erro processando a requisição, por favor tente novamente.");
                        }
                      }
                    });
                }
            }
        });
    }

    function setErrorMessage(message){
        $("#error-message").html("<span>"+message+"</span>")
        $("#error-message").css("display", 'block')
    }
    
})
