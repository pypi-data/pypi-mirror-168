import PIL.Image

def main():
    path = input("Enter the path to the image fiel : \n")
    try:
        image = PIL.Image.open(path)
    except:
        print(path, "Unable to find image ");

# ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
# ASCII_CHARS = ["@", "#", "$", "%", "?", "*", " ", " ", " ", " ", " "]
ASCII_CHARS = ["*", "*", "*", "*", "*", "*", " ", " ", " ", " ", " "]

def resize(image, new_width = 20):
    width, height = image.size
    new_height = int(new_width * height / width)
    return image.resize((new_width, new_height))

### for batman logo
# def resize(image, new_width = 70):
#     width, height = image.size
#     # new_height = int(new_width * height / width)
#     new_height = 25
#     return image.resize((new_width, new_height))

def to_greyscale(image):
    return image.convert("L")

def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "";
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//25];
    return ascii_str

def main():
    # path = input("Enter the path to the image fiel : \n")
    path = 'thammer.jpg'
    # path = 'car.jpg'
    # path = 'batman.jpg'
    try:
        image = PIL.Image.open(path)
    except:
        print(path, "Unable to find image ")
    #resize image
    image = resize(image);
    #convert image to greyscale image
    greyscale_image = to_greyscale(image)
    # convert greyscale image to ascii characters
    ascii_str = pixel_to_ascii(greyscale_image)
    img_width = greyscale_image.width
    ascii_str_len = len(ascii_str)
    ascii_img=""
    #Split the string based on width  of the image
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
    print(ascii_img)
    #save the string to a file
    with open("ascii_image.txt", "w") as f:
        f.write(ascii_img);

def signature():
    print('''
       ** 
        ** 
         **    
          **     *     
           **   ***    
            ** ******   
             ********* 
             *      *** 
            ****  **** 
           *****  ***  
            ****  **   
             ******     
              ****     
               **
    ''')

if __name__ == '__main__':
    # main()
    signature()