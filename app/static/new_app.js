var userSet = new Set();
var querySet = new Set();

function querylist_add_element(user) {
  var li = $("<li>", {
    "id": user + "_query"
  }).text(user + " ");
  var a = $("<a>", {
    "href": "#",
    "class": "add_user",
    "data-user": user
  }).text("(add)");
  // bind event handler
  a.on('click', add_user_to_list);
  li.append(a);
  $("#query_result").append(li);
}

function add_user_to_list(event) {
  event.preventDefault();
  // only add entry if it hasn't been yet
  var user = $(event.target).attr('data-user');
  if (!userSet.has(user)) {
    // add entry to list
    var li = $("<li>", {
      "id": user + "_add"
    }).text(user + " ");
    var a = $("<a>", {
      "href": "#",
      "class": "remove_user",
      "data-user": user
    }).text("(remove)");
    a.on("click", remove_user_from_list);
    li.append(a);
    $("#added_users").append(li);
    // remove entry from query results
    $("#" + user + "_query").remove();
    // add user to set for easy retrieval
    userSet.add(user);
  }
}

function remove_user_from_list(event) {
  event.preventDefault();
  user = $(event.target).attr('data-user');
  $("#" + user + "_add").remove();
  userSet.delete(user);
  // add user to query list if in current query
  if (querySet.has(user)) {
    querylist_add_element(user);
  }
}

$(document).ready(function() {
  $("#user_query").on('input', function(event) {
    $.getJSON('/ajax/user_query', {
      searchterm: $(event.target).val()
    }, function(data) {
      // remove all entries
      $("#query_result").empty();
      querySet.clear();
      // add results as entries
      $(data.users).each(function(index, value) {
        // add user to query set
        querySet.add(value);
        // only add entry if it wasn't added to set yet
        if (!userSet.has(value)) {
          querylist_add_element(value);
        }
      });
    });
  });

  $("#submit").on("click", function(event) {
    event.preventDefault();
    $.ajax({
      type: 'POST',
      url: '/ajax/admin/new_app/submit',
      data: JSON.stringify({
        name: $("#name").val(),
        filepath: $("#path").val(),
        users: Array.from(userSet)
      }),
      contentType: 'application/json;charset=UTF-8',
      success: function(data) {
        window.location.href = "/admin";
      }
    });
  });
});
