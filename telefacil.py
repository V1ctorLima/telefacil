#!/bin/python
# coding: utf-8
from datetime import date
import requests
import json

def getting_lotery_results():
    try:
        get_lotofacil_content = requests.get('http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_61L0H0G0J0VSC0AC4GLFAD2003/res/id=buscaResultado')
    except:
        print("An exception occurred")
    json_content = get_lotofacil_content.text
    wdatajson_content = json.loads(json_content)
    numero_concurso = wdatajson_content['nu_concurso']
    parsing_numeros_sorteados = wdatajson_content['resultadoOrdenado']
    numeros_sorteados = parsing_numeros_sorteados.split("-")

    return numeros_sorteados, numero_concurso

def compare_lotery_game(n_sorteados, n_concurso):

    jogo_1 = ["01","02","04","05","06","07","09","10","12","14","15","16","20","24","25"]
    jogo_2 = ["01","02","04","05","06","08","09","10","12","13","16","18","19","20","25"]

    today = date.today()
    jogos_premiados = []
    cont = 0
    for k in (jogo_1,jogo_2):
        for i in k:
            for j in n_sorteados:
                if i == j:
                    cont = cont + 1
        if cont >= 11:
            jogos_premiados.append(cont)
        cont = 0 

    if len(jogos_premiados) != 0:
        msg = str(today) + " ## " + n_concurso + " - Parabens, voce teve " + str(len(jogos_premiados)) + " jogos premiados, sendo eles de " + str(jogos_premiados) + " acertos !!!"
    elif len(jogos_premiados) == 1:
        msg = str(today) + " ## " + n_concurso + " - Parabens, voce teve " + str(len(jogos_premiados)) + " jogo premiado, sendo eles de " + str(jogos_premiados) + " acertos !!!"
    else:
        msg = str(today) + " ## " + n_concurso + " - Infelizmente nenhum jogo foi premiado...  =("
    return msg

def post_message_telegram(msg_enc):
    try:
        requests.get('https://api.telegram.org/bot<TELEGRAM_TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=' + msg_enc )
    except:
        print("An exception occurred")

def main():
    get_lotery_results = getting_lotery_results()
    numeros_sorteados = get_lotery_results[0]
    numero_concurso = get_lotery_results[1]
    msg = compare_lotery_game(numeros_sorteados, numero_concurso)
    msg_enc = requests.utils.quote(msg)
    post_message_telegram(msg_enc)

if __name__ == "__main__":
    main()