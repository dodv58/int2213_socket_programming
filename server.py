# import socket programming library 
import socket, os

# import thread module 
from _thread import *
import threading

online_users = []
user_sock = {}
file_dir = '/Users/dodang/workspace/uet/int2213/programming_excercise'

def login(user_id, msg):
    try:
        user = msg.split(' ')[1].strip()
        if len(user) <= 0:
            return b'Wrong format!!!', user_id
        if not user_id and user not in online_users:
            online_users.append(user)
            return b'You are logged in! Send #Help to get guidance.', user
        if not user_id and user in online_users:
            return b'User already logged in!!!', user_id
        if user_id and user_id == user:
            return b'You already logged in!!!', user_id
        if user_id and user_id != user:
            return b'Please Logout first', user_id
        return '', None
    except:
        return b'Wrong format!!!', user_id

def send_msg(user_id, msg):
    try:
        receiver = msg.split(' ')[1]
        if receiver not in online_users:
            return 'Receiver is not online'
        else:
            message = 'Message from {}: {}'.format(user_id, ' '.join(msg.split(' ')[2:]))
            user_sock[receiver].send(message.encode())
            return 'Message sent'
    except Exception as e:
        print(e)
        pass

def remove_user(user_id):
    try:
        online_users.remove(user_id)
        user_sock.pop(user_id, None)
    except:
        pass

def download(user_id, msg):
    try:
        conn = user_sock[user_id]
        file_path = file_dir + '/' + msg.split(' ')[1]
        if not os.path.isfile(file_path):
            conn.send(b'File does not exist')
        else:
            print('filesize: {}'.format(os.path.getsize(file_path)))
            conn.send(str(os.path.getsize(file_path)).encode())
            with open(file_path, 'rb') as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    conn.sendall(bytes_read)
    except Exception as e:
        print(e)
        pass



def handle_message(user_id, msg):
    if msg == '#EXIT':
        remove_user(user_id)
        return None
    elif msg == '#Help':
        return b'''
- Please login by sending message: #Login <student_id>
After logged in, please wait for incomming message from server.
- If you are logged in, please choose:
1. Get list active users: #list_users
2. Send message to another user: #msg <receiver_id> <message>
3. List files: #list_files
4. Download file: #download <file_name>
    If file is valid, server will send a message contain file size to client first.
    After that, server will send each 1024-byte file data until the end of the file.
5. Help: #Help
6. Exit: #EXIT
'''
    else:
        if not user_id:
            return b'You are not logged in, send #Help to get guidance'
        if msg == '#list_users':
            res = str(online_users)
        elif msg.startswith('#msg'):
            res = send_msg(user_id, msg)
        elif msg.startswith('#list_files'):
            res = ''
            for f in os.listdir(file_dir):
                if os.path.isfile(f):
                    res += "{}\n".format(f)
        elif msg.startswith('#download'):
            download(user_id, msg)
            res = 'Done'
        else:
            res = 'Send #Help to get guidance'
        return res.encode()

# thread function 
def threaded(c):
    user_id = None
    while True:
        # data received from client 
        data = c.recv(1024)
        if not data:
            c.send(b'No data provided, bye!')
            remove_user(user_id)
            print('Close connection')
            # lock released on exit 
            #print_lock.release()
            break

        data = data.decode().strip()
        if data.startswith('#Login'):
            response, user_id = login(user_id, data)
            if user_id:
                user_sock[user_id] = c
        else:
            response = handle_message(user_id, data)
        if not response:
            c.send(b'Bye')
            break

        # send back reversed string to client 
        c.send(response)

    # connection closed 
    c.close()


def Main():
	host = ""

	# reverse a port on your computer 
	# in our case it is 12345 but it 
	# can be anything 
	port = 12346
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("socket binded to port", port)

	# put the socket into listening mode 
	s.listen(5)
	print("socket is listening")

	# a forever loop until client wants to exit 
	while True:

		# establish connection with client 
		c, addr = s.accept()

		# lock acquired by client 
		#print_lock.acquire()
		print('Connected to :', addr[0], ':', addr[1])

		# Start a new thread and return its identifier 
		start_new_thread(threaded, (c,))
	s.close()


if __name__ == '__main__':
	Main()

