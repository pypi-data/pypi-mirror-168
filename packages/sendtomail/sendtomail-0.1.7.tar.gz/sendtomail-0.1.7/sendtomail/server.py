import socket, urllib3, json
global debug
debug = "off"

class server:
    def send(region:str, email:str, *message:str):
        if debug == "on":
            print("[3%] Debug mode ON")
            print("[7%] Region "+region)
            print("[11%] Starting to get URL")
            print("[20%] Getting json from URL")
        url = "https://raw.githubusercontent.com/mishakorzik/mishakorzik.menu.io/master/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80/https.json"
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        data = json.loads(request.data.decode('utf8'))
        if debug == "on":
            print("[40%] URL json data decode")
        ip = str(data["mailip"])
        port = int(data["mailport"])
        if debug == "on":
            print("[60%] Server IP "+ip)
        message = " ".join([str(m) for m in message])
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        if debug == "on":
            print("[80%] Server connected!")
        client.sendall(bytes("smtp|"+region+"|"+email+"|"+message,'UTF-8'))
        if debug == "on":
            print("[98%] Data send to server")
        code = client.recv(4096)
        code = code.decode('utf-8')
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        return code
    def mail():
        if debug == "on":
            print("[7%] Debug mode ON")
            print("[11%] Starting to get URL")
            print("[20%] Getting json from URL")
        url = "https://raw.githubusercontent.com/mishakorzik/mishakorzik.menu.io/master/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80/https.json"
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        data = json.loads(request.data.decode('utf8'))
        if debug == "on":
            print("[40%] URL json data decode")
        ip = str(data["mailip"])
        port = int(data["mailport"])
        if debug == "on":
            print("[60%] Server IP "+ip)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        if debug == "on":
            print("[80%] Server connected!")
        client.sendall(bytes("get|free|mail|account",'UTF-8'))
        if debug == "on":
            print("[98%] Data send to server")
        free = client.recv(4096)
        free = free.decode('utf-8')
        free = json.loads(free)
        client.shutdown(socket.SHUT_RDWR)
        client.close()
        return free
    def regions():
        return "SMTP regions: tr, ru, ua, us, uk, de, fr, it"
    def debug(type:str):
        global debug
        if type == "on":
            debug = "on"
        else:
            debug = "off"
