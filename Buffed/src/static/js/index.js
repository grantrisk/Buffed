$(document).ready(function() {
    $("#signin-form").bind('submit', function(e) {
        e.preventDefault();
        let ajax = $.ajax({
            type: "POST",
            data: $("#signin-form").serialize(),
            url: "/"
        }).done(function(data) {
            let json = JSON.parse(JSON.stringify(data));
            let success_val = json.success;
            console.log(success_val);
            if (success_val === "true") {
                window.location.replace("/dashboard");
            } else if (success_val === "false") {
                let alert = document.createElement("div")
                alert.className = "alert alert-danger"
                alert.ariaRoleDescription = "alert"
                alert.innerText = "The username or password you entered is incorrect."
                document.getElementById("login-content").appendChild(alert)
            } else if (success_val === "error") {
                window.location.reload();
            }
        });
        ajax.fail(function(data) {
            window.location.reload();
        });
    });
});