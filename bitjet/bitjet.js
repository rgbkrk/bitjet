define(function(require) {
   var widget = require("widgets/js/widget");

   var BitView = widget.DOMWidgetView.extend({
       render: function() {
           
           // Create the viewing frame.
           this.$frame = $('<canvas/>')
               .css({
                   overflow: 'hidden',
                   width:  420,
                   height: 420,
                   border: '2px solid grey'
               }).appendTo(this.$el);


           this.model.on('change:data', this._redraw, this);
           this.model.on('change:bitwidth', this._redraw, this);
           this._redraw();
       },

       _redraw: function() {
          // Grab the canvas context
          var context = this.$frame[0].getContext("2d");

          var data = this.model.get("data");
          // data will come in as a list traitlet
          var bitwidth = this.model.get("bitwidth");



          context.fillRect(0,10,5,5); 
       },
   });

   return {
       BitView: BitView
   };
});
