# Teste 1: Soma, subtração e PRINT
ADDI $t0, $zero, 5      # $t0 = 5
ADDI $t1, $zero, 3      # $t1 = 3
ADD  $t2, $t0, $t1      # $t2 = $t0 + $t1 = 8
SUB  $t3, $t2, $t0      # $t3 = $t2 - $t0 = 3
PRINT $t2               # Deve mostrar 8
PRINT $t3               # Deve mostrar 3
HALT