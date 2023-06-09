<?php
/*
// dispitem.php  Contains class DispItem, which
// parses a records from a dictionary's html database.
// Jul 20, 2015 cssshade
// 11-09-2017. Add tooltips for p= and L=
// 01-17-2019. 
   1) Change L= to ID= (for consistency with Basic display)
   2) Add line break after non-empty pageshow.
   3) For IAST output in MW, italicize text.
*/
require_once('dbgprint.php');
require_once('parm.php');
class DispItem { // info to construct a row of the display table
 public $dict,$dictup,$key,$lnum,$info,$html;
 public $pginfo,$hcode,$key2,$hom;
 public $hrefdata_prev,$hrefdata;
 public $err; // Boolean
 public $keyshow;
 public $cssshade; // July 20, 2015. See basicDisplayRecord2 for use.
 public $firstHom; // Aug 15, 2015
 public function __construct($dict,$dbrec) {
  $this -> cssshade=False;
  $this->dict = $dict;
  $this->dictup = strtoupper($dict);
  $this->err = False;
  list($this->key,$this->lnum,$rec) = $dbrec;
  $dbg=false;
  $reclen=strlen($rec);dbgprint($dbg,"  DispItem reclen = $reclen\n");
  //dbgprint($dbg,"dispitem: rec=\n$rec\n");
  /* $rec is a string. It can be large. php has a parameter that
   controls whether the preg_match will work for the string. The default
   for the parameter is 1000000 (one million).
  */
  $ok = false;
  if (preg_match('|<info>(.*?)</info><body>(.*?)</body>|',$rec,$matchrec)) {
   $ok = true;
  }else {
   // increase the PHP parameter. Not sure if  is always big enough!
   $newlim = 1500000;
   $oldlim = ini_get('pcre.backtrack_limit');
   //dbgprint(true,"dispitem: oldlim=$oldlim\n");
   ini_set('pcre.backtrack_limit',$newlim);
   if (preg_match('|<info>(.*?)</info><body>(.*?)</body>|',$rec,$matchrec)) {
    $ok = true;
   }
   ini_set('pcre.backtrack_limit',$oldlim);
  }
  if (! $ok) {
   $this->err = True; // rare, if ever
   dbgprint($dbg,"DispItem: Error 1\n");
   $reclen=strlen($rec);
   dbgprint($dbg,"  DispItem reclen = $reclen\n");
   return;
  }
  $this->info = $matchrec[1];
  $this->html = $matchrec[2];
  dbgprint($dbg,"this->info starts as {$this->info}\n");
  //Some derived fields
  if($this->dictup == 'MW') {
   list($this->pginfo,$this->hcode,$this->key2,$this->hom) = preg_split('/:/',$this->info);
  }else {
   $this->pginfo = $this->info;
  }
  // compute $hrefdata
  $this->hrefdata= $this->getHrefPage();
  // compute $keyshow;
  $this->keyshow = $this->keyshow();
 } // __construct

 public function keyshow() {
  $dictup=$this->dictup;
  $english = in_array($dictup,array("AE","MWE","BOR")); // boolean flag
  $dbg=false;
  if ($english) {
    return $this->key;
  }
  if ($dictup != 'MW') {
   // Sanskrit headwords, not MW
   $keyshow = "<span class='sdata'><SA>$this->key</SA></span>";
   return $keyshow;
  }
  // Special handling for MW
  dbgprint($dbg,"this->info before keyshow_MW(): {$this->info}\n");
  $ans = $this->keyshow_MW();
  dbgprint($dbg,"this->info after keyshow_MW(): {$this->info}\n");
  return $ans;
 } //keyshow

 public function keyshow_MW() {
  $hcode = $this->hcode;
  $key2 = $this->key2;
  $hom = $this->hom;
  /* This is not the right place to make this test
  if ((strlen($hcode) != 2)and(!$hom)) {
   return "";
  }
  */
  $hshow = "($hcode)";  //H1, H2a, etc
  //04-17-2018
  // don't show key and homonym, which is what the rest of this
  // function is devoted to.
  // In the current revision of web/webtc/disp.php, these values are
  // printed elsewhere when needed, so showing them here is duplicative.
  return $hshow;
  // rest of this function not applicable as of 04-17-2018
  $homshow = "";
  if ($hom && ($hom!='')) {
   $homshow = "<span class='hom'>$hom</span>";
  }
  /* key2 can have
   (a) '-'  not changed
   (b) '~'  raised circle (incomplete)
   (c) </?root/?> (as in ati-<root>kf</root>)
   (d) </?hom>   (as in ati-dA<hom>1</hom> )
   (e) <shortlong/>
   The strategy is to split key2 on all these things, appropriately 
   constructing html for keyshow
  Here is how key2 looks initially for key=vivf:
     vi-<root>vf<hom>1</hom></root>
  And here is the (sep 2, 2015) erroneous expansion:
  <span class='sdata'><SA>vi-</SA></span>
  <span class='sdata'><SA>vf</SA></span>
  <span class='sdata'><SA>1<hom><root></SA></span>   This is wrong
  */
$dbg=False;
dbgprint($dbg,"dispitem: key={$this->key}, lnum={$this->lnum}, hom={$this->hom}\n");
dbgprint($dbg,"dispitem: info=" . $this->info . "\n");
dbgprint($dbg,"dispitem. key2=$key2\n");
  $outarr = array();
  $flags=PREG_SPLIT_DELIM_CAPTURE + PREG_SPLIT_NO_EMPTY;
  $parts = preg_split(':(<hom>.*?</hom>)|(@)|(~)|(<.*?>):',$key2,-1,$flags);
  foreach ($parts as $part) {
   if (!$part) {continue;}
   $outpart='';
   if ($part == '@') { // <srs/>
    $outpart = "<span class='red'>*</span>";
   }else if ($part == '~') { //<sr/>
    $outpart = "<span class='red'>&deg;</span>";
   }else if (preg_match('|<hom>(.*?)</hom>|',$part,$matches)) {
    $homroot = $matches[1]; // Sep 7, 2015. 
    $outpart = "<span class='red'>&nbsp;$homroot</span>";
   }else if (($part == '<root>') or ($part == '<root/>')) {
    $outpart = " &#x221a;"; // root symbol
   }else if (($part == '</root>') or ($part == '<shortlong/>')) {
    $outpart = "";
   }else { // Should just be text, to be considered devanagari
    $outpart = "<span class='sdata'><SA>$part</SA></span>";
   }
   $outarr[]=$outpart;
   dbgprint($dbg,"dispitem: part=$part  => $outpart\n");
  }
  $key2show = join('',$outarr);
  // Finally return the join of these strings
  // Sep 3, 2015
  // There are two kinds of 'hom':  The 'vivf' example is one such,
  // where the hom refers to the root 'vf', not to the headword, vivf.
  // In this case, we don't want to show $hom again. The 'real' kind,
  // where hom refers to headword, occurs as a different part of the
  // <info> record.  So, in short we never want to show $hom separately
  // Sep 7, 2015.  '$homroot' used above.  $hom is a separate field,
  // which should be retained
  $ans = "$hshow $key2show <span class='hom'>$hom</span>";
  #$ans = "$hshow $key2show";
  dbgprint($dbg,"dispitem returns: $ans\n");
  return $ans; 
 }
 public function basicRow1DefaultParts($prev) {
  
  if($prev) {	 
   $hrefdata_prev = $prev->hrefdata;
   $keyshow_prev = $prev->keyshow;
  }else {
   $hrefdata_prev="";
   $keyshow_prev = "";
  }
  $hrefdata = $this->hrefdata;
  $key = $this->key;
  $keyshow = $this->keyshow;
  $lnum = $this->lnum;
  if ($keyshow == $keyshow_prev) {
   $keyshow = ""; // Don't reshow same key on subsequent records
  }
  #$lnumshow = "<span class='lnum'> [<span title='Cologne record ID'>L=</span>$lnum]</span>";
  if (in_array($this->dictup,['GRA','STC','AP','AP90','PWG','BUR','PW','ACC'])) {
   // Add extra spaces so preceding text will not be overwritten.
   // This applies to dictionaries where a 'position:relative' css style 
   // is used to indent text.
   //$lnumshow = "<span class='lnum'> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;[<span title='Cologne record ID'>ID=</span>$lnum]</span>";
   $lnumshowid = $this->get_lnumshow_id($lnum);
   $lnumshow = "<span class='lnum'> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;&nbsp; &nbsp;$lnumshowid";
  }else {
   //$lnumshow = "<span class='lnum'> [<span title='Cologne record ID'>ID=</span>$lnum]</span>";
   $lnumshowid = $this->get_lnumshow_id($lnum);
   $lnumshow = "<span class='lnum'> $lnumshowid</span>";
  }
  $pageshow = $this->get_pageshow($hrefdata); 
  $pageshow = "<span class='hrefdata'> [<span title='Printed book page-column'>p=</span> $hrefdata]</span>";
  if ($hrefdata == $hrefdata_prev) {
   $pageshow="";
  }
  return array($keyshow,$lnumshow,$pageshow);
 }
 public function get_pageshow($hrefdata) {
  // 08-04-2020 make consistent with basicdisplay.php
  $style = "font-weight:normal; color:rgb(160,160,160);";
  $ans = "<span class='hrefdata'><span style='$style'> [Printed book page $hrefdata]</span></span>";
  return $ans;
 }
 public function get_lnumshow_id($lnum) {
  // 08-04-2020
  $style = "font-size:normal; color:rgb(160,160,160);";
  return "[<span title='Cologne record ID' style='$style'>ID=$lnum</span>]";
 }
 public function basicRow1Default($prev) {
  list($keyshow,$lnumshow,$pageshow) = $this->basicRow1DefaultParts($prev);
  $row1 = "$keyshow $lnumshow $pageshow";  
  return $row1;
 }
 public function basicDisplayRecordDefault($prev) {
  $row1 = $this->basicRow1Default($prev);
  $row = $this->html;
  return ( "<tr><td class='display' valign=\"top\">$row1</td>\n" .
   "<td class='display' valign=\"top\">$row</td></tr>\n");
 }

 public function basicDisplayRecord1($prev) {
  $row1 = $this->basicRow1Default($prev);
  $row = $this->html;
  return ( "<tr><td class='display' valign=\"top\">$row1</td></tr>\n" .
   "<tr><td class='display' valign=\"top\">$row</td></tr>\n");
 } 

 public function basicDisplayRecord2($prev) {
  list($keyshow,$lnumshow,$pageshow) = $this->basicRow1DefaultParts($prev);
  $row = $this->html;
  // 01-17-2019. for MW, when user requests IAST output, make this output italic
  if ($this->dictup == 'MW') {
   // The Parm constructor for dispitem here requires 'dict' parameter
   // but in csl-apidev/dispitem.php, no argument is required.
   // 11-02-2020. Use from $dictinfo
   //$getParms = new Parm($this->dict); 
   $getParms = new Parm();
   if ($getParms->filter == "roman") {
    $row = preg_replace('|<SA>|','<i><SA>',$row);
    $row = preg_replace('|</SA>|','</SA></i>',$row);
   }
  }
  $hrefdata = $this->hrefdata;
  //$pageshow = "<span class='hrefdata'> [<span title='Printed book page-column'>p=</span> $hrefdata]</span>";
  if ($this->hom) { // for MW
   $pre1 = ""; // incomplete  need a link with onclick
   $pageshow = $this->get_pageshow($hrefdata); 
   $pre2="<span style='font-weight:bold'>$keyshow $pageshow</span> :";
   $pre = $pre1 . $pre2;
  }else if (($keyshow == "") and ($pageshow == "")) {
   $pre = "";
  }else {
   $pageshow = $this->get_pageshow($hrefdata); 
   $pre="<span style='font-weight:bold'>$keyshow $pageshow</span>";
  }
  if (($this->dictup == 'MW') and ($this->hom)) {
   // make a link to change list view to be centered at this lnum
   $symbol = "&#8592;";  // unicode left arrow
   $lnum = $this->lnum;
   $class='listlink';
   if ($this->firstHom)  { 
    $class='listlink listlinkCurrent';
   }
   /* for use of 'this', refer
//stackoverflow.com/questions/925734/whats-this-in-javascript-onclick
   */
   $a = "<a class='$class' onclick='listhier_lnum(\"$lnum\",this);'>$symbol</a>&nbsp;\n";
   $pre = $a . $pre;
  }
  # 01-17-2019
  if ($pageshow != "") {
   $pre = $pre . "<br>";
  }
  $class = "display";
  if ($this->cssshade) {
   $class = "display cssshade";
  }
  $ans = ( "<tr><td class='$class' valign=\"top\"> $pre \n" .
   "$row $lnumshow</td></tr>\n");
  $dbg=False;
  dbgprint($dbg,"basicDisplayRecord2: pre = $pre\n");
   return $ans;
} // basicDisplayRecord2
public function getHrefPage() {
include('dictinfowhich.php');  

 $ans="";
 $data = $this->pginfo;
 $dict = $this->dict;
 $lnums = preg_split('/[,]/',$data);  
 $serve = "servepdf.php";
 if ($dictinfowhich == "cologne") {
  #$serve = "//www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/$serve";
  $serve = "//www.sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/$serve";
 }else {
  $serve = "../webtc/$serve";
 }
 #dbgprint(true,"dispitem.getHrefPage: serve=$serve\n");
 foreach($lnums as $lnum) {
  if ($ans == "") {
   $args = "dict=$dict&page=$lnum"; #"page=$page";
   $ans = "<a href='$serve?$args' target='_$dict'>$lnum</a>";
  }else {
   $ans .= ",$lnum";
  }
 }
 return $ans;
}


} // class dispItem


?>
