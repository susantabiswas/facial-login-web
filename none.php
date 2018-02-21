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

// getting the data from the registration form into variables
$students_name = $_GET['students-name'];
$fathers_name = $_GET['fathers-name'];
$postal_address = $_GET['postal-address'];
$permanent_address =$_GET['permanent-address'];
$pincode = $_GET['pincode'];
$sex = $_GET['sex'];
$qualification  =$_GET['qualification'];
$mobile_no = $_GET['mobile-no'];
$email_address = $_GET['email-id'];
$password  = $_GET['password'];
	

//constructing the sql query
$sql = "INSERT INTO students (students_name,fathers_name,postal_address,permanent_address,
       pincode, sex, qualification, mobile_no, email_id,password)
        VALUES ('".$students_name."','"
        .$fathers_name."','"
        .$postal_address."','"
        .$permanent_address."','"
        .$pincode."','"
        .$sex."','"
        .$qualification."','"
        .$mobile_no."','"
        .$email_address."','"
        .$password."')";


// check if the data is inserted into the data base sucessfully
if($conn->query($sql) === True){
       	print("record inserted into the table sucessfully\n");
       } 
       else
       	print("problem in inserting record into the table\n");


      $conn->close();

?>