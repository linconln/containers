# ADA Tech

### Conteinirização

# Projeto

# O docker-compose tem todos os passos para execução do projeto
docker compose up -d

# Para testar, executar o producer.py que lê o arquivo json e gera um cache no REDIS
docker exec projeto-app-1 python3 producer.py

# O relatório é gerado em seguida, poderia ter feito tudo em um python junto, mas foi o desenho da aula
docker exec projeto-app-1 python3 report.py

# A informação em tela, mostra os endereços para acessar os relatórios gerados no Min-io
# O Min-IO foi configurado com várias réplicas para testar, usando o nginx como proxy
# O "relatório" só tem os dados sem formatação
# Deixei o acesso web ao RabbitMQ e Min-IO para acompanhar a execução
# Não consegui configurar o consumer pra executar por último, assim usei o restart, pois dava erro na conexão aos serviços
# poderia ter alterado a lógica do programa, mas foi mais rápido assim