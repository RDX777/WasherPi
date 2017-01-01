<html>
<body>
<meta http-equiv="refresh" content="5">

<div align="left">
		
	<h2 style="color:red;">
		<strong>Status:</strong>
	</h2>

<?php

$ArqTex = '/var/www/html/Programas/status.txt';

if (file_exists($ArqTex)) {

$handle = @fopen($ArqTex, "r");
if ($handle) {
    while (($buffer = fgets($handle, 4096)) !== false) {
        echo $buffer;
	echo "<br>";
    }
    if (!feof($handle)) {
        echo "Erro: falha inexperada de fgets()\n";
    }

    fclose($handle);
}

} else {
    echo "Maquina Parada!";
};

?>

</div>
</body>
</html>