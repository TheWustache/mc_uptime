$(document).ready(function() {
  $("#recalculate_session").on('click', function(event) {
    if (confirm("Remember that recalculating the next session may result in times that some users have not agreed to. Proceed?") == true) {
      $.post("/ajax/admin/general/recalculate_session");
    }
  });
});
