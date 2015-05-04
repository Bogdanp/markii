$(function() {
    var $frames = $("div.frame");
    var $funcs = $("ul#frames li.func");
    var $toggle = $("input#app-local-toggle");

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

    $toggle.on("change", function() {
        $funcs.show();
        if ($toggle.is(":checked")) {
            $("ul#frames li.func[data-app-local=False]").hide();
        }
    });
});
