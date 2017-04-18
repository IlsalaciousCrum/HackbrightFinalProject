function showCurrentDietReason(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".modal.in").modal("hide");
    $(".dietReason").load(location.href + " #dietReason");
}


$(document).ready(function() {
    "use strict";
    $('#changeDietReason').on('submit', (function(event) {
        event.preventDefault();
        var url = $('#changeDietReason').attr('action');
        $.ajax({
            type: "POST",
            url: url,
            data: $('#changeDietReason').serialize(),
            success: showCurrentDietReason
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


function refreshDietReason(results) {
    "use strict";
    console.dir(results); // for debugging
    $(".modal.in").modal("hide");
    $(".dietReason").load(location.href + " #dietReason");
}

$(document).ready(function() {
    "use strict";
    $('#clearDietReason').on('click', (function(event) {
    
        var url = "/profiles/cleardietreason.json";
        $.ajax({
            type: "POST",
            url: url,
            data: $('#changeDietReason').serialize(),
            success: refreshDietReason
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