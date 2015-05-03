$(function() {
    var $frames = $("div.frame");
    var $funcs = $("ul#frames li.func");

    $funcs.on("click", function() {
        var $func = $(this);
        var frameId = $(this).data("frame");
        var $frame = $("div.frame[data-frame=" + frameId + "]");

        $funcs.removeClass("current");
        $func.addClass("current");
        $frames.hide();
        $frame.show();
    });
    $("ul#frames li.func:first-child").trigger("click");
});
