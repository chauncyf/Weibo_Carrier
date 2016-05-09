Weibo Carrier
=============

We don't create weibo, We generate pic from weibo

This program aims to generate delicate pics with your posts or other users' posts you would like to save.


#### Here are color schemes
|  ![light_grey](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample_light_grey.jpg)  |  ![red](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample_red.jpg) |
| :-----: | :-----: |
|  ![pink](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample_pink.jpg)  |  ![purple](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample_purple.jpg) |
|  ![blue](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample_blue.jpg)  |  ![cyan](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample_cyan.jpg) |
|  ![teal](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample_teal.jpg)  |  ![green](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample_green.jpg) |
|  ![orange](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample_orange.jpg) |  ![brown](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample_brown.jpg) |

#### Here are samples
|  ![sample](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample1.jpg)  |  ![sample](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample2.jpg) |
| :-----: | :-----: |
|  ![sample](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample3.jpg)  |  ![sample](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample4.jpg) |
|  ![sample](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample5.jpg)<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>  |  ![sample](https://github.com/chauncygrey/weibo_carrier/blob/master/sample/sample6.jpg) |


## How to use
Default font is NotoSansCJKsc-DemiLight.otf, it's an awesome font provided by Google  
You can change layout, color scheme and font at **top** of the code
``` python
    LAYOUT = LAYOUT_ONE
    COLOR_SCHEME = LIGHT_GREY
    FONT = 'NotoSansCJKsc-DemiLight.otf'
```

This program command cookie to simulate login, thus you have to get you cookie manually
* Firstly, login at [weibo.com](http://weibo.com "http://weibo.com")
* Secondly, press F12 to open developer tools, switch to Network tab, then press F5 to refresh page  
(Using Chrome to handle this is a ideal choice)
* Then, drag the scroll bar to the top and click the first tab, copy 'SUP=xxx;SUB=xxx;' at the right window
* Last, paste it to 'your cookie' at the top of the code (don't delete the quotation mark)
``` python
    HEADER = {'cookie': 'your cookie'}
    URL = ['url']
```

![get_cookie](https://github.com/chauncygrey/weibo_pic_carrier/blob/master/get_cookie.jpg)


#### Caution
For batch carry, input your target users' homepage url **like this** ['url', 'url2', 'url3']

Some errors may occur when open with console.


## Welcome to Fork & Star

#### Contact me
chauncygrey@foxmail.com

#### Follow me at Weibo
[ChauncyGrey's Weibo](http://weibo.com/fancy996 "http://weibo.com/fancy996")


## Needs
* Python 3.5
* Requests, a HTTP library for human beings.
* Lxml, a binding for the libxml2 and libxslt libraries.
* Pillow, The Python Image Library, which provides image processing functionality and supports many file formats.

#### Python
https://www.python.org/

#### Extension package installation
Install with pip:

    $ pip install requests
    $ pip install lxml
    $ pip install pillow
