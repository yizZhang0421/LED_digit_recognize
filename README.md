# LED_digit_recognize
辨識影像中LED螢幕中數字為多少

<h3>作法</h3>

![image](https://github.com/yizZhang0421/LED_digit_recognize/raw/master/readme_image/origin.jpg)
根據設備特徵切出螢幕部分。</br>
</br>
![image](https://github.com/yizZhang0421/LED_digit_recognize/raw/master/readme_image/denoise.jpg)
辨識前的去噪，調整亮度、二值化、腐蝕、膨脹等等。</br>
</br>
![image](https://github.com/yizZhang0421/LED_digit_recognize/raw/master/readme_image/2.jpg)
![image](https://github.com/yizZhang0421/LED_digit_recognize/raw/master/readme_image/6.jpg)
![image](https://github.com/yizZhang0421/LED_digit_recognize/raw/master/readme_image/9.jpg)
抓出輪廓並根據其像素判斷出數字。</br>
</br>
![image](https://github.com/yizZhang0421/LED_digit_recognize/raw/master/readme_image/finish.jpg)
最終結果再做一些段落分析和字串處理就可以得到結果。</br>
</br>
