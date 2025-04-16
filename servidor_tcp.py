import socket
from datetime import datetime

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço de loopback (localhost)
PORT = 65432        # Porta para escutar (não privilegiada)

try:
    # Criação do socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Associa o socket ao endereço e porta
        s.bind((HOST, PORT))
        # Habilita o socket para aceitar conexões, com fila de até 5 conexões
        s.listen(5)
        print(f"Servidor escutando em {HOST}:{PORT}")

        # Loop para aceitar conexões
        while True:
            # Espera por uma conexão
            conn, addr = s.accept()
            with conn:
                inicio_conexao = datetime.now()
                print(f"\nConectado por {addr} em {inicio_conexao.strftime('%Y-%m-%d %H:%M:%S')}")

                # Loop para receber dados
                while True:
                    data = conn.recv(1024)
                    if not data:
                        # Se não receber dados, encerra a conexão
                        break
                    timestamp = datetime.now()
                    print(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] Recebido de {addr}: {data.decode('utf-8')}")
                    # Envia resposta ao cliente
                    conn.sendall(f"Eco: {data.decode('utf-8')}".encode('utf-8'))

                fim_conexao = datetime.now()
                duracao = fim_conexao - inicio_conexao
                print(f"Conexão com {addr} encerrada às {fim_conexao.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"Duração da conexão: {duracao}")
except KeyboardInterrupt:
    print("\nServidor encerrado pelo usuário")
except Exception as e:
    print(f"Erro: {e}")


    