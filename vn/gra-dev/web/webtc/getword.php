<?php
// Exclude WARNING messages also, to solve Peter Scharf Mac version.
error_reporting(E_ALL & ~E_NOTICE & ~E_WARNING);
?>
<?php
//getword.php
if (isset($_GET['callback'])) {
 header('content-type: application/json; charset=utf-8');
}
header("Access-Control-Allow-Origin: *");
require_once("getwordClass.php");
function getwordCall() {
  $temp = new GetwordClass();
  $table1 = $temp->table1;
  if (isset($_GET['callback'])) {
   $callback = $_GET['callback'];
   // Only allow a safe JSONP callback identifier. Echoing the raw callback
   // is a reflected-XSS / JSONP-injection vector, so reject anything else.
   // Mirrors the guard in csl-websanlexicon webtc/getword.php (issue #27, PR #63).
   if (!preg_match('/^[A-Za-z_$][A-Za-z0-9_$.]{0,127}$/',$callback)) {
    header('content-type: text/plain; charset=utf-8');
    http_response_code(400);
    echo "invalid callback";
    return;
   }
   $json = json_encode($table1);
   echo "{$callback}($json)";
  }else {
   echo $table1;
  }
 }
 getwordCall();
?>
