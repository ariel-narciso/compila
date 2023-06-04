# Análise Semântica
## Gerenciamento de escopo e verificação de tipos por meio de tabela de símbolos
> Pra cada print, uma nova linha na saída é gerada contendo o nº
> da linha correspondente e o valor da variável.
> Adicionalmente, eventuais erros também serão mostrados
> contendo uma breve descrição e sua localização no código
### Instruções de Execução
```
python3 main.py < "input.txt" > "output.txt"
```
### Exemplo
*input.txt*
```
BLOCO _principal_
  NUMERO a = 10, b = 20
  PRINT b
  PRINT a
  BLOCO _n1_
    CADEIA a = “Compiladores”
    NUMERO c
    c=-0.45
    PRINT b
    PRINT c
  FIM _n1_
  BLOCO _n2_
    CADEIA b = “Compiladores”
    PRINT a
    PRINT b
    BLOCO _n3_
      NUMERO a=+0.28, c=-0.28, d
      PRINT a
      PRINT b
      PRINT c
      d=c
      PRINT d
    FIM _n3_
  FIM _n2_
  PRINT c
FIM _principal_
```
*output.txt*
```
(3, 20.0)
(4, 10.0)
(9, 20.0)
(10, -0.45)
(14, 10.0)
(15, 'Compiladores')
(18, 0.28)
(19, 'Compiladores')
(20, -0.28)
(22, -0.28)
('** ERRO **', 25, '(c) não encontrado')
```
