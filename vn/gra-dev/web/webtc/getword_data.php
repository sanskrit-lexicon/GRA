<?php
error_reporting(E_ALL & ~E_NOTICE );
?>
<?php 
/* getword_data.php
 class to get the html data for getword.php
*/
require_once('dbgprint.php');
require_once('dal.php');
require_once('basicadjust.php');
require_once('basicdisplay.php');

class Getword_data {
 /* $matches contains array of records. 
   Each record is an array with three elements:
   - key
   - lnum (cologne id)
   - computed html string
 */
 public $matches;  
 public function __construct() {
 $dbg=false;
 $getParms = new Parm();
 $dict = $getParms->dict;
 dbgprint($dbg,"getword_data.php #1 getword_data_html\n");
 $dal = new Dal($dict);
 $key = $getParms->key;
 dbgprint($dbg,"getword_data.php #2: key=$key, dict=$dict \n");
  // xmlmatches is array of records rec, where
  // rec is array with 3 items:
  //  0: key0  the headword of the record (usu. but not always same as key)
  //  1: lnum0 The Cologne id
  //  2: data:  xml string from xxx.xml
 $xmlmatches = $dal->get1_mwalt($key); 
 $dal->close();

  $xmldata = [];
  for ($i=0;$i<count($xmlmatches);$i++) {
   $xmlmatch = $xmlmatches[$i];
   list($key0,$lnum0,$xmldata0) = $xmlmatch;
   $xmldata[] = $xmldata0;
  }
  $adjxml = new BasicAdjust($getParms,$xmldata);
  $adjmatches = $adjxml->adjxmlrecs;

  $htmlmatches = [];
  for($i=0;$i<count($xmlmatches);$i++) {
   $xmlmatch = $xmlmatches[$i];
   list($key0,$lnum0,$xmldata0) = $xmlmatch;
   $adjxmldata0 = $adjmatches[$i];
   $html = $this->getword_data_html_adapter($key0,$lnum0,$adjxmldata0,$dict,$getParms,$xmldata0);
   $htmlmatches[] = array($key0,$lnum0,$html);
  }
 if ($dbg) {
  dbgprint($dbg,"getword_data returns:\n");
  for($i=0;$i<count($htmlmatches);$i++) {
   dbgprint($dbg,"record $i = {$htmlmatches[$i][2]}\n"); //[0] $htmlmatches[$i][1] $htmlmatches[$i][2] \n");
  }
 }
 $this->matches = $htmlmatches;
}
/* ------------------------------
  getword_data_html_adapter and related functions
*/
public function getword_data_html_adapter($key,$lnum,$adjxml,$dict,$getParms,$xmldata)
{
 // 08-07-2020.  This is the only place where BasicAdjust and
 // BasicDisplay are called.
 // We don't need to have arrays of strings, but only one string
 //  ($data is a string, one record  from xxx.xml)
 // BasicDisplay is written to allow a string for the second argument.
 /*
 $matches1=array($data);
 $adjxml = new BasicAdjust($getParms,$matches1);
 $matches = $adjxml->adjxmlrecs;
 */
 $filter = $getParms->filter;
 $display = new BasicDisplay($key,array($adjxml),$filter,$dict);
 $row1 = $display->row1;
 $row1x = $display->row1x; 
 $row = $display->row;
 $info = $row1;
 if ($row1x == '') { // True except for some mw verbs
  $body = "$row";
 } else {
  $body = "$row1x<br>$row";
 }
 $dbg=false;
 dbgprint($dbg,"adapter\n");
 dbgprint($dbg,"info = $info\n");
 dbgprint($dbg,"body = $body\n");

 # adjust body
 $body = preg_replace('|<td.*?>|','',$body);
 $body = preg_replace('|</td></tr>|','',$body);
 if ($dict == 'mw') {
  // in case of MW, we remove [ID=...]</span>
  $body = preg_replace('|<span class=\'lnum\'.*?\[ID=.*?\]</span>|','',$body);
 }
 # adjust $info - keep only the displayed page
 if ($dict == 'mw') {
  if(!preg_match('|>([^<]*?)</a>,(.*?)\]|',$info,$matches)) {
   dbgprint(true,"html ERROR 2: \n" . $info . "\n");
   exit(1);
  }
  $page=$matches[1];
  $col = $matches[2];
  $pageref = "$page,$col";
 }else {
  if(!preg_match('|>([^<]*?)</a>|',$info,$matches)) {
   dbgprint(true,"html ERROR 2: \n" . $info . "\n");
   exit(1);
  }
  $pageref=$matches[1];
 }
 if ($dict == 'mw') {
  list($hcode,$key2,$hom) = $this->adjust_info_mw($xmldata); 
  # construct return value as colon-separated values
  if ($getParms->basicOption) {
   $hom="";
  }
  $infoval = "$pageref:$hcode:$key2:$hom";
  $ans = "<info>$infoval</info><body>$body</body>";
 }else {
  # construct return value
  $ans = "<info>$pageref</info><body>$body</body>";
 }
 return $ans;
}

public function adjust_info_mw($data) {
 # In case of MW, also retrieve Hcode and hom from head of $data
 $hom='';
 if (preg_match('|</key2><hom>(.*?)</hom>|',$data,$matches)) {
  $hom = $matches[1];
 }
 $hcode='';
 if (preg_match('|^<(H.*?)>|',$data,$matches)) { // always matches
  $hcode=$matches[1];
 }
 $key2='';
 if (preg_match('|<key2>(.*?)</key2>|',$data,$matches)) {
  $key2 = $matches[1];
 }
 $key2a = $this->adjust_key2_mw($key2);
 return array($hcode,$key2a,$hom);
}
public function adjust_key2_mw($key2) {
 $ans = preg_replace('|--+|','-',$key2);  // only 1 dash
 $ans = preg_replace('|<sr1?/>|','~',$ans); # ~ not in key1 for MW (?)
 $ans = preg_replace('|<srs1?/>|','@',$ans); # @ not in SLP1
 // Leave some xml in place:
 // <root>kf</root>
 // <root/>daMh
 // dA<hom>1</hom>
 // <shortlong/>
 $ans1 = preg_replace('|</?root/?>|','',$ans);
 $ans1 = preg_replace('|</?hom>|','',$ans1);
 $ans1 = preg_replace('|<shortlong/>|','',$ans1);
 if (preg_match('|<|',$ans1)) {
  #dbgprint(true,"adjust_key2: $ans1\n");
  exit(1);
 }
 return $ans;
 $ans = preg_replace('||','',$ans);
 $ans = preg_replace('||','',$ans);
 return $ans;
}
}
?>
