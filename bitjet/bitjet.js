define(function(require) {
   var widget = require("widgets/js/widget");

   var BinaryModel = widget.WidgetModel.extend({
     initialize: function() {
       this.on('change:data', this._decode, this);
     },

     _decode: function() {
       var msg = this.get("data");
       this.set('_data', atob(msg['b64data']));
     }
   });

   var BinaryView = widget.DOMWidgetView.extend({
       render: function() {

           // Create the viewing frame.
           this.$frame = $('<canvas/>')
               .css({
                   overflow: 'hidden',
                   border: '1px solid lightgray',
                   "-webkit-box-shadow": "0 0 12px 1px rgba(87,87,87,0.2)",
                   "box-shadow": "0 0 12px 1px rgba(87,87,87,0.2)",
                   background: "rgba(87,87,87,0.2)"
               }).appendTo(this.$el);

           this.model.on('change:_data', this._redraw, this);
           this.model.on('change:datawidth', this._redraw, this);
           this.model.on('change:blockwidth', this._redraw, this);
           this.model.on('change:blockheight', this._redraw, this);

           this.model.on('change:width', this._redraw, this);
           this.model.on('change:height', this._redraw, this);

           this._redraw();
       },

       _redraw: function() {
          var data = this.model.get('_data');

          var width = this.model.get('width');
          var height = this.model.get('height');

          // Set width/height of the Canvas on the DOM
          this.$frame.width(width);
          this.$frame.height(height);

          // Set width/height of the canvas drawing area
          this.$frame[0].width = width;
          this.$frame[0].height = height;

          // Grab the canvas context
          var canvas = this.$frame[0];
          var context = canvas.getContext("2d");

          // Color the background gray
          context.fillStyle = "rgb(87,87,87,0.2)";
          context.clearRect(0, 0, canvas.width, canvas.height );

          var datawidth = this.model.get("datawidth");
          var blockwidth = this.model.get("blockwidth");
          var blockheight = this.model.get("blockheight");

          this._paintData(context, data, datawidth,
                          blockwidth, blockheight)

       }

   });

   var BitView = BinaryView.extend({

     _paintData: function(canvasCtx, data, datawidth,
                          blockwidth, blockheight) {

          // Paint the canvas with our bit view
          for(var idx=0; idx < data.length; idx++) {
            // The decoded data is a string in JavaScript land, we'll strip uint8s off
            var el = data.charCodeAt(idx);
            var charsize = 8;

            for (i=0; i<charsize; i++){
              //Mask off that first bit
              var bit = (el >> 7-i) & 0x1; // shift down from the leftmost bit

              // Where does this bit fit in it?
              var x = ((idx*charsize+i) % datawidth)*blockwidth;
              var y = (Math.floor((idx*charsize+i)/datawidth))*blockheight;

              if(bit) { //on
                canvasCtx.fillStyle = "rgb(255,255,255)";
                canvasCtx.fillRect(x,y,blockwidth,blockheight);
              } else {
                canvasCtx.fillStyle = "rgb(0,0,0)";
                canvasCtx.fillRect(x,y,blockwidth,blockheight);
              }

            }

          }

       }
   });

   var ByteView = BinaryView.extend({

       _paintData: function(canvasCtx, data, datawidth,
                            blockwidth, blockheight) {

         // Paint the canvas with our byte view
         for(var idx=0; idx < data.length; idx++) {
           // The decoded data is a string in JavaScript land, we'll strip uint8s off
           var el = data.charCodeAt(idx);

           // Where does this byte get painted?
           var x = (idx % datawidth)*blockwidth;
           var y = (Math.floor(idx/datawidth))*blockheight;

           canvasCtx.fillStyle = "rgb(" +  [el,el,el].join() + ")"
           canvasCtx.fillRect(x,y,blockwidth,blockheight);

         }
       }
   });

   return {
       BitView: BitView,
       ByteView: ByteView,
       BinaryView: BinaryView,
       BinaryModel: BinaryModel
   };
});
