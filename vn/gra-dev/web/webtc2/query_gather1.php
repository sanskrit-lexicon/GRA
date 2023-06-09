<?php
// web/webtc2/query_gather1.php
// 08-05-2020  Combines previous query_gather and query_multi
// Revised 06-29-2018, 09-07-2018
// 08-07-2020  Use GetwordClass
// This is more general -- Could be called elsewhere.
// Basic input is a 'data' POST parameter, which is a JSON array
// of keys which are currently required to be in SLP1 coding.
if (isset($_GET['callback'])) {
 header('content-type: application/json; charset=utf-8');
 header("Access-Control-Allow-Origin: *");
}
$meta = '<meta charset="UTF-8">'; 
//require_once('../webtc/dictcode.php');
require_once('../webtc/dbgprint.php');
require_once('../webtc/parm.php');
require_once('../webtc/getwordClass.php');

//$filter = $getParms->filter;  unused variable
echo "$meta\n";
if (isset($_POST['data'])) {
 $data = $_POST['data'];
 $keyar = json_decode($data);
}else {
 $data = "";
 $keyar = array();
}
$nkey = 0;

foreach($keyar as $key) {
 $nkey++;
 $_REQUEST['key'] = $key;
 $_REQUEST['input'] = 'slp1';
 $vm = new GetwordClass();
 $table1 = $vm->table1;
 $table0 = "<span class='key' id='record_$nkey' /></span>\n";
 echo $table0;
 echo $table1;
}
return;

?>
