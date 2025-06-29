# Teste 3: Soma de dois números usando LUI e PRINT
LUI $t0, 0        # $t0 = 0
ADDI $t0, $t0, 10 # $t0 = 10
LUI $t1, 0        # $t1 = 0
ADDI $t1, $t1, 10 # $t1 = 10
ADD $t2, $t0, $t1 # $t2 = $t0 + $t1 = 20
PRINT $t2         # Deve mostrar: 20
HALT