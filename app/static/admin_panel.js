$(document).ready(function() {
  $('a.remove_user').on('click', function(event) {
    event.preventDefault();
    question = "Are you sure you want to remove user '" + $(event.target).attr('data-user') + "'?"
    if (confirm(question) == true) {
      $.ajax({
        type: 'POST',
        url: '/ajax/admin/remove_user',
        data: JSON.stringify({
          'user': $(event.target).attr('data-user')
        }),
        contentType: 'application/json;charset=UTF-8',
        success: function(data) {
          if (data.success == 'True') {
            // remove p with user
            $('#users > #' + data.user).remove();
          }
        }
      });
    }
  });
});
