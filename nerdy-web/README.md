NerdyMap

Sistema web de monitoramento de acessos com detecção de comportamento suspeito.

Tecnologias:
- Python
- Flask
- SQLite
- HTML / CSS / JS

Funcionalidades:
- Sistema de login
- Registro de logs de acesso
- Dashboard com estatísticas
- Detecção de possíveis ataques brute force
- API para atualização de logs

Projeto acadêmico desenvolvido para análise de segurança e integração futura com sistema de IA para classificação de criticidade.

# Passo a Passo

- pip install -r requirements.txt
- gunicorn -w 4 -b 127.0.0.1:8000 app:app