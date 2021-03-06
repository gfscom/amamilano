<?php
  $content = file_get_contents("php://input");
  $update = json_decode($content, true);
  if(!$update) { exit; }

  $message = isset($update['message']) ? $update['message'] : "";
  $messageId = isset($message['message_id']) ? $message['message_id'] : "";
  $chatId = isset($message['chat']['id']) ? $message['chat']['id'] : "";
  $firstname = isset($message['chat']['first_name']) ? $message['chat']['first_name'] : "";
  $lastname = isset($message['chat']['last_name']) ? $message['chat']['last_name'] : "";
  $username = isset($message['chat']['username']) ? $message['chat']['username'] : "";
  $date = isset($message['date']) ? $message['date'] : "";
  $text = isset($message['text']) ? $message['text'] : "";

  $text = trim($text);
  $text = strtolower($text);
  header("Content-Type: application/json");

  $response = '';

  if(strpos($text, "/engage") === 0 || strpos($text, "/engage@AmaMilanoBot")) {
    $f_contents = file("verbs.txt");
    $line = $f_contents[rand(0, count($f_contents) - 1)];
    $verb = trim($line);
    $verb .= 'MILANO';
  	$response = 'Lascio colare un po\' di engagement: '. $verb;
  	//DEBUG $response = $verb;

  } elseif(strpos($text, "/version") === 0 || strpos($text, "/version@AmaMilanoBot")) {
    $file="verbs.txt";
    $linecount = 0;
    $handle = fopen($file, "r");
    while(!feof($handle)){
      $line = fgets($handle);
      $linecount++;
    }
    fclose($handle);
    $response = '#AmaMilano versione 0.5, edizione "SalaStopSmartWorking"';
	  $response .= chr(10).'Voci caricate in libreria: '.$linecount;
	  $response .= chr(10).'https://github.com/gfscom/amamilano/blob/master/verbs.txt';
  } else {}

  $parameters = array('chat_id' => $chatId, "text" => $response);
  $parameters["method"] = "sendMessage";
  echo json_encode($parameters);
