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
   $json = json_encode($table1);
   echo "{$_GET['callback']}($json)";
  }else {
   echo $table1;
  }
 }
 getwordCall();
?>
