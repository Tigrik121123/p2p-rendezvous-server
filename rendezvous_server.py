import socket
import threading
import json
import os # Импортируем os для получения порта от Render

user_database = {}
lock = threading.Lock()

def handle_client(conn, addr):
    print(f"[НОВОЕ ПОДКЛЮЧЕНИЕ] {addr} подключился.")
    try:
        while True:
            data = conn.recv(1024)
            if not data: break
            request = json.loads(data.decode('utf-8'))
            command = request.get("command")
            payload = request.get("payload")
            response = {"status": "error", "message": "Unknown command"}
            with lock:
                if command == "register":
                    username = payload.get("username")
                    address = payload.get("address")
                    if username and address:
                        user_database[username] = address
                        response = {"status": "ok", "message": f"User {username} registered."}
                        print(f"База данных обновлена: {user_database}")
                elif command == "get_all_users":
                    response = {"status": "ok", "users": user_database}
            conn.send(json.dumps(response).encode('utf-8'))
    except Exception as e: print(f"[ОШИБКА] {e}")
    finally:
        print(f"[ОТКЛЮЧЕНИЕ] {addr} отключился.")
        conn.close()

def start_server():
    host = '0.0.0.0'
    # Render предоставляет порт через переменную окружения PORT
    port = int(os.environ.get('PORT', 9999))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[СТАРТ] Сервер запущен на {host}:{port}")
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()