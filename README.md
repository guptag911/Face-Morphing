# Face-Morphing
## Introduction
Here we are trying to apply morphing on two images, in particular, we want to map the changes
from the source image to the destination image. On applying this we can see how pixel values
are converting from source image to destination image. To get better results triangulation is
used to do the region-wise mapping.

### API and Language used
1. Python 3.7
2. Open-CV
3. Numpy

### How to install and Run
1. Open terminal (CTRL+ALT+T)
2. Install Python by the command “sudo apt-get install python”
3. Run the command“python -m pip install requirements.txt”
4. Change the path in the code for your input images.
5. Run the command on the terminal - “python file_name.py”

### What to do after running
1. You will be prompt with image1
2. Use mouse to mark 3 control points and press ‘q’
3. You will be prompt with image2
4. Use mouse to mark 3 control points and press ‘q’
5. Now you can see 2 triangulated images
6. Press q
7. Now You can see intermediate triangles getting morphed
8. The final Image along with two triangulated image will be shown as output.
9. Images will be saved automatically in the working directory.

### Program in Action(Video Demonstration!)
Check the following video to see what the program does!
[Watch the video here](https://youtu.be/fsQUcMbcFIs)

### Input Images
Source Image

![Source Image](https://github.com/guptag911/Face-Morphing/blob/master/Bush.jpg)

Destination Image

![Destination Image](https://github.com/guptag911/Face-Morphing/blob/master/Clinton.jpg)

### Triangulated Images
Source Triangulated Image

![Triangulated Image Source](https://github.com/guptag911/Face-Morphing/blob/master/Frames/Triangulated_Image1.jpg)

Destination Triangulated Image

![Triangulated Image Destination](https://github.com/guptag911/Face-Morphing/blob/master/Frames/Triangulated_Image2.jpg)


### Result
Final Morphed Image

![Morphed Image](https://github.com/guptag911/Face-Morphing/blob/master/Final_Morphed.jpg)

