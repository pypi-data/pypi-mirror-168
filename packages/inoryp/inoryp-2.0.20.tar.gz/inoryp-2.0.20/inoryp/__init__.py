# Autor: R0htg0r
# Versão: 2.0.16
# Atualização de: 16/09/2022 até...

import os
import re
import time
import json
import requests
import Raney

idioma = str()
idiomas = ["pt_BR.json", "ru_RU.json", "en_US.json"]

try:
    if (os.path.exists("C:\ProgramData\Worda Team") != True): # Apenas uma vez!
        os.mkdir("C:\ProgramData\Worda Team")
        os.mkdir("C:\ProgramData\Worda Team\lang")

        open("C:\ProgramData\Worda Team\lang\pt_BR.json", "a", encoding="UTF-8").write(requests.get("https://raw.githubusercontent.com/R0htg0r/inoryp/main/lang/pt_BR.json").text)
        open("C:\ProgramData\Worda Team\lang\\ru_RU.json", "a", encoding="UTF-8").write(requests.get("https://raw.githubusercontent.com/R0htg0r/inoryp/main/lang/ru_RU.json").text)
        open("C:\ProgramData\Worda Team\lang\en_US.json", "a", encoding="UTF-8").write(requests.get("https://raw.githubusercontent.com/R0htg0r/inoryp/main/lang/en_US.json").text)
    else:
        pass
except:
    pass

if (os.path.exists('"C:\ProgramData\Worda Team"') != True): # Etapa 1
    if (os.path.exists("C:\ProgramData\Worda Team\cache.dat") == True): # Etapa 2
        if (os.path.exists("C:\ProgramData\Worda Team\cookies.dat") == True): # Etapa 3
            pass
            idioma = json.load(open("C:\ProgramData\Worda Team\lang\\" + idiomas[int(open("C:\ProgramData\Worda Team\cookies.dat", "r").read())], "r", encoding="UTF-8"))
    else:
        os.system('"cd C:\ProgramData\Worda Team && wmic os get MUILanguages >> cache.dat"') 
        cache = str(re.sub('["}{,]', "", open("C:\ProgramData\Worda Team\cache.dat", "r", encoding="UTF-16").read()).replace("MUILanguages", "").replace("-", "_").strip().split()[0])

        if cache == idiomas[0].replace(".json", ""): open("C:\ProgramData\Worda Team\cookies.dat", "w").write("0"); idioma = json.load(open(f"C:\ProgramData\Worda Team\lang\{idiomas[0]}", "r", encoding="UTF-8"))
        if cache == idiomas[1].replace(".json", ""): open("C:\ProgramData\Worda Team\cookies.dat", "w").write("1"); idioma = json.load(open(f"C:\ProgramData\Worda Team\lang\{idiomas[1]}", "r", encoding="UTF-8"))
        if cache == idiomas[2].replace(".json", ""): open("C:\ProgramData\Worda Team\cookies.dat", "w").write("2"); idioma = json.load(open(f"C:\ProgramData\Worda Team\lang\{idiomas[2]}", "r", encoding="UTF-8"))


def getIP(Proxy=None, Type=None):
    if Proxy != None:
        if(Type == "http"):
            try:
                ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php", proxies={"http": "http://" + Proxy, "https": "https://" + Proxy}).text
            except:
                ZFsiYDmRYWgVPtg4MDTm = "0.0.0.0" 
            return ZFsiYDmRYWgVPtg4MDTm
        elif(Type == "socks5"):
            try:
                ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php", proxies={"http": "socks5://" + str(Proxy),"https": "socks5://" + str(Proxy)}).text
            except Exception as e:
                print(e)
                ZFsiYDmRYWgVPtg4MDTm = "0.0.0.0"
            return ZFsiYDmRYWgVPtg4MDTm
        elif(Type == "socks4"):
            try:
                ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php", proxies={"http": "socks4://" + Proxy, "https": "socks4://" + Proxy}).text
            except:
                ZFsiYDmRYWgVPtg4MDTm = "0.0.0.0"
            return ZFsiYDmRYWgVPtg4MDTm
        else:
            return idioma["inoryp_erro_proxy"]
    else:
        ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php").text
        return ZFsiYDmRYWgVPtg4MDTm

def getCode(Proxy=None, Type=None):
    if Proxy != None:
        if(Type == "http"):
            try:
                ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php", proxies={"http": "http://" + Proxy, "https": "https://" + Proxy}).status_code
            except:
                ZFsiYDmRYWgVPtg4MDTm = "-1" 
            return ZFsiYDmRYWgVPtg4MDTm
        elif(Type == "socks5"):
            try:
                ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php", proxies={"http": "socks5://" + Proxy, "https": "socks5://" + Proxy}).status_code
            except:
                ZFsiYDmRYWgVPtg4MDTm = "-1"
            return ZFsiYDmRYWgVPtg4MDTm
        elif(Type == "socks4"):
            try:
                ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php", proxies={"http": "socks4://" + Proxy, "https": "socks4://" + Proxy}).status_code
            except:
                ZFsiYDmRYWgVPtg4MDTm = "-1"
            return ZFsiYDmRYWgVPtg4MDTm
        else:
            return idioma["inoryp_erro_proxy"]
    else:
        ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php").status_code
        return ZFsiYDmRYWgVPtg4MDTm

def getJSON(Proxy=None, Type=None):
    if Proxy != None:
        if(Type == "http"):
            try:
                ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php", proxies={"http": "http://" + Proxy,"https": "https://" + Proxy})
                YaVHqQTJFnxpzVzQFNWo = {idioma["inoryp_ip"]: ZFsiYDmRYWgVPtg4MDTm.text,idioma["inoryp_codigo"]: ZFsiYDmRYWgVPtg4MDTm.status_code, idioma["inoryp_sessao"]: Raney.criar(0, "C", 20)}
            except:
                YaVHqQTJFnxpzVzQFNWo = {idioma["inoryp_ip"]: "0.0.0.0", idioma["inoryp_codigo"]: "-1", idioma["inoryp_sessao"]: Raney.criar(0, "C", 20)}
            
            return YaVHqQTJFnxpzVzQFNWo

        elif(Type == "socks5"):
            try:
                ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php", proxies={"http": "socks5://" + Proxy,"https": "socks5://" + Proxy})
                YaVHqQTJFnxpzVzQFNWo = {idioma["inoryp_ip"]: ZFsiYDmRYWgVPtg4MDTm.text,idioma["inoryp_codigo"]: ZFsiYDmRYWgVPtg4MDTm.status_code,idioma["inoryp_sessao"]: Raney.criar(0, "C", 20)}
            except:
                YaVHqQTJFnxpzVzQFNWo = {idioma["inoryp_ip"]: "0.0.0.0",idioma["inoryp_codigo"]: "-1",idioma["inoryp_sessao"]: Raney.criar(0, "C", 20)}
            
            return YaVHqQTJFnxpzVzQFNWo

        elif(Type == "socks4"):
            try:
                ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php", proxies={"http": "socks4://" + Proxy,"https": "socks4://" + Proxy})
                YaVHqQTJFnxpzVzQFNWo = {idioma["inoryp_ip"]: ZFsiYDmRYWgVPtg4MDTm.text,idioma["inoryp_codigo"]: ZFsiYDmRYWgVPtg4MDTm.status_code,idioma["inoryp_sessao"]: Raney.criar(0, "C", 20)}
            except:
                YaVHqQTJFnxpzVzQFNWo = {idioma["inoryp_ip"]: "0.0.0.0",idioma["inoryp_codigo"]: "-1",idioma["inoryp_sessao"]: Raney.criar(0, "C", 20)}
            
            return YaVHqQTJFnxpzVzQFNWo

        else:
            return idioma["inoryp_erro_proxy"]

    else:
        ZFsiYDmRYWgVPtg4MDTm = requests.get("https://sinkable-coils.000webhostapp.com/py.php")
        YaVHqQTJFnxpzVzQFNWo = {idioma["inoryp_ip"]: ZFsiYDmRYWgVPtg4MDTm.text,idioma["inoryp_codigo"]: ZFsiYDmRYWgVPtg4MDTm.status_code,idioma["inoryp_sessao"]: Raney.criar(0, "C", 20)}
        return YaVHqQTJFnxpzVzQFNWo

def RetornarIP(Procurador=None, Metodo=None):
    if (Procurador != None):
        return getIP(Procurador, Metodo)
    else:
        return getIP()

def RetornarCodigo(Procurador=None, Metodo=None):
    if (Procurador != None):
        return getCode(Procurador, Metodo)
    else:
        return getCode()
    
def RetornarJSON(Procurador=None, Metodo=None):
    if (Procurador != None):
        return getJSON(Procurador, Metodo)
    else:
        return

# Versão clássica
def classico(Conteudo=None, Proxy=None, Type=None):
    if (Conteudo == 0):
        if (Proxy != None):
            return getIP(Proxy, Type)
        else:
            return getIP()
    
    elif (Conteudo == 1):
        if (Proxy != None):
            return getCode(Proxy, Type)
        else:
            return getCode()

    elif (Conteudo == 2):
        if (Proxy != None):
            return getJSON(Proxy, Type)
        else:
            return getJSON()