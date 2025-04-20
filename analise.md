### Descrição da captura do Wireshark

O Wireshark foi iniciado capturando pacotes na interface de loopback.
Aplicando o filtro tcp.port == 65432:
<img src="img/img1.png" alt="..."/>


Identificando o Three-way handshake (SYN, SYN-ACK, ACK)

**SYN**:
<img src="img/img2.png" alt="..."/>


**SYN-ACK**:
<img src="img/img3.png" alt="..."/>


**ACK**:
<img src="img/img4.png" alt="..."/>


**Fechamento de conexão (FIN, ACK)**:
<img src="img/img5.png" alt="..."/>

---

### Problemas identificados no código original e soluções implementadas

| Problema | Solução |
| -------- | ------- |
| Servidor indisponível no início da conexão | Uso de `try`/`except` para capturar ConnectionRefusedError e socket  | Solução |
| Servidor que cai durante a comnunicação |  Detecção da perda de conexão com `if not data` e encerramento automático do cliente com aviso ao usuário  |
|Timeout de resposta do servidor | Adicionado s.settimeout(10), se o servidor não responder, o cliente é encerrado com aviso |
| Falta de validação de comandos do usuário | função `validar_comando()` para validar comandos /nick e /whisper antes de enviar evitando uso incorreto e mensagens quebradas |
| Encerramento | Tratamento de KeyboardInterrupt e exceções genéricas para enviar /quit ao servidor antes de fechar o socket e sair de forma limpa |
| Mensagens vazias sendo enviadas |	Ignoradas com `if not message.strip(): continue`, evitando flood desnecessário no chat |
---
 **(soluções implementadas no código "cliente_chat_melhorado.py")**


###  Resultados dos testes de resiliência

<img src="img/img6.png" alt="..."/>


### Desafios Extra

#### Atividade 1 - Modificar o servidor para registrar o timestamp de cada mensagem recebida e mostrar quanto tempo cada conexão permaneceu ativa.
<img src="img/img7.png" alt="..."/>


#### Atividade 2 - Adicionar um novo comando /whisper <usuário> <mensagem> que envia uma mensagem privada para um usuário específico

Enviando uma mensagem para user_127.0.0.1_39396:

<img src="img/img8.png" alt="..."/>

user_127.0.0.1_39396 recebendo a mensagem:

<img src="img/img9.png" alt="..."/>
