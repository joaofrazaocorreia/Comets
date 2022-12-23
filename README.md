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
1. Variable Initialization
Define as variáveis globais de cor, fontes, imagens, sons, hitboxes e pontuação;
2. Main Loop Functions
Define as funções a usar no Main Game Loop, tais como:
    - `play_music()`: Começa a tocar uma música de fundo e para a anterior;
    - `shootBullet()`: Verifica se a cooldown de disparo já acabou para poder disparar novamente;
    - `wrap_around()`: Verifica se a posição de um conjunto de coordenadas se encontra fora do ecrã, e passa-o para o lado oposto.
    - `moveBullet()`: Utiliza as variáveis de cada tiro para determinar e desenhar a sua próxima posição.

3. Comet Class and Functons
Define a classe dos cometas e as variáveis e funções usadas nestes, como por exemplo:
    - `Comet.initial()`: Cria dois cometas largos ao início do jogo com velocidade, posição e direção aleatórios;
    - `Comet.move()`: Calcula a nova posição de cada cometa a partir da sua posição anterior, e move a sua hitbox para a nova posição;
    - `Comet.draw()`: Desenha todos os cometas em jogo nas posições das suas hitboxes e nos seus respetivos tamanhos;
    - `Comet.split()`: Quando chamada, esta função divide um cometa com base no seu tamanho: Cometas largos tornam-se em 3 médios, Cometas médios tornam-se em 5 pequenos, e Cometas pequenos são destruidos.

**Referências:**
Foram usadas a bibliotecas `pygame`, `random`, `numpy` e `math` do Python.
Todo o audio do jogo provém do site www.epidemicsound.com
A inspiração para as mecânicas de colisão provêm de uma resposta a um post do Stack Overflow, encontrado em https://stackoverflow.com/questions/29640685/how-do-i-detect-collision-in-pygame#:~:text=Use%20pygame.,instances%20of%20Sprite%20and%20Bullet%20.