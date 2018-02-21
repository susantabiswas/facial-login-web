<!DOCTYPE html>
<html>
<head>
	<title>login page</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>
<body>

<form action='login_check.php' method="GET">
	<div class='form-group'>
		<label for ='Email-id'>Enter Email id:</label>
		<input type='Email-id' class='form-control' id='Email-id' name = 'Email-id' required="True"></input>
	</div>

	<div class='form-group'>
		<label for ='password'>Enter Password:</label>
		<input type='password' class='form-control' id='password' name = 'password' required="True"></input>
	</div>
    <button type='submit' class = 'btn btn-submit'>Submit </button>
</form>
</body>
</html>