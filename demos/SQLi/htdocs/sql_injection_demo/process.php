<?php
// Simulating a connection to a MySQL database (using local server)
$servername = "localhost";
$username = "root"; // Default username for MAMP
$password = "root"; // Default password for MAMP
$dbname = "demo_db"; // Database name where users table exists

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get user input
$user = $_POST['username'];
$pass = $_POST['password'];

// Vulnerable SQL query without prepared statements
$query = "SELECT * FROM users WHERE username = '$user' AND password = '$pass'";

$result = $conn->query($query);

// Check if query returned any result
if ($result->num_rows > 0) {
    // Success message if credentials are correct
    echo "Login successful!";
} else {
    // Failure message if credentials are incorrect
    echo "Invalid credentials!";
}

$conn->close();
?>