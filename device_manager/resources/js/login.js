$(document).ready(
function(){
    $("button[type=submit]").click(function(event){
        event.preventDefault();
        event.stopPropagation();
        var pass = $("input[name='password']").val();
        console.log("pass ", pass);
        var url = "http://localhost:8080" + $($('form')[0]).attr('action');
        var crypted_pass = criptografar(pass);
        var username = $("input[name='username']").val();
        var data = {"username": username, "password": crypted_pass};
        console.log("pass crypted ", crypted_pass);
        $.ajax({
          type: "POST",
          url: url,
          data: data,
          success: function(data){ window.location.href = url.replace('login', 'home')},
          error: function(jqXHR, textStatus, errorThrown){ $("#error-message").css("display", 'block') }
        });
    });
})
