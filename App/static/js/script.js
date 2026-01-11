$(document).ready(function () {
    if ($("#task-success").length) {
      $("form")[0].reset(); // reset form fields
    }
    $("#task-success").delay(3000).fadeOut();

  });