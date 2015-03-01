$(function() {
    var downloadLink = $("#download-link");

    downloadLink.click(function () {
        $("#email-form").show();
    });

    $("#email-form").on('click', function(e) {
        var target = e.target
        if (target === this || target.classList.contains("close") ) {
            $(this).css("display", "none");
        };
    })

    $("#submit-email").click(function () {
        $("#submit-email").attr("disabled", "disabled");
        $.ajax("https://www.crypto101.io/subscribe", {
            "type": "POST",
            "data": {
                "address": $("#email").val(),
                "force": false
            },
            "dataType": "json"
        }).done(function(data) {
            console.log("data");
            if (data.success === true) {
                $("#email-message").text("Thanks, you're signed up!");
                $("#submit-email").attr("disabled", "disabled");
            }
            else {
                $("#submit-email").attr("disabled", false);
                if (data.reason === "duplicate") {
                    $("#email-message").text("Looks like you're already signed up :-)");
                }
                else if (data.reason === "invalid") {
                    var msg = "That address doesn't look quite right.";
                    if (data.suggestion !== null) {
                        msg += " Did you mean " + data.suggestion + "?"
                    }
                    $("#email-message").text(msg);
                }
                else {
                    $("#email-message").text("Something appears to be broken :-(");
                }
            }
        });
    });
});
