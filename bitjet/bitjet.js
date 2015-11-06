define(function(require) {
   var widget = require("widgets/js/widget");

   var BinaryModel = widget.WidgetModel.extend({});

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

           this.model.on('change:data', this._redraw, this);
           this.model.on('change:datawidth', this._redraw, this);
           this.model.on('change:blockwidth', this._redraw, this);
           this.model.on('change:blockheight', this._redraw, this);

           // Used for 1 bit per block (binary view) or 8 bit per block (hex view)
           this.model.on('change:bits_per_block', this._redraw, this);

           this._redraw();
       },

       _redraw: function() {
          var data = this.model.get('data');
          var datawidth = this.model.get("datawidth");
          var blockwidth = this.model.get("blockwidth");
          var blockheight = this.model.get("blockheight");
          var bitsPerBlock = this.model.get("bits_per_block");
          var datacol = 0;
          if (data !== null) {
            datacol = Math.ceil(data.byteLength/datawidth);
          }


          var width = datawidth*bitsPerBlock*blockwidth;
          var height = datacol*bitsPerBlock*blockheight*8;

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
          
          if (data === null) {
            // no data
            return;
          }
          if (bitsPerBlock === 1) {
            paintBits(context, data, datawidth, blockwidth, blockheight);
          } else if (bitsPerBlock === 8) {
            paintBytes(context, data, datawidth, blockwidth, blockheight);
          }

       }

   });

   var BitView = BinaryView.extend({});
   var ByteView = BinaryView.extend({});

   function paintBits(canvasCtx, data, datawidth,
                      blockwidth, blockheight) {

    // Paint the canvas with our bit view
    for(var idx=0; idx < data.byteLength; idx++) {
      // The decoded data is a DataView in JavaScript land, we'll strip uint8s off
      var el = data.getUint8(idx);
      var charsize = 8;

      for (i=0; i<charsize; i++){
        //Mask off that first bit
        var bit = (el >> 7-i) & 0x1; // shift down from the leftmost bit

        // Where does this bit fit in it?
        var x = ((idx*charsize+i) % datawidth)*blockwidth;
        var y = (Math.floor((idx*charsize+i)/datawidth))*blockheight;

        if(bit) { // on
          canvasCtx.fillStyle = "rgb(255,255,255)";
          canvasCtx.fillRect(x,y,blockwidth,blockheight);
        } else { // off
          canvasCtx.fillStyle = "rgb(0,0,0)";
          canvasCtx.fillRect(x,y,blockwidth,blockheight);
        }

      }

    }

   }

   function paintBytes(canvasCtx, data, datawidth,
                       blockwidth, blockheight) {

         // Paint the canvas with our byte view
         for(var idx=0; idx < data.byteLength; idx++) {
           // The decoded data is a DataView in JavaScript land, we'll strip uint8s off
           var el = data.getUint8(idx);

           // Where does this byte get painted?
           var x = (idx % datawidth)*blockwidth;
           var y = (Math.floor(idx/datawidth))*blockheight;

           canvasCtx.fillStyle = "rgb(" +  [el,el,el].join() + ")";
           canvasCtx.fillRect(x,y,blockwidth,blockheight);

         }
   }

   return {
       BitView: BitView,
       ByteView: ByteView,
       BinaryView: BinaryView,
       BinaryModel: BinaryModel
   };
});
