<?php
// Enable error reporting
ini_set('display_errors', 1);
error_reporting(E_ALL);
header('Content-Type: application/json');

// Define your Python server endpoint
$python_server_url = "http://localhost:8090/query/";

// Read JSON input from the frontend
$input = json_decode(file_get_contents("php://input"), true);
$user_message = trim($input["message"] ?? "What is CISSE?");
// Ensure chat_history is an array, even if empty from the frontend
$chat_history = $input["chat_history"] ?? [];

if (!$user_message) {
    echo json_encode(["error" => "No message provided."]);
    exit;
}

// Prepare the payload for your Python server
// The Python server expects 'query' and 'chat_history'
$payload = [
    #ARTEM
    "query" => $user_message,
    "chat_history" => $chat_history // Send the chat history directly
];

// Call your Python server
$ch = curl_init($python_server_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json",
    // No Authorization header needed here, as the Python server handles OpenAI API key
]);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // Important for localhost if using HTTPS without proper certs
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));

$response = curl_exec($ch);

if (curl_errno($ch)) {
    echo json_encode(["error" => "Error connecting to Python server: " . curl_error($ch)]);
    exit;
}

if (!$response) {
    echo json_encode(["error" => "Empty response from Python server."]);
    exit;
}
curl_close($ch);

// Decode the response from your Python server
$result = json_decode($response, true);

if (!$result) {
    echo json_encode(["error" => "Invalid JSON response from Python server: " . $response]);
    exit;
}

// Check for errors returned by the Python server
if (isset($result["error"])) {
    echo json_encode(["error" => "Python server error: " . $result["error"]]);
    exit;
}
if (isset($result["detail"])) { // FastAPI error format
    echo json_encode(["error" => "Python server error: " . $result["detail"]]);
    exit;
}

// Extract ONLY the answer from the Python server's response
// Your Python server's /query/ endpoint returns 'summary_response'
#ARTEM
$answer = $result["summary_response"] ?? "No answer received from Python server.";

// Return only the 'answer' to the frontend
echo json_encode([
    "answer" => $answer
]);

?>
