$(function () {
    function LayerDisplayViewModel(parameters) {
        var self = this;
        layerString = ko.observable("-");

        self.onStartup = function () {
            var element = $("#state").find(".accordion-inner .progress");
            if (element.length) {
                var text = gettext("Layer");
                var tooltip = gettext("Might be inaccurate!");
                element.before(text + ": <strong title='" + tooltip + "' data-bind='text: layerString'></strong><br>");
            }
            self.retrieveData();
        };

        self.retrieveData = function () {
            
            var url = "/api" + PLUGIN_BASEURL + "layerdisplay";
            $.ajax({
                url: url,
                type: "GET",
                dataType: "json",
                contentType: "application/json; charset=UTF-8",
                success: function (data) {
                    layerString(data.layerString);
                }
            })
        }

        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (plugin === "LayerDisplay") {
                layerString(data.layerString);
            }
        }
    }

    // view model class, parameters for constructor, container to bind to
    ADDITIONAL_VIEWMODELS.push([LayerDisplayViewModel, [], []]);
});
