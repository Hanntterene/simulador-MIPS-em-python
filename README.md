# simulador-MIPS-em-python
um mini simulador MIPS feito em python, trabalho para diciplina de Arquitetura e Organização de Computadores

Autores: Luís Guilherme Amorim Dessia Lohanna da Silva Monteiro

-------------------------------------------
REQUISITOS:
-------------------------------------------
- Python 3.x instalado (recomendado >= 3.8)
- Não requer bibliotecas adicionais (utiliza apenas tkinter, que já vem no Python padrão)

-------------------------------------------
COMO COMPILAR E EXECUTAR:
-------------------------------------------
1) Extraia todos os arquivos em uma pasta.
2) Abra um terminal (Prompt de Comando ou PowerShell no Windows, Terminal no Linux/Mac) na pasta do projeto.
3) Execute o comando abaixo:

    python interface.py

4) A interface gráfica será aberta. Digite ou cole seu código MIPS Assembly no campo principal.

-------------------------------------------
COMO USAR:
-------------------------------------------
- Digite seu programa MIPS no campo de texto.
- Clique em "OK" para executar o programa todo de uma vez.
- Ou utilize "Executar Passo" para executar instrução por instrução (passo a passo).
- Use "Reiniciar Passo" para recomeçar a execução passo a passo.

- As saídas do PRINT e PRINTS aparecerão no painel "Saída do PRINT".
- O painel "Resultado do programa" mostra os valores dos registradores e da memória.
- O painel "Código binário executado" mostra a versão binária de cada instrução executada.

-------------------------------------------
INSTRUÇÕES SUPORTADAS:
-------------------------------------------
- ADD, SUB, AND, OR, SLL, MULT, SLT
- ADDI, SLTI, LW, SW, LUI
- BEQ, BNE
- PRINT (imprime valor de registrador)
- PRINTS (imprime string definida com .data)
- HALT ou EXIT

-------------------------------------------
EXEMPLOS DE USO:
-------------------------------------------
Veja os arquivos de teste "teste1.asm", "teste2.asm", "teste3.asm" para exemplos prontos!

-------------------------------------------
DÚVIDAS OU ERROS:
-------------------------------------------
Se aparecer alguma mensagem de erro, confira se a instrução digitada está correta e se todos os registradores usados existem.

-------------------------------------------