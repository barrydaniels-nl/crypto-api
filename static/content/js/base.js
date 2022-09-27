$(document).ready(function() { 

    $('.news-card').on('click', function() {
        window.open($(this).data('news-url'), '_blank');
    })

    $("[data-background]").each(function () {
        $(this).css("background-image", "url(" + $(this).attr("data-background") + ")")
    })

})