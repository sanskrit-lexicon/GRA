<?php
// modified June 24, 2013 to allow search for sanskrit words in body of text
// modified Nov 25,2013 for pwg.
if (isset($_GET['callback'])) {
 header('content-type: application/json; charset=utf-8');
}
 header("Access-Control-Allow-Origin: *");
$dbg = false;
require_once("../webtc/dbgprint.php");
require_once('../webtc/dictcode.php');
require_once('queryparm.php');
require_once('querymodel.php');
$getParms = new QueryParm($dictcode);

$model = new QueryModel($getParms);
if ($model->status == false) {
 echo $model->errmsg;
 exit;
}
$qmatches = $model->querymatches;
$lastLnum = $model->lastLnum;

// construct answer as an associative array, which is passed as JSON
// A Javascript routine in main.js will construct the html.
// Fields of $ans:
// 'lastlnum' value is numeric. last line number searched in query_dump
// 'dict'  Dictionary code (probably unused)
// 'data'  An array of 'objects' (associative arrays). Each object has Fields,
//     with string values:
//      'key'  SLP1 form of headword
//      'keyout'  Transcoding of key, using the output filter
//      'matchword'  Blank, except for text searches; then the word matching.
$ans = construct_outputarr($getParms,$model,$dictcode,$getParms->filter);
$json = json_encode($ans);
if(isset($_GET['callback'])) {
 echo "{$_GET['callback']}($json)";
}else {
 echo $json;
}

function construct_outputarr($getParms,$model,$dict,$filter) {
 $dbg=false;
 // $model is a QueryModel object
 //$dict = $queryParms->dict;
 $qmatches = $model->querymatches;
 $lastLnum = $model->lastLnum;
 $resultarr = array();
 $resultarr['lastlnum'] = $lastLnum;
 $resultarr['dict'] = $dict;
 $resultarr['filter'] = $filter;
 $keyarr = [];
 if (count($qmatches) == 0) {
  $resultarr['status'] = 400;
  $resultarr['data'] = $keyarr;
  // $errmsg = "<p>No matches found</p>";
  // $resultarr['errmsg'] = $errmsg;   
  return $resultarr;
 }
 
 $nx=0;
 //$xmlnew = "<p class='words'>\n";
 $search_regexp_nonSanskrit = $model->search_regexp_nonSanskrit;
 foreach($qmatches as $qmatch) {
  $nx++;
  $key = $qmatch['key'];
  $matchword = $qmatch['matchword'];
  $keyout = $key;  
  //$xmlcur="";
  if (in_array($dict,array('ae','mwe','bor'))) {
   $keyout = $key; // for English headword, no need to transcode key.
  }else {
   $keyout = transcoder_processString($key,"slp1",$filter);
   // for English headword, no need to transcode key.
   //$xmlcur .= "$nx <!-- $key --><a class='words' onclick='getWord4(\"$nx\");'>$key</a>";
  }
  $datarr = array();
  $datarr['key'] = $key;
  $datarr['keyout'] = $keyout;
  $datarr['matchword'] = $matchword;
  $keyarr[] = $datarr;
 }
 $resultarr['data'] = $keyarr;
 return $resultarr;
}

?>
