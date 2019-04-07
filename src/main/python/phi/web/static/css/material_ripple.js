/*
 *Material Ripple jQuery plugin
 *MIT License
 *Version 0.1
 */
;
(function ($, window, document, undefined) {
    var pluginName = 'material_ripple',
            defaults = {
                rippleClass: "ripple-animate",
                background: "#fff",
                animateDuration: 2000
            };
    //constructor
    function Plugin(element, options) {
        this.element = element;
        this.options = $.extend({}, defaults, options);
        this._defaults = defaults;
        this._name = pluginName;
        this.init();
    }

    Plugin.prototype.init = function () {
        var options = this.options;
        $(this.element).on('click', function (e) {
            e.preventDefault();
            var self = $(this);
            var height = self.height();
            var width = self.width();

            var thisOffset = $(this).offset();
            var offsetX = e.pageX - thisOffset.left;
            var offsetY = e.pageY - thisOffset.top;

            var container = $('<div/>');
            container.addClass(options['rippleClass']);
            var cssProperties = {
                //animating circle
                width: height,
                height: height,
                top: offsetY - (height / 2),
                left: offsetX - (height / 2),
                background: $(this).attr("data-color") !== undefined ? $(this).attr("data-color") : options['background']
            }
            container.css(cssProperties);
            container.appendTo(self);
            setTimeout(function () {
                container.remove();
            }, options['animateDuration']);
        });
    };

    $.fn[pluginName] = function (options) {
        return this.each(function () {
            if (!$.data(this, 'plugin_' + pluginName)) {
                $.data(this, 'plugin_' + pluginName,
                        new Plugin(this, options));
            }
        });
    }
})(jQuery, window, document);
