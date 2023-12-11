# Rendering Pipeline
<!-- 1. Load sheet of 16x16 tiles into the `tiles` array
2. Save the tiles at the resolution they will actually be displayed at (4x scale, in our case)
3. Load text-based tilemap, and save the  -->
1. load in tileset of 16x16 tiles
2. save the tiles in the scale factor (4)
3. rendering:
   a. take an offset into the tiles array
      based on the tile's position in the
      tileset
   b. iterate over the tiles in the display
      (stepping by the rendered size of the
      tiles after the scale factor)
   c. profit