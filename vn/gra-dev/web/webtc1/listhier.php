<?php
// web/webtc1/listhier.php
// Revised 06-28-2018 to work with revised webtc programs

if (isset($_GET['callback'])) {
 header('content-type: application/json; charset=utf-8');
 header("Access-Control-Allow-Origin: *");
}
$meta = '<meta charset="UTF-8">';
echo $meta; // why?

require_once('../webtc/dictcode.php');
require_once('listparm.php');
$getParms = new ListParm($dictcode);

require_once('listhiermodel.php');
$model = new ListHierModel($getParms);
$listmatches = $model->listmatches;
require_once('listhierview.php');
$view = new ListHierView($listmatches,$getParms);
$table = $view->table;
if (in_array($getParms->dict,array('ae','mwe','bor'))) {
 // for dictionaries with english headwords, no transcoding of list of words
 // This accomplished by transcoding from slp1 to slp1
 $table1 = transcoder_processElements($table,"slp1","slp1","SA");
} else {
 $table1 = transcoder_processElements($table,"slp1",$getParms->filter,"SA");
}
echo $table1;
exit;

?>
