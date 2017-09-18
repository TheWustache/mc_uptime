function remove_user(event) {
  $.ajax({
    type: 'POST',
    url: '/ajax/app/remove_user',
    data: JSON.stringify({
      'user': $(event.target).attr('data-user'),
      'app_id': $("#app_id").val()
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

$(document).ready(function() {
  $('a.remove_user').on('click', remove_user);

  $('#add_user').on('click', function(event) {
    event.preventDefault();
    $.ajax({
      type: 'POST',
      url: '/ajax/app/add_user',
      data: JSON.stringify({
        'user': $('#new_user').val(),
        'app_id': $("#app_id").val()
      }),
      contentType: 'application/json;charset=UTF-8',
      success: function(data) {
        if (data.success == 'True') {
          // create new user entry
          var li = $('<li>', {
            'id': data.user
          }).text(data.user + ' ');
          var a = $('<a>', {
            'href': '#',
            'class': 'remove_user',
            'data-user': data.user
          }).text('(remove)');
          // bind remove_user function to link
          a.on('click', remove_user);
          li.append(a);
          $('#users').append(li);
        }
      }
    });
  });

  $('#update_settings').on('click', function( event ) {
    event.preventDefault();
    $.ajax({
      type: 'POST',
      url: '/ajax/app/update_settings',
      data: JSON.stringify({
        'name': $('#settings_name').val(),
        'filepath': $('#settings_filepath').val(),
        'slot_length': $('#settings_slot_length').val(),
        'app_id': $("#app_id").val()
      }),
      contentType: 'application/json;charset=UTF-8',
      success: function(data) {
        $('#title').text(data.name)
      }
    });
  });
});
