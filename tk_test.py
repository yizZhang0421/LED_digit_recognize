import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import io
def get_tk_image(mat):
    mat=cv2.resize(mat, (round((700*mat.shape[1])/mat.shape[0]), 700), interpolation=cv2.INTER_CUBIC)
    img_encode = cv2.imencode('.jpg', mat)[1]
    data_encode = np.array(img_encode)
    str_encode = data_encode.tostring()
    return io.BytesIO(str_encode)
window = tk.Tk()
window.title("haha")
window.geometry("700x700+10+10")
window.configure(background='grey')
import cv2
img=cv2.imread('66274.jpg')
tk_img=ImageTk.PhotoImage(Image.open(get_tk_image(img)))
panel = tk.Label(window, image = tk_img)
panel.pack(anchor = "center", fill = "both", expand = "yes")
window.mainloop()