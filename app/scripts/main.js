$("#download-button").click(function () {
  $(this).find("button").attr("disabled", true);
  $("#email-form").show();
});
