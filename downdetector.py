import requests # requisição http
import time # contador de tempo
import threading # criação de threads

# Lista de sites a serem monitorados
sites = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.youtube.com",
    "https://www.airbnbb.com.br" # erro proposital na digitação da URL do site do airbnb, causando erro
]

# URL do webhook do Discord
WEBHOOK_URL = "https://discordapp.com/api/webhooks/seu_webhook"

def send_notification(site):
    data = {
        "content": f"O site {site} está fora do ar!"
    }
    response = requests.post(WEBHOOK_URL, json=data) # envia uma requisição http do tipo post para aquele url com a informação data
    if response.status_code == 204: # se der certo a requisição retorna 204
        print(f"Notificação enviada para {site}.")
    else:
        print(f"Falha ao enviar notificação para {site}. Status: {response.status_code}")  # mostra o código de erro da requisição

def monitor_site(site):
    attempts = 3
    for attempt in range(attempts):
        print(f"Tentando acessar {site}, tentativa {attempt + 1}...")
        try:
            response = requests.get(site, timeout=5) # faz a requisição para endereço de site e aguarda no máximo 5 segundos para um resposta
            if response.status_code == 200: # se retornar ok, o site está no ar
                print(f"{site} está online.")
                return # finaliza a função
        except requests.exceptions.RequestException as e: # caso exceda os 5 segundos, captura a exceção do timeout
            print(f"Tentativa {attempt + 1} para {site} falhou: {e}")
            time.sleep(10) # espera por 10 segundos

    print(f"{site} está fora do ar após {attempts} tentativas.")
    send_notification(site) # envia ao site que está fora do ar, chamando a função 

def monitor_sites():
    while True:
        threads = [] # para cada site, cria-se uma thread para execução independente
        for site in sites: # para cada elemento da lista sites, grava-se na variável site
            thread = threading.Thread(target=monitor_site, args=(site,)) # a vírgula após o único item é para o python identificar como uma tupla
            threads.append(thread) # adiciona a thread na lista de threads
            thread.start() # inicializa a execução

        for thread in threads: # para cada elemento da lista threads, grava-se na variável thread
            thread.join() # pausa todas as threads, continua a execução do programa principal (monitor_sites) e sincroniza as threads
        
        # aguarda 10 segundos antes da próxima verificação
        time.sleep(10)

if __name__ == "__main__": # método que inicializa o programa monitor_sites
    monitor_sites()
