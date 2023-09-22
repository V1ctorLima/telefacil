# coding: utf-8
from datetime import date
import argparse
import requests
import json
import sys
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

empty = ''

if not os.path.exists("ultimo_resultado.txt"):
    with open("ultimo_resultado.txt","w") as file:
        file.write(empty)  
with open("ultimo_resultado.txt","r") as file:
    ultimo_resultado = file.read()

def read_games_from_file(user_input_filename):
    try:
        with open(user_input_filename,"r") as input_filename:
            return input_filename.read()
    except FileNotFoundError:
        sys.exit("Não consegui encontrar o arquivo " + user_input_filename)

def validate_quantity_of_numbers(user_file_readed_raw):
    if len(user_file_readed_raw.split(',')) != 15:
        sys.exit("Jogo não tem a quantidade de numeros correta, deve ter exatamente 15 números!")

def validate_number_of_game(user_file_readed_raw):
    jogo = (user_file_readed_raw.split(','))
    for j in jogo:
        if not 1 <= int(j) <= 25:
            sys.exit("O número " + str(j) + " não pode estar no jogo!\nPor favor corrija antes de continuar...")

def getting_lotofacil_json_content():
    try:
        lotofacil_content = requests.get('https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/', verify=False)
        return lotofacil_content.json()
    except requests.RequestException as e:
        sys.exit("Não foi possivel acessar o resultado dos jogos! - Exception " + e)

def parsing_drawing(lotofacil_content_raw):
    try:
        drawing_number = lotofacil_content_raw['numero']
        return str(drawing_number)
    except:
        sys.exit("Não foi encontrado o número do concurso a partir da URL consultada...")

def parsing_winning_numbers(lotofacil_content_raw):
    try:
        winning_numbers_raw = lotofacil_content_raw['listaDezenas']
        return winning_numbers_raw
    except:
        sys.exit("Não foi encontrado os números sorteados a partir da URL consultada...")

def compare_several_lotery_game(user_file_readed_games, winning_numbers):
    parsed_games = user_file_readed_games.split(',')
    total_hits = 0
    for game in parsed_games:
        if game in winning_numbers:
            total_hits += 1
    return str(total_hits)

def check_if_several_games_lottery_win(total_games_hits):
    final_result = []
    for game in total_games_hits:
        if int(game) >= 11:
            final_result.append(game)
    return final_result

def check_if_one_lottery_game_win(total_game_hit):
    if int(total_game_hit) >= 11:
        return [total_game_hit]
    return ["0"]

def generate_final_msg(final_result , drawing_number):
    today = date.today()
    lenght_final_result = len(final_result)
    if lenght_final_result != 0:
        final_message = str(today) + " ## " + drawing_number + " - Parabens, você teve " + lenght_final_result + " jogos premiados, sendo eles de " + str(final_result) + " acertos !!!"
    elif lenght_final_result == 1:
        final_message = str(today) + " ## " + drawing_number + " - Parabens, você teve " + lenght_final_result + " jogo premiado, sendo eles de " + str(final_result) + " acertos !!!"
    else:
        final_message = str(today) + " ## " + drawing_number + " - Infelizmente nenhum jogo foi premiado...  =("
    with open("ultimo_resultado.txt","w") as resultado:
        resultado.write(str(drawing_number))
    return final_message

def send_results_to_telegram_api(final_message):
    final_message_url_encoded = requests.utils.quote(final_message)
    try:
        with open("./.credentials/telegram.json","r") as telegram_file:
            telegram_creds = telegram_file.read()
            token_telegram_creds = json.loads(telegram_creds)
    except:
        sys.exit("Não foi possivel abrir o arquivo .credentials/telegram.json")

    try:
        requests.get('https://api.telegram.org/bot' + token_telegram_creds["TELEGRAM_TOKEN"] + '/sendMessage?chat_id=' + token_telegram_creds["CHAT_ID"] + '&text=' + final_message_url_encoded)
    except:
        sys.exit("Não foi possivel enviar um request para a API do Telegram")

def adding_arguments():
    parse_arg = argparse.ArgumentParser(prog='telefacil.py', description='Telefácil mostra o resultado de seus jogos da Lotofacil')
    parse_arg.add_argument('-f', metavar="filename.json", help='Insira o nome de um arquivo com seus jogos no formato json para ser lido. Exemplo: python telefacil.py -f <arquivo.json>')
    parse_arg.add_argument('-j', metavar="1,...,25", help='Insira os números de um jogo separado por virgula. Exemplo: python telefacil.py -j 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15')
    parse_arg.add_argument('-t', action='store_true', help='Use esta opção caso queira enviar o resultado para um grupo do Telegram. Lembre-se de configurar o arquivo .credentials/telegram.json. Exemplo: python telefacil.py (-f ou -j) -t')
    user_raw_input = parse_arg.parse_args()
    return user_raw_input

def main():
    user_raw_input = adding_arguments()
    if user_raw_input.f is not None:
        file_input_raw = read_games_from_file(user_raw_input.f)
        file_user_input_json = json.loads(file_input_raw)
        user_quantity_of_games = 0
        for game in file_user_input_json["jogos"]:
            validate_quantity_of_numbers(game)
            validate_number_of_game(game)
            user_quantity_of_games += 1
        print("Tudo certo com seus jogos, você informou " + str(user_quantity_of_games) + " jogos de Lotofácil!")
        print("Baixando conteúdo da caixa")
        lotofacil_json_content = getting_lotofacil_json_content()
        drawing_number = parsing_drawing(lotofacil_json_content)
        if ultimo_resultado != drawing_number:
            winning_numbers = parsing_winning_numbers(lotofacil_json_content)
            game_list = []
            for game in file_user_input_json["jogos"]:
                result = compare_several_lotery_game(game, winning_numbers)
                game_list.append(result)
            final_results = check_if_several_games_lottery_win(game_list)
            final_mesage = generate_final_msg(final_results, drawing_number)
            if user_raw_input.t is True:
                send_results_to_telegram_api(final_mesage)
            else:
                print(final_mesage)
        else:
            sys.exit(f"Jogo {drawing_number} já validado")

    elif user_raw_input.j is not None:
        input_raw = user_raw_input.j
        validate_quantity_of_numbers(input_raw)
        validate_number_of_game(input_raw)
        print("Tudo certo com seu jogo da Lotofácil!")
        print("Baixando conteúdo da caixa")
        lotofacil_json_content = getting_lotofacil_json_content()
        drawing_number = parsing_drawing(lotofacil_json_content)
        if ultimo_resultado != drawing_number:
            winning_numbers = parsing_winning_numbers(lotofacil_json_content)
            result = compare_several_lotery_game(input_raw, winning_numbers)
            final_results = check_if_one_lottery_game_win(result)
            final_mesage = generate_final_msg(final_results, drawing_number)
            if user_raw_input.t is True:
                send_results_to_telegram_api(final_mesage)
            else:
                print(final_mesage)
        else:
            sys.exit(f"Jogo {drawing_number} já validado")

    else:
        sys.exit('Por favor, insira algum argumento para continuar, ou -h para ver as opções disponivéis')

if __name__ == "__main__":
    main()