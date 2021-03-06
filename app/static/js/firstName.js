function showCurrentFirstName(results) {
    "use strict";
    $(".modal.in").modal("hide");
    $(".first").load(location.href + " #first");
}

$(document).ready(function() {
    "use strict";
    $('#changeFirstName').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#changeFirstName').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#changeFirstName').serialize(),
            success: showCurrentFirstName
        });
    }));

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}");
            }
        }
    });
});