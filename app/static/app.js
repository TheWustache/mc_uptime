function remove_user( event ) {
  alert("NYI. User: " + $(event.target).attr('data-user'));
}

$( document ).ready(function() {
  $('a.remove_user').on('click', remove_user);

  $('button#add_user').on('click', function( event ) {
    $.ajax({
      type:'POST',
      url:'/ajax/app/add_user',
      data: JSON.stringify({'user':$('#new_user').val(), 'app_id':$("#app_id").val()}),
      contentType: 'application/json;charset=UTF-8',
      success: function(data) {
        if (data.success == 'True') {
          var p = $('<p>').text(data.user + ' ');
          var a = $('<a>', {'href':'#', 'class':'remove_user', 'data-user':data.user}).text('(remove)');
          a.on('click', remove_user);
          p.append(a);
          $('#users').append(p);
        }
      }
    });
  });
});
