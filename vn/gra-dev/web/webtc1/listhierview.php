<?php
class ListHierView {
 // constructs html from a certain array of data
 public $table;  // a string of html 
 public function __construct($listmatches,$getParms) {
 // step 3 format listmatches
 $i=0;
 $table="";
 $spcchar = "&nbsp;";
 $spcchar = ".";
 while($i < count($listmatches)) {
  // code governs a detail of format 
  list($code,$key2,$lnum2,$data2) = $listmatches[$i];
  $hom2=$this->get_hom($data2);
  if ($i == 0) {
   //  put 'upward button'
   $spc="&nbsp;&nbsp;";
   $c="color:black";
   $out1 = "$spc<a  onclick='getWordlistUp_keyboard(\"<SA>$key2</SA>\");'><span style='$c'>&#x25B2;</span></a><br/>\n";  
   $table .= $out1;
  }
  $i++;
  if ($code == 0) {$c="color:teal";}
  else {$c="color:black";}
  // Apr 7, 2013.  Color Supplement records. 
  // Jun 29, 2018 This relevant for MW onlyu
  if (preg_match('/<L supL="/',$data2,$matches)) {
   $c = "color:red";
  }
  if (preg_match('/<L revL="/',$data2,$matches)) {
   $c = "color:green";
  }
  if (preg_match('/^<H([2])/',$data2,$matches)) {
   $spc="$spcchar";
  }else if(preg_match('/^<H([3])/',$data2,$matches)) {
   $spc="$spcchar$spcchar";
  }else if(preg_match('/^<H([4])/',$data2,$matches)) {
   $spc="$spcchar$spcchar$spcchar";
  }else {
   $spc="";
  }
  if ($hom2 != "") {
   $hom2=" <span style=\"color:red; font-size:smaller\">$hom2</span>";
  }
  // Apr 10, 2013. key2show: 
  $key2show=$key2;
  if (False) { //dbg
   if (preg_match('/^<(H.[BC])>/',$data2,$matches)) {
    $temp = $matches[1];
    $key2show = "($key2show):$temp";
   }  
  }
  // Apr 14, 2013: xtraskip
  $xtraskip='';
  if($this->listhierskip_data($data2)) {
   $xtraskip='<span style="font-size:smaller; color:blue;"> (skip)</span>';
  }
  $filterin = $getParms->filter;
  if ($filterin == "deva") {
   /* use $filterin to generate the class to use for Sanskrit (<s>) text 
    This repeats logic of basicdisplay.php
    This lets us use siddhanta font for Devanagari.
   */
   $sdata = "sdata_siddhanta"; // consistent with font.css
  } else {
   $sdata = "sdata"; // default. for san
  }
  
  # add class=sdata when the headwords are Sanskrit. 07-09-2018
  if (in_array($getParms->dict,array('ae','mwe','bor'))) {
   $class = "";
  }else {
   $class = " class='$sdata'";
  }
  $out1 = "$spc<a  onclick='getWordAlt_keyboard(\"<SA>$key2</SA>\");'><span style='$c'$class><SA>$key2show</SA></span>$hom2</a>$xtraskip<br/>\n";

  $table .= $out1;
  if ($i == count($listmatches)) {
   //  put 'downward button'
   $spc="&nbsp;&nbsp;";
   $out1 = "$spc<a  onclick='getWordlistDown_keyboard(\"<SA>$key2</SA>\");'><span style='$c'>&#x25BC;</span></a><br/>\n";  
   $table .= $out1;
  }
 }
 $this->table = $table;
} // __construct
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
