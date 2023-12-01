# Playwright Compare Images

O script nesse repositório tem como objetivo comparar imagens extraidas de dois endpoints e calcular o grau de diferença entre elas

Ele recebe um arquivo no formato .csv com o seguinte formato: NOME,URL 1,URL 2,DIFERENCA

Abaixo temos um exemplo de como o código analiza as imagens:

IMAGE 1           |  IMAGE 2 | RESULT
:-------------------------:|:-------------------------:|:-------------------------:
![](src/print1.png)  |  ![](src/print2.png)  | ![](src/result.png)

O resultado final é a imagem da coluna RESULT, que realça as áreas onde o código encontrou as diferenças entre as duas imagens.

Também preenchemos o campo DIFERENCA na tabela de entrada, assim conseguimos ordenar as imagens do maior para o menor grau de diferença, facilitando o trabalho de homologação
