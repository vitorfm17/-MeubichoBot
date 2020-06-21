<?php

include 'conexao.php';

$especie = $_POST['especie'];
$texto = $_POST['texto'];

$sql = "SELECT distinct u.chatid FROM pet p INNER JOIN usuario u ON u.id_usuario=p.tutor where p.especie='$especie'";
$buscar = mysqli_query($conexao,$sql);

while ($array = mysqli_fetch_array($buscar)){
	
		$cid = $array['chatid'];
		
		echo $msg = "sudo telegramMsg '" . $cid . "' '$texto'";
		
		$saida = exec($msg);

		echo "<pre>$saida</pre>";

}

?>