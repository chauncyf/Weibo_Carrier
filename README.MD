##Weibo Carrier
We don't create weibo, We generate pic from weibo

## This program aims to generate delicate pics with your posts or other users' posts you would like to save.  
I have already make 8 themes for you, default theme is light yellow  
default font is NotoSansCJKsc-Light.otf, it's a awesome font provided by Google
you can change theme and font at the top of code  
'''python
    LAYOUT = LAYOUT_ONE
    COLOR_SCHEME = LIGHT_YELLOW
    FONT = 'NotoSansCJKsc-DemiLight.otf'
'''    

##
This program command cookie to simulate login, thus you have to get you cookie manually  
Firstly, login at http://weibo.com  
Secondly, press F12 to open developer tools, switch to Network tab, then press F5 to refresh page  
(Using Chrome to handle this is a ideal choice  
Then, Drag the scroll bar to the top and click the first tab, copy 'SUP=xxx;SUB=xxx;' at the right window  
Last, paste it to 'your cookie' at the top of the code (don't delete the quotation mark)  
``` python
    urls = ['url']
    header = {'Cookie': 'your cookie'}
```

![image](https://github.com/chauncygrey/weibo_pic_carrier/blob/master/get_cookie.jpg)

Input your target users' homepage url like this ['url', 'url2', 'url3']


##Caution
Recommend to open with IDLE

## Welcome to Fork & Star

### Contact
chauncygrey@foxmail.com

### Python
https://www.python.org/downloads/windows/

## Needs
1. Python 3.5  
2. Requests, a HTTP library for human beings. 
3. Lxml, a binding for the libxml2 and libxslt libraries. 
4. Pillow, a replacement for PIL, the Python Image Library, which provides image processing functionality and supports many file formats.

### Extension package installation
Install with pip:
$ pip install requests
$ pip install lxml
$ pip install Pillow
