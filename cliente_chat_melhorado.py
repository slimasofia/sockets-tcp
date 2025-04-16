# ATIVIDADE 3 - ANÁLISE E RESOLUÇÃO DE PROBLEMAS
# Parte 2: Implementação de Tratamento de Erros

import socket
import threading
import sys
import time

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 65433
BUFFER_SIZE = 1024
TIMEOUT = 10  # Tempo máximo de espera por resposta do servidor (em segundos)

def receive_messages(sock):
    """Função para receber mensagens do servidor em uma thread separada"""
    while True:
        try:
            # Espera por uma mensagem do servidor
            data = sock.recv(BUFFER_SIZE)
            if not data:
                # Caso a conexão seja fechada pelo servidor
                print("\n[!] Conexão com o servidor foi encerrada.")
                sock.close()
                sys.exit(1)
            print(data.decode('utf-8'), end='')
        except socket.timeout:
            # Caso o servidor demore demais para responder
            print("\n[!] Timeout: servidor não respondeu.")
            sock.close()
            sys.exit(1)
        except Exception as e:
            # Qualquer outro erro na recepção da mensagem
            print(f"\n[!] Erro ao receber mensagem: {e}")
            sock.close()
            sys.exit(1)

def validar_comando(mensagem):
    # Valida comandos antes de enviá-los para o servidor
    # Valida formato do /nick
    if mensagem.startswith('/nick') and len(mensagem.strip().split()) != 2:
        print("[!] Uso correto: /nick <novo_nome>")
        return False
    # Valida formato do /whisper
    if mensagem.startswith('/whisper'):
        partes = mensagem.strip().split(' ', 2)
        if len(partes) < 3:
            print("[!] formato correto: /whisper <usuário> <mensagem>")
            return False
    return True

def main():
    try:
        # Criação do socket TCP/IP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(TIMEOUT)  # Define um tempo limite para operações de rede

        try:
            s.connect((HOST, PORT))
        except (ConnectionRefusedError, socket.timeout):
            # Caso o servidor esteja offline ou demore demais
            print("Não foi possível conectar ao servidor. Ele está indisponível.")
            return

        print(f"Conectado ao servidor de chat em {HOST}:{PORT}")

        # Inicia uma thread para escutar mensagens do servidor
        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        receive_thread.daemon = True
        receive_thread.start()

        # Loop principal de envio de mensagens
        while True:
            try:
                message = input()

                # Ignora mensagens vazias
                if not message.strip():
                    continue

                # Valida comandos como /nick e /whisper
                if not validar_comando(message):
                    continue

                # Envia mensagem para o servidor
                s.send(message.encode('utf-8'))

                # Sai do loop se o comando for /quit
                if message == '/quit':
                    print("Saindo do chat...")
                    break

            except KeyboardInterrupt:
                # Trata Ctrl+C para encerrar o cliente de forma limpa
                print("\nEncerrando cliente...")
                try:
                    s.send('/quit'.encode('utf-8'))
                except:
                    pass
                break
            except Exception as e:
                # Qualquer erro ao enviar mensagem
                print(f"Erro ao enviar mensagem: {e}")
                break

        # Fecha o socket no fim da aplicação
        s.close()

    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()