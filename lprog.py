import argparse
import os
import sys
import psutil
import pygetwindow as gw

# argumentos de linha de comando

parser = argparse.ArgumentParser(description='Lista de programas em execução')
parser.add_argument('-b', '--background', action='store_true', help='Lista os programas em execução em background')
parser.add_argument('-s', '--system', action='store_true', help='Lista os programas em execução no sistema')
args = parser.parse_args()

# comportamento padrão (sem argumentos)

if not args.background and not args.system:
    print('=== Programas em Janelas Visiveis ===')
    janelas = gw.getAllTitles()
    janelas_visiveis = [janela for janela in janelas if janela.strip()]

    if not janelas_visiveis:
        print('Nenhuma janela visivel encontrada.')
    else:
        for janela in janelas_visiveis:
            print(janela)

# com argumento -b: lista programas no background

if args.background:
    print('=== Programas em Background ===')
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            info = proc.info
            print(f"PID: {info['pid']:<6} Nome: {info['name']:<30} Usuario: {info.get('username', 'N/A')}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        
# com argumento -s: lista programas do sistema

if args.system:
    print('=== Programas do Sistema ===')
    system_processes = []
    
    # Definindo critérios para identificar programas do sistema
    system_users = ['SYSTEM', 'LOCAL SERVICE', 'NETWORK SERVICE', 'root']
    system_paths = []
    
    if os.name == 'nt':  # Windows
        system_paths = ['C:\\Windows\\', 'C:\\Windows\\System32\\']
    else:  # Linux/Mac
        system_paths = ['/bin/', '/sbin/', '/usr/bin/', '/usr/sbin/']
    
    # Listar processos do sistema
    for proc in psutil.process_iter(['pid', 'name', 'username', 'exe']):
        try:
            info = proc.info
            is_system_user = info.get('username') in system_users
            is_system_path = False
            if info.get('exe'):
                is_system_path = any(path in str(info.get('exe')) for path in system_paths)
            if is_system_user or is_system_path:
                print(f"PID: {info['pid']:<6} Nome: {info['name']:<30} Caminho: {info.get('exe', 'N/A')}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
