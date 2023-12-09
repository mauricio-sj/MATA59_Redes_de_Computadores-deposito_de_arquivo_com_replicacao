import socket
import storage  # Importação de um módulo "storage", que parece ser próprio
import pickle
import os
import sys
import pandas as pd
import numpy as np


# Esse módulo implementa um sistema distribuído de armazenamento de arquivos entre vários servidores. 
# o código lida com a distribuição de arquivos entre diferentes servidores e garante que haja redundância suficiente para tolerar falhas em alguns desses servidores. 
# Isso pode ser útil em sistemas distribuídos para garantir a disponibilidade e integridade dos dados.

BUFFER_SIZE = 1000  # Definição do tamanho do buffer para leitura de dados
SERVER_PORTS = [3001, 3002, 3003, 1238, 1239]  # Lista de portas de servidores


# Função para excluir um arquivo do servidor e da tabela de arquivos
def delete_file(port, file_name):
    # Obtém a tabela de arquivos
    df = get_table()
    # Verifica se o arquivo está na tabela
    file_in_table = check_file_in_table(df, file_name)
    print(file_in_table)
    # Obtém a coluna correspondente ao servidor que possui o arquivo
    column = file_in_table.columns[(file_in_table == port).iloc[0]].values[0]
    print(column)
    # Obtém o índice da linha onde está o arquivo na tabela
    row_index = file_in_table.index.values.astype(int)[0]
    # Marca o valor como nulo (nan) na tabela
    df.loc[row_index, column] = np.nan
    df.to_csv('tabela.csv', index=False)  # Atualiza o arquivo CSV da tabela
    file = os.path.join('server', f'port_{port}', file_name)  # Obtém o caminho do arquivo
    os.remove(file)  # Remove o arquivo do servidor


# Verifica se o arquivo está na tabela
def check_file_in_table(df, file_name):
    return df[df['file_name'] == file_name]


# Obtém os endereços dos servidores que possuem o arquivo
def file_adresses(df):
    df.dropna(axis=1)  # Remove colunas com valores nulos (na)
    servers_to_search_file = df.drop(axis=1, columns=['file_name'])  # Remove a coluna de nomes de arquivo
    servers_to_search_file = servers_to_search_file.values[0]  # Obtém os valores da linha como array
    return servers_to_search_file


# Envia uma solicitação para um servidor específico para obter um arquivo
def request_file(s, port, data):
    new_socket = connect_to_server(port)  # Conecta-se ao servidor específico
    new_socket.send(pickle.dumps(data))  # Envia os dados serializados
    full_msg = b''
    while True:
        msg = new_socket.recv(BUFFER_SIZE)  # Recebe os dados do servidor
        full_msg += msg
        if len(msg) < BUFFER_SIZE:
            break

    return pickle.loads(full_msg)  # Retorna os dados deserializados


# Conecta-se a um servidor específico
def connect_to_server(port):
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um novo socket
    new_socket.connect((socket.gethostname(), port))  # Conecta-se ao servidor na porta específica
    return new_socket


# Obtém a tabela de arquivos
def get_table():
    if not os.path.exists('tabela.csv'):  # Verifica se o arquivo da tabela existe
        df = pd.DataFrame(columns=['file_name', 'server_1', 'server_2',
                                   'server_3', 'server_4', 'server_5'])  # Cria um DataFrame vazio
        return df
    return pd.read_csv('tabela.csv')  # Retorna a tabela se o arquivo existir


def handle_deposito(data, s):
    # Verifica se a conexão é feita pela porta principal
    if s.getsockname()[1] == storage.MAIN_PORT:
        df = get_table()  # Obtém a tabela de arquivos
        file_in_table = check_file_in_table(df, data['file_name'])  # Verifica se o arquivo está na tabela
        file_in_table = file_in_table.dropna(axis=1)  # Remove colunas com valores nulos (na)
        file_in_table = file_in_table.drop(axis=1, columns=['file_name'])  # Remove a coluna de nomes de arquivo
        try:
            servers_to_search_file = file_in_table.values[0]  # Obtém os servidores que possuem o arquivo
        except:
            servers_to_search_file = []

        # Identifica os servidores onde o arquivo ainda não está armazenado
        servers_to_save_file = list(set(SERVER_PORTS) - set(servers_to_search_file))

        index = 0
        saves = 0
        while saves < int(data['tolerancia']):
            try:
                # Conecta-se aos servidores para salvar cópias do arquivo
                new_socket = connect_to_server(servers_to_save_file[index])
                new_socket.send(pickle.dumps(data))  # Envia os dados do arquivo
                saves += 1
                index += 1
            except:
                index += 1

                # Verifica se excedeu o número de servidores
                if (index > len(servers_to_save_file)):
                    return {'error': 'falha na comunicação entre os servidores'}
                continue

            print(f'cópia {saves} salva')

            # Atualiza a tabela com o servidor onde o arquivo foi salvo
            file_in_table = check_file_in_table(df, data['file_name'])
            if not file_in_table.empty:
                row_index = file_in_table.index.values.astype(int)[0]
                empty_column = file_in_table.columns[file_in_table.isna().any()].tolist()[0]
                df.loc[row_index, empty_column] = str(servers_to_save_file[index - 1])
            else:
                # Adiciona uma nova linha na tabela para o arquivo salvo
                new_row = [data['file_name'], str(servers_to_save_file[index - 1]),
                           np.nan, np.nan, np.nan, np.nan]
                df.loc[len(df)] = new_row
        df.to_csv('tabela.csv', index=False)  # Salva a tabela atualizada

    else:
        # Caso contrário, salva o arquivo no servidor
        folder = os.path.join("server", f'port_{s.getsockname()[1]}')
        file_name = os.path.join(folder, data['file_name'])
        storage.save_file(folder, file_name, data['file'])

    return {}


def handle_recuperacao(data, s):
    df = get_table()  # Obtém a tabela de arquivos
    file_in_table = check_file_in_table(df, data['file_name'])  # Verifica se o arquivo está na tabela
    if file_in_table.empty:
        return {'error': 'Arquivo não encontrado no servidor'}

    # Se a conexão é feita pela porta principal
    if s.getsockname()[1] == storage.MAIN_PORT:
        file_in_table = file_in_table.dropna(axis=1)  # Remove colunas com valores nulos (na)
        file_in_table = file_in_table.drop(axis=1, columns=['file_name'])  # Remove a coluna de nomes de arquivo
        servers_to_search_file = file_in_table.values[0]  # Obtém os servidores que possuem o arquivo

        # Solicita o arquivo aos servidores onde ele está armazenado
        for server in servers_to_search_file:
            try:
                file = request_file(s, int(server), data)  # Solicita o arquivo ao servidor específico
                if 'file' in file:
                    return file
            except:
                pass
        return {'error': 'arquivo não encontrado'}
    else:
        # Se a conexão não for pela porta principal, recupera o arquivo do servidor atual
        try:
            file_name = os.path.join('server', f'port_{s.getsockname()[1]}', data['file_name'])
            file = storage.get_file(file_name)  # Obtém o arquivo do servidor
            return {'file': file}
        except:
            print('arquivo não encontrado')
            return {'error': 'arquivo não encontrado'}


def handle_edicao(data, s):
    if s.getsockname()[1] == storage.MAIN_PORT:  # Verifica se a conexão é feita pela porta principal
        df = get_table()
        file_in_table = check_file_in_table(df, data['file_name'])
        if file_in_table.empty:
            return {'error': 'arquivo não encontrado'}

        # Obtenção dos servidores que possuem o arquivo
        file_in_table = file_in_table.dropna(axis=1)
        file_in_table = file_in_table.drop(axis=1, columns=['file_name'])
        servers_to_search_file = file_in_table.values[0]

        # Verifica a quantidade de servidores onde o arquivo está armazenado
        if len(servers_to_search_file) == data['tolerancia']:
            return {'message': 'success'}

        # Caso haja mais servidores do que o necessário, deleta de alguns
        if len(servers_to_search_file) > data['tolerancia']:
            print('deletar de alguns servidores')
            delete_n_times = len(servers_to_search_file) - data['tolerancia']
            for n in range(delete_n_times):
                new_socket = connect_to_server(servers_to_search_file[n])
                data = {'operacao': 'deletar', 'file_name': data['file_name']}
                new_socket.send(pickle.dumps(data))
            return {}

        # Caso haja menos servidores do que o necessário, replica para outros servidores
        if len(servers_to_search_file) < data['tolerancia']:
            print('replicar para outros servidores')
            server_data = handle_recuperacao(
                {'operacao': 'recuperacao', 'file_name': data['file_name']}, s)
            if 'error' in server_data:
                return {'error': 'Arquivo não encontrado no servidor'}
            elif server_data['file']:
                print('fazer depósito -- ',
                      data['tolerancia'] - len(servers_to_search_file))
                data = handle_deposito(
                    {'operacao': 'deposito', 'file_name': data['file_name'],
                     'tolerancia': data['tolerancia'] - len(servers_to_search_file), 'file': server_data['file']}, s)
                return {'message': 'sucesso'}


def create_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port))
    return s


def main():
    # Inicialização do servidor
    df = get_table()
    args = sys.argv[1:]
    if args and args[0] == "main":
        server_port = storage.MAIN_PORT
        try:
            s = create_socket(server_port)
        except OSError as e:
            if e.errno == 98:
                print(f"Porta {server_port} já está em uso")
                exit()
    else:
        for port in SERVER_PORTS:
            try:
                s = create_socket(port)
                break
            except OSError as e:
                if e.errno == 98:
                    print(f"Porta {port} já está em uso")
    if not s:
        exit()

    print(f"Servidor ativo na porta {s.getsockname()[1]}")
    s.listen(5)

    while True:
        # Aceita a conexão do cliente
        clientSocket, address = s.accept()
        print(f"Conexão estabelecida : {address}")

        full_msg = b''
        while True:
            # Recebe a mensagem do cliente
            msg = clientSocket.recv(BUFFER_SIZE)
            full_msg += msg
            if len(msg) < BUFFER_SIZE:
                print('Mensagem recebida')
                break
        try:
            # Tenta carregar os dados da mensagem recebida
            data_rcvd = pickle.loads(full_msg)
            print(f"operacao : {data_rcvd['operacao']}")
            print(f"file_name : {data_rcvd['file_name']}")
        except ValueError as error:
            print(error)
            clientSocket.send(pickle.dumps({'error': str(error)}))
            clientSocket.close()
            continue

        # Executa a operação adequada com base nos dados recebidos
        if data_rcvd['operacao'] == "deposito":
            try:
                data = handle_deposito(data_rcvd, s)
            except IndexError as e:
                print(e)
                data = {'error': 'Falha nos servidores'}
            if 'error' in data:
                clientSocket.send(pickle.dumps(data))
            else:
                clientSocket.send(pickle.dumps({'message': 'Arquivo salvo !'}))
        if data_rcvd['operacao'] == "recuperacao":
            data = handle_recuperacao(data_rcvd, s)
            clientSocket.send(pickle.dumps(data))
        if data_rcvd['operacao'] == "edicao":
            data = handle_edicao(data_rcvd, s)
            clientSocket.send(pickle.dumps(data))
        if data_rcvd['operacao'] == 'deletar':
            delete_file(s.getsockname()[1], data_rcvd['file_name'])

        clientSocket.close()


if __name__ == '__main__':
    main()
