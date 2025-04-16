## Atividade 3: Análise e Resolução de Problemas
### Parte 1: Identificação de Problemas


#### 1. Tratamento inadequado de desconexões
Se o cliente se desconectar inesperadamente (por exemplo, fechando o terminal), o servidor tenta detectar isso com recv() e remove o cliente. No entanto, esse tratamento está muito genérico e silencioso, usando apenas except: sem verificar o tipo de exceção.

#### 2. Ausência de confirmação de entrega de mensagens
O servidor envia mensagens, mas o cliente apenas as imprime, não há nenhuma confirmação de que a mensagem foi realmente recebida, exibida corretamente ou até mesmo processada.

#### 3. Falha no gerenciamento de recursos
O servidor cria uma nova thread por cliente, sem controle sobre quantas estão ativas.
Se muitos clientes conectarem (mesmo que só por 1 segundo), você pode ter 100+ threads zumbis.


