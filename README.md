# Fantasy Battle Defense Dealer

**Autoria:**
Tom�s Carvalho n� 22203333
    -Escreveu as fun��es do Title Screen e do Game Over Screen + Leaderboard;
    -Implementou a classe Comets() e todas as funcionalidades dos cometas;
    -Definiu as fun��es a usar na classe Comets();
    -Implementou todas as funcionalidades da Leaderboard.

Jo�o Correia n� 22202506
    -Escreveu o Main Game Loop, incluindo todas as funcionalidades do jogador e dos tiros;
    -Escreveu a documenta��o README.md;
    -Definiu as fun��es a usar no Main Game Loop;
    -Implementou sistemas de som e de dificuldade aumentativa;
    -Implementou o sistema de score em conjunto com o colega.




**Arquiquetura da Solu��o:**
O c�digo est� organizado por:
1. Inicializa��o de vari�veis
Define as vari�veis globais de cor, fontes, imagens, sons, hitboxes e pontua��o;
2. Main Loop Functions
Define as fun��es a usar no Main Game Loop:
    - `play_music()`: Come�a a tocar uma m�sica de fundo e para a anterior;
    - `shootBullet()`: Verifica se a cooldown de disparo j� acabou para poder disparar novamente;
    - `wrap_around()`: Verifica se a posi��o de um conjunto de coordenadas se encontra fora do ecr�, e passa-o para o lado oposto.
    - `checkBalance()`: Verifica se o jogador tem 0 ou menos dinheiro, ou 100000 ou mais, e se sim, atribui um final correspondente ao jogo. 

3. Main Game Loop
Mostra a interface ao jogador, pede, recebe e computa inputs deste.

**Refer�ncias:**
Foi usada a biblioteca `random` do Python.