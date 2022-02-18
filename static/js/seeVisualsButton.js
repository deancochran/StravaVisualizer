$("#start-visuals").click(function(){
    $(this).remove();
    var $prev = $("#hero");
    var $target = $("#elevations-screen");
        
    $('html, body').animate({
        scrollTop: $target.offset().top
    }, 'slow');

    $('.active').removeClass('active');
    $target.addClass('active');
    
    setTimeout(() => {$prev.remove()}, 1000);
});