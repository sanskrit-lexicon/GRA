<?php  error_reporting (E_ALL & ~E_NOTICE & ~E_WARNING); 
/* queryparm.php  Jul 10, 2015  Contains Queryparm class, which
  converts various $_GET parameters into member attributes. 
  Parameters are for listhier view. Essentially extends the
  Parm class of webtc/parm.php.
  $_GET   Parm attribute   Related attribute
  filter  filter0          filter
  transLit filterin0       filterin
  key     keyin            keyin1, key
  dict    dict             dictinfo   ***
  accent  accent
 *** for individual dictionaries, this parameter is provided to
 the constructor
 Aug 4, 2015 - synonym for $_GET:
  input == transLit
  output == filter
 Jun 2, 2017. changed $_GET to $_REQUEST
*/
require_once('../webtc/dictinfo.php');
require_once('../webtc/parm.php');
#require_once('dbgprint.php');
class Queryparm extends Parm {
 # from Parm
  #public $filter0,$filterin0,$keyin,$dict,$accent;
  #public $filter,$filerin;
  #public $dictinfo,$english;
  #public $keyin1,$key;
 # new for Queryparm
 public $filename,$lastLnum,$max;
 public $opt_sregexp,$opt_sword,$opt_stransLit;
 public $word, $opt_regexp, $sopt_case, $outopt;
 public $opt_swordhw; // both, hwonly, textonly
 public $accent;
 public function __construct($dict) {
  // Part 1 of construction identical to Parm class
  parent::__construct($dict);  // Parm's constructor
  #Use parms filter and filterin from Parm 
  #$this->filter = $_REQUEST['filter'];
  #$this->opt_stransLit = $_REQUEST['transLit'];
  $this->opt_stransLit = $this->filterin; # rename filterin to opt_stransLit
  if (isset($_REQUEST['dictionary'])) {
   $this->filename = $_REQUEST['dictionary'];
  }else {
   $this->filename = "query_dump.txt";
  }
  $this->lastLnum = $_REQUEST['lastLnum']; // file position, for seek&tell
  $this->max = $_REQUEST['max'];
  
  // parms for sanskrit word
  $this->opt_sregexp = $_REQUEST['sregexp'];
  $this->opt_sword = $_REQUEST['sword'];
  
  // parms for non-Sanskrit word
  if (isset($_REQUEST['word'])){
   $this->word = $_REQUEST['word'];
   $this->word = strtolower($this->word);
  }else {
   $this->word="";
  }
  $this->opt_regexp = $_REQUEST['regexp'];
  $this->sopt_case = $_REQUEST['scase'];
  $this->outopt = $_REQUEST['outopt'];
  $this->opt_swordhw = $_REQUEST['swordhw'];
  if (!in_array($this->opt_swordhw,array('both', 'hwonly', 'textonly'))) {
   $this->opt_swordhw = "hwonly";
  }
  if (!($this->filename)) {$this->filename = "query_dump.txt";}
  if (!($this->max)) {$this->max = 5;}
  if (!($this->lastLnum)) {$this->lastLnum = 0;}
  $this->lastLnum = intval($this->lastLnum);
  if ($this->lastLnum < 0) {
      $this->lastLnum=0;
  }
  if ($this->lastLnum > 25000000) {
      $this->lastLnum = 0;
  }  
  #$this->printparms(); # dbg
 }  
 public function printparms() {
  $dbg=true;
  dbgprint($dbg,"queryparms:\n");
  dbgprint($dbg," opt_sword={$this->opt_sword}\n");
  dbgprint($dbg," word={$this->word}\n");
 }

}

?>
