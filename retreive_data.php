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
	print('failed to connect <br/');


$sql = "SELECT * from students";
$result = $conn->query($sql);
?>
<!-- <h1 style="text-align: center;">DETAILS OF THE STUDENTS</h1> -->
 <table style="width:100%">
<tr style="background-color:lightblue;">
	<th>id</th>
	<th>students name</th>
	<th>fathers name</th>
	<th>postal address</th>
	<th>permanent address</th>
	<th>pincode</th>
	<th>sex</th>
	<th>qualification</th>
	<th>mobile no</th>
	<th>email id</th>
	<th>password</th>
</tr>

<?php
$counter = 0;
if ($result->num_rows > 0) 
{
    // output data of each row
    while($row = $result->fetch_assoc()) {
    	if($counter %2 == 0)
    		print('<tr  style="background-color:pink">');
    	else
    		print('<tr  style="background-color:#FF7043">');
    	
    	$counter = $counter + 1;
    	?>
    	<td>
    	<?php
        print($row['id']);
        ?>
    	</td>
        

        <td>
    	<?php
        print($row['students_name']);
        ?>
    	</td>
        

        <td>
    	<?php
        print($row['fathers_name']);
        ?>
    	</td>
        

        <td>
    	<?php
        print($row['postal_address']);
        ?>
    	</td>
        

        <td>
    	<?php
        print($row['permanent_address']);
        ?>
    	</td>
        

        <td>
    	<?php
        print($row['pincode']);
        ?>
    	</td>
        
        <td>
    	<?php
        print($row['sex']);
        ?>
    	</td>
        

        <td>
    	<?php
        print($row['qualification']);
        ?>
    	</td>
        


        <td>
    	<?php
        print($row['mobile_no']);
        ?>
    	</td>
        


        <td>
    	<?php
        print($row['email_id']);
        ?>
    	</td>

    	<td>
    	<?php
        print($row['password']);
        ?>
    	</td>


        </tr>
        <?php
    }
}
 else 
 {
    echo "0 results";
}
$conn->close();



?>

</table>