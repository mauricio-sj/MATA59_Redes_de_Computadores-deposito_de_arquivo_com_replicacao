# Importação de módulos necessários
import os

# As funções deste módulo servem para facilitar operações comuns, como criar pastas, salvar e obter arquivos, 
# e validar parâmetros para garantir a consistência e a integridade das operações realizadas no sistema distribuído.

# Lista de métodos suportados
supported_methods = ["deposito", "recuperacao", "edicao"]

# Porta principal padrão
MAIN_PORT = 3000


# Função para criar uma pasta se ela não existir
def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


# Função para salvar um arquivo em uma pasta especificada
def save_file(folder, file_name, file):
    create_folder(folder)
    with open(file_name, 'wb') as f:
        f.write(file)
    return


# Função para obter o conteúdo de um arquivo
def get_file(file_name):
    with open(file_name, 'rb') as file:
        return file.read()


# Função para validar os parâmetros da operação
def validate_params(params):
    if params['operacao'] not in supported_methods:
        raise ValueError("Método solicitado inválido")
