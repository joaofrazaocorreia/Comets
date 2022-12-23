# Fantasy Battle Defense Dealer

**Autoria:**
Tomás Carvalho nº 22203333
    -Escreveu as funções do Title Screen e do Game Over Screen + Leaderboard;
    -Implementou a classe Comets() e todas as funcionalidades dos cometas;
    -Definiu as funções a usar na classe Comets();
    -Implementou todas as funcionalidades da Leaderboard.

João Correia nº 22202506
    -Escreveu o Main Game Loop, incluindo todas as funcionalidades do jogador e dos tiros;
    -Escreveu a documentação README.md;
    -Definiu as funções a usar no Main Game Loop;
    -Implementou sistemas de som e de dificuldade aumentativa;
    -Implementou o sistema de score em conjunto com o colega.




**Arquiquetura da Solução:**
O código está organizado por:
1. Inicialização de variáveis
Define as variáveis globais de cor, fontes, imagens, sons, hitboxes e pontuação;
2. Main Loop Functions
Define as funções a usar no Main Game Loop:
    - `play_music()`: Começa a tocar uma música de fundo e para a anterior;
    - `shootBullet()`: Verifica se a cooldown de disparo já acabou para poder disparar novamente;
    - `wrap_around()`: Verifica se a posição de um conjunto de coordenadas se encontra fora do ecrã, e passa-o para o lado oposto.
    - `checkBalance()`: Verifica se o jogador tem 0 ou menos dinheiro, ou 100000 ou mais, e se sim, atribui um final correspondente ao jogo. 

3. Main Game Loop
Mostra a interface ao jogador, pede, recebe e computa inputs deste.

**Referências:**
Foi usada a biblioteca `random` do Python.