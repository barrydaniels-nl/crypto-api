$('.news-card').on('click', function() {
    window.open($(this).data('news-url'), '_blank');
})