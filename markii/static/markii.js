$(function() {
    var $frames = $("div.frame");
    var $funcs = $("ul#frames li.func");
    var $toggle = $("input#app-local-toggle");
    var $editor = $("select#editor");
    var storageKey = "markii-config";
    var config = JSON.parse(localStorage.getItem(storageKey) || "{}");

    var updateConfig = function(k, v) {
        config[k] = v;
        localStorage.setItem(storageKey, JSON.stringify(config));
    };

    $funcs.on("click", function() {
        var $func = $(this);
        var frameId = $(this).data("frame");
        var $frame = $("div.frame[data-frame=" + frameId + "]");

        $funcs.removeClass("current");
        $func.addClass("current");
        $frames.hide();
        $frame.show();
    });

    $funcs.on("dblclick", function() {
        var $func = $(this);
        var scheme = $editor.val();
        var filename = $func.data("filename");
        var line = $func.data("line");

        window.location.href = scheme + "://open/?url=file://" + filename + "&line=" + line;
    });

    $toggle.on("change", function() {
        var toggled = $toggle.is(":checked");

        $funcs.show();
        if (toggled) {
            $("ul#frames li.func[data-app-local=False]").hide();
        }

        updateConfig("tracesToggled", toggled);
    });
    if (config.tracesToggled) {
        $toggle.prop("checked", true);
        $toggle.trigger("change");
    }

    $editor.on("change", function() {
        updateConfig("editor", $(this).val());
    });
    if (config.editor) {
        $editor.val(config.editor);
    }

    $("ul#frames li.func:first-child").trigger("click");
});
