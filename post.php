<?php
$server = "";
$username = "";
$password = "";
$dbname = "OpRw";
$pass = (string)$_POST['pass'];
$id = (string)$_POST['id'];

// Create connection
$conn = new mysqli($server, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "INSERT INTO Data (pass, id) VALUES ('$pass', '$id');";

if ($conn->query($sql) === TRUE) {
    echo "Ok.";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>

