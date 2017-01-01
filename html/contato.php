<?php

    if ($fp = fopen("Mensagens/" . date('His-dmY') . ".txt", "a")){  
    	$escreve = fwrite($fp, $_POST["Mensagem"]);
    	fclose($fp);
    	echo "Mensagem enviada com sucesso!";
    	echo '<br>';
    	echo '<a target="baixo"href="contato.html">Voltar</a>';
    }else{
    	Echo "A mensagem não foi enviada!";
    };
    
?>