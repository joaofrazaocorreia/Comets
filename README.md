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
1. Variable Initialization
Define as vari�veis globais de cor, fontes, imagens, sons, hitboxes e pontua��o;
2. Main Loop Functions
Define as fun��es a usar no Main Game Loop, tais como:
    - `play_music()`: Come�a a tocar uma m�sica de fundo e para a anterior;
    - `shootBullet()`: Verifica se a cooldown de disparo j� acabou para poder disparar novamente;
    - `wrap_around()`: Verifica se a posi��o de um conjunto de coordenadas se encontra fora do ecr�, e passa-o para o lado oposto.
    - `moveBullet()`: Utiliza as vari�veis de cada tiro para determinar e desenhar a sua pr�xima posi��o.

3. Comet Class and Functons
Define a classe dos cometas e as vari�veis e fun��es usadas nestes, como por exemplo:
    - `Comet.initial()`: Cria dois cometas largos ao in�cio do jogo com velocidade, posi��o e dire��o aleat�rios;
    - `Comet.move()`: Calcula a nova posi��o de cada cometa a partir da sua posi��o anterior, e move a sua hitbox para a nova posi��o;
    - `Comet.draw()`: Desenha todos os cometas em jogo nas posi��es das suas hitboxes e nos seus respetivos tamanhos;
    - `Comet.split()`: Quando chamada, esta fun��o divide um cometa com base no seu tamanho: Cometas largos tornam-se em 3 m�dios, Cometas m�dios tornam-se em 5 pequenos, e Cometas pequenos s�o destruidos.

**Refer�ncias:**
Foram usadas a bibliotecas `pygame`, `random`, `numpy` e `math` do Python.
Todo o audio do jogo prov�m do site www.epidemicsound.com
A inspira��o para as mec�nicas de colis�o prov�m de uma resposta a um post do Stack Overflow, encontrado em https://stackoverflow.com/questions/29640685/how-do-i-detect-collision-in-pygame#:~:text=Use%20pygame.,instances%20of%20Sprite%20and%20Bullet%20.