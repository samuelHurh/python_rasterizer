# python_rasterizer
A program that applies DDA and Scanline algorithms to create raster images from text input.

In order to do so, you'll need to run the makefile in your terminal once pulling the code.
Type:
make run file="./rasterizer-files/filename.txt"
and choose one of those files to insert for "filename"
This can be used to generate one of the images provided (delete the image and run to verify).

The images that can be generated from provided txt files:
<br>
![alt_text](https://github.com/samuelHurh/python_rasterizer/blob/main/rasterizer/gray.png?raw=true)
A gray gradient applied to triangles<br>
![alt_text](https://github.com/samuelHurh/python_rasterizer/blob/main/rasterizer/smallGap.png?raw=true)
A colorful gradient applied to triangles<br>
![alt_text](https://github.com/samuelHurh/python_rasterizer/blob/main/rasterizer/smoothcolor.png?raw=true)
A smoother colorful gradient applied to triangles <br>
![alt_text](https://github.com/samuelHurh/python_rasterizer/blob/main/rasterizer/checkers.png?raw=true)
A rasterized checkerboard <br>
![alt_text](https://github.com/samuelHurh/python_rasterizer/blob/main/rasterizer/sRGB.png?raw=true)
Triangles with SRGB colors <br>
![alt_text](https://github.com/samuelHurh/python_rasterizer/blob/main/rasterizer/gammabox.png?raw=true)
The checkerboard with SRGB colors <br>
![alt_text](https://github.com/samuelHurh/python_rasterizer/blob/main/rasterizer/depth.png?raw=true)
A rasterized image where z-depth is important for deciding what gets shown <br>
![alt_text](https://github.com/samuelHurh/python_rasterizer/blob/main/rasterizer/alpha.png?raw=true)
A rasterized image with transparent triangles <br>
