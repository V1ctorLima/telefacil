# Telefacil

Simples programa que notifica através do telegram qual o resultado de suas apostas na Lotofácil.

## Installation

Não é necessário instalar nenhum pacote adicional que já não venha nativamente com o Python. Basta alterar os parâmetros de TOKEN, CHAT_ID e jogos, e executá-lo normalmente:

```bash
python telefacil.py
```

## Usage

Antes de começar a usá-lo é necessário criar um bot no telegram através do `@BotFather` e (recomendado) criar um canal também no telegram onde será recebida todas as notificações.

Após o processo acima substituia os campos `<TELEGRAM_TOKEN>` e `<CHAT_ID>` com suas respectivas informações adiquiridas do passo acima. 

Defina os seus jogos/apostas na função `compare_lotery_game()` adicionando a quantidades de jogos que desejar conforme snippet abaixo:


```
def compare_lotery_game(n_sorteados, n_concurso):

    jogo_1 = ["01","02","04","05","06","07","09","10","12","14","15","16","20","24","25"]
    jogo_2 = ["01","02","04","05","06","08","09","10","12","13","16","18","19","20","25"]

    for k in (jogo_1,jogo_2):

```

Como a programação do sorteio de jogos da lotofácil são de segunda, quarta e sexta, defina o crontab do seu linux com os parâmetros abaixo:


```
0 22 * * 1,3,5       /usr/bin/python $TELEFACIL/FOLDER/telefacil.py
```
