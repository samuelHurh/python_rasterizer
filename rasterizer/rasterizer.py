from PIL import Image
import numpy as np

import sys

#viewport transformation algorithm:
# divide all points by w first
# take the answers for x and y and input them like so:
# x_screen = ((x + 1) / 2) * width 
# y_screen = ((y+1) / 2) * height

def CombinePosCol(positions, colors):
    to_return = []
    for i in range(0, len(positions)):
        to_append = positions[i] + colors[i]
        to_return.append(to_append)
        
    return to_return
def tosRGB(color):
    to_return = []
    for i in range(0, len(color)):
        if (color[i] <= 0.0031308):
            to_return.append(color[i] * 12.92)
        else:
            to_return.append(1.055*color[i]**(1/2.4) - 0.055)
    return to_return

def ViewportTransformation(p, width, height):
    #takes an array of (x,y,z,w) points
    # converts it into an array of (x,y) points via viewport transformation
    to_return = []
    #print("view")
    #print(len(p))
    for i in range(0,len(p)):
        i_div_w = []
        for j in range(0,len(p[0])):
            div_w = p[i][j] / p[i][3]
            i_div_w.append(div_w)
        #print(i_div_w)
        new_x = ((i_div_w[0] + 1) / 2) * width
        new_y = ((i_div_w[1] + 1) / 2) * height
        if (len(p[0]) == 3):
            to_append = [new_x, new_y, p[i][2]]
        elif (len(p[0]) == 4):
            to_append = [new_x, new_y, p[i][2], p[i][3]]
        else:
            to_append = [new_x, new_y]
        #print(to_append)
        to_return.append(to_append)

    return to_return


def DDA(input_a, input_b, int_dim, consider_alpha):
    #a and b are endpoints of a line
    #int_dim is the dimension that should be taken at integers only. The other dimension can be floats
    a = input_a
    b = input_b
    to_return = []
    #print(a[int_dim])
    if (a[int_dim] == b[int_dim]):
        #print("A and B are the same point")
        return to_return
    if (a[int_dim] > b[int_dim]):
        a = input_b
        b = input_a
    #print("DOING DDA WITH A: " + str(a) + " AND B: " + str(b))
    #print(len(a))
    if (not consider_alpha):
        delta = [0, 0, 0, 0, 0, 0]
        for i in range(0, 3):
            delta[i] = b[i] - a[i]
        coord_length = len(a)
        a_color = [a[coord_length - 4], a[coord_length - 3], a[coord_length - 2], 1]
        b_color = [b[coord_length - 4], b[coord_length - 3], b[coord_length - 2], 1]
        for i in range(0, 3):
            delta[i + 3] = b_color[i] - a_color[i]
        #print(b[int_dim], a[int_dim])
        step_length = [0,0,0, 0, 0, 0]
        step_length[0] = delta[0] / (b[int_dim] - a[int_dim])
        step_length[1] = delta[1] / (b[int_dim] - a[int_dim])
        step_length[2] = delta[2] / (b[int_dim] - a[int_dim])
        step_length[3] = delta[3] / (b[int_dim] - a[int_dim])
        step_length[4] = delta[4] / (b[int_dim] - a[int_dim])
        step_length[5] = delta[5] / (b[int_dim] - a[int_dim])

        #print(step_length)
        e = np.ceil(a[int_dim]) - a[int_dim]
        o = [0,0, 0, 0,0,0] 
        o[0] = e * step_length[0]
        o[1] = e * step_length[1]
        o[2] = e * step_length[2]
        o[3] = e* step_length[3]
        o[4] = e* step_length[4]
        o[5] = e*step_length[5]
        #print(o)
        p = [0,0,0, 0,0,0]
        p[0] = a[0] + o[0]
        p[1] = a[1] + o[1]
        p[2] = a[2] + o[2]
        p[3] = a_color[0] + o[3]
        p[4] = a_color[1] + o[4]
        p[5] = a_color[2] + o[5]
        #print(p)
        num_pixels = 0
        while(p[int_dim] < b[int_dim]):
            tempx = p[0]
            tempy = p[1]
            tempz = p[2]
            tempr = p[3]
            tempg = p[4]
            tempb = p[5]
            tempa = 1
            to_return.append([tempx, tempy, tempz, tempr, tempg, tempb, tempa])
            #print(to_return)
            p[0] += step_length[0]
            p[1] += step_length[1]
            p[2] += step_length[2]
            p[3] += step_length[3]
            p[4] += step_length[4]
            p[5] += step_length[5]
            #keep curr_color_val[3] at 1
            #print(p[int_dim], b[int_dim])
            num_pixels += 1
    else:
        #for alpha:
        delta = [0, 0, 0, 0, 0, 0, 0]
        for i in range(0,3):
            delta[i] = b[i] - a[i]
        coord_length = len(a)
        a_color = [a[coord_length - 4], a[coord_length - 3], a[coord_length - 2], a[coord_length-1]]
        b_color = [b[coord_length - 4], b[coord_length - 3], b[coord_length - 2], b[coord_length-1]]
        for i in range(0, 4):
            delta[i + 3] = b_color[i] - a_color[i]
        step_length = [0,0,0, 0, 0, 0, 0]
        step_length[0] = delta[0] / (b[int_dim] - a[int_dim])
        step_length[1] = delta[1] / (b[int_dim] - a[int_dim])
        step_length[2] = delta[2] / (b[int_dim] - a[int_dim])
        step_length[3] = delta[3] / (b[int_dim] - a[int_dim])
        step_length[4] = delta[4] / (b[int_dim] - a[int_dim])
        step_length[5] = delta[5] / (b[int_dim] - a[int_dim])
        step_length[6] = delta[6] / (b[int_dim] - a[int_dim])
        e = np.ceil(a[int_dim]) - a[int_dim]
        o = [0,0, 0, 0,0,0, 0] 
        o[0] = e * step_length[0]
        o[1] = e * step_length[1]
        o[2] = e * step_length[2]
        o[3] = e* step_length[3]
        o[4] = e* step_length[4]
        o[5] = e*step_length[5]
        o[6] = e*step_length[6]
        p = [0,0,0, 0,0,0, 0]
        p[0] = a[0] + o[0]
        p[1] = a[1] + o[1]
        p[2] = a[2] + o[2]
        p[3] = a_color[0] + o[3]
        p[4] = a_color[1] + o[4]
        p[5] = a_color[2] + o[5]
        p[6] = a_color[3] + o[6]
        while(p[int_dim] < b[int_dim]):
            tempx = p[0]
            tempy = p[1]
            tempz = p[2]
            tempr = p[3]
            tempg = p[4]
            tempb = p[5]
            tempa = p[6]
            #print(tempa)
            to_return.append([tempx, tempy, tempz, tempr, tempg, tempb, tempa])
            #print(tempa)
            #print(to_return)
            p[0] += step_length[0]
            p[1] += step_length[1]
            p[2] += step_length[2]
            p[3] += step_length[3]
            p[4] += step_length[4]
            p[5] += step_length[5]
            p[6] += step_length[6]
            #keep curr_color_val[3] at 1
            #print(p[int_dim], b[int_dim])
        #print("e")
    return to_return

# def hypDDA(input_a, input_b, int_dim):
#     #a and b are endpoints of a line
#     #int_dim is the dimension that should be taken at integers only. The other dimension can be floats
#     a = input_a
#     b = input_b
#     to_return = []
#     #print(a[int_dim])
#     if (a[int_dim] == b[int_dim]):
#         #print("A and B are the same point")
#         return to_return
#     if (a[int_dim] > b[int_dim]):
#         a = input_b
#         b = input_a
#     #print("DOING DDA WITH A: " + str(a) + " AND B: " + str(b))

#     div_w_a =[]
#     div_w_b = []
#     for i in range(0, len(a)):
#         if (i == 3):
#             div_w_a.append(1 / a[3])
#             div_w_b.append(1 / b[3])
#         else:
#             div_w_a.append(a[i] / a[3])
#             div_w_b.append(b[i] / b[3])
#     print(a, b)
#     print(div_w_a, div_w_b)

#     delta = [0, 0, 0, 0, 0, 0, 0]
#     #added w because it didn't matter before
#     for i in range(0, 7):
#         delta[i] = div_w_b[i] - div_w_a[i]
#     #print(b[int_dim], a[int_dim])
#     step_length = [0,0,0, 0, 0, 0, 0]
#     step_length[0] = delta[0] / (div_w_b[int_dim] - div_w_a[int_dim])
#     step_length[1] = delta[1] / (div_w_b[int_dim] - div_w_a[int_dim])
#     step_length[2] = delta[2] / (div_w_b[int_dim] - div_w_a[int_dim])
#     step_length[3] = delta[3] / (div_w_b[int_dim] - div_w_a[int_dim])
#     step_length[4] = delta[4] / (div_w_b[int_dim] - div_w_a[int_dim])
#     step_length[5] = delta[5] / (div_w_b[int_dim] - div_w_a[int_dim])
#     step_length[6] = delta[6] / (div_w_b[int_dim] - div_w_a[int_dim])
#     #print(step_length)
#     e = np.ceil(div_w_a[int_dim]) - div_w_a[int_dim]
#     o = [0,0, 0, 0, 0,0,0] 
#     o[0] = e * step_length[0]
#     o[1] = e * step_length[1]
#     o[2] = e * step_length[2]
#     o[3] = e* step_length[3]
#     o[4] = e* step_length[4]
#     o[5] = e*step_length[5]
#     o[6] = e*step_length[6]
#     #print(o)
#     p = [0,0,0,0, 0,0,0]
#     p[0] = div_w_a[0] + o[0]
#     p[1] = div_w_a[1] + o[1]
#     p[2] = div_w_a[2] + o[2]
#     p[3] = div_w_a[3] + o[3]
#     p[4] = div_w_a[0] + o[4]
#     p[5] = div_w_a[1] + o[5]
#     p[6] = div_w_a[2] + o[6]
#     #print(p)
#     num_pixels = 0
#     while(p[int_dim] < div_w_b[int_dim]):
#         tempx = p[0]
#         tempy = p[1]
#         tempz = p[2]
#         #fix everything after z for hyp
#         tempw = 1 / p[3]
#         tempr = p[4] / p[3]
#         tempg = p[5] / p[3]
#         tempb = p[6] / p[3]
#         #print(tempr,tempg,tempb)
#         tempa = 1
#         to_return.append([tempx, tempy, tempz, tempw, tempr, tempg, tempb, tempa])
#         #print(to_return)
#         p[0] += step_length[0]
#         p[1] += step_length[1]
#         p[2] += step_length[2]
#         p[3] += step_length[3]
#         p[4] += step_length[4]
#         p[5] += step_length[5]
#         p[6] += step_length[6]
#         #keep curr_color_val[3] at 1
#         #print(p[int_dim], b[int_dim])
#         num_pixels += 1
    
#     #print(len(to_return))

#     return to_return



def Scanline(p, q, r, hyp, consider_alpha): #p, q, and r are the endpoints of the triangle
    to_return = []
    t = p
    b = p
    m = p
    points = [p,q,r]
    for i in range(0, len(points)):
        if (points[i][1] < t[1]):
            t = points[i]
        if (points[i][1] > b[1]):
            b = points[i]
    for j in range(0, len(points)):
        if (points[j] != t and points[j] != b):
            m = points[j]
    #print("TMB")
    #print(p)
    if (not consider_alpha):
        t_to_b_dda = DDA(t, b, 1, False) # this is the longest point array
        #print("t to b: " + str(len(t_to_b_dda)))
        t_to_m_dda = DDA(t, m, 1, False)
        #print("t to m: " + str(len(t_to_m_dda)))
        m_to_b_dda = DDA(m,b,1, False)
        #print("m to b: " + str(len(m_to_b_dda)))
        #the number of points in t_to_m + m_to_b should be equal to t_to_b
        #print(len(t_to_b_dda[0]), len(t_to_m_dda[0]), len(m_to_b_dda[0]))
        #first set of loops for upper-most non-longest side
        for i in range(0, len(t_to_m_dda)):
            row_pixels = DDA(t_to_b_dda[i], t_to_m_dda[i], 0, False) #assuming row-wise dim is x for now (may need to change later)
            for j in range(0, len(row_pixels)):
                to_return.append(row_pixels[j])

        # #second set of loops for lower-most non-longest side
        for i in range(len(t_to_m_dda), len(t_to_b_dda)):
            row_pixels = DDA(t_to_b_dda[i], m_to_b_dda[i - len(t_to_m_dda)], 0, False)
            for j in range(0, len(row_pixels)):
                to_return.append(row_pixels[j])
    else:
        t_to_b_dda = DDA(t, b, 1, True) # this is the longest point array
        #print("t to b: " + str(len(t_to_b_dda)))
        t_to_m_dda = DDA(t, m, 1, True)
        #print("t to m: " + str(len(t_to_m_dda)))
        m_to_b_dda = DDA(m,b,1, True)
        #print("m to b: " + str(len(m_to_b_dda)))
        #the number of points in t_to_m + m_to_b should be equal to t_to_b
        #print(len(t_to_b_dda[0]), len(t_to_m_dda[0]), len(m_to_b_dda[0]))
        #first set of loops for upper-most non-longest side
        for i in range(0, len(t_to_m_dda)):
            row_pixels = DDA(t_to_b_dda[i], t_to_m_dda[i], 0, True) #assuming row-wise dim is x for now (may need to change later)
            for j in range(0, len(row_pixels)):
                to_return.append(row_pixels[j])

        # #second set of loops for lower-most non-longest side
        for i in range(len(t_to_m_dda), len(t_to_b_dda)):
            row_pixels = DDA(t_to_b_dda[i], m_to_b_dda[i - len(t_to_m_dda)], 0, True)
            for j in range(0, len(row_pixels)):
                to_return.append(row_pixels[j])
    #     t_to_b_dda = hypDDA(t, b, 1) # this is the longest point array
    #     print("t to b: " + str(len(t_to_b_dda)))
    #     t_to_m_dda = hypDDA(t, m, 1)
    #     print("t to m: " + str(len(t_to_m_dda)))
    #     m_to_b_dda = hypDDA(m,b,1)
    #     print("m to b: " + str(len(m_to_b_dda)))
    #     #the number of points in t_to_m + m_to_b should be equal to t_to_b

    #     #first set of loops for upper-most non-longest side
    #     for i in range(0, len(t_to_m_dda)):
    #         row_pixels = hypDDA(t_to_b_dda[i], t_to_m_dda[i], 0) #assuming row-wise dim is x for now (may need to change later)
    #         for j in range(0, len(row_pixels)):
    #             to_return.append(row_pixels[j])

    #     # #second set of loops for lower-most non-longest side
    #     for i in range(len(t_to_m_dda), len(t_to_b_dda)):
    #         row_pixels = hypDDA(t_to_b_dda[i], m_to_b_dda[i - len(t_to_m_dda)], 0)
    #         for j in range(0, len(row_pixels)):
    #             to_return.append(row_pixels[j])


    return (to_return) 


    #returns all points between a and b where p_d is an integer

with open(sys.argv[1], 'r') as f:
    
    #print(f)
    lines = f.readlines()
    #file setup state
    png_filename = ""
    width = 0
    height = 0
    #image = Image.new("RGBA", (width, height))
    #mode state (Ignore until done with core functionality)
    depth = False #depth buffer and depth tests
    sRGB = False   # sRGB conversions of color before saving to png file
    hyp = False # enables hyperbolic interpolation of depth, color, and texture coords
    fsaa = 0 #full screen anti-aliasing/multisampling level ranges from 1 to 8
    cull = False #enables back-face culling
    decals = False #when drawing transparent textures, include the vertex colors underneath
    frustum = False #enables frustum clipping
    image = Image.new("RGBA", (width, height))
    #uniform state
    texture = "" #will be a filename
    uniformMatrix = [] #Will be a 4x4 matrix n0-n15 multiplied by (x,y,z,w)

    #buffer provision
    positions_raw = [] #will contain a number first representing size which will be used to group together following listed numbers
    #Note x= -1 to 1 is left to right, y = -1 to 1 is top to bottom
    positions = [] #positions after viewport transformations are applied
    color = [] #will contain a size value used like position of 3 or 4. 3 for RGB, 4 for RGBA. A is alpha for transparency
    textcoord = [] #size is always 2. gives texel coordinates of size 2.
    point_size = [] #size is always 1. (size of rendered points)
    elements = [] #all indices are non-negative integers
    depth = False
    sRGB = False
    hyp = False
    consider_alpha = False
    pastPoints = []
    #lines in a file will either manipulate state or draw current state
    for line in lines:
        line = line.strip()
        #print(line)
        curr_str = ""
        item_idx = 0 #this pertains to each item of interest in the string
        char_idx = 0 #this pertains to the char index in the line
        for c in line:
            if (c != " "):
                curr_str += c
            #=========================================PNG==================================================
            if (curr_str == "png"):
                curr_str = ""
                item_idx += 1
                char_idx += 1
                curr_substr = ""
                for d in range(char_idx, len(line)):
                    if (line[d] == " "):
                        if (len(curr_substr) != 0):
                            if (item_idx == 1):
                                width = int(curr_substr)
                            elif(item_idx == 2):
                                height = int(curr_substr)
                            item_idx += 1
                            curr_substr = ""
                    elif (d >= len(line) - 1):
                        filename = curr_substr 
                        filename += line[len(line) - 1]
                    else:
                        curr_substr += line[d]
                #print("Finished processing png file information. width is " + str(width) + " height is " + str(height) + " filename is " + str(filename))
                image = Image.new("RGBA", (width, height))
                break #break here because we finished processing a line
            #==========================================PNG==============================================
            
            #==========================================POS2=============================================
            elif (curr_str == "position2"):
                #Set z to 0 and w to 1
                #print("found position2")
                char_idx += 1
                curr_str = ""
                curr_substr = ""
                curr_coord = [] #list containing (x,y)
                is_x_coord = True #this bool keeps track of if we are tracking x coordinate to decide whether to append to curr_coord_list or not
                for d in range(char_idx, len(line)):
                
                    if (line[d] == " " ):
                        if (len(curr_substr) != 0):
                            if (is_x_coord):
                                curr_coord.append(float(curr_substr))
                                is_x_coord = False
                            else:
                                curr_coord.append(float(curr_substr))
                                curr_coord.append(0) #for z
                                curr_coord.append (1) #for w
                                positions_raw.append(curr_coord)
                                curr_coord = []
                                is_x_coord = True

                            curr_substr = ""
                    elif (d >= len(line) - 1):
                        curr_coord.append(float(curr_substr + line[len(line) - 1]))
                        curr_coord.append(0)
                        curr_coord.append(1)
                        positions_raw.append(curr_coord)
                    else:
                        curr_substr += line[d]
                
                positions = ViewportTransformation(positions_raw, width, height)
                break
            #===================================================POS2================================================

            #===================================================POS3================================================
            elif (curr_str == "position3"):
                #set w to 1
                #print("found position3")
                char_idx += 1
                curr_str = ""
                curr_substr = ""
                curr_coord = [] #list containing (x,y)
                curr_coord_idx = 0 #this int keeps track of if we are writing x, y, or z
                for d in range(char_idx, len(line)):
                    if (line[d] == " " ):
                        if (len(curr_substr) != 0):
                            if (curr_coord_idx < 2):
                                curr_coord.append(float(curr_substr))
                                curr_coord_idx += 1
                            else:
                                curr_coord.append(float(curr_substr))
                                curr_coord.append(1) #for w
                                positions_raw.append(curr_coord)
                                curr_coord = []
                                curr_coord_idx = 0
                            curr_substr = ""
                    elif (d >= len(line) - 1):
                        curr_coord.append(float(curr_substr + line[len(line) - 1]))
                        curr_coord.append(1)
                        positions_raw.append(curr_coord)
                    else:
                        curr_substr += line[d]
                positions = ViewportTransformation(positions_raw, width, height)
                break
            #===================================================POS3===================================================

            #===================================================POS4===================================================
            elif (curr_str == "position4"):
                #no need to use default values
                if (len(positions_raw) != 0):
                    positions_raw = []
                
                #print("found position4")
                char_idx += 1
                curr_str = ""
                curr_substr = ""
                curr_coord = [] #list containing (x,y)
                curr_coord_idx = 0
                for d in range(char_idx, len(line)):
                    if (line[d] == " " ):
                        if (len(curr_substr) != 0):
                            if (curr_coord_idx < 3):
                                curr_coord.append(float(curr_substr))
                                curr_coord_idx += 1
                            else:
                                curr_coord.append(float(curr_substr))
                                positions_raw.append(curr_coord)
                                curr_coord = []
                                curr_coord_idx = 0

                            curr_substr = ""
                    elif (d >= len(line) - 1):
                        curr_coord.append(float(curr_substr + line[len(line) - 1]))
                        positions_raw.append(curr_coord)
                    else:
                        curr_substr += line[d]
                #print(positions_raw)
                positions = ViewportTransformation(positions_raw, width, height)
                #print(positions)
                break
            #=======================================================================POS4=================================================

            #===============================================================COLOR3=======================================================
            elif (curr_str == "color3"):
                #note, when getting later in the assignment, figure out what sRGB storage means as that is a 3-val coord
                #otherwise, assume alpha is 1 or completely opaque
                if (len(color) != 0):
                    color = []
                #print("found color3")
                char_idx += 1
                curr_str = ""
                curr_substr = ""
                curr_coord = [] #list containing (r,g,b,a)
                coord_idx = 0 #idx pertaining to which coordinate we are filling
                for d in range(char_idx, len(line)):
                    if (line[d] == " " ):
                        if (len(curr_substr) != 0):
                            if (coord_idx < 2):
                                curr_coord.append(float(curr_substr))
                                coord_idx += 1
                            else:
                                curr_coord.append(float(curr_substr))
                                curr_coord.append(1)
                                color.append(curr_coord)
                                curr_coord = []
                                coord_idx = 0

                            curr_substr = ""
                    elif (d >= len(line) - 1):
                        curr_coord.append(float(curr_substr + line[len(line) - 1]))
                        curr_coord.append(1)
                        color.append(curr_coord)

                    else:
                        curr_substr += line[d]
                #positions = ViewportTransformation(positions_raw, width, height)
                break
            #===============================================================COLOR3=======================================================

            #==============================================================COLOR4========================================================
            elif (curr_str == "color4"):
                #print("found color4")
                char_idx += 1
                curr_str = ""
                curr_substr = ""
                
                curr_coord = [] #list containing (r,g,b,a)
                coord_idx = 0 #idx pertaining to which coordinate we are filling
                for d in range(char_idx, len(line)):
                    if (line[d] == " " ):
                        if (len(curr_substr) != 0):
                            if (coord_idx < 3):
                                curr_coord.append(float(curr_substr))
                                coord_idx += 1
                            else:
                                curr_coord.append(float(curr_substr))
                                color.append(curr_coord)
                                curr_coord = []
                                coord_idx = 0

                            curr_substr = ""
                    elif (d >= len(line) - 1):
                        curr_coord.append(float(curr_substr + line[len(line) - 1]))
                        color.append(curr_coord)

                    else:
                        curr_substr += line[d]
                consider_alpha = True
                break
            #================================================================COLOR4======================================================
            
            #===============================================================elements===================================================
            elif (curr_str == "elements"):
                char_idx += 1
                curr_str = ""
                curr_substr = ""
                curr_coord = [] #list containing (1,2,3)
                curr_coord_idx = 0 #this int keeps track of if we are writing x, y, or z
                for d in range(char_idx, len(line)):
                    if (line[d] == " " ):
                        if (len(curr_substr) != 0):
                            if (curr_coord_idx < 2):
                                curr_coord.append(float(curr_substr))
                                curr_coord_idx += 1
                            else:
                                curr_coord.append(float(curr_substr))
                                elements += (curr_coord)
                                curr_coord = []
                                curr_coord_idx = 0
                            curr_substr = ""
                    elif (d >= len(line) - 1):
                        curr_coord.append(float(curr_substr + line[len(line) - 1]))
                        elements += (curr_coord)
                    else:
                        curr_substr += line[d]
                #print(elements)
                break
            #============================================elements======================================

            #---------------------------------------------sRGB------------------------------------------------
            elif (curr_str == "sRGB"):
                sRGB = True

            elif (curr_str == "depth"):
                depth = True
            
            elif (curr_str == "drawPixels"):
                #print("found drawPixels")
                curr_substr = ""
                char_idx += 1
                for d in range(char_idx, len(line)):
                    if (line[d] != " "):
                        curr_substr += line[d]
                #print(curr_substr)
                num_pixels = int(curr_substr)
                break
            #-----------------------------------------------sRGB---------------------------------------------

            #===============================================hyp==============================================
            elif (curr_str == "hyp"):
                hyp = True

            #=======================================================DrawArrayTriangles(first, count)=====================================
            elif (curr_str == "drawArraysTriangles"):
                curr_substr = ""
                char_idx += 1
                DAT_first = -1 #-1 indicates not assigned yet
                DAT_count = -1
                #print("LINE LENGTH: " + str(len(line)))
                for d in range(char_idx, len(line)):
                    #print(str(d) + curr_substr)
                    if (line[d] != " "):
                        curr_substr += line[d]
                        if (d >= len(line) - 1):
                            DAT_count = int(curr_substr)
                    else:
                        if (curr_substr != ""):
                            if (DAT_first == -1):
                                DAT_first = int(curr_substr)
                                curr_substr = ""
                curr_first = DAT_first
                PosCol = CombinePosCol(positions, color)
                for i in range(0,int(DAT_count / 3)):
                    pointsToReturn = Scanline(PosCol[curr_first], PosCol[curr_first + 1], PosCol[curr_first + 2], hyp, consider_alpha)
                    for j in range(0, len(pointsToReturn)):
                        if (pointsToReturn[j][0] >= width or pointsToReturn[j][1] >= height):
                            continue
                        if (image.getpixel((pointsToReturn[j][0], pointsToReturn[j][1])) != (0,0,0,0) and depth):
                            existing_z = 0
                            counter = 0
                            for i in range(0, len(pastPoints)):
                                if (pastPoints[i][0] == pointsToReturn[j][0] and pastPoints[i][1] == pointsToReturn[j][1]):
                                    counter += 1
                                    if (i == j):
                                        continue
                                    else:
                                        existing_z = pastPoints[i][2]
                        
                            new_z = pointsToReturn[j][2]
                            if (existing_z >= new_z):
                                
                                if (sRGB):
                                    sRGBColors = tosRGB([pointsToReturn[j][3], pointsToReturn[j][4], pointsToReturn[j][5]])
                                    image.putpixel((int(pointsToReturn[j][0]), int(pointsToReturn[j][1])), (int(np.floor(sRGBColors[0] * 256)), int(np.floor(sRGBColors[1]*256)), int(np.floor(sRGBColors[2]*256)), int(np.floor(pointsToReturn[j][6]) * 256)))
                                else:
                                    image.putpixel((int(pointsToReturn[j][0]), int(pointsToReturn[j][1])), (int(np.floor(pointsToReturn[j][3] * 256)), int(np.floor(pointsToReturn[j][4]*256)), int(np.floor(pointsToReturn[j][5]*256)), int(np.floor(pointsToReturn[j][6]) * 256)))
                        else:
                            if (sRGB):
                                sRGBColors = tosRGB([pointsToReturn[j][3], pointsToReturn[j][4], pointsToReturn[j][5]])
                                image.putpixel((int(pointsToReturn[j][0]), int(pointsToReturn[j][1])), (int(np.floor(sRGBColors[0] * 256)), int(np.floor(sRGBColors[1]*256)), int(np.floor(sRGBColors[2]*256)), int(np.floor(pointsToReturn[j][6]) * 256)))
                            else:
                                image.putpixel((int(pointsToReturn[j][0]), int(pointsToReturn[j][1])), (int(np.floor(pointsToReturn[j][3] * 256)), int(np.floor(pointsToReturn[j][4]*256)), int(np.floor(pointsToReturn[j][5]*256)), int(np.floor(pointsToReturn[j][6]) * 256)))
                    pastPoints += pointsToReturn
                    curr_first += 3
                num_pixels = int(curr_substr)
                image.save(filename)
                break
            #========================================================DrawArrayTriangles(first, count)====================================
            #========================================================DrawElementsTriangle=================================================
            
            elif (curr_str == "drawElementsTriangles"):
                curr_substr = ""
                char_idx += 1
                DET_count = -1 #-1 indicates not assigned yet
                DET_offset = -1
                #print("LINE LENGTH: " + str(len(line)))
                for d in range(char_idx, len(line)):
                    #print(str(d) + curr_substr)
                    if (line[d] != " "):
                        curr_substr += line[d]
                        if (d >= len(line) - 1):
                            DET_offset = int(curr_substr)
                    else:
                        if (curr_substr != ""):
                            if (DET_count == -1):
                                DET_count = int(curr_substr)
                                curr_substr = ""
                curr_first = DET_offset
                PosCol = CombinePosCol(positions, color)
                
                #print("no")
                for i in range(0,int(DET_count / 3)):
                    #print("begin length: " + str(len(pastPoints)))
                    pointsToReturn = Scanline(PosCol[int(elements[curr_first])], PosCol[int(elements[curr_first + 1])], PosCol[int(elements[curr_first + 2])], hyp, consider_alpha)                    
                    for j in range(0, len(pointsToReturn)):
                        if (pointsToReturn[j][0] >= width or pointsToReturn[j][1] >= height):
                            continue
                        if (image.getpixel((pointsToReturn[j][0], pointsToReturn[j][1])) != (0,0,0,0) and depth):
                            #print("nO")
                            existing_z = 0
                            counter = 0
                            for i in range(0, len(pastPoints)):
                                if (pastPoints[i][0] == pointsToReturn[j][0] and pastPoints[i][1] == pointsToReturn[j][1]):
                                    counter += 1
                                    if (i == j):
                                        continue
                                    else:
                                        existing_z = pastPoints[i][2]
                        
                            new_z = pointsToReturn[j][2]
                            if (existing_z > new_z):
                                if (sRGB):
                                    sRGBColors = tosRGB([pointsToReturn[j][3], pointsToReturn[j][4], pointsToReturn[j][5]])
                                    image.putpixel((int(pointsToReturn[j][0]), int(pointsToReturn[j][1])), (int(np.floor(sRGBColors[0] * 256)), int(np.floor(sRGBColors[1]*256)), int(np.floor(sRGBColors[2]*256)), int(np.floor(pointsToReturn[j][6] * 256))))
                                else:
                                    image.putpixel((int(pointsToReturn[j][0]), int(pointsToReturn[j][1])), (int(np.floor(pointsToReturn[j][3] * 256)), int(np.floor(pointsToReturn[j][4]*256)), int(np.floor(pointsToReturn[j][5]*256)), int(np.floor(pointsToReturn[j][6] * 256))))
                        elif (image.getpixel((pointsToReturn[j][0], pointsToReturn[j][1])) != (0,0,0,0)):
                            #print(image.getpixel((pointsToReturn[j][0], pointsToReturn[j][1])))
                            #print(len(pastPoints))
                            existing_col = []
                            for i in range(0, len(pastPoints)):
                                if (pastPoints[i][0] == pointsToReturn[j][0] and pastPoints[i][1] == pointsToReturn[j][1]):
                                    if (i == j):
                                        continue
                                    else:
                                        existing_col.append(pastPoints[i][3])
                                        existing_col.append(pastPoints[i][4])
                                        existing_col.append(pastPoints[i][5])
                                        existing_col.append(pastPoints[i][6])
                            
                            #print(existing_col)
                            a_d = existing_col[3]
                            a_s = pointsToReturn[j][6]
                            #print(a_d, a_s)
                            alpha = a_s + (a_d) * (1-a_s)
                            #print(alpha)
                            r = (a_s / alpha) * pointsToReturn[j][3] + (((1-a_s)*a_d) / alpha) * (existing_col[0])
                            g = (a_s / alpha) * pointsToReturn[j][4] + (((1-a_s)*a_d) / alpha) * (existing_col[1])
                            b = (a_s / alpha) * pointsToReturn[j][5] + (((1-a_s)*a_d) / alpha) * (existing_col[2])
                            #print(r,g,b)
                            # new_z = pointsToReturn[j][2]
                            #if (existing_z >= new_z):
                            
                            if (sRGB):
                                sRGBColors = tosRGB([r,g,b])
                                image.putpixel((int(pointsToReturn[j][0]), int(pointsToReturn[j][1])), (int(np.floor(sRGBColors[0] * 256)), int(np.floor(sRGBColors[1]*256)), int(np.floor(sRGBColors[2]*256)), int((np.floor(alpha * 256)))))
                            else:
                                image.putpixel((int(pointsToReturn[j][0]), int(pointsToReturn[j][1])), (int(np.floor(r * 256)), int(np.floor(g*256)), int(np.floor(b*256)), int(np.floor(alpha * 256))))
                        else:
                            #print(pointsToReturn[j][6] * 255)
                            if (sRGB):
                                sRGBColors = tosRGB([pointsToReturn[j][3], pointsToReturn[j][4], pointsToReturn[j][5]])
                                image.putpixel((int(pointsToReturn[j][0]), int(pointsToReturn[j][1])), (int(np.floor(sRGBColors[0] * 256)), int(np.floor(sRGBColors[1]*256)), int(np.floor(sRGBColors[2]*256)), int(np.floor(pointsToReturn[j][6] * 256))))
                            else:
                                image.putpixel((int(pointsToReturn[j][0]), int(pointsToReturn[j][1])), (int(np.floor(pointsToReturn[j][3] * 256)), int(np.floor(pointsToReturn[j][4]*256)), int(np.floor(pointsToReturn[j][5]*256)), int(np.floor(pointsToReturn[j][6] * 256))))
                    if (len(pastPoints) == 0):
                        pastPoints = pointsToReturn
                    else:

                        pastPoints += pointsToReturn
                    #print(len(pointsToReturn))
                    #print("endlength: " + str(len(pastPoints)))
                    curr_first += 3
                num_pixels = int(curr_substr)
                image.save(filename)
                break

            char_idx += 1
    #print(len(positions), len(color), len(elements))    
    #drawing algos to implement:
    #drawArraysTriangles(first, count) #first is the first point of the first triangle to draw, count is the number of points after the first that is the last point
    # - Count is a multiple of 3
    # - draws a triangle with vertices position[first + 0], position[first+1], position[first+2] and corresponding color and texture coords
    # and so on

    #drawElementsTriangles(count, offset):
    #- count will be % 3
    # - draws a triangle with vertices position[elements[offset+0]], position[elements[offset+1]], position[elements[offset+2]] and corresponding color and texcoords
    #and so on
    
    #drawArrayPoints(first, count)
    # - draw a square centered on position[first+0] with diameter pointsize[first+0] pixels and color color[first+0]
    # and so on for count val
    # - Each square has texture coordinates varying from (0,0) in its top-left corner to (1,1) in its bottom-right corner




