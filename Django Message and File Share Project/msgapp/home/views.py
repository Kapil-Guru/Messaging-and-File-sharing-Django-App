from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import os
import socket
import tqdm
import mimetypes
# Create your views here.

class SearchView(View):
    def get(self, request):
        # Gte list of phone numbers
        return render(request, 'home/search.html', {})

    def post(self,request):
        receiver_phone_number = request.POST['receiver_phone_number']
        request.session['receiver_phone_number'] = receiver_phone_number
        if int(request.session['phone_number']) < int(receiver_phone_number):
            table_name = request.session['phone_number'] + "_" + receiver_phone_number
        else:
            table_name = receiver_phone_number + "_" + request.session['phone_number']
        table_name = 'msgs/'+table_name
        request.session['table_name'] = table_name
        print(table_name)
        url = reverse('home:chat')
        return redirect(url)

class ChatView(View):
    def get(self, request):
        if int(request.session['phone_number']) < int(request.session['receiver_phone_number']):
            table_name = request.session['phone_number'] + "_" + request.session['receiver_phone_number']
        else:
            table_name = request.session['receiver_phone_number'] + "_" + request.session['phone_number']

        request.session['table-name'] = table_name

        ctx = {
        'table_name': request.session['table_name'],
        'phone_number': request.session['phone_number'],
        'receiver_phone_number': request.session['receiver_phone_number'],
        }
        return render(request, 'home/chat.html', ctx)
    def post(self, request):
        #for files
        table_name = request.session['table-name']
        file = request.FILES['file']
        fs = FileSystemStorage()
        direc_location = 'media/' + table_name + '/sent'
        if not os.path.exists(direc_location):
            os.makedirs(direc_location)
        
        saved_location = fs.save(table_name+'/sent/'+file.name, file)
        uploaded_file_location = 'media/' + saved_location

        filename = file.name

        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        host = "27.5.211.221"
        # the port, let's use 5001
        port = 8000
        # the name of file we want to send, make sure it exists
        # get the file size

        s = socket.socket()

        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")

        s.send(f"0{SEPARATOR}{table_name}{SEPARATOR}{filename}".encode())

        with open(uploaded_file_location, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)

        # close the socket
            s.close()
        os.remove(uploaded_file_location)
        request.session['file_name'] = filename

        return redirect(reverse('home:filesend'))

class DownloadView(View):
    def get(self, request):
        file_name = request.GET['file']
        table_name = request.session['table-name']

        direc_storage = 'media/'+table_name +'/receive'

        if not os.path.exists(direc_storage):
            os.makedirs(direc_storage)
        
        file_storage_location = 'media/'+table_name+'/receive/'+file_name

        if not os.path.exists(file_storage_location):

            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096 # send 4096 bytes each time step

            host = "27.5.211.221"
            # the port, let's use 5001
            port = 8000
            # the name of file we want to send, make sure it exists
            # get the file size

            s = socket.socket()

            print(f"[+] Connecting to {host}:{port}")
            s.connect((host, port))
            print("[+] Connected.")


            s.send(f"1{SEPARATOR}{table_name}{SEPARATOR}{file_name}".encode())

            with open(file_storage_location, "wb") as f:
                while True:
                    # read 1024 bytes from the socket (receive)
                    bytes_read = s.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        # nothing is received
                        # file transmitting is done
                        break
                    # write to the file the bytes we just received
                    f.write(bytes_read)

            # close the client socket
            s.close()

        fd = open(file_storage_location, 'rb')

        mime_type, _ = mimetypes.guess_type(file_storage_location)
        # Set the return value of the HttpResponse
        response = HttpResponse(fd, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % file_name
        # Return the response value
        return response

class FileSendView(View):
    def get(self, request):
        ctx = {
            'file_name': request.session['file_name'],
            'table_name': request.session['table_name'],
            'sender_phone_number': request.session['phone_number'],
        }
        return render(request, 'home/file.html', ctx)