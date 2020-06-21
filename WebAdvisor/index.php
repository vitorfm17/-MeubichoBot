<html>
<header>
		<meta charset='utf-8'>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
		<title>Formulário de Envio</title>
</header>
<body>
	<div class="container" style="margin-top:100px; width:600px">
	<form method="post" action="enviomsg.php">
		<div class="form-group">
			<label for="especie">Selecione o Grupo alvo</label>
			<select name="especie" class="form-control">
   <option value="Gato">Gato</option>
   <option value="Cachorro">Cachorro</option>
   <option value="Ave">Ave</option>
   <option value="Roedor">Roedor</option>
  </select>
		</div>
		
		<div class="form-group">
			<label for="Textarea1">Texto de envio</label>
			<textarea name="texto" class="form-control" rows="3"></textarea>
		</div>	
	
		<input class="btn btn-primary" type="submit" name="submit" value="Enviar"/>

	</form>  
	</div>

</body>
</html>