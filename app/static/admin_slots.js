function remove_slot(event) {
  event.preventDefault();
  $.ajax({
    type: "POST",
    url: "/ajax/admin/slots/remove_slot",
    data: JSON.stringify({
      "slot": $(event.target).attr("data-slot")
    }),
    contentType: 'application/json;charset=UTF-8',
    success: function(data) {
      slot_num = $(event.target).attr("data-slot");
      slot_text = $("#slots li[data-slot='" + slot_num + "']").text().slice(0, -3);
      // remove selected slot from list
      $("#slots li[data-slot='" + slot_num + "']").remove();
      // add option to select box
      $("#select_box_slots").append('<option value='+ slot_num +'>' + slot_text + '</option>');
    }
  });
};

$(document).ready(function() {
  // update settings
  $("form").submit(function(event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: "/ajax/admin/slots/update",
      data: JSON.stringify({
        "slot_length": parseInt($("#slot_length").val())
      }),
      contentType: 'application/json;charset=UTF-8'
    });
  });

  // remove slot
  $(".remove_slot").on("click", remove_slot);

  // add slot
  $("#button_add_slot").on("click", function(event) {
    // send to selected slot to server
    $.ajax({
      type: "POST",
      url: "/ajax/admin/slots/add_slot",
      data: JSON.stringify({
        "slot": $("#select_box_slots").val()
      }),
      contentType: 'application/json;charset=UTF-8',
      success: function(data) {
        selected_slot = $("#select_box_slots").val();
        slot_text = $("#select_box_slots option[value='" + selected_slot + "']").text();
        // remove option from select box
        $("#select_box_slots option[value='" + selected_slot + "']").remove();
        // add selected slot to list
        li = $("<li>", {
          "data-slot": selected_slot
        }).text(slot_text + " ");
        a = $("<a>", {
          href: "#",
          class: "remove_slot",
          "data-slot": selected_slot
        }).text("(X)");
        a.on("click", remove_slot);
        li.append(a);
        $("#slots").append(li);
      }
    });
  });
});
