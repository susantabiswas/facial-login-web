</!DOCTYPE html>
<html>
<head>
	<title>this is a new page</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<style type="text/css">
		.form-1{
			height: 140%;
			width: 50%;
			position: relative;
			padding: 20px;
			margin: 10%;
			background-color: #64B5F6;
		}
	</style>
</head>
<body>


<!-- to get inserted rows in the database
<form action='retreive_data.php' class="form-2">
	<button type='submit' class = 'btn btn-submit' id ='validate'>Get Data </button>
</form>
-->


<!-- to get the details of the user -->
<form action='none.php' class='form-1'>
	<div class='form-group'>
		<label for ='students-name'>Student Name:</label>
		<input type='students-name' class='form-control' id='students-name' name = 'students-name' required="True"></input>
	</div>

	<div class='form-group'>
		<label for ='fathers-name'>Fathers Name:</label>
		<input type='fathers-name' class='form-control' id='fathers-name' name = 'fathers-name' required="True"></input>
	</div>

	<div class='form-group'>
		<label for ='postal-address'>Postal Address:</label>
		<input type='postal-address' class='form-control' id='postal-address' name = 'postal-address' required="True"></input>
	</div>

	<div class='form-group'>
		<label for ='permanent-address'>Permanent Address:</label>
		<input type='permanent-address' class='form-control' id='permanent-address' name = 'permanent-address' required="True"></input>
	</div>

	<div class='form-group'>
		<label for ='pincode'>Pincode:</label>
		<input type='pincode' class='form-control' id='pincode' name = 'pincode' required="True"></input>
	</div>
	
	<div class='form-group'>
		<label for ='sex'>sex:</label>
		<input type='sex' class='form-control' id='sex' name = 'sex' required="True"></input>
	</div>
	

	<div class='form-group'>
		<label for ='qualification'>Qualification:</label>
		<input type='qualification' class='form-control' id='qualification' name = 'qualification' required="True"></input>
	</div>

	<div class='form-group'>
		<label for ='mobile-no'>Mobile No:</label>
		<input type='mobile-no' class='form-control' id='mobile-no' name = 'mobile-no' required="True"></input>
	</div>

	<div class='form-group'>
		<label for ='email-id'>Email Address:</label>	
		<input type='email-id' class='form-control' id='email' name = 'email-id' required="True"></input>
	</div>

	<div class='form-group'>
		<label for ='password'>Email password:</label>	
		<input type='password' class='form-control' id='password' name = 'password' required="True"></input>
	</div>
	
	<div class='form-group'>
		<label for ='password'>Confirm password:</label>	
		<input type='password' class='form-control'  required="True"></input>
	</div>


	<button type='submit' class = 'btn btn-submit' id ='validate'>Submit </button>
	<button type='reset' class = 'btn btn-submit'>Reset </button>
</form>

<!-- 
 to retreive the data from the data base and display it in the form of the table
-->

</body>
</html>