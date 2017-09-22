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

  $('a.remove_app').on('click', function(event) {
    event.preventDefault();
    question1 = "Are you sure you want to remove app '" + $(event.target).attr('data-app-name') + "' (ID: " + $(event.target).attr('data-app-id') +")?"
    question2 = "Are you really sure?"
    if (confirm(question1) == true) {
      if(confirm(question2) == true) {
        $.ajax({
          type: 'POST',
          url: '/ajax/admin/remove_app',
          data: JSON.stringify({
            'app_id': $(event.target).attr('data-app-id')
          }),
          contentType: 'application/json;charset=UTF-8',
          success: function(data) {
            if (data.success == 'True') {
              // remove p with user
              $('#app_' + data.app_id).remove();
            }
          }
        });
      }
    }
  });
});
