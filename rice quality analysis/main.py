import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tm

fontScale = 1
fontColor = (0, 0, 0)
cond = 0


bgcolor = "#E1FCFB"
bgcolor1 = "#B7C526"
fgcolor = "black"

window = tk.Tk()
window.title("Harish")

window.geometry('1280x720')
window.configure()
# window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

lbl = tk.Label(window, text="Select Dataset", width=20, height=2, fg=fgcolor, font=('times', 15, ' bold '))
lbl.place(x=10, y=100)

txt = tk.Entry(window, width=20, bg="white", fg="black", font=('times', 15, ' bold '))
txt.place(x=200, y=110)



def clear():
    txt.delete(0, 'end')
    res = ""



def browse():
    path = filedialog.askopenfilename()
    print(path)
    txt.insert('end', path)
    if path != "":
        print(path)
    else:
        tm.showinfo("Input error", "Select Dataset")
def process():
    image_data= txt.get()
    print("sunil")
    import cv2
    import numpy as np
    from matplotlib import pyplot as plt

    def get_classificaton(ratio):
        ratio = round(ratio, 1)
        toret = ""
        if (ratio >= 3):
            toret = "Slender"
        elif (ratio >= 2.1 and ratio < 3):
            toret = "Medium"
        elif (ratio >= 1.1 and ratio < 2.1):
            toret = "Bold"
        elif (ratio <= 1):
            toret = "Round"
        toret = "(" + toret + ")"
        return toret

    # rnjn
    print("Starting")
    img = cv2.imread(image_data, 0)  # load in greyscale mode

    # convert into binary
    ret, binary = cv2.threshold(img, 160, 255,
                                cv2.THRESH_BINARY)  # 160 - threshold, 255 - value to assign, THRESH_BINARY_INV - Inverse binary

    # averaging filter
    kernel = np.ones((5, 5), np.float32) / 9
    dst = cv2.filter2D(binary, -1, kernel)  # -1 : depth of the destination image

    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # erosion
    erosion = cv2.erode(dst, kernel2, iterations=1)

    # dilation
    dilation = cv2.dilate(erosion, kernel2, iterations=1)

    # edge detection
    edges = cv2.Canny(dilation, 100, 200)

    ### Size detection
    _, contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print("No. of rice grains=", len(contours))
    total_ar = 0
    ar_1 = []
    ar_2 = []
    ar_3 = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        if (aspect_ratio < 1):
            aspect_ratio = 1 / aspect_ratio
        print(round(aspect_ratio, 2), get_classificaton(aspect_ratio))
        ar_1.append(round(aspect_ratio, 2))
        ar_2.append(get_classificaton(aspect_ratio))
        total_ar += aspect_ratio
    avg_ar = total_ar / len(contours)
    ar_3 = list(zip(ar_1, ar_2))
    print(ar_3)

    for items in ar_3:
        mylistbox.insert("end", items)
    print("Average Aspect Ratio=", round(avg_ar, 2), get_classificaton(avg_ar))
    '''av1 = []
    av2 = []
    av1.append(round(avg_ar, 2))
    av2.append(get_classificaton(avg_ar))
    avg_final = list(zip(av1, av2))
    print(avg_final)
    label2['text'] = avg_final'''

    # plot the images
    imgs_row = 2
    imgs_col = 3
    plt.subplot(imgs_row, imgs_col, 1), plt.imshow(img, 'gray')
    plt.title("Original image")

    plt.subplot(imgs_row, imgs_col, 2), plt.imshow(binary, 'gray')
    plt.title("Binary image")

    plt.subplot(imgs_row, imgs_col, 3), plt.imshow(dst, 'gray')
    plt.title("Filtered image")

    plt.subplot(imgs_row, imgs_col, 4), plt.imshow(erosion, 'gray')
    plt.title("Eroded image")

    plt.subplot(imgs_row, imgs_col, 5), plt.imshow(dilation, 'gray')
    plt.title("Dialated image")

    plt.subplot(imgs_row, imgs_col, 6), plt.imshow(edges, 'gray')
    plt.title("Edge detect")

    plt.show()

def take_photo():
    import tkinter as tk
    from tkinter import filedialog
    import tkinter.messagebox as tm

    fontScale = 1
    fontColor = (0, 0, 0)
    cond = 0

    bgcolor = "#E1FCFB"
    bgcolor1 = "#B7C526"
    fgcolor = "black"

    window1 = tk.Tk()
    window1.title("Harish")

    window1.geometry('1280x720')
    window1.configure()
    # window1.attributes('-fullscreen', True)

    window1.grid_rowconfigure(0, weight=1)
    window1.grid_columnconfigure(0, weight=1)

    lbl = tk.Label(window1, text="Select Dataset", width=20, height=2, fg=fgcolor, font=('times', 15, ' bold '))
    lbl.place(x=10, y=100)

    def Camera():
        print("second module")
        import cv2
        key = cv2.waitKey(1)
        webcam = cv2.VideoCapture(0)
        while True:
            try:
                check, frame = webcam.read()
                print(check)  # prints true as long as the webcam is running
                print(frame)  # prints matrix values of each framecd
                cv2.imshow("Capturing", frame)
                key = cv2.waitKey(1)
                if key == ord('s'):
                    cv2.imwrite(filename='saved_img.jpg', img=frame)
                    webcam.release()
                    img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
                    img_new = cv2.imshow("Captured Image", img_new)
                    cv2.waitKey(1650)
                    cv2.destroyAllWindows()
                    print("Processing image...")
                    img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
                    print("Converting RGB image to grayscale...")
                    gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                    print("Converted RGB image to grayscale...")
                    print("Resizing image to 28x28 scale...")
                    img_ = cv2.resize(gray, (377, 244))
                    print("Resized...")
                    img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
                    print("Image saved!")

                    break
                elif key == ord('q'):
                    print("Turning off camera.")
                    webcam.release()
                    print("Camera off.")
                    print("Program ended.")
                    cv2.destroyAllWindows()
                    break

            except(KeyboardInterrupt):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break
    Btn_Camera = tk.Button(window1, text="take_photo", command=Camera, width=18, height=1,
                               activebackground="Red", font=('times', 15, ' bold '))
    Btn_Camera.place(x=420, y=200)

    window1.mainloop()







def Email():
    import tkinter as tk
    from tkinter import filedialog
    import tkinter.messagebox as tm

    fontScale = 1
    fontColor = (0, 0, 0)
    cond = 0

    bgcolor = "#E1FCFB"
    bgcolor1 = "#B7C526"
    fgcolor = "black"

    window2 = tk.Tk()
    window2.title("Harish")

    window2.geometry('1280x720')
    window2.configure()
    # window1.attributes('-fullscreen', True)

    window2.grid_rowconfigure(0, weight=1)
    window2.grid_columnconfigure(0, weight=1)

    lbl = tk.Label(window2, text="Select Dataset", width=20, height=2, fg=fgcolor, font=('times', 15, ' bold '))
    lbl.place(x=10, y=100)

    def email1():
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders
        mail_content = '''Hello,
        This is a test mail.
        In this mail we are sending some attachments.
        The mail is sent using Python SMTP library.
        Thank You
        '''
        # The mail addresses and password
        sender_address = 'harishg069@gmail.com'
        sender_pass = 'h9972735125'
        receiver_address = 'ghari9071@gmail.com'
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'A test mail sent by Python. It has an attachment.'
        # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        attach_file_name = 'project-report.pdf'
        attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload)  # encode the attachment
        # add payload header with filename
        payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
        message.attach(payload)
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')

    email = tk.Button(window2, text="email", command=email1, width=18, height=1,
                           activebackground="Red", font=('times', 15, ' bold '))
    email.place(x=420, y=200)

    window2.mainloop()







clearButton = tk.Button(window, text="Clear", command=clear, fg=fgcolor, width=15, height=1,
                        activebackground="Red", font=('times', 15, ' bold '))
clearButton.place(x=650, y=100)

browse = tk.Button(window, text="Browse", command=browse, fg=fgcolor, width=15, height=1,
                   activebackground="Red", font=('times', 15, ' bold '))
browse.place(x=420, y=100)

quitWindow = tk.Button(window, text="QUIT", command=window.destroy, fg=fgcolor, width=15, height=1,
                       activebackground="Red", font=('times', 15, ' bold '))
quitWindow.place(x=900, y=100)

process = tk.Button(window, text="process", command=process ,width=18  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
process.place(x=650, y=200)

take_photo = tk.Button(window, text="take_photo", command=take_photo ,width=18  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
take_photo.place(x=420, y=200)

email = tk.Button(window, text="Email", command=Email ,width=18  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
email.place(x=900, y=200)

mylistbox = tk.Listbox(window,width=60, height=10)
mylistbox.place(x=50,y=400)

label1 = tk.Label(window, text="Avg aspect ratio = ")
label1.place(x=500, y=500)

label2 = tk.Label(window,text = "avg aspect ")
label2.place(x=800, y=500)
window.mainloop()
