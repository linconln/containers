# ADA Tech

### Conteinirização

# Projeto

# O docker-compose tem todos os passos para execução do projeto
docker compose up -d

# A informação em tela, mostra os endereços para acessar os relatórios gerados no Min-io
# O Min-IO foi configurado com várias réplicas para testar, usando o nginx como proxy
# O "relatório" só tem os dados sem formatação
# Deixei o acesso web ao RabbitMQ e Min-IO para acompanhar a execução
# O acesso aos relatórios do Min-IO estava com erro, pois gera uma chave com o endereço do link de acesso, contornei inserindo um nome de host/ip no python que faz a chamada