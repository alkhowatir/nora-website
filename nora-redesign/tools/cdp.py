import socket, os, base64, hashlib, json, struct, urllib.parse

class SimpleWebSocket:
    def __init__(self, ws_url):
        parsed = urllib.parse.urlparse(ws_url)
        self.host = parsed.hostname
        self.port = parsed.port or 80
        self.path = parsed.path
        self.sock = socket.create_connection((self.host, self.port), timeout=10)
        self._handshake()

    def _handshake(self):
        key = base64.b64encode(os.urandom(16)).decode('utf-8')
        req = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode('utf-8'))
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += self.sock.recv(4096)
        if b" 101 " not in resp and b"101 Switching" not in resp and b"101 WebSocket" not in resp:
            raise RuntimeError("WebSocket handshake failed: " + resp.decode('utf-8', errors='ignore'))

    def send(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        payload = data.encode('utf-8')
        length = len(payload)
        mask_key = os.urandom(4)
        header = bytearray([0x81]) # text frame, fin=1
        if length <= 125:
            header.append(0x80 | length)
        elif length <= 65535:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", length))
        header.extend(mask_key)
        masked_payload = bytearray(payload[i] ^ mask_key[i % 4] for i in range(length))
        self.sock.sendall(header + masked_payload)

    def recv(self):
        header = self.sock.recv(2)
        if not header:
            return None
        length = header[1] & 0x7F
        if length == 126:
            length = struct.unpack("!H", self.sock.recv(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self.sock.recv(8))[0]
        payload = b""
        while len(payload) < length:
            chunk = self.sock.recv(length - len(payload))
            if not chunk:
                break
            payload += chunk
        return payload.decode('utf-8', errors='ignore')

    def call(self, method, params=None, msg_id=1):
        msg = {"id": msg_id, "method": method, "params": params or {}}
        self.send(msg)
        while True:
            res = self.recv()
            if not res:
                return None
            data = json.loads(res)
            if data.get("id") == msg_id:
                return data.get("result")
