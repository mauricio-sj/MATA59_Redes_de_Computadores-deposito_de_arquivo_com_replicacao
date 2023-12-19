# Depósito de Arquivos com Replicação

<p align="center">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/mauricio-sj/MATA59_Redes_de_Computadores-deposito_de_arquivo_com_replicacao?color=%2304D361">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/mauricio-sj/MATA59_Redes_de_Computadores-deposito_de_arquivo_com_replicacao">
  <a href="https://github.com/mauricio-sj/MATA59_Redes_de_Computadores-deposito_de_arquivo_com_replicacao/commits/main">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/mauricio-sj/MATA59_Redes_de_Computadores-deposito_de_arquivo_com_replicacao">
  </a>
  <a href="https://github.com/mauricio-sj/MATA59_Redes_de_Computadores-deposito_de_arquivo_com_replicacao/stargazers">
    <img alt="Stargazers" src="https://img.shields.io/github/stars/mauricio-sj/MATA59_Redes_de_Computadores-deposito_de_arquivo_com_replicacao?style=social">
  </a>
</p>


<h4 align="center"> 
	🚧 Depósito de Arquivos com Replicação 🚧
</h4>

<p align="center">
	<img alt="Status do Projeto" src="https://img.shields.io/badge/STATUS-Concluido-green">
</p>

<p align="center">
 <a href="#-sobre-o-projeto">Sobre</a> •
 <a href="#-Funcionalidades">Funcionalidades</a> •
 <a href="#-como-executar-o-projeto">Como executar</a> • 
 <a href="#-tecnologias">Tecnologias</a>
</p>

## 💻 Sobre o projeto

📄 Este projeto consiste em um servidor de arquivos que utiliza sockets para depósito e replicação de arquivos.

---

## ⚙️ Funcionalidades

- [x] Servidor
  - [x] Armazena "N" cópias do arquivo
  - [x] Recupera o arquivo e o entrega ao cliente

- [x] Cliente
  - [x] Deposita arquivos
    - [x] Aumenta a quantidade de réplicas
    - [x] Diminui a quantidade de réplicas

---

## 🛣️ Como executar o projeto

#### 🎲 Rodando a aplicação

```bash

# Clone este repositório

```sh
git clone https://github.com/mauricio-sj/MATA59_Redes_de_Computadores-deposito_de_arquivo_com_replicacao.git
```

# Acesse a pasta do projeto no terminal/cmd
```sh
cd MATA59_Redes_de_Computadores-deposito_de_arquivo_com_replicacao
```

# Execute a aplicação

*Habilita o servidor Main que server como controlador pra verificar se as funções de deposito, recuperação e edição estão acontecendo
```sh
  python server.py main
```
*Habilita o servidor que recebe, deleta ou recupera os arquivos
```sh
  python server.py
```

*Habilita o cliente, onde terá um menu para seleção de qual operação vc quer fazer
```sh
  python client.py
```
*No cliente a tolerância é dado onde vc adiciona a quantos servidores ativo vc quer enviar o arquivo, por exemplo: se vc tem 3 servidores ativos mas só quer enviar para 1, a tolerância será de 1, se posteriormente, você quiser enviar para mais servidores, selecione a opção edicão e coloque 3, e as imagens irão para os 3 servidores ativos, o mesmo vale para remoção.

---
---
## 🛠 Etapa do projeto
O projeto está concluído e validado.

---

## 🛠 Tecnologias

* Python
* Socket
* Git
* GitHub
---
