# Import socket module 
import socket

def Main():
    # local host IP '127.0.0.1' 
    host = '127.0.0.1'

    # Define the port on which you want to connect 
    port = 12346

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # connect to server on local computer 
    s.connect((host,port))
    print('Connected')
    s.send(b'Login')
    data = s.recv(1024)
    print('Received from the server :',str(data.decode('ascii')))
    while True:
        ans = input('Enter your message:')

        # message sent to server 
        s.send(ans.encode('ascii'))

        # messaga received from server 
        data = s.recv(1024)

        # print the received message 
        # here it would be a reverse of sent message 
        print('Received from the server :',str(data.decode('ascii')))

        if ans == '@EXIT':
            break

        # ask the client whether he wants to continue 
    # close the connection 
    s.close()

if __name__ == '__main__':
	Main()

