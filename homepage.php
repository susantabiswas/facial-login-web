<?php
session_start();

// checking if the session variable is set or not
if(isset($_SESSION['email_id']))
{
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
	print('failed to connect <br/');


//making an sql query to  get the details of the user
$sql = 'SELECT * from students where email_id="'.$_SESSION['email_id'].'"';
$result = $conn->query($sql);

if ($result->num_rows > 0) 
{
    // output data of each row
    while($row = $result->fetch_assoc()) 
    {
    	 print('WELCOME: '.$row['students_name']); 
    }
}

//ending the session 
session_destroy();
}
else
{
	// the person should not be here and is redirected to the dashboard
	header('Location:index.php');

}

?>