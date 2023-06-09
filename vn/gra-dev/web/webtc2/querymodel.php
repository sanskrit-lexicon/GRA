<?php error_reporting (E_ALL & ~E_NOTICE & ~E_WARNING); //querymodel.php
require_once("../webtc/dal.php");
require_once("../webtc/dbgprint.php");
class QueryModel{
 // Gathers a collection of dictionary records 
 public $querymatches; // primary result of constructor
 public $dict; 
 public $status,$lastLnum;
 public $queryParms;
 public $errmsg;
 public $word;
 public $fp;
 public $search_regexp_nonSanskrit;
 public $sopt_case;
 public function __construct($queryParms) {
  $this->dict = $queryParms->dict;
  //$this->dal = new Dal($this->dict);
  $this->queryParms = $queryParms;
  $this->querymatches = array();
  $this->word = $queryParms->word;
  $this->sopt_case = false;
  $n = 0;
  $xmldata;
  $xmlnew="";
  $wordin="";
  if (!($this->openfile())) {return;}

  if ($this->word !="") {
   $this->match_nonSanskrit();
  }else if (($this->queryParms->opt_stransLit) && ($this->queryParms->opt_sword))  {
   $this->match_Sanskrit();
  }
  fclose($this->fp);
 }
 public function openfile() {
  $this->fp = fopen($this->queryParms->filename,"r");
  if (!$this->fp) {
   $this->status = false;
   $this->errmsg = "Could not open Dictionary '{$this->queryParms->filename}'";
   return false;
  }else {
   return true;
  }
 }
 public function match_nonSanskrit() {
   $non_word = "[^a-zA-Z0-9]";
   $wordreg = "[a-zA-Z0-9-]";
   /*
   $wordchrs = preg_split ('/[^a-zA-Z.*?+]/',$this->word);
   $this->word = join('',$wordchrs);
   */
   $wordin = $this->word;
   $word = $this->word; // for simplicity in following string expressions
   $word = mb_strtolower($word);
   if ($this->queryParms->opt_regexp == "exact"){
    $search_regexp = "[\t].*$non_word($word)$non_word";
   }else if ($this->queryParms->opt_regexp == "prefix") {
    $search_regexp = "[\t].*$non_word($word$wordreg+)$non_word";
   }else if ($this->queryParms->opt_regexp == "suffix") {
    $search_regexp = "[\t].*$non_word($wordreg+$word)$non_word";
   }else if ($this->queryParms->opt_regexp == "instring"){
    $search_regexp = "[\t].*$non_word($wordreg+$word$wordreg+)$non_word";
   }else if ($this->queryParms->opt_regexp == "substring"){
    $search_regexp = "[\t].*$non_word($wordreg*$word$wordreg*)$non_word";
   }else {
    $search_regexp = "[\t].*$word";
   } 
   $this->search_regexp_nonSanskrit = $search_regexp;
   $search_opt = $this->sopt_case;
   $tempar = $this->matchkey($search_regexp,$search_opt,$word);
   $this->querymatches = $tempar['ans'];
   $this->lastLnum = $tempar['lastLnum'];
   if (count($this->querymatches) == 0) {
    $this->status = true;
    $this->errmsg = "No matches found for '$word'";
   } else {
    $this->status = true;
   }
 }
 public function match_Sanskrit() {
  //in the file, the 'key' field is given in SLP.
  //we may need to modify from HK or ITRANS
  
   $slpword = $this->translate_string2SLP($this->queryParms->opt_stransLit,$this->queryParms->opt_sword);
   $wordchrs = preg_split ('/[^a-zA-Z.*?+|]/',$slpword); // 10-9-2021
   $slpword = join('',$wordchrs);
   //dbgprint(true,"match_Sanskrit: slpword='$slpword'\n");
   if ($slpword == '') {
    $this->status = true;
    $this->querymatches = array();
    $this->errmsg = "No matches found for '$slpword'";
    return;
   }
   $non_word = "[^a-zA-Z0-9|]";  // 10-9-2021
   $wordreg = "[a-zA-Z0-9-|]";
   $wordin = $slpword;
   if ($this->queryParms->opt_sregexp == "exact"){
    //$search_regexp = "^$slpword" . "[\t]";
    $search_regexp = "$non_word($slpword)$non_word.*[\t]";
   }else if ($this->queryParms->opt_sregexp == "prefix") {
    //$search_regexp = "^$slpword.+" . "[\t]";
    $search_regexp = "$non_word($slpword$wordreg+)$non_word.*[\t]";
   }else if ($this->queryParms->opt_sregexp == "suffix") {
    //$search_regexp = ".+$slpword" . "[\t]";
    $search_regexp = "$non_word($wordreg+$slpword)$non_word.*[\t]";
   }else if ($this->queryParms->opt_sregexp == "instring"){
    //$search_regexp = ".+$slpword.+" . "[\t]";
    $search_regexp = "$non_word($wordreg+$slpword$wordreg+)$non_word.*[\t]";
   }else if ($this->queryParms->opt_sregexp == "substring"){
    //$search_regexp = ".*$slpword.*" . "[\t]";
    $search_regexp = "$non_word($wordreg*$slpword$wordreg*)$non_word.*[\t]";
   }else {
    $search_regexp = "$slpword.*[\t]";
   }
   //dbgprint(true,"search_regexp='$search_regexp'\n");
   $search_regexp = preg_replace('/\|/','\\|',$search_regexp);
   //dbgprint(true,"search_regexp ADJ='$search_regexp'\n");
   $this->search_regexp_nonSanskrit = null;
   #$search_opt = $this->queryParms->opt_stransLit;
   $opt_swordhw = $this->queryParms->opt_swordhw;
   $tempar = $this->smatchkey($search_regexp);
   $this->querymatches = $tempar['ans'];
   $this->lastLnum = $tempar['lastLnum'];
   $this->status = true;
 }

 public function matchkey($regexp,$opt,$word) {
 // word is lower case. $opt is 
 $fp = $this->fp;
 $lastLnum = $this->queryParms->lastLnum;
 $max = $this->queryParms->max;
// print "matchkey: $lastLnum,$regexp,$max,$opt,$word\n";
 $ntot=0;
 if (!($word)) {
  $word = "XYZ"; // so no match
 }
 fseek($fp,$lastLnum,0); // reposition
 if (!feof($fp)) {
  $line=fgets($fp);
 }else {
  $line = FALSE;
 }
 $ans = array();
 $nline=0;
 $nothing=0;
 while ($line) {
  $nline++;
  $linex="";
  $liney=$line;
  if (!preg_match("/$word/",$liney)) {
  //nothing to do
   $nothing++;
  }else if ($opt == "false"){
   if (preg_match("/$regexp/",$liney)) {   
    $linex=$line;
   }
  }else { 
   // print "Checking line: $liney\n";
   if (preg_match("/$regexp/i",$liney)) {   
    $linex=$line;
   }
  }
  if ($linex !="") {
    //$ans[$ntot] = $line;
    // return key and non-sanskrit matchword
    if (!preg_match('/^(.*?)\t(.*?)$/',$linex,$matches)) {
     continue; // should not happen
    }
    $keypart = $matches[1];
    list($key,$sanskrit) = preg_split('|:|',$keypart);
    $key = trim($key);  // the headword
    if (!preg_match("/$regexp/",$linex,$matches)){
     $matchword=""; // should not happen
    }else {
     $matchword = $matches[1];
     //dbgprint(true,"querymodel: matchword=$matchword, regexp=$regexp\n");
    }
    if ($this->new_key_line($ntot,$key,$ans)){
     $ans[$ntot] = array( "key"=>$key, "matchword"=>$matchword);
     $ntot++;
     $lastLnum=ftell($fp); // get new file position
    }
   }
  
  if (!feof($fp)) {
   $line=fgets($fp);
  }else {
   $line = FALSE;
  }
  if (!($line)){$lastLnum = -1;}
  if ($ntot >= $max) {
   $line=FALSE; // end loop
  }
 }
 // print "chk: nline=$nline, nothing = $nothing, ntot=$ntot\n";
 $ans1=array();
 $ans1['ans']=$ans;
 $ans1['lastLnum']=$lastLnum;
 $ans1['nline']=$nline;
 $ans1['nothing']=$nothing;
 $ans1['ntot'] = $ntot;
 return $ans1;
}

public function smatchkey($regexp) {
 //dbg: $fplog = fopen('query_log.txt','w');
 //dbg: fwrite($fplog,"smatchkey regexp = $regexp\n");
 //dbg: fclose($fplog);
 $dbg=false;
 dbgprint($dbg,"QueryModel.smatchkey. regexp=$regexp\n");
 $fp = $this->fp;
 $lastLnum = $this->queryParms->lastLnum;
 $lastLnum = (int)$lastLnum;
 $max = (int)$this->queryParms->max;
 $opt_swordhw = $this->queryParms->opt_swordhw;
 dbgprint($dbg," lastLnum=$lastLnum, max = $max\n");
 #$transLit = $this->queryParms->opt_stransLit;
 $ntot = 0;
 fseek($fp,$lastLnum,0); // reposition
 //$line=fgets($fp);
 $ans=array();
 if (!feof($fp)) {
  $line=fgets($fp);
 }else {
  $line = FALSE;
 }
 $ntry = 0;
 while ($line) {
  $ntry = $ntry + 1;
  $linex="";
  list($a,$b) = preg_split("|\t|",$line);
  #$liney=" " . $a . " \t"; // 
  // New logic when searching for sanskrit within text is possible.
  if (preg_match("|^(.*?)::(.*?)$|",$a,$matches)) {
   $ahw = $matches[1];
   $atext = $matches[2];
  }else { // unexpected. Probably doesn't occur
   $ahw = $a;
   $atext = $a;
  }
  if (in_array($this->dict,array('ae','mwe','bor'))) {
   # search for sanskrit word only within text.
   $liney=" " . $atext . " \t"; //    
  }else  if ($opt_swordhw == 'both') {
   $liney=" " . $a . " \t"; // 
  } else if ($opt_swordhw == 'hwonly'){
   $liney=" " . $ahw . " \t"; // 
   //dbgprint($dbg,"liney = $liney\n");  // generates too much output
  } else if ($opt_swordhw == 'textonly'){
   $liney=" " . $atext . " \t"; //    
  } else { // should not occur. Same as both
   $liney=" " . $a . " \t"; // 
  }
  
  if (preg_match("/$regexp/",$liney)) {   
   $linex=$line;
  }
  if ($linex !="") {
   dbgprint($dbg,"liney=$liney\n");
    //$ans[$ntot] = $line ;
    if (!preg_match('/^(.*?)\t(.*?)$/',$linex,$matches)) {
     continue; // should not happen
    }
    $keypart = $matches[1];
    list($key,$sanskrit) = preg_split('|:|',$keypart);
    $key = trim($key);  // the headword
    $matchword = ""; // only relevant for non-sanskrit match
    if ($this->new_key_line($ntot,$key,$ans)){
     $ans[$ntot] = array( "key"=>$key, "matchword"=>$matchword);
     $ntot++;
     $lastLnum=ftell($fp); // get new file position
    }
   }
  
  if (!feof($fp)) {
   $line=fgets($fp);
  }else {
   $line = FALSE;
  }
  if (!($line)){$lastLnum = -1;}
  if ($ntot >= $max) {
   $line=FALSE; // end loop
  }
 }
 dbgprint($dbg," ntry = $ntry, ntot=$ntot\n");
 $ans1=array();
 $ans1['ans']=$ans;
 $ans1['lastLnum']=$lastLnum;
 return $ans1;
}
public function translate_string2SLP($transLit,$keyin) {
 $key = $keyin;
 $key = transcoder_processString($key,$transLit,'slp1');
 return $key;
}
public function extract_key($line) {
 // 11-13-2018.  Do same as in querlistview.php function display_outopt4
 if (! preg_match('/^(.*?)\t(.*?)$/',$line,$matches)) {
  return FALSE;
 }
 $keypart = $matches[1];
 list($key,$sanskrit) = preg_split('|:|',$keypart);
 $key = trim($key);
 return $key;
}

 public function new_key_line($ntot,$key,$ans) {
  $dbg=false;
  dbgprint($dbg,"new_key_line: key=$key, line=$line\n");
  foreach($ans as $a) {
   $key1 = $a['key'];
   if ($key1 == $key) {
    return false;  # duplicate key
   }
  }
  dbgprint($dbg,"new_key_line returns true\n");
  return true;
 }

}
  
?>
