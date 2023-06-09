<?php //listhiermodel.php
require_once("../webtc/dal.php");
class ListHierModel{
 // Gathers a collection of dictionary records 
 public $listmatches; // primary result of constructor
 public $dict, $key, $dal; 
 public $direction;
 public function __construct($listParms) {
  $this->dict = $listParms->dict;
  $this->key = $listParms->key;
  $this->direction = $listParms->direction;
  $this->dal = new Dal($this->dict);
  // step 1: get a match for key
  $matches = $this->match_key($this->key);
  list($key1,$lnum1,$data1) = $matches[0];
  // step 2:  get several keys preceding and several keys following $key1
  $nprev=12;
  $nnext=12;
  if ($this->direction == 'UP') {
   $this->listmatches = $this->list_center($key1,$lnum1,$data1,$nprev+$nnext,0);
  }else if ($this->direction == 'DOWN') {
   $this->listmatches = $this->list_center($key1,$lnum1,$data1,0,$nprev+$nnext);
  }else {
   $this->listmatches = $this->list_center($key1,$lnum1,$data1,$nprev,$nnext);
  }
 } // __construct

 // Many helper methods
 
 public function match_key($key) {
  // this function 'guaranteed' to return an array with one entry
  $matches = $this->list1a($key);
  $nmatches = count($matches);
  if ($nmatches != 1) {
   $key1 = $key;
   $nmatches=0;
   $n1 = strlen($key1);
   while (($nmatches == 0) && ($n1 > 0)) {
    $key2 = substr($key1,0,$n1);
    $matches = $this->list1b($key2);
    $nmatches = count($matches);
    if ($nmatches == 0) {$n1--;}
   } 
  }
  if ($nmatches == 0) {
   $key = "a"; // sure to match
   $key1 = $key;
   $nmatches=0;
   $n1 = strlen($key1);
   while (($nmatches == 0) && ($n1 > 0)) {
    $key2 = substr($key,0,$n1);
    $matches = $this->list1b($key2);
    $nmatches = count($matches);
    if ($nmatches == 0) {$n1--;}
   } 
  }
   return $matches;
 }
 public function list1a($key) {
  // first exact match
  $recarr = $this->dal->get1($key);
  $matches=array();
  $nmatches=0;
  $more=True;
  foreach($recarr as $rec) {
   if ($more) {
    list($key1,$lnum1,$data1) = $rec;
    // May 23, 2013.  Do not consider the listhierskip records
    if ($this->listhierskip_data($data1)) { continue;}
    $matches[0]=$rec;
    $more=False;
   }
  }
  
  return $matches;
 }
 public function list1b($key) {
  // first  partial match
  $recarr = $this->dal->get3($key); // records LIKE key%
  $matches=array();
  $nmatches=0;
  $keylen = strlen($key);
  $more=true;
  foreach($recarr as $rec) {
   if ($more) {
    list($key1,$lnum1,$data1) = $rec;
    // May 23, 2013.  Do not consider the listhierskip records
    if ($this->listhierskip_data($data1)) { continue;}
    $keylen1 = strlen($key1);
    if (($keylen1 >= $keylen) && (substr($key1,0,$keylen) == $key)) {
     $matches[$nmatches]=$rec;
     $nmatches++;
     $more=false;
    }
   }
  }
  return $matches;
 }
 
 public function list_prev($key0,$lnum0,$nprev) {
  $ans = array();
  if ($nprev <= 0) {return $ans;}
  $max = 5 * $nprev;  // 5 is somewhat arbitrary.
  $recarr = $this->dal->get4a($lnum0,$max);
  // 1. get records to be displayed
  $matches = $this->list_filter($lnum0,$recarr);
  // 2. get the last $nprev records for return
  $nmatches = count($matches);
  if ($nmatches == 0) {return $ans;}
  if ($nprev <= $nmatches) {
   $n1 = $nprev;
  }else {
   $n1 = $nmatches;
  }
  // we retrieved in descending order. Now, we get back to ascending order
  $j=$n1-1;
  for($i=0;$i<$n1;$i++) {
   $x = $matches[$j];
   $ans[]=$x;
   $j--;
  }
  return $ans;
 }
 public function list_next($key0,$lnum0,$n0) {
  $ans = array();
  if ($n0 <= 0) {return $ans;}
  // next $n0 different keys
  $max = 5 * $n0;  // 5 is somewhat arbitrary.
  $recarr = $this->dal->get4b($lnum0,$max);
  // 1. get records to be displayed
  $matches = $this->list_filter($lnum0,$recarr);
  // 2. get the last $nprev records for return
  $nmatches = count($matches);
  
  if ($nmatches == 0) {return $ans;}
  if ($n0 <= $nmatches) {
   $n1 = $n0;
  }else {
   $n1 = $nmatches;
  }
  for($i=0;$i<$n1;$i++) {
   $x = $matches[$i];
   $ans[]=$x;
  }
  return $ans;
 }
 public function list_filter($lnum0,$recarr) {
  // This variant matches on key+hom
  $matches=array();
  $recarr0 = $this->dal->get2($lnum0,$lnum0); 
  if (count($recarr0) != 1) {return $matches;} // should not happen
  // Apr 6, 2013. Changed $recarr[0] to $recarr0[0] in next.
  list($key0,$lnum0a,$data0)=$recarr0[0];  
  $keyhom0 = $this->get_keyhom($key0,$data0);
  $keyhom = '';
  foreach($recarr as $rec) {
   list($key1,$lnum1,$data1) = $rec;
   if (!preg_match('/^<H[1-4][BC]?>/',$data1)) {continue;}
   // Apr. 10, 2013. Don't show H.[BC]
   if (preg_match('/^<H[1-4][BC]>/',$data1)) {continue;}
   
   $keyhom1 = $this->get_keyhom($key1,$data1);
   if ($keyhom1 == $keyhom){continue;}
   // Apr 13, 2013 commented out next line. Consider example avata
   // if ($keyhom1 == $keyhom0) {continue;}
   // found a new one
   $matches[]=$rec;
   $keyhom = $keyhom1; 
  }
  return $matches;
 }
 
 public function list_center($key1,$lnum1,$data1,$nprev,$nnext) {
  $listmatches = array();
  $matches1 = $this->list_prev($key1,$lnum1,$nprev);
  $matches2 = $this->list_next($key1,$lnum1,$nnext);
  $nmatches1 = count($matches1);
  $nmatches2 = count($matches2);
  // handle special cases
  $i=0;
  while($i < count($matches1)) {
   list($key2,$lnum2,$data2) = $matches1[$i];
   $listmatches[]=array(-1,$key2,$lnum2,$data2);
   $i++;
  }
   $listmatches[]=array(0,$key1,$lnum1,$data1);
  $i=0;
  while($i < count($matches2)) {
   list($key2,$lnum2,$data2) = $matches2[$i];
   $listmatches[]=array(1,$key2,$lnum2,$data2);
   $i++;
  }
  return $listmatches;
 }
 
 public function get_keyhom($key,$data){
  $hom = $this->get_hom($data);
  return "$key+$hom";
 }
 public function get_hom($data) {
  $hom="";
  if (preg_match('|<hom>(.*?)</hom>.*?</h>|',$data,$matches)) {
   $hom = $matches[1];
  }
  return $hom;
 }
 public function listhierskip_data($data2) {
  // dummy routine, always return False
  return False;
 }
 
}
?>
