import os
import getpass
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException, NetmikoTimeoutException
# Colors
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
RED = '\033[0;31m'
PURPLE = '\033[0;35m'
NC = '\033[0m'
def init():
    print("Welcome to {}SCRIPT SWITCH CISCO{}.".format(BLUE, NC))
    print("Developed by: {}g0bust3r (Leonardo Mayer){}.\n".format(PURPLE, NC))
def clear_screen():
# Limpar a tela (Windows)
    os.system('cls')
def clear_end_next():
    clear = input("Digite 'c' para limpar a tela e seguir para o próximo passo: ")
    if clear.strip().lower() == 'c' or clear.strip().lower() == 'clear':
        clear_screen()
def instructions():
    print("\n{}Configuração inicial antes de realizar o script deve seguir os seguintes comandos:{}\n ".format(GREEN , NC))
    print("enable ")
    print("configure terminal")
    print("interface vlan 1")
    print("ip add {}<ip> <mask>{}".format(BLUE , NC))
    print("no shut")
    print("exit")
    print("ip default-gateway {}<ip>{}".format(BLUE , NC))
    print("enable password {}<password>{}".format(BLUE, NC))
    print("enable secret {}<password_secret>{}".format(BLUE , NC))
    print("username {}<username>{} privilege 15 password {}<password>{}".format(BLUE, NC, BLUE, NC))
    print("service password-encryption")
    print("line vty 0 15 {}Conferir com comando line vty ? se é de 0 a 15.{}".format(BLUE , NC))
    print("no password")
    print("login local")
    print("transport input ssh")
    print("exit")
    print("ip domain name {}<domain>.com.br{}".format(BLUE , NC))
    print("crypto key generate rsa")
    print("2048")
    print("ip ssh version 2")
    print("exit")
    print("wr")
    print("{}\nFinalizado Configuração inicial para acesso ao switch{}\n".format(GREEN , NC))
    print("{}\nVolte para o Menu e selecione a opção 2 para conectar via SSH ao switch.{}\n".format(BLUE , NC))
def connection_switch():
    global ssh, device
    while True:
        print("\n{}Digite as informações para conectar ao switch:{}".format(BLUE , NC))
        host = input("Digite o endereço IP configurado para SSH: ")
        username = input("Digite o nome de usuário para SSH: ")
        password = getpass.getpass("Digite a senha para SSH: ")
        
        # Define as informações de conexão com o switch
        device = {
            'device_type': 'cisco_ios',
            'host': host,
            'username': username,
            'password': password,  
        }
        
        try:
            # Iniciando a conexão SSH
            ssh = ConnectHandler(**device)
            clear_screen()
            print("{}Conectado ao switch via SSH...{}".format(GREEN , NC))
            break  # Se a conexão for bem-sucedida, saia do loop
        except NetmikoAuthenticationException:
            clear_screen()
            print("Erro de autenticação. Verifique suas credenciais e tente novamente.")
        except NetmikoTimeoutException:
            clear_screen()
            print("Erro de tempo esgotado. Verifique o endereço IP do dispositivo e a conectividade de rede.")
            retry = input("Deseja tentar novamente? (s/n): ")
            if retry.lower() != 's':
                break  # Se o usuário não quiser tentar novamente, saia do loop
def save_config():
    ssh.send_command  ('wr')
    print(f"{GREEN}Salvo Configurações:{NC}")
    print(f"{GREEN}wr{NC}")
def set_hostname():
    print("{}Setando Hostname: {}".format(GREEN,NC))
    hostname = input ("Qual hostname deseja definir ? ")
    commands = [f'hostname {hostname}']
    connection = ConnectHandler(**device)
    ssh.send_config_set(commands)
    connection.disconnect()
    clear_screen()
    print(f"{GREEN}configure terminal{NC}")
    print(f"{GREEN}hostname {hostname}{NC}")
    print(f"{GREEN}exit{NC}")
def set_vlangerencia():
    print("{}\nCreating VLAN Gerencia: {}".format(BLUE,NC))
    global show_int
    #lista interfaces
    show_int = ssh.send_command("sh ip int br")
    print(show_int)
    #Input vlan gerencia e ip 
    vlan_gerencia = input("\nDigite o ID da VLAN Gerencia: ")
    ip_gerencia = input("Digite o ip e mascara da gerencia: (sintax: {}192.168.1.1 255.255.255.0{}) ".format(BLUE,NC))
    #input dos comandos:
    commands = [f'interface vlan {vlan_gerencia}', f'ip address {ip_gerencia}','no shutdown','exit']
    connection = ConnectHandler(**device)
    connection.send_config_set(commands)
    connection.disconnect()
    print(f"{GREEN}interface vlan {vlan_gerencia}{NC}")
    print(f"{GREEN}ip address {ip_gerencia}{NC}")
    print(f"{GREEN}no shutdown{NC}")
    print(f"{GREEN}exit{NC}\n")
def set_vlan():
    clear_screen()
    show_vlan_brief = ssh.send_command('show vlan brief')
    print(f"\n{GREEN}show vlan brief{NC}:{show_vlan_brief}\n")
    
    print(f"{BLUE}Consulta de VLANS:{NC}")
    vlan_ids = input("\nEscolha quais IDs de VLAN deseja configurar no switch, ex: 23,24,27: ")
    vlan_ids = vlan_ids.split(',')  # Transforma a string em uma lista de IDs
    
    commands = []
    
    for vlan_id in vlan_ids:
        nome_vlan = input(f"Digite o nome para a VLAN {vlan_id}: ")  # Solicita o nome da VLAN
        commands.append(f'vlan {vlan_id}')
        commands.append(f'name {nome_vlan}')
        commands.append('exit')
    
    ssh.send_config_set(commands)
    
    show_vlan_brief = ssh.send_command('show vlan brief')
    print(f"\n{GREEN}show vlan brief{NC}:{show_vlan_brief}\n")
    
    ssh.disconnect()
def port_trunk():
    global show_int_status
    show_int_status = ssh.send_command("sh int status")
    print("{}\nSetando porta(s) trunk: {}".format(BLUE,NC))
    print(show_int_status)
    print(F"{BLUE}\nConfigurando uma porta VLAN TRUNK:{NC}")
    port_trunk_vlan = input("Digite qual porta deseja passar a trunk \nex: {}fa0/48{} ou {}Et0/48{} ou {}Gi0/48{}: ".format(BLUE,NC,BLUE,NC,BLUE,NC))
    allow_trunk = input("\nDigite qual porta trunk ira ser passada conforme necessidade ex: 1,2,23,24,26,27,28,29,30,33: ")
    commands = [f'interface {port_trunk_vlan}','switchport trunk encapsulation dot1q','switch mode trunk',f'switch trunk allowed vlan add {allow_trunk}','exit']
    connection = ConnectHandler(**device)
    connection.send_config_set(commands)
    connection.disconnect()
    print(f"\n{GREEN}interface {port_trunk_vlan}{NC}")
    print(f"{GREEN}switchport trunk encapsulation dot1q{NC}")
    print(f"{GREEN}switch mode trunk{NC}")
    print(f"{GREEN}switch trunk allowed vlan {allow_trunk}{NC}\n")
def port_access():
    global show_int_status
    clear_screen()
    print(f"{GREEN}Configurando Porta de Acesso{NC}:")
    opcao = input(f"\nEscolha uma opção:\n1- Configurar uma porta somente\n2- Configurar várias portas de uma vez ({BLUE}range{NC})\nOpção: ")

    if opcao == '1':
        output = ssh.send_command("sh int status")
        print(output)
        porta = input("\nDigite a interface que deseja configurar ex: {}fa0/48{} ou {}Et0/48{} ou {}Gi0/48{} ".format(BLUE,NC,BLUE,NC,BLUE,NC))
        vlan = input("\nDigite qual VLAN que deseja atribuir à porta ex: {}27{} ".format(BLUE,NC))
    
        commands = [f'interface {porta}','switchport mode access',f'switchport access vlan {vlan}','exit']
        connection = ConnectHandler(**device)
        connection.send_config_set(commands)
        connection.disconnect()
       
    elif opcao == '2':
        print(f"\nPara configurar um range sem intervalos use: {BLUE}Et0/1-10{NC} Irá configurar da porta 1 até a 10. ")
        print(f"Para configurar um range com intervalos variados use virgula para separar as portas ex: {BLUE}Et0/1{NC},{BLUE}Et0/3{NC} ")
        print("{}fa0/48{} ou {}Et0/48{} ou {}Gi0/48{} ".format(BLUE,NC,BLUE,NC,BLUE,NC))
        show_int_status = ssh.send_command("sh int status")
        print(show_int_status)
        range_port = input("\nDigite as interfaces que deseja configurar conforme exemplos acima: ")
        vlan = input("\nDigite qual VLAN que deseja atribuir à porta ex: {}40{} ".format(BLUE,NC))

        commands = [f'interface range {range_port}','switchport mode access',f'switchport access vlan {vlan}','exit']
        connection = ConnectHandler(**device)
        connection.send_config_set(commands)
        connection.disconnect()
        
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
def voice_vlan():
    global show_int_status
    clear_screen()
    print(f"{GREEN}Configurando Voice Vlan{NC}:")
    opcao = input(f"\nEscolha uma opção:\n1- Configurar uma porta somente\n2- Configurar várias portas de uma vez ({BLUE}range{NC})\nOpção: ")

    if opcao == '1':
        show_int_status = ssh.send_command("sh int status")
        print(show_int_status)
        porta = input("\nDigite a interface que deseja configurar a voice vlan ex: {}fa0/48{} ou {}Et0/48{} ou {}Gi0/48{} ".format(BLUE,NC,BLUE,NC,BLUE,NC))
        vlan = input("\nDigite qual VLAN que deseja atribuir à porta ex: {}33{} ".format(BLUE,NC))
    
        commands = [f'interface {porta}',f'sw voice vlan {vlan}','exit']
        connection = ConnectHandler(**device)
        connection.send_config_set(commands)
        connection.disconnect()
       
    elif opcao == '2':
        print(f"\nPara configurar um range sem intervalos use: {BLUE}Et0/1-10{NC} Irá configurar da porta 1 até a 10. ")
        print(f"Para configurar um range com intervalos variados use virgula para separar as portas ex: {BLUE}Et0/1{NC},{BLUE}Et0/3{NC} ")
        print("{}fa0/48{} ou {}Et0/48{} ou {}Gi0/48{} ".format(BLUE,NC,BLUE,NC,BLUE,NC))
        show_int_status = ssh.send_command("sh int status")
        print(show_int_status)
        range_port = input("\nDigite as interfaces que deseja configurar a voice vlan conforme exemplos acima: ")
        vlan = input("\nDigite qual VLAN que deseja atribuir à porta ex: {}33{} ".format(BLUE,NC))

        commands = [f'interface range {range_port}',f'sw voice vlan {vlan}','exit']
        connection = ConnectHandler(**device)
        connection.send_config_set(commands)
        connection.disconnect()
        
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")
def ntp():
    commands = ['ntp server 200.160.6.133','clock timezone BRA -3 0','exit']
    connection = ConnectHandler(**device)
    connection.send_config_set(commands)
    print("{}Configurado NTP{}".format(GREEN,NC))
    connection.disconnect()
def banner():
    print(" O banner deve ser copiado da pasta de documentação do switch com o nome.")
def create_users():
    clear_screen
    print("{}Creating Users{}".format(BLUE,NC))
    username = input("Digite o nome do usuário: ")
    senha = getpass.getpass("Digite sua senha: ")
    opcao = input("Escolha uma das opções:\n1- Para permissão de escrita {}15{}\n2- Para permissão de leitura {}1{}\nOpção: ".format(BLUE,NC,BLUE,NC))
    if opcao == '1':
        commands = [f'username {username} privilege 15 secret {senha}']
        connection = ConnectHandler(**device)
        connection.send_config_set(commands)
        connection.disconnect()
    elif opcao == '2':
        commands = [f'username {username} privilege 1 secret {senha}']
        connection = ConnectHandler(**device)
        connection.send_config_set(commands)
        connection.disconnect()
    else:
        print(f"{RED}Opção inválida{NC}")    
def show_commands():
    clear_screen()
    print("================= Menu =================")
    print("1.  show ip interface brief")
    print("2.  show vlan brief")
    print("3.  show interfaces trunk")
    print("4.  show ip route")
    print("5.  show running-config")
    print("6.  show mac address")
    print("7.  show vlan status")
    print("0.  Sair")
    print("=======================================")
    opc = input("Escolha uma opção: ")

    if opc == '1':
        clear_screen()
        output = ssh.send_command('show ip int brief')
        print(output)
        print("")
        clear_end_next()
    elif opc== '2':
        clear_screen()
        output = ssh.send_command('show vlan brief')
        print(output)
        print("")
        clear_end_next()
    elif opc == '3':
        clear_screen()
        output = ssh.send_command('show int trunk')
        print(output)
        print("")
        clear_end_next()
    elif opc == '4':
        clear_screen()
        output = ssh.send_command('show ip route')
        print(output)
        print("")
        clear_end_next()
    elif opc == '5':
        clear_screen()
        output = ssh.send_command('show running-config')
        print(output)
        print("")
        clear_end_next()
    elif opc == '6':
        clear_screen()
        output = ssh.send_command('show mac address')
        print(output)
        print("")
        clear_end_next()
    elif opc == '7':
        clear_screen()
        output = ssh.send_command('show int status')
        print(output)
        print("")
        clear_end_next()
    elif opc == '0':
        print("Saindo do programa...")
        exit()
    else:
        print(f"{RED}Opção inválida{NC}")


    
def main():

    init()
    print("================= Menu =================")
    print("Execute sempre a {}opção 2{} para executar os menus seguintes.".format(RED,NC))
    print("1.  Instruções iniciais")
    print("2.  Conexão com switch")
    print("3.  Set Hostname")
    print("4.  Set vlans")
    print("5.  Portas de acesso")
    print("6.  Voice VLAN")
    print("7.  Setar port trunk")
    print("8.  Setar vlan gerencia")
    print("9.  NTP")
    print("10. Banner")
    print("11. Criar usuários")
    print("12. Salvar")
    print("13. Show Comandos")
    print("0.  Sair")
    print("=======================================")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        instructions()
        clear_end_next()
    elif escolha == '2':
        connection_switch()
    elif escolha == '3':
        set_hostname()
        clear_end_next()
    elif escolha == '4':
        set_vlan()
        clear_end_next() 
    elif escolha == '5':
        port_access()
        clear_end_next()
    elif escolha == '6':
        voice_vlan()
        clear_end_next()
    elif escolha == '7':
        port_trunk()
        clear_end_next()
    elif escolha == '8':
        set_vlangerencia()
        clear_end_next()
    elif escolha == '9':
        ntp()
        clear_end_next()
    elif escolha == '10':
        banner()
        clear_end_next()
    elif escolha == '11':
        create_users()
        clear_end_next()
    elif escolha == '12':
        save_config()
    elif escolha == '13':
        show_commands()
    elif escolha == '0':
        print("Saindo do programa...")
        exit()
    else:
        print("Opção inválida")
if __name__ == "__main__":
    while True:
        main()
#send_command - send one command
#send_config_set - send list of commands or command in configuration mode
#send_config_from_file - send commands from the file (uses method inside)send_config_set
#send_command_timing - send command and wait for the output based on timer
