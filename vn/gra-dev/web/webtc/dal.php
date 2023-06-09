<?php
//error_reporting( error_reporting() & ~E_NOTICE );
?>
<?php
/* dal.php  Apr 28, 2015 Multidictionary access to sqlite Databases
 June 4, 2015 - use pywork/html/Xhtml.sqlite
 May 10, 2015 - also allow use of web/sqlite/X.sqlite
 June 29, 2018. Recode as a class.
*/
require_once('dictinfo.php');
require_once('dbgprint.php');
class Dal {
 public $dict;
 public $dictinfo;
 public $sqlitefile;
 public $file_db, $file_db_xml;
 public $dbg=false;
 public $dbname; 
 public $tabname;  # name of table in sqlitefile. 
 public $tabid;    # name of 'id' key used by getgeneral
 // 01-28-2020
 public $keydoc_file, $keydoc_db,$keydoc_tabname,$keydoc_tabid;
 public $devFlag; // development version if True.
 // dbname is assumed to be for auxiliary sqlite data, such as
 // abbreviations  xab.sqlite, xath.sqlite -- new Dal('mw','mwab')
 // Not yet implemented.  Would need to modify dictinfo for filenames also.
 public $status;
 public function __construct($dict,$dbname=null) {
  $this->dict=strtolower($dict);
  $this->dbname = $dbname;
  $this->dictinfo = new DictInfo($dict);
  $sqlitedir = $this->dictinfo->sqlitedir;
  if (isset($_REQUEST['dev']) && ($_REQUEST['dev'] == 'yes')) {
   $this->devFlag = True;
  }else {
   $this->devFlag = False;
  }
  if ($dbname == null) {
   $this->sqlitefile = "$sqlitedir/{$this->dict}.sqlite";
   $this->tabname = $this->dict;
   $this->tabid = 'key';
   dbgprint($this->dbg,"Dal construct. sqlitefile={$this->sqlitefile}, tabname={$this->tabname}\n");
   // 01-28-2020
   $this->keydoc_file = "$sqlitedir/keydoc.sqlite";
   $this->keydoc_tabname = 'keydoc';
   $this->keydoc_tabid = 'key';
  }else if ($dbname == "ab") {
   $this->tabname = $this->dict . "ab";
   $this->sqlitefile = "$sqlitedir/{$this->tabname}.sqlite";
   $this->tabid = 'id';
  }else if ($dbname == "bib") {  // author file for pwg, pw, pwkvn
   $this->tabname = $this->dict . "bib";
   $this->sqlitefile = "$sqlitedir/{$this->tabname}.sqlite";
   $this->tabid = 'id';
  }else if ($dbname == "authtooltips") {  // author file for mw
   $this->tabname = $this->dict . "authtooltips";
   $this->sqlitefile = "$sqlitedir/{$this->tabname}.sqlite";
   $this->tabid = 'key';
  }else { // unknown $dbname
   $this->file_db = null;
   $this->status=false;
   return;
  }
  // connection to sqlitefile
  $dbg=false;
  if (($this->sqlitefile) &&file_exists($this->sqlitefile)) {
  try {
   $this->file_db = new PDO('sqlite:' .$this->sqlitefile);
   $this->file_db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
   dbgprint($dbg,"dal.php: opened " . $this->sqlitefile . "\n");
   $this->status=true;
   $this->file_db_xml = $this->file_db;  
  } catch (PDOException $e) {
   $this->file_db = null;
   $this->file_db_xml = $this->file_db;  
   dbgprint($dbg,"dal.php: Cannot open " . $this->sqlitefile . "\n");
   $this->status=false;
  }
 } else {
   $this->file_db = null;
   $this->file_db_xml = null;
   #dbgprint($dbg,"dal.php: Cannot open " . $this->sqlitefile . "\n");
   $this->status=false;
 }
  // connection to keydoc file
  //$dbg=false;
  if (($this->keydoc_file) && file_exists($this->keydoc_file) && $this->devFlag) {
  try {
   $this->keydoc_db = new PDO('sqlite:' .$this->keydoc_file);
   $this->keydoc_db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
   dbgprint($dbg,"dal.php: opened " . $this->keydoc_file . "\n");
   #$this->status=true;
  } catch (PDOException $e) {
   $this->keydoc_db = null;
   dbgprint($dbg,"dal.php: Cannot open " . $this->keydoc_file . "\n");
   #$this->status=false; // 01-28-2020  currently, keydoc is optional
  }
 } else {
   $this->keydoc_db = null;
   dbgprint($dbg,"dal.php: File does not exist. Cannot open " . $this->keydoc_file . "\n");
   #$this->status=false; // 01-28-2020  currently, keydoc is optional
 }
 }
 public function close() {
  if ($this->file_db) {
   $this->file_db = null;  //ref: //php.net/manual/en/pdo.connections.php
  }
  if ($this->keydoc_db) {
   $this->keydoc_db = null;  //ref: //php.net/manual/en/pdo.connections.php
  }
  if ($this->file_db_xml) { // not sure of usage here
   $this->file_db_xml = null;  
  }
 }
 public function get($sql) {
  $ansarr = array();
  if (!$this->file_db) {
   //"file_db is null for $this->sqlitefile.
   return $ansarr;
  }
  $result = $this->file_db->query($sql);
  if ($result == false) {
   return $ansarr;
  }
  foreach($result as $m) {
   $rec = array($m['key'],$m['lnum'],$m['data']);
   $ansarr[]=$rec;
  }
  return $ansarr; 
 }
 public function get_xml($sql) {
  $ansarr = array();
  if (!$this->file_db_xml) {
   dbgprint($this->dbg, "file_db_xml is null. sqlitefile={$this->sqlitefile}\n");
   return $ansarr;
  }
  $result = $this->file_db_xml->query($sql);
  foreach($result as $m) {
   $rec = array($m['key'],$m['lnum'],$m['data']);
   $ansarr[]=$rec;
  }
  return $ansarr; 
 }
 public function get1($key) {
  // Returns associative array for the records in dictionary with this key
  $sql = "select * from {$this->dict} where key='$key' order by lnum";
  return $this->get($sql);
 }
 public function get1_xml($key) {
  // Returns associative array for the records in dictionary with this key
  $sql = "select * from {$this->dict} where key='$key' order by lnum";
  dbgprint($this->dbg, "get1_xml, sql=$sql\n");
  return $this->get_xml($sql);
 }

 public function get2($L1,$L2) {
  //  Used in listhier
  // returns an array of records, one for each L-value in the range
  // $L1 <= $L <= $L2
  // each record is an array with three elements: key,lnum,data
  $sql="select * from {$this->dict} where  $L1 <= lnum and lnum <= $L2  order by lnum"; 
  return $this->get($sql);
 }
 public function get3($key) {
  // returns an array of records, which start like $key
  $sql = "select * from {$this->dict} where key LIKE '$key%' order by lnum";
  return $this->get($sql);
 }

 public function get3a_keydoc($key,$max) {
  // returns an array of records, which start like $key
  // Setting a pragma must for case_sensitive
  $dbg=False;
  $db = $this->keydoc_db;
  if ($db == null) {return array();}
  $pragma="PRAGMA case_sensitive_like=true;";
  $db->query($pragma);
  $sql = " select * from {$this->keydoc_tabname} where {$this->keydoc_tabid} LIKE '$key%' LIMIT $max";
  dbgprint($dbg,"get3a_keydoc: sql=$sql\n");
 $result = $db->query($sql);
 dbgprint($dbg,"get3a_keydoc $key->" . count($result) . "\n");
 $keys = array();
 foreach($result as $m) {
  // expect th
  // $m[1] is a string.  A comma-separated list of keys
  $newkeys = explode(",",$m['data']);
  dbgprint($dbg,"{$m['key']} -> {$m['data']}\n");
  foreach($newkeys as $newkey) {
   $keys[] = $newkey;
  }
 }
 // Now, access xxx.sqlite for each key
 $arr = array();
 foreach($keys as $key1) {

  $sql = " select * from {$this->dict} where key='$key1' order by lnum;" ;
  $ans1 = $this->get($sql);
  dbgprint($dbg,"get3a_keydoc($key1) ans1 has " . count($ans1) . "results\n");
  if (count($ans1) > 0) {
   $rec = $ans1[0];
   $lnum = floatval($rec[1]);
   $lnum1 = $lnum * 1000.0;
   $sortkey = intval($lnum1);
   $arr[$sortkey] = $ans1[0];
   dbgprint($dbg,"get3a_keydoc($key): $sortkey\n");
  }
 }
 ksort($arr);
 $ansarr = array();
 $nrecs = 0;
 foreach($arr as $x=>$rec) {
  $ansarr[] = $rec;
  $nrecs = $nrecs + 1;
  if ($nrecs >= $max) {
   break;
  }
 }
 
 return $ansarr;
 }

 public function get3a($key,$max) {
  // returns an array of records, which start like $key
  // Setting a pragma must for case_sensitive
  $dbg=False;
  if ($this->keydoc_db != null) {
   dbgprint($dbg,"get3a: using get3a_keydoc\n");
   return $this->get3a_keydoc($key,$max);
  }
  dbgprint($dbg,"get3a: keydoc not available\n");
  
  $db = $this->file_db;
  $pragma="PRAGMA case_sensitive_like=true;";
  $db->query($pragma);
  $sql = " select * from {$this->dict} where key LIKE '$key%' order by lnum LIMIT $max";
  return $this->get($sql);
 }
 public function prev_get3a($key,$max) {
  // returns an array of records, which start like $key
  // Setting a pragma must for case_sensitive
  $pragma="PRAGMA case_sensitive_like=true;";
  $this->file_db->query($pragma);
  $sql = " select * from {$this->dict} where key LIKE '$key%' order by lnum LIMIT $max";
  return $this->get($sql);
 }

 public function get3b($key,$max) {
 /*
 returns an array of records, where 'key' is like $key
 The wildcards for sqlite are: 
   (ref=https://www.sqlitetutorial.net/sqlite-like/)
 The percent sign % wildcard matches any sequence of zero or more characters.
 The underscore _ wildcard matches any single character.
 Setting a pragma for case_sensitive
*/
  $pragma="PRAGMA case_sensitive_like=true;";
  $this->file_db->query($pragma);
  $sql = " select * from {$this->dict} where key LIKE '$key' order by lnum LIMIT $max";
  return $this->get($sql);
 }

public function get4a($lnum0,$max) {
  //  Used in listhier
  // in mw, with L=99930.1, $lnum0 appears as if L=99930.1000000001
  // To guard against this, we round lnum0 to 3 decimal places.
  //  [This is consistent with the schema definition]
  $lnum0 = round($lnum0,3);
  $sql = "select * from {$this->dict} where (lnum < '$lnum0') order by lnum DESC LIMIT $max";
  return $this->get($sql);
 }
 public function get4b($lnum0,$max) {
  //  Used in listhier
  // in mw, with L=99930.1, $lnum0 appears as if L=99930.1000000001
  // To guard against this, we round lnum0 to 3 decimal places.
  //  [This is consistent with the schema definition]
  $lnum0 = round($lnum0,3);
  $sql = "select * from {$this->dict} where ('$lnum0' < lnum) order by lnum LIMIT $max";
  return $this->get($sql);
 }
 /* Alternate test version for mw
   Jul 19, 2015
 */
public function get1_keydoc_keys($key) {
 // 01-28-2020.  using keydoc.sqlite database and xxx.sqlite
 $dbg=False;
  $pragma="PRAGMA case_sensitive_like=true;";
  $this->keydoc_db->query($pragma);
  $sql = " select data from {$this->keydoc_tabname} where {$this->keydoc_tabid}='$key';";
 $result = $this->keydoc_db->query($sql);
 // $result is an array; expect it to be of length = 0 or 1
 $keys = array();
 foreach($result as $m) {
  // expect th
  // $m is a string.  A comma-separated list of keys
  $newkeys = explode(",",$m[0]);
  foreach($newkeys as $newkey) {
   $keys[] = $newkey;
  }
 }
return $keys;
}
public function get1_keydoc($key) {
 // 01-28-2020.  using keydoc.sqlite database and xxx.sqlite
 $dbg=False;
 #$dbg=True;
 $keys = $this->get1_keydoc_keys($key);
 $recs = array();
 $nrecs = 0;
 foreach($keys as $key) {
  $recs1 = $this->get1($key);
  foreach($recs1 as $rec) {
   // $rec is array($m['key'],$m['lnum'],$m['data'])
   // assume lnum is a string representing a floating point number
   // key may be integer or string.  Next loses items
   //
   //$sortkey = floatval($rec[1]); 
   // We know our lnum has at most 3 decimal places 
   // 02-09-2020 skip records which come from alternate headwords
   // These have '<alt>' tag
   $data = $rec[2];
   if (preg_match('/<alt>/',$data)) {
    continue;
   }
   $lnum = floatval($rec[1]);
   $lnum1 = $lnum * 1000.0;
   $sortkey = intval($lnum1);
   $recs[$sortkey] = $rec;
   $nrecs = $nrecs + 1;
   $type = gettype($rec[1]);
   dbgprint($dbg,"$sortkey, {$rec[0]}, {$rec[1]} ($type)\n");
  }
 }
 dbgprint($dbg,"nrecs=$nrecs\n");
 //sort by $m['lnum'], treated as a float
 ksort($recs);
 $ans = array();
 foreach($recs as $x=>$rec) {
  $ans[] = $rec;
 }
 $nans = count($ans);
 dbgprint($dbg,"count of ans = $nans\n");
 return $ans;
}
public function get1_mwalt($key) {
 // 05-03-2018. Based on dal_get1_mwalt.php of apidev
 // This code initially copied from mw/web/webtc/dal_sqlite.php
 // and adjusted for use within Dal class.
 // 01-28-2020.  replaced
$dbg=False;
if ($this->keydoc_db) { // use keydoc if it is available
 return $this->get1_keydoc($key);
}else {
 return $this->get1_mwalt_prev($key);
}
}
public function get1_mwalt_prev($key) {
$dbg=False;
# first step is to call the original dal_mw1_get1
$recs = $this->get1($key);
$nrecs = count($recs);
// 07-15-2018. When no recs found, return $recs
if ($nrecs == 0) {
 return $recs;
}
// Step 1: fill in forward gaps in $recs
$newitems=array();
// So defined even if next loop doesn't run. Else error at line 415
$lnum1 = -1; 
for($i=0;$i<$nrecs-1;$i++) {
 $item0 = $recs[$i];  // key,lnum,data
 $item1 = $recs[$i+1];
 $newitems[] = $item0;
 $lnum1 = $item1[1];
 while(True) {
  $lnum0 = $item0[1];
  $hcode0 = $this->dal_mw1_hcode($item0[2]); // data = <Hx>{rest} ==> Hx
  $item00 = $item0[0];
  dbgprint($dbg,"Chk 1: $lnum0, $hcode0, $item00\n");
  $temprecs = $this->get4b($lnum0,1);
  if(count($temprecs) != 1) { // only at last record in database
   break;
  }
  $rec = $temprecs[0]; // key,lnum,data
  $lnum = $rec[1];
  if ($lnum == $lnum1) {
   break;
  }
  $hcode = $this->dal_mw1_hcode($rec[2]);
  if (strlen($hcode) != 3) { //is $hcode like HnA, HnB, HnC ?
   break;
  }
  if(substr($hcode0,0,2) != substr($hcode,0,2)) {
   break;
  }
  // We have another rocord
  $newitems[] = $rec;
  $item0 = $rec;
 } // while True
} // for($i)
// Add the last record of $dispItems
$item0 = $recs[$nrecs-1];
$newitems[] = $item0;
if ($dbg) {
 $lnum0 = $item0[1];
 $hcode0 = $this->dal_mw1_hcode($item0[2]); // data = <Hx>{rest} ==> Hx
 $item00 = $item0[0];
 dbgprint($dbg,"Chk 1-LAST: $lnum0, $hcode0, $item00\n");
}
// Add any records after last record of $dispItems
 while(True) {
  $lnum0 = $item0[1];
  $hcode0 = $this->dal_mw1_hcode($item0[2]); // data = <Hx>{rest} ==> Hx
  $this->get4b($lnum0,1);
  $temprecs = $this->get4b($lnum0,1);
  if(count($temprecs) != 1) { // only at last record in database
   break;
  }
  $rec = $temprecs[0]; // key,lnum,data
  $lnum = $rec[1];
  if ($lnum == $lnum1) {
   break;
  }
  $hcode = $this->dal_mw1_hcode($rec[2]);
  if (strlen($hcode) != 3) { //is $hcode like HnA, HnB, HnC ?
   break;
  }
  if(substr($hcode0,0,2) != substr($hcode,0,2)) {
   break;
  }
  // We have another rocord
  $newitems[] = $rec;
  $item0 = $rec;
  if ($dbg) {
   $lnum0 = $item0[1];
   $hcode0 = $this->dal_mw1_hcode($item0[2]); // data = <Hx>{rest} ==> Hx
   $item00 = $item0[0];
   dbgprint($dbg,"Chk 1-extra: $lnum0, $hcode0, $item00\n");
  }
 } // end while
// reset $recs as $newitems
$recs = $newitems;
$nrecs = count($recs);
// Step 2. fill in backward gaps in $recs
//    Similar to Step 1, but backwards
$newitems = array();
for($i=$nrecs-1;$i>0;$i--) {
 $item0 = $recs[$i];  // key,lnum,data
 $item1 = $recs[$i-1];
 $newitems[] = $item0;
 $lnum1 = $item1[1];
 while(True) {
  $lnum0 = $item0[1];
  $hcode0 = $this->dal_mw1_hcode($item0[2]); // data = <Hx>{rest} ==> Hx
  dbgprint($dbg,"Chk 2: $lnum0, $hcode0, $item00\n");
  $item00 = $item0[0];
  $temprecs = $this->get4a($lnum0,1);
  if(count($temprecs) != 1) { // only at last record in database
   break;
  }
  $rec = $temprecs[0]; // key,lnum,data
  $lnum = $rec[1];
  if ($lnum == $lnum1) {
   break;
  }
  $hcode = $this->dal_mw1_hcode($rec[2]);
  if (strlen($hcode0) != 3) { //is $hcode0 like HnA, HnB, HnC ?
   break;
  }
  if(substr($hcode0,0,2) != substr($hcode,0,2)) {
   break;
  }
  // We have another rocord
  $newitems[] = $rec;
  if ($lnum0 == $lnum) {
    break;  // 2017-07-24  ? why needed
  }
  $item0 = $rec;
 } // while True
} // end step 2
// Add the first record 
$item0 = $recs[0];
$newitems[] = $item0;
// Get ones occurring Before first record 
if ($dbg) {
 $lnum0 = $item0[1];
 $hcode0 = $this->dal_mw1_hcode($item0[2]); // data = <Hx>{rest} ==> Hx
 $item00 = $item0[0];
 dbgprint($dbg,"Chk 2-LAST: $lnum0, $hcode0, $item00\n");
}

 while(True){
  $lnum0 = $item0[1];
  $hcode0 = $this->dal_mw1_hcode($item0[2]); // data = <Hx>{rest} ==> Hx
  $item00 = $item0[0];
  dbgprint($dbg,"Chk 2a: $lnum0, $hcode0, $item00\n");
  $temprecs = $this->get4a($lnum0,1);
  if(count($temprecs) != 1) { // only at last record in database
   break;
  }
  $rec = $temprecs[0]; // key,lnum,data
  $lnum = $rec[1];
  /* why skip this ?
  if ($lnum == $lnum1) {
   break;
  }
  */
  $hcode = $this->dal_mw1_hcode($rec[2]);
  if (strlen($hcode0) != 3) { //is $hcode like HnA, HnB, HnC ?
   break;
  }
  if(substr($hcode0,0,2) != substr($hcode,0,2)) {
   break;
  }
  // We have another rocord
  $newitems[] = $rec;
  /*
  if ($lnum0 == $lnum) {
    break;  // 2017-07-24  ? why needed
  }
  */
  $item0 = $rec;
  if ($dbg) {
   $lnum0 = $item0[1];
   $hcode0 = $this->dal_mw1_hcode($item0[2]); // data = <Hx>{rest} ==> Hx
   $item00 = $item0[0];
   dbgprint($dbg,"Chk 2-extra: $lnum0, $hcode0, $item00\n");
  }
 }
// newitems is 'backwards' lnum order. Get it back in forward lnum order
$nitems = count($newitems);
$newitems1=$newitems;
$newitems=array();
for($i=$nitems-1;$i>=0;$i--) {
 $newitems[]=$newitems1[$i];
 if ($dbg) {
  $item0 = $newitems1[$i];
  $lnum0 = $item0[1];
  $hcode0 = $this->dal_mw1_hcode($item0[2]); // data = <Hx>{rest} ==> Hx  
  $item00 = $item0[0];
  dbgprint($dbg,"Chk 3: $lnum0, $hcode0, $item00\n");
 }
}
 $ans=$newitems;
 return $ans;
}

public function dal_mw1_hcode($data){
 if (preg_match('/^<(H.*?)>/',$data,$matches)) {
  return $matches[1];
 }else {
  return ""; // should not happen
 }
} 
public function getgeneral($key,$table) {
  if (!$this->file_db) {
   //"file_db is null for $this->sqlitefile.
   return array();
  }
#$sql = "select * from $table where id='$key'";
$key = str_replace("'","''",$key); // 02-08-2020
$sql = "select * from $table where {$this->tabid}='$key'";
$result = $this->file_db->query($sql);
$ansarr = array();
foreach($result as $m) {
 $ansarr[] = $m;
}
return $ansarr;
}
}
?>
