import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import ipaddress as ipad
import requests as rqst
import json
import os
from geopy.geocoders import Nominatim

import webbrowser
from requests.auth import HTTPDigestAuth


#API ZABBIX
TOKEN = 'SEU TOKEN'
zabbix_url = 'https://zabbix.clouditservice.com.br/api_jsonrpc.php'


#VERIFICAÇÃO DE CAMERAS, VERIFICA SE É DAHUA OU INTELBRAS.
def get_device_type(ip, username, password):
    
    isdahua = False
    url = f"http://{ip}/cgi-bin/magicBox.cgi?action=getDeviceType"
    try:
        response = rqst.get(url, auth=HTTPDigestAuth(username, password))
        if response.status_code == 200 and response.text[:7]=='type=DH':
            
            isdahua = True    
        else:
            print(f"CAMERA INTELBRÁS")

            
    except Exception as e:
        print(f"Erro: {e}")
    return isdahua
#VERIFICAÇÃO DE CAMERAS, VERIFICA SE É DAHUA OU INTELBRAS.


#CRIAR UM HOST COM INTERFACE SNMP

def create_host_snmp(nomehost, ipdispositivo, groupid, templateid, interfacetype, interfacemain, useip, localizacao, tagcliente, tagprojeto, nometag, distrito, designador, link,latitude,longitude):
    headers = {'Content-Type': 'application/json'}
    #DADOS DO HOST,(TAGS,PORT,IP,TYPE, ETC...)
    data = {
        'jsonrpc': '2.0',
        'method': 'host.create',
        'params': {
            'host': nomehost,
            'interfaces': [
                {
                    'type': interfacetype,
                    'main': interfacemain,
                    'useip': useip,
                    'ip': ipdispositivo,
                    'dns': '',
                    'port': '161',
                    'details': {
                        'version': 2,  # Versão SNMP: 1 - SNMPv1, 2 - SNMPv2c, 3 - SNMPv3
                        'community': 'h0wb3'  # Comunidade SNMP
                    }
                }
            ],
            'groups': [
                {
                    'groupid': groupid
                }
            ],
            'tags': [
                {'tag': 'CLIENTE', 'value': tagcliente},
                {'tag': 'DISTRITO', 'value': distrito},
                {'tag': 'DS', 'value': designador},
                {'tag': 'LINK', 'value': link},
                {'tag': 'NOME', 'value': nometag},
                {'tag': 'PROJETO', 'value': tagprojeto}
            ],
            'templates': templateid,

            'inventory_mode': 0,  # Modo de inventário automático
            'inventory': {
                'location': localizacao,
                'location_lat':latitude,
                'location_lon':longitude
            },
            "description": "Inserido via software feito por ALEXANDRE",
            "proxy_hostid":"12944"
        },
        'auth': TOKEN,
        'id': 1
    }
    
    response = rqst.post(zabbix_url, headers=headers, data=json.dumps(data))
    result = response.json()
    print('ADICIONADO COM SUCESSO')
    return result

#CRIAR UM HOST COM INTERFACE SNMP

#CRIAR UM HOST COM INTERFACE AGENT ZABBIX
def create_host_agent(nomehost, ipdispositivo, groupid, templateid, interfacetype, interfacemain, useip, localizacao, tagcliente, tagprojeto, nometag, distrito, designador, link,latitude,longitude):
    headers = {'Content-Type': 'application/json'}
    #DADOS DO HOST,(TAGS,PORT,IP,TYPE, ETC...)
    data = {
        'jsonrpc': '2.0',
        'method': 'host.create',
        'params': {
            'host': nomehost,
            'interfaces': [
                {
                    'type': interfacetype,#feito
                    'main': interfacemain,#feito
                    'useip': useip,#feito
                    'ip': ipdispositivo,#feito
                    'dns': '',
                    'port': '10050',
                    'details': {
        'version': 2,  # Versão SNMP: 1 - SNMPv1, 2 - SNMPv2c, 3 - SNMPv3
        'community': 'h0wb3'  # Comunidade SNMP
                }
                }
            ],
            'groups': [
                {
                    'groupid': groupid
                }
            ],
            'tags': [
                {'tag': 'CLIENTE', 'value': tagcliente},
                {'tag': 'DISTRITO', 'value': distrito},
                {'tag': 'DS', 'value': designador},
                {'tag': 'LINK', 'value': link},
                {'tag': 'NOME', 'value': nometag},
                {'tag': 'PROJETO', 'value': tagprojeto}
            ],
            'templates':templateid,
                
            
            'inventory_mode': 0,  # Modo de inventário automático
            'inventory': {
                'location': localizacao,
                'location_lat':latitude,
                'location_lon':longitude
            },
            "description": "Inserido via software feito por ALEXANDRE",
            "proxy_hostid":"12944"
        },
        'auth': TOKEN,
        'id': 1
    }
        
        
    
    response = rqst.post(zabbix_url, headers=headers, data=json.dumps(data))
    result = response.json()
    print('ADICIONADO COM SUCESSO')
    return result
#CRIAR UM HOST COM INTERFACE AGENT ZABBIX


#INTERFACE GRÁFICA

#START JANELA PRINCIPAL
janela = tk.Tk()
janela.geometry('505x620')
janela.title("ADICIONAR DISPOSITIVOS ZABBIX")
janela.configure(bg='#A52A2A')


# IMAGEM
diretorio=os.path.dirname(os.path.abspath(__file__))
imagem = tk.PhotoImage(file=f'{diretorio}\zabbixlogo.png')
label_imagem = tk.Label(janela, image=imagem)
label_imagem.place(x=1, y=10)


#TEXTO NOME DISPOSITIVO
titulonome = tk.Label(janela, text="NOME DISPOSTIVO", font=("IMPACT", 20), bg='#A52A2A', fg='white')
titulonome.place(x=18, y=250)


#EFEITO PLACEHOLDER NOME DISPOSITIVO
def limpar_placeholder(event):
    if entrynome.get() == placeholder_texto:
        entrynome.delete(0, tk.END)
        entrynome.config(fg='black')


# EntryNome com placeholder que apaga
placeholder_texto = 'EM MARIA MENEZES...'
entrynome = tk.Entry(janela, width=36, font=('Arial', 16), fg='grey')
entrynome.place(x=20, y=285)
entrynome.insert(0, placeholder_texto)
entrynome.bind("<FocusIn>", limpar_placeholder)  # Limpa o texto placeholder quando a entrynome recebe foco

# ComboBox tipo de dispositivo
titulotipo = tk.Label(janela, text="TIPO", font=("IMPACT", 20), bg='#A52A2A', fg='white')
titulotipo.place(x=19, y=155)

optionsTipo = ['CAM', 'LEITOR', 'RB', 'RB + CAM']
comboTipo = ttk.Combobox(janela, values=optionsTipo, height=30)
comboTipo.place(x=19, y=195)

# TITULO E ENTRY Quantidade
tituloquant = tk.Label(janela, text="QUANTIDADE:", font=("IMPACT", 20), bg='#A52A2A', fg='white')
tituloquant.place(x=190, y=183)
entryquant = tk.Entry(janela, width=3, font=('Arial', 16))
entryquant.place(x=339, y=190)



tituloipinicial = tk.Label(janela, text="IP INICIAL", font=("IMPACT", 20), bg='#A52A2A', fg='white')
tituloipinicial.place(x=18, y=339)
entryipinicial = tk.Entry(janela, width=13, font=('Arial', 16))
entryipinicial.place(x=18, y=375)



# Distrito
titudistrito = tk.Label(janela, text="DISTRITO", font=("IMPACT", 20), bg='#A52A2A', fg='white')
titudistrito.place(x=220, y=434)
optionsDistrito = ['1', '2', '3', '4','5','6']
combodistrito = ttk.Combobox(janela, width=5, font=('Arial', 13), values=optionsDistrito)
combodistrito.place(x=332, y=442)
# DESIGNADOR
titulodesignador = tk.Label(janela, text="DESIGNADOR", font=("IMPACT", 20), bg='#A52A2A', fg='white')
titulodesignador.place(x=220, y=339)
entrydesignador = tk.Entry(janela, width=19, font=('Arial', 16))
entrydesignador.place(x=220, y=376)
# ENTRY E TITULO ENDEREÇO
tituloendereco = tk.Label(janela, text="ENDEREÇO", font=("IMPACT", 20), bg='#A52A2A', fg='white')
tituloendereco.place(x=18, y=434)
entryendereco = tk.Entry(janela, width=36, font=('Arial', 16))
entryendereco.place(x=18, y=470)

def enviardados():
    try:
        tipodisp = comboTipo.get()
        quantidade = int(entryquant.get()) 
        nome = entrynome.get()
        ip = entryipinicial.get()
        endereco = entryendereco.get()
        
        
        
        #LATITUDE E LONGITUDE
        geolocator = Nominatim(user_agent="meu_geolocalizador777")
        location = geolocator.geocode(endereco)
        
        if location:
            print(location.latitude, location.longitude)
            latitude = location.latitude
            longitude = location.longitude
        else:
            print(" Cordenadas não foram adicionadas pois o endereço não foi encontrado.")

        # TAGS
        tagcliente = 'SME-FORTALEZA'
        distrito = combodistrito.get()
        tagdesignador = entrydesignador.get()
        tagnome = nome
        tagprojeto = 'SME CAMERAS'
        listatemplate=[]
        if ip[:6] == "172.23":
            link = 'MOB'
        else:
            link = 'SIGA'
        
        
            
        # CONDIÇÃO DE GRUPO(CAMERAS LEITORES ROTEADORES)
        
        for cont in range(quantidade):
            listatemplate=[]
            
            # IP FINAL
            ipa = ipad.IPv4Address(ip)
            ipfinal = f'{ipa + cont}'
            interfacetype = 1
            numdisp = cont
            # QUANDO O DISPOSITIVO FOR CAMERA
            if tipodisp == 'CAM':
                groupid = '366'
                if get_device_type(ipfinal,username='usuario',password='PasswordDaCamera')==True:
                    listatemplate.extend([{'templateid':'10564'},{'templateid':'12941'}])
                    interfacetype = 2 #snmp
                    useip = 1  # USAR OU NÃO O IP
                    interfacemain = 1
                    listatemplate.append({'templateid':'10226'})#add generic snmp
                else:
                    listatemplate.append({'templateid':'10564'})
                    interfacetype = 1
                    useip = 1  # USAR OU NÃO O IP
                    interfacemain = 1
                dispname = f'CAM{numdisp + 1}'
                 # QUANDO O DISPOSITIVO FOR LEITOR
            elif tipodisp == 'LEITOR':
                groupid = '283'
                listatemplate.extend([{'templateid':'10380'},{'templateid':'16225'}])
                interfacetype = 1
                useip = 1  # USAR OU NÃO O IP
                interfacemain = 1
                dispname = f'LEITOR{numdisp + 1}'
                 # QUANDO O DISPOSITIVO FOR RB
            elif tipodisp == 'RB':
                if cont == 0 and link == 'SIGA':
                    groupid = '284'
                    listatemplate.append({'templateid':'10233'})
                    dispname = 'RB'
                    interfacetype = 2
                    useip = 1  # USAR OU NÃO O IP
                    interfacemain = 1
                elif cont == 0 and link == 'MOB':
                    groupid = '284'
                    listatemplate.append({'templateid':'10564'})
                    dispname = 'RB'
                    interfacetype = 1
                    useip = 1  # USAR OU NÃO O IP
                    interfacemain = 1
            else:  # # QUANDO O DISPOSITIVO FOR RB + CAM
                if cont == 0 and link == 'SIGA':
                    groupid = '284'
                    listatemplate.append({'templateid':'10233'})
                    dispname = 'RB'
                    interfacetype = 2
                    useip = 1  # USAR OU NÃO O IP
                    interfacemain = 1
                elif cont == 0 and link == 'MOB':
                    groupid = '284'
                    listatemplate.append({'templateid':'10564'})
                    dispname = 'RB'
                    interfacetype = 1
                    useip = 1  # USAR OU NÃO O IP
                    interfacemain = 1
                else:
                    groupid = '366'
                    if get_device_type(ipfinal,username='usuario',password='PasswordDaCamera')==True:
                        listatemplate.extend([{'templateid':'10564'},{'templateid':'12941'}])
                        dispname = f'CAM{numdisp}'
                        interfacetype = 2 #snmp
                        useip = 1  # USAR OU NÃO O IP
                        interfacemain = 1
                        listatemplate.append({'templateid':'10226'})#add generic snmp
                    else:
                        listatemplate.append({'templateid':'10564'})  # cam intelbras
                        dispname = f'CAM{numdisp}'
                        interfacetype = 1
                        useip = 1  # USAR OU NÃO O IP
                        interfacemain = 1
            #NOME DO HOST
            nomefinal = f'{dispname}-{nome}'

            if interfacetype == 2:
                result = create_host_snmp(nomefinal, ipfinal, groupid, listatemplate, interfacetype, interfacemain, useip, endereco, tagcliente, tagprojeto, nome, distrito, tagdesignador, link,latitude,longitude)
            else:
                result = create_host_agent(nomefinal, ipfinal, groupid, listatemplate, interfacetype, interfacemain, useip, endereco, tagcliente, tagprojeto, nome, distrito, tagdesignador, link,latitude,longitude)
        
            print(result)

    except Exception as e:
        print(f"Error: {e}")
        

# Botão ENVIAR DADOS
botaofinal = tk.Button(janela, text='ENVIAR', font=("IMPACT", 20), bg='#363636', fg='white', command=enviardados)
botaofinal.place(x=20, y=550)

def abrir_url():
    webbrowser.open("https://www.linkedin.com/in/joão-alexandre-0b5120189/")

#Texto com a URL do LINKEDLN#
texto = tk.Text(janela, wrap=tk.WORD, height=1, width=35, borderwidth=-1, bg='#A52A2A', font=("Bahnschrift", 10, "bold"))
texto.pack()
texto.insert(tk.END, "Desenvolvido por ")
texto.tag_configure("link", foreground="DeepSkyBlue", underline=True)
texto.place(x=300, y=600)
texto.tag_bind("link", "<Button-1>", lambda event: abrir_url())
texto.insert(tk.END, "João Alexandre", "link")
texto.config(state=tk.DISABLED)  # Impedir edição do texto

# Loop principal da aplicação
janela.mainloop()
