<?php
// create a new connection with the data base
$server = "localhost";
$hosname = "root";
$pass = "";
$user="";
$dbname = "test";
$conn  = new mysqli($server,$hosname,$pass,$dbname);

// check the connection
if($conn)
	print('connected to the data base <br/>');
else
	print('failed to connect <br/>');

//getting the required information from the html form

$email_address = $_GET['Email-id'];
$password  = $_GET['password'];

$sql = "SELECT * from students";
$result = $conn->query($sql);

$flag = 0;
if ($result->num_rows > 0) 
{
    // output data of each row
    while($row = $result->fetch_assoc()) 
    {
    	// if the email id and the password matches with any one of the rows in the data base 
    	if(strcmp($email_address,$row['email_id'])==0 and strcmp($password,$row['password']) ==0 )
    	{
    		print("inside the loop");
    		
    		$flag = 1;
    		//starting a new session
    		session_start();
    		//setting session variables
    		
    		$_SESSION['email_id'] = $email_address;
    		$_SESSION['password'] = $password;
    		header( "location: http://localhost/homepage.php"); 
    		break;
       	} 
    }
}
// in case no such email id and password conversation exists
if($flag == 0)
{
	print("no such user with this email id and password found in the data base<br/>");
}
