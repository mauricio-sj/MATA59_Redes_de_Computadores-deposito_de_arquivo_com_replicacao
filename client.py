import socket
import storage  # Módulo com funções comuns
import pickle
import os
import sys

# Este módulo representa um cliente que se comunica com um servidor em um sistema de armazenamento distribuído.
# Ele recebe comandos da linha de comando para realizar operações como depósito, recuperação ou edição de arquivos.

# Tamanho do buffer para receber dados
BUFFER_SIZE = 1024

# Dicionário de operações disponíveis
operacoes = {
    1: 'deposito',
    2: 'recuperacao',
    3: 'edicao'
}

print("Escolha a operação:")
print("1. Depósito")
print("2. Recuperação")
print("3. Edição")

# Obtém a escolha do usuário
try:
    escolha = int(input("Digite o número correspondente à operação desejada: "))
    if escolha not in operacoes:
        print("Escolha inválida. Por favor, selecione um número de 1 a 3.")
        exit()

    operacao = operacoes[escolha]
    file_name = input("Digite o nome do arquivo: ")
    
    # Se a operação não for 'recuperacao', pede a tolerância
    tolerancia = 0 if operacao == 'recuperacao' else int(input("Digite a tolerância: "))

except ValueError:
    print("Entrada inválida. Por favor, insira um número.")
    exit()

# Cria um dicionário com os dados da operação
data = {'operacao': operacao,
        'tolerancia': tolerancia,
        'file_name': file_name}

# Se a operação for 'deposito', obtém o arquivo e o adiciona aos dados
if data['operacao'] == 'deposito':
    file = storage.get_file(file_name)  # Obtém o conteúdo do arquivo
    data['file'] = file

# Serializa os dados para envio
data = pickle.dumps(data)

# Estabelece conexão com o servidor e envia os dados serializados
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), storage.MAIN_PORT))  # Conecta-se ao servidor na porta principal
s.send(data)  # Envia os dados serializados

# Recebe a resposta do servidor
full_msg = b''
while True:
    msg = s.recv(BUFFER_SIZE)
    full_msg += msg
    if len(msg) < BUFFER_SIZE:
        print('Mensagem recebida')
        break

# Desserializa os dados recebidos
data_rcvd = pickle.loads(full_msg)

# Verifica se há erros na resposta
if 'error' in data_rcvd:
    print(data_rcvd['error'])
    exit()

# Exibe mensagens de sucesso ou outras mensagens retornadas pelo servidor
if 'message' in data_rcvd:
    print(data_rcvd['message'])

# Salva o arquivo recebido na pasta 'client' se existir na resposta do servidor
if 'file' in data_rcvd:
    file_name = os.path.join('client', file_name)
    storage.save_file('client', file_name, data_rcvd['file'])
    print('Arquivo salvo na pasta "client"')
