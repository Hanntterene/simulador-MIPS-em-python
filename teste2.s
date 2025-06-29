# Teste 2: MULT, SLT, SLTI e PRINT
ADDI $t0, $zero, 7      # $t0 = 7
ADDI $t1, $zero, 6      # $t1 = 6
MULT $t0, $t1           # $t0 = $t0 * $t1 = 42 (resultado em $t0)
SLT  $t2, $t0, $t1      # $t2 = ($t0 < $t1) ?  (0, pois 42 < 6 é falso)
SLTI $t3, $t1, 10       # $t3 = ($t1 < 10) ? (1, pois 6 < 10)
PRINT $t0               # Deve mostrar 42
PRINT $t2               # Deve mostrar 0
PRINT $t3               # Deve mostrar 1
HALT