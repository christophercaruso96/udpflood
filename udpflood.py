#import dei moduli necessari
#socket --> per la gestione delle connessioni di rete
#random --> per la generazione randomica di un pacchetto da 1KB
#ipaddress --> per validare l'ip inserito dall'utente
#time --> per impostare un delay nell'invio dei pacchetti (altrimenti la connessione viene interrotta)
import socket, random, ipaddress, time

#da specifica viene richiesto l'ip e non l'hostname
ip_target = ""
#inizializzata con un valore non valido per il range UDP per validare l'inserimento dell'utente
port_target = 99999
#inizializzato a 0 per controllo inserimento
tot_packets = 0

#funzione per la validazione dell'indirizzo ip inserito
def is_valid_ip(ip_address):
    #se l'ip è valido ritorna True
    try:
        #ip_address riceve in input la stringa dell'ip e se non è valido genera una eccezione
        ipaddress.ip_address(ip_address)
        return True;
    #se entra in exception restituisce false
    except ValueError:
        #chiedo all'utenet di inserire un IP valido
        print("Inserisci una stringa con indirizzo IP valido (e.g. 192.168.1.6) \n")
        return False;

#Input IP target con validazione
while True:
    #input dall'utente per la stringa ip_target
    ip_target = str(input("Inserisci l'indirizzo IP del target:\n"))
    #esce dall'iterazione solo se l'ip è valido (call function is_valid_ip definita in precedenza)
    if (is_valid_ip(ip_target)):
        break

#Input Porta target con validazione
#N.B. Si potrebbe costruire un ciclo iterativo per la verifica delle 
#porte disponibili sull'IP indicato per far scegliere all'utente
while True:
    #medesimo principio dell'input relativo all'ip target
    try:
        port_target = int(input("Inserisci la porta UDP (range: 0-65535) del target:\n"))
    except ValueError:
        print("Inserisci una porta UDP valida nel range 0-65535 \n")
    #esce dall'iterazione solo se viene inserito un intero che rientri nel range UDP
    if(0 <= port_target <= 65535):
        break

#Input Totale pacchetti da inviare
while True:
    #medesimo principio dell'input relativo all'ip target
    try:
        tot_packets = int(input("Inserisci il numero totale di pacchetti che vuoi inviare: \n"))
    except ValueError:
        print("Inserisci un numero intero valido! \n")
    #esce dall'iterazione solo se viene inserito un numero di pacchetti valido > 0
    if( tot_packets > 0):
        break

#istanza dell'oggetto socket
#creazione nuovo socket, AF_INET = IPV4, SOCK_DGRAM = connessione UDP (DGRAM, datagram che usa protocollo UDP)
udp_socket = socket.socket (socket.AF_INET,socket.SOCK_DGRAM)

#try-except per stabilire la connessione con ip e porta target
try:
    #connect riceve come input una tupla indirizzo - porta
    #serve a stabilire la connessione
    udp_socket.connect((ip_target, port_target))
    #stampa in caso di connessione con successo
    print("Connessione stabilita ...\n")
#se si verifica l'errore di timeout stampa un messaggio di errore per l'utente
except TimeoutError:
    print("Impossibile stabilire la connessione!\n")
    #N.B. UNA POSSIBILE MIGLIORIA CONSISTE NELL' INTRODUZIONE DI UN CICLO FINO A QUANDO
    #NON VIENE INSERITO UN TARGET RAGGIUNGIBILE
    #NON LO ABBIAMO MESSO PER NON RENDERE IL CODICE TROPPO COMPLESSO PER LA COMPRENSIONE DEL GRUPPO
#Inizializzazione vuota del package da inviare
package = ""
#iterazione da 1 fino al numero inserito dall'utente (sfruttata la funzione range vista a lezione)
for packet in range(1, tot_packets + 1):
    #generazione pachetto random con funzione randbytes
    #1024 dimensione byte generati randomici 1024 byte = 1KB
    package = random.randbytes(1024)
    #invio del byte object (pacchetto generato) sul target
    udp_socket.sendto(package, (ip_target, port_target))
    #impostato sleep di 2 secondi per mantenere 
    time.sleep(2)

#deallocazione del socket con solo l'uso di socket.close
#possibile solo se c'è solo un thread sul socket altrimenti antrebbe va messo a monte socket.shutdown()
#socket.SHUT_RDWR - sia invio e ricezione disallowed
#introdotto nel caso di più thread attivi sul socket
udp_socket.shutdown(socket.SHUT_RDWR)
udp_socket.close()