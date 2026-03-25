import time
import re
import yaml

from watchdog.events import FileSystemEvent, FileSystemEventHandler,FileModifiedEvent
from watchdog.observers import Observer

services_list = ['Flask','Nginx']

with open('nerdy_web/MiniMim/config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
    aceito = re.compile(".* nerdy-web flask[.*]: Accepted password for .*")
    negado = re.compile(".* nerdy-web flask[.*]: Failed password for .*")

def pre_filtragem(aceito,negado,arquivo):
    log_accepted = re.findall(aceito,arquivo)
    log_failure = re.findall(negado,arquivo)
    print(log_accepted, arquivo)
    print(log_failure, arquivo)
    

class MyEventHandler(FileSystemEventHandler):
    def on_any_event(self, event: FileSystemEvent) -> None:
        #print(f"Evento: {event.event_type} / caminho: {event.src_path} / Destino: {event.dest_path} / {event.is_synthetic}")
        #print(event)
        if event.src_path == ".\\flask_logs.txt" and event.event_type == "modified":
            print("Nova tentativa de Login detectada")
            print("Analisando log...")
            pre_filtragem(aceito,negado,"/flask_logs.txt")
            


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
