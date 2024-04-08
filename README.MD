# Projeto final modulo conteiners

# Basta baixar os arquivos e executar o docker-compose
# Serão mostradas na tela os links para baixa dos arquivos
# não funcionam, pois é preciso ter um nome/ip de host para substituir o hostname usado que é o nome do serviço
# Para testar, alterar a linha abaixo no app\producer.py
# endpoint="nginx:9000" => nginx = fqdn
# O Min-IO foi executado com uma interface web, para poder olhar os resultados e fazer o donwload manual dos arquivos, assim como o RabbitMQ
# Os relatórios só tem os dados, sem formatação
# São criados 4 serviços do Min-IO com acesso gerenciado pelo nginx (apenas pra teste)
# Usei sintaxes diferentes em alguns comandos e versões de imagens, para testes também
