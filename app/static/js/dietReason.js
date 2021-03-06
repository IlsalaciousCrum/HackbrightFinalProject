function showCurrentDietReason(results) {
    "use strict";
    $(".modal.in").modal("hide");
    $(".dreason").load(location.href + " #dreason");
}

$(document).ready(function() {
    "use strict";
    $('#changeDietReason').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#changeDietReason').attr('action');
        $.ajax({
            type: "POST",
            url:url,
            data: $('#changeDietReason').serialize(),
            success: showCurrentDietReason
            });
    }));

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{  form.csrf_token.value()  }}");
            }
        }
    });
});

$(document).ready(function() {
    "use strict";
    $('#clearDietReason').on('click', (function(event) {
        var url = Flask.url_for("profiles.cleardietreason");
        $.ajax({
            type: "POST",
            url:url,
            data: $('#changeDietReason').serialize(),
            success: showCurrentDietReason
            });
    }));

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{  form.csrf_token.value()  }}");
            }
        }
    });
});

