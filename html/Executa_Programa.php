<html>
<body>
<div align="right">

	<h2 style="color:red;">
		<strong>Sistema:</strong>
	</h2>

<?php

$ArqTex = '/var/www/html/Programas/status.txt';

if (!isset($_POST['CA'])){

	if (!file_exists($ArqTex)) {
		$DateIni = date('H:i:s - d/m/Y');

		while ($name = current($_POST)) {
			if ($name !== "TurboLavagem"){
        			$a = key($_POST);
			}
    		next($_POST);
		};

		if ($_POST['TurboLavagem'] == "True"){
			$turbo = "Sim";
		} else {
			$turbo = "Não";
		};
		
		echo "Programa selecionado: " . $_POST[$a];
		echo "<br />";
		echo "Turbo Lavagem: " . $turbo;
		echo "<br />";
		echo "Inicio as: $DateIni";

		exec('sudo python Programas/Executa.py ' . $a . ' ' . $_POST['TurboLavagem']);

		$DateFim = date('H:i:s - d/m/Y');
		echo "<br />";
		echo "Fim as: $DateFim";
	};

};

if ((file_exists($ArqTex)) and (!isset($_POST['CA']))){
	echo "A Maquina ocupada, por favor aguarde!";
};

if (isset($_POST['CA'])) {
     	echo "Cancelando...";
	echo "<br />";
		system('sudo python Programas/Reset.py');
		if (system('sudo pkill -9 python')){
			echo "Não foi possivel parar!";
			echo "<br />";	
		}else {
			echo "Terminado processo!";
			echo "<br />";
		};
		
		if (system('sudo rm ' .$ArqTex)){
			echo "Não foi possivel deletar o arquivo !(" .$ArqTex . ")"; 
			echo "<br />";
		}else{
		echo "Processo Cancelado!";
		};
};

if (isset($_POST['SH'])) {
	exec('sudo poweroff');
};
?>
</div>
</body>
</html>