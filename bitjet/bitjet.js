define(function(require) {
   var widget = require("widgets/js/widget");

   var BitView = widget.DOMWidgetView.extend({
       render: function() {
           
           // Create the viewing frame.
           this.$frame = $('<canvas/>')
               .css({
                   overflow: 'hidden',
                   width:  800,
                   height: 800,
                   border: '1px solid lightgray',
                   "-webkit-box-shadow": "0 0 12px 1px rgba(87,87,87,0.2)",
                   "box-shadow": "0 0 12px 1px rgba(87,87,87,0.2)"
               }).appendTo(this.$el);


           this.model.on('change:data', this._redraw, this);
           this.model.on('change:bitwidth', this._redraw, this);
           this.model.on('change:blockwidth', this._redraw, this);
           this.model.on('change:blockheight', this._redraw, this);
           this._redraw();
       },

       _redraw: function() {
          // Grab the canvas context
          var canvas = this.$frame[0];
          var context = canvas.getContext("2d");

          context.clearRect(0, 0, canvas.width, canvas.height );

          var data = this.model.get("data");
          // data will come in as a list traitlet
          var bitwidth = this.model.get("bitwidth");

          var width = this.model.get("blockwidth");
          var height = this.model.get("blockheight");

          data.forEach(function(el, idx) {
            // Within each byte, fill for each bit
            for (i=0; i<8; i++){
              bit = el >> i
              var x = ((idx*8+i) % bitwidth)*width;
              var y = (Math.floor((idx*8+i)/bitwidth))*height;
              if(bit) { //on
                context.fillRect(x,y,width,height);
              }

            }
              
          });

       },
   });

   return {
       BitView: BitView
   };
});
