#====================================================================================
import time
import re
import yaml
from collections import deque
from watchdog.events import FileSystemEvent, FileSystemEventHandler,FileModifiedEvent
from watchdog.observers import Observer
#====================================================================================


#====================================================================================
# Variaveis Globais
lista_de_servico = ['Flask']
caminho_de_configuracao = "nerdy_web/MiniMim/config.yaml"
caminho_de_log = '.\\flask_logs.txt'
quantidade_de_ultimas_linhas = 1
fila_de_linhas = []
id = 0
#====================================================================================


#====================================================================================
# Abre o arquivo de Configuracao e compila para melhor desempenho
# Abre regras individualmente, tem mais processamento na primeira rodagem por compilar
# todas as configurações inicialmente
with open(caminho_de_configuracao, 'r') as arquivo_de_configuracao_puro:
    configuracao = yaml.safe_load(arquivo_de_configuracao_puro)

regras = {
    servico: {
        tipo: re.compile(padrao)
        for tipo, padrao in padroes.items()
    }
    for servico, padroes in configuracao.items()
}
#====================================================================================


#====================================================================================
# Funcao de pre_Filtro do Flask
def flask_pre_filter(ultimas_linhas,regras):
    # Pega cada linha da ultima linha lida, default = 1
    for cada_linha in ultimas_linhas:
        ''' Pega cada serviço e seu padrao. 
        EX: Servico: 
                PadraoA: "Valor"
                PadraoB: "Valor"
                ...
        '''
        for servico, padrao in regras.items():
            ''' Pega cada padrao (nome_padrao) e seu compile (str_padrao). 
                EX:
                        (PadraoA) nome_padrao: "str_padrao"
                        (PadraoB) nome_padrao: "str_padrao"
                        ...
                '''
            for nome_padrao,str_padrao  in padrao.items():
                # Verifica se atende os padrões daquele servico
                if re.search(regras[servico][nome_padrao], cada_linha.strip()):
                    print(f'Log do servico {servico} encontrado, aplicando pre-filtro do {servico}: {nome_padrao}')
                    #print(f'Log de Acordo com a configuração encontrado ')

# Todo o PRE-FILTRO, precisa de uma função com essa mesma logica, 
#====================================================================================


#====================================================================================
# Classe evento do Watchdog
class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        if event.src_path == caminho_de_log and event.event_type == "modified":
            print("Nova tentativa de Login detectada")
            print("Analisando log...")
            with open(caminho_de_log, "r", encoding="utf-8") as f:
                ultimas_linhas = deque(f, maxlen=quantidade_de_ultimas_linhas)
                id = 0
                flask_pre_filter(ultimas_linhas,regras)
#====================================================================================


#====================================================================================
#Chama evento e mantem em loop
event_handler = MyEventHandler()
observer = Observer()
observer.schedule(event_handler, ".", recursive=True)
observer.start()
try:    
    while True:
        time.sleep(2)
finally:
    observer.stop()
    observer.join()
#====================================================================================