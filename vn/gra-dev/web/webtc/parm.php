<?php
//error_reporting (E_ALL & ~E_NOTICE & ~E_WARNING);
?>
<?php
/* parm.php  Jul 10, 2015  Contains Parm class, which
  converts various $_GET parameters into member attributes. 
  $_GET   Parm attribute   Related attribute
  filter  filter0          filter
  transLit filterin0       filterin
  key     keyin            keyin1, key
  dict    dict             dictinfo   ***
  accent  accent
  basicOption == true   webtc style display. GetwordViewModel 
 *** for individual dictionaries, this parameter is provided to
 the constructory
 Aug 4, 2015 - synonym for $_GET:
  input == transLit
  output == filter
 Jun 2, 2017. changed $_GET to $_REQUEST
 Jul 20, 2019. Add viewAs to attributes. This used in webtc1
 Nov 2, 2020. Change constructor to take no parameters (formerly $dict)
 Get $dict from dictcode.php
*/
require_once('dictinfo.php');
require_once('dbgprint.php');
class Parm {
 public $filter0,$filterin0,$keyin,$dict,$accent,$viewAs;
 public $filter,$filterin,$basicOption;
 public $dictinfo,$english;
 public $keyin1,$key;
 //public function __construct($dict) {
 public function __construct() {
  $this->basicOption = true; 
  include('dictcode.php'); # init $dictcode variable
  $this->dict = $dictcode;
  $dbg=false;
  dbgprint($dbg,"enter parm construct\n");
  $this->dictinfo = new DictInfo($this->dict);
  require_once($this->dictinfo->transcodefile);
  $this->filter0 = $this->init_request(array('filter','output'),'slp1');
  /*
  if ($_REQUEST['filter']) {
   $this->filter0 = $_REQUEST['filter'];
  }else{
   $this->filter0 = $_REQUEST['output'];
  }
  */
  $this->filterin0 = $this->init_request(array('transLit','input'),'slp1');
  /*
  if ($_REQUEST['transLit']) {
   $this->filterin0 = $_REQUEST['transLit']; 
  }else {
   $this->filterin0 = $_REQUEST['input']; 
  }
  */
  //$this->keyin = $_REQUEST['key'];
  $this->keyin = $this->init_inputs_key();
  if ($this->keyin) {
   $this->keyin = trim($this->keyin); // remove leading and trailing whitespace
  }
  // $this->dict = $_REQUEST['dict'];
  //$this->accent = $this->init_request(array('yes','no'),'no');
  $this->accent = $this->init_request(array('accent'),'no');
  // $this->accent = $_REQUEST['accent']; 
  // How to set viewAs ?
  if (!isset($_REQUEST['viewAs'])) {
   $this->viewAs = "" ;  // 07/20/2019
  } else {
   $this->viewAs = $_REQUEST['viewAs'];
  }
  if(!$this->accent) {$this->accent="no";}  # no, yes

  $this->filter = transcoder_standardize_filter($this->filter0);
  $this->filterin = transcoder_standardize_filter($this->filterin0);
  dbgprint($dbg,"parm.php. filter0={$this->filter0}, filter={$this->filter}\n");

  $this->english = $this->dictinfo->english;
  if ($this->english) {
   $this->keyin1 = $this->keyin;
   $this->key = $this->keyin1;  
  }else {
   $this->keyin1 = $this->preprocess_unicode_input($this->keyin,$this->filterin,$this->viewAs);
   $this->key = transcoder_processString($this->keyin1,$this->filterin,"slp1");
  }
 dbgprint($dbg,"parm construct keyin = {$this->keyin}\n");
 dbgprint($dbg,"parm construct keyin1 = {$this->keyin1}\n");
 dbgprint($dbg,"parm construct key = {$this->key}\n");
 dbgprint($dbg,"leave parm construct\n");

 }  

 public function preprocess_unicode_input($x,$filterin,$viewAs) {
 // when a unicode form is input in the citation field, for instance
 // rAma (where the unicode roman for 'A' is used), then,
 // the value present as 'keyin' is 'r%u0101ma' (a string with 9 characters!).
 // The transcoder functions assume a true unicode string, so keyin must be
 // altered.  This is what this function aims to accomplish.
 /* June 15, 2015 - try php urldecode */
// return urldecode($x);
// link=http://localhost/cologne/mw/web/webtc1/disphier.php?key=j%F1%u0101&keyboard=yes&inputType=phonetic&unicodeInput=devInscript&phoneticInput=slp1&serverOptions=roman&accent=no&viewAs=roman
// $actual_link = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://{$_SERVER['HTTP_HOST']}{$_SERVER['REQUEST_URI']}";

 $hex = "0123456789abcdefABCDEF";
 $x1 = $x;
 if (($filterin == 'roman')|| ($viewAs   == 'roman')) {
  /* special logic when n-tilde is present in $x (keyin. e.g. keyin = jYA (slp1)
   Although the raw URI ($actual_link above) is j%F1%u0101,  php changes this
   to j\xf1%u0101.    The next preg changes this to j%u00f1%u0101.
   */
  $x1 = preg_replace("/\xf1/","%u00f1",$x);
 }
 if (! $x1) {$x1 = "";}
 $ans = preg_replace_callback("/(%u)([$hex][$hex][$hex][$hex])/",
     "Parm::preprocess_unicode_callback_hex",$x1);
 return $ans;
}
 public function preprocess_unicode_callback_hex($matches) {
 $x = $matches[2]; // 4 hex digits
 $y = unichr(hexdec($x));
 return $y;
}
 public function init_inputs_key() {
 // word = citation.  
 $ans = "";
 if (isset($_REQUEST['word'])) {
  $x = $_REQUEST['word'];
 }else if (isset($_REQUEST['citation'])) {
  $x = $_REQUEST['citation'];
 }else if (isset($_REQUEST['key'])) {
  $x = $_REQUEST['key'];
 }else {
  $x = "";
 }
 //'%' is used in html_encoding of unicode.
 //$invalid_characters = array("$", "%", "#", "<", ">", "=", "(", ")");
 $invalid_characters = array("$",  "#", "<", ">", "=", "(", ")");
 $ans = str_replace($invalid_characters, "", $x);
 return $ans;
}
public function init_request($keys,$default) {
 $ans = $default;
 foreach($keys as $key) {
  if (isset($_REQUEST[$key])) {
   $ans = $_REQUEST[$key];
   break;
  }
 }
 return $ans;
}

}
?>
