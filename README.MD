# Telefacil

Simples programa que notifica através do telegram qual o resultado de suas apostas na Lotofácil.

## Installation

Não é necessário instalar nenhum pacote adicional que já não venha nativamente com o Python. É possivel utiliza-lo de duas formas, a primeira passando um arquivo contendo todos os seus jogos do Lotofácil no arquivo `jogos.json` e executá-lo da seguinte maneira:

```bash
python telefacil.py -f jogos.json
```

Ou também é possivel rodá-lo passando um único jogo de forma direta como argumento do programa da seguinte maneira:

```bash
python telefacil.py -j 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
```

Caso deseje receber os resultados via um bot do telegram basta configurar os parâmetros de TOKEN e CHAT_ID no arquivo `.credentials/telegram.json`:

```bash
python telefacil.py -f jogos.json -t
```

## Usage

Para usa-lo integrado ao Telegram, é necessário antes de mais nada criando um bot no telegram através do `@BotFather` e (recomendado) criar um canal também no telegram onde será recebida todas as notificações.

Após o processo acima substituia os campos `<TELEGRAM_TOKEN>` e `<CHAT_ID>` do arquivo `.credencials/telegram.json` com suas respectivas informações adiquiridas do passo acima.

Como a programação do sorteio de jogos da Lotofácil são de segunda, quarta e sexta, defina o crontab do seu linux com os parâmetros abaixo:

```
0 22 * * 1,3,5       /usr/bin/python $TELEFACIL/FOLDER/telefacil.py -f jogos.json -t
```
