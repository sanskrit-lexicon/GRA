<?php
error_reporting(E_ALL & ~E_NOTICE & ~E_WARNING);
?>
<?php
/*
// web/webtc/basicdisplay.php
// The main function basicDisplay constructs an HTML table from
// an array of data elements.
// Each of the  data elements is a string which is valid XML.
// The XML is processed using the XML Parser routines (see PHP documentation)
// This XML string is further assumed to be in UTF-8 encoding.
// July 2, 2018 - begin universal version of BasicDisplay.  Objective is
// for this to work for all Cologne dictionaries.
// Aug 7, 2020.  Restructure under assumption that input to
// constructor is either a string or an array of strings.
*/
require_once("dbgprint.php");
require_once("parm.php");
class BasicDisplay {
 public $parentEl;
 public $row;
 public $row1;
 public $row1x;
 public $pagecol;
 public $dbg;
 public $inSanskrit;
 public $inkey2;
 public $table;
 public $dict;
 public $sdata; // class to use for Sanskrit
 public $filterin; // transcoding for output
 public $key; // the original key being searched for
 public $basicOption,$serve;
 public $getParms,$status,$mwx,$html;
public function __construct($key,$string_or_array,$filterin,$dict) {
 
 $this->key = $key;
 $this->dict = $dict;
 $this->filterin = $filterin;
 $this->getParms = new Parm();
 $this->basicOption = $this->getParms->basicOption;
 if ($this->basicOption) {
  $this->serve = "../webtc/servepdf.php";
 } else {
  $this->serve = "servepdf.php";
 }
 
 $this->pagecol="";
 $this->dbg=false; #false;
 $this->inSanskrit=false;
 if ($filterin == "deva") {
 /* use $filterin to generate the class to use for Sanskrit (<s>) text 
    This was previously done in main_webtc.js.
    This let's us use siddhanta font for Devanagari.
 */
  $this->sdata = "sdata_siddhanta"; // consistent with font.css
 }else if (($filterin == 'roman')&&($this->dict == 'mw')) {
  $this->sdata = "sdata_italic_iast";
 } else {
  $this->sdata = "sdata"; // default.
 }
 $sdata = $this->sdata;
 // 
 if (in_array($this->dict,array('ae','mwe','bor'))) {
  // no transliteration of $key for English headword
  $this->table = "<h1>&nbsp;$key</h1>\n";
 }else {
  $this->table = "<h1 class='$sdata'>&nbsp;<SA>$key</SA></h1>\n";
 }


 $this->table .= "<table class='display'>\n";
 if (is_string($string_or_array)) {
  $matches = array($string_or_array);
 }else if (is_array($string_or_array)) {
  if (count($string_or_array) == 0) {
   $matches = array();
  }else {
   // take only first item
   $matches = array($string_or_array[0]);
  }
 }else {
  $matches = array();
 }
 
 $ntot = count($matches);  // either 0 or 1.
 // Associative array. keys are:
 // status 
 // mwx  (whitney/westergaard links -- currently requires dict == mw
 // 
 $this->status = true;
 $this->mwx = "";
 $this->row = "";
 $this->row1 = "";
 $this->html = "";
 $i = 0;
 while($i<$ntot) {
  $linein=$matches[$i];
  $line=$linein;
  
  dbgprint($this->dbg,"basicdisplay: line[$i+1]=$line\n");
  $line=trim($line);
  $l0=strlen($line);
  $this->row = "";
  $this->row1 = "";
  $this->row1x = "";
  if ($dict == 'mw') {
   $row1x = $this->mw_extra_line($line);
   $this->row1x = $row1x;
  }else if ($dict == 'mci') {
   $row1x =  $this->mci_extra_line($line);
   $this->row1x = $row1x;
  }else {
   $row1x = "";
  }
  $this->inSanskrit=false;
  $this->inkey2 = false;
  $p = xml_parser_create('UTF-8');
  xml_set_element_handler($p,array($this,'sthndl'),array($this,'endhndl'));
  xml_set_character_data_handler($p,array($this,'chrhndl'));
  xml_parser_set_option($p,XML_OPTION_CASE_FOLDING,FALSE);
  dbgprint($this->dbg,"chk 1\n");
  if (!xml_parse($p,$line)) {
   dbgprint(true,"basicdisplay.php: xml parse error\nline=$line\n");
   $row = $line;
   $this->status = false;
   $this->html = "<p>basicdisplay.php: xml parse error</p>";
   return;
  }
  dbgprint($this->dbg,"chk 2\n");
  xml_parser_free($p);
  dbgprint($this->dbg,"chk 3\n");
  $this->table .= "<tr>";
  $this->table .= "<td>";
  // $style = "background-color:beige";
  $style = ""; #none  
  // Since style is "", the use of $style below has no impact on display
  // in browser.
  $row1a = "";
  if ($this->dict == 'mw') {
   /* adjust $this->row */
   $this->mw_row_key_adjust($line);
   $row1a = "";
   if ($this->row1 != "") {
    $row1a = "<span style='$style'>{$this->row1}</span>";
   }
   if ($row1x != "") {
    $row1a = "$row1a<br/>\n$row1x";
   }
   if ($row1a != "") {
    $this->table .= "$row1a<br/>\n{$this->row}\n";
   }else {
    $this->table .= "{$this->row}\n";
   }
   /* Summary for MW. Note that row1 is NEVER the empty string
    row1x can be empty (usual) or not-empty (Whitney, Westergaard links)
    if row1x is not empty, then
      table = row1 <br> row1x <br> row
    if row1x is empty, then
      table = row1 <br> row
   */
  } else {
   $row1a = "<span style='$style'>{$this->row1}</span>";
   $this->table .= "$row1a\n<br/>{$this->row}\n";
   /* table = row1 + <br> + row */
  }
  /*  row1, row
  */
  $this->table .= "</td>";
  // This is so that there will be no need for a horizontal scroll. 12-14-2017
  $this->table .= "<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>";
  $this->table .= "</tr>";
  $i++;
 }
 $this->table .= "</table>\n";
}

 public function getline_key1($line) {
  if (preg_match('|<key1>(.*?)</key1>|',$line,$matches)) {
   $key1 = $matches[1];
   return $key1;
  }else {
   return $this->key;
  }
 }
 public function mw_row_key_adjust($line){
  $keyline = $this->getline_key1($line);
  if ($keyline == $this->key) {
   return; // no adjustment
  }
  //Do something to visually distinguish (exclude) this line.
  // modify $this->row
  $row = $this->row;
  $style = "background-color:rgb(235,235,235)"; # 235
  $this->row = "<span style='$style'>$row</span>";
  return;  // not implemented
 }
 public function sthndl_div($attribs) {
  // 07-05-2018. This function is still dictionary specific
   $n=$attribs['n'];
   if ($this->dict == 'gra') {
    if ($n == 'H') {$indent = "1.0em";}
    else if ($n == 'P') {$indent = "2.0em"; }
    else if ($n == 'P1') {$indent = "3.0em";}
    else {$indent = "";}
    $style="position:relative; left:$indent;";
    return "<br/><span style='$style'>";
   }else if ($this->dict == 'bur') {
    if (($n == '2')) {
     $style="position:relative; left:1.0em;";
     $ans = "<br/><span style='$style'>";
    } else if (($n == 'P')) {
     $style="";
     $ans = "<br/><span style='$style'>";
    } else if (($n == '3')) {
     $style="position:relative; left:2.0em;";
     $ans = "<br/><span style='$style'>";
    } else {
     // e.g. n="3"
     $style="";
     $ans = "<br/><span style='$style'>";
    }
    return $ans;
   }else if ($this->dict == 'stc') {
     if (($n == 'P')) {
      $style="position:relative; left:1.5em;";
     }else {
      $style="";
     }
     $ans = "<br/><span style='$style'>";
     return $ans;
   }else if ($this->dict == 'pwg') {
     if ($n == '1') {$indent = "1.0em";}
     else if ($n == '2') {$indent = "2.0em"; }
     else if ($n == '3') {$indent = "3.0em";}
     else {$indent = "";}
     $style="position:relative; left:$indent;";
     $ans = "<br/><span style='$style'>";
     return $ans;
   }else if ($this->dict == 'skd') {
    // for skd (only for n="F", 5 cases as of 8/23/2017)
    // also endhndl
    // Treat the same as "<F>"
    $ans = "<br/>";
    if ($n == "F") {
     #$ans .= "<strong>Footnote: ";
     $ans .= "<br/>&nbsp;<span class='footnote'>[Footnote: ";
    }
    return $ans; 
   }else if ($this->dict == 'krm') {
    if ($n == "F") {
     $ans = "<br/><b>Footnote </b> <span>";
    }else {
     // krm: n=lb, NI, P
     $ans = "<br/><span>";
    }
    return $ans; 
   }else if ($this->dict == 'pw') {
    //  n = 1 (number div), n = 2 (English letter), n = 3 (Greek letter)
    //  n = p (prefixed form, in verbs
    if ($n == '1') {$indent = "1.5em";}
    else if ($n == '2') {$indent = "3.0em";}
    else if ($n == '3') {$indent = "4.5em";}
    else {$indent = "";}
    $style = "position:relative; left:$indent;";
    $ans = "<br/><span style='$style'>";
    return $ans;
   }else if ($this->dict == 'ap') {
    // line break, and 
    // indent, whether 'n' is '2' or 'P' (only values allowed) 05-04-2017
    // also, n='3' 05-21-2017 
    //  Examples: n=2: akulAgamatantra
    //  n=P paRqitasvAmin
    //  n=3 agastyasaMhitA
    if ($n == '3') {
     $style="position:relative; left:2em;";
    }else if ($n == '2') {
     $style="position:relative; left:1em;";
    }else {
     $style="";
    }
    $ans = "<br/><span style='$style'>";
    return $ans;
   }else if (in_array($this->dict,array('pd','bhs','mwe','mw72','sch','snp','vei'))) {
    //  n = lb (line break)
    //  But for 'sch', there is no n attribute  (so $n is null or undefined).
    // snp has n=lb, P, HI.  Currently all are rendered as line break.
    // vei has n=lb, P.  Both are rendered as line break.
    $ans = "<br/><span>";
    return $ans;
   }else if (in_array($this->dict,array('wil','shs'))) {
    // line break, and 
    // indent, indent if 'n' is '2'
    // no indent if n='1' , 'E', 'lex' (for wil)
    //              n='1' , 'E', 'Poem' (for wil)
    if ($n == '2') {
     $style="position:relative; left:1.5em;";
    } else {
     $style="";
    }
     $ans = "<br/><span style='$style'>";
    return $ans;
   }else if (in_array($this->dict,array('gst','ieg','inm','mci'))) {
    if ($n == 'P') {$indent = "1.0em";}
    #else if ($n == 'lb') {$indent = "0.0em"; }
    else {$indent = "0.0em"; }
    $style="position:relative; left:$indent;";
    $ans = "<br/><span style='$style'>";
    return $ans;
   }else if (in_array($this->dict,array('ben','pui'))) {
    // in ben, this div is an empty div. The display
    // should begin a new indented paragraph.
    // Example under dIkz and garj.
    if ($n == 'P') {
     $ans = "<br/>&nbsp;&nbsp;&nbsp;<span>";
    } else { // doesn't occur for ben
     $ans = "<br/><span>";
    } 
    return $ans;
   }else if ($this->dict == 'vcp') {
    if ($n == 'Picture') {
     $ans = "<br/> &nbsp;<span style='font-size:smaller;'>(Picture)";
    } else { //P, H, HI
     $ans = "<br/> <span>";
    }
    return $ans;  
   }else if ($this->dict == 'bop') {
    // n = "lb" or "pfx".  Currently always a line break
    $ans = "<br/> <span>";
    return $ans;  
   }else if ($this->dict == 'bor') {
    if ($n == "lb") {  // 
     $ans = "<br/> <span>";   
    } else {
     $ans = "<span>";
    }
    return $ans;  
   }else if ($this->dict == 'pe') {
    // the div tag is empty for pe.
    // hence, indentation doesn't work using the position:relative trick.
    if ($n == 'P') {
     // line break plus indent. Since div is empty tag, it has no
     // content. Thus, position:relative; left:3.0em  doesn't indent.
     // Instead, use several &nbsp;
     $ans= "<br/><span>&nbsp;&nbsp;&nbsp;"; 
    }else if ($n == 'NI') {
     // two line breaks, no indent
     $ans = "<br/><br/><span>";
    }else { 
     // $n == "lb" . line break, no indent
     $ans = "<br/><span>";
    }
    return $ans;  
    } else if ($this->dict == 'pgn') {
    // the div tag is empty for pgn.
    // hence, indentation doesn't work using the position:relative trick.
    if ($n == 'P') {
     // line break plus indent. Since div is empty tag, it has no
     // content. Thus, position:relative; left:3.0em  doesn't indent.
     // Instead, use several &nbsp;
     $ans= "<br/><span>&nbsp;&nbsp;&nbsp;"; 
    }else { 
     // $n == "lb" . line break, no indent
     $ans = "<br/><span>";
    }
    return $ans;  
    } else if ($this->dict == 'acc') {
     // line break, and 
     // indent, whether 'n' is '2' or 'P' (only values allowed) 05-04-2017
     // also, n='3' 05-21-2017 
     //  Examples: n=2: akulAgamatantra
     //  n=P paRqitasvAmin
     //  n=3 agastyasaMhitA
     if (($n == '2') || ($n=='P')) {
      $style="position:relative; left:1.5em;";
      $ans = "<br/><span style='$style'>";
     } else {
     // e.g. n="3"
     $style="";
     $ans = "<br/><span style='$style'>";
   }
    return $ans;  
  }else { // default
    // currently applies to:
    // cae with <div n="p"/>
    // mw 
    // ap90 with <div n="1"/> or <div n="P"/>. See basicadjust
    #$style="position:relative; top:1.0em";
    #$ans = "<br/><span>";
    $style="margin-top:0.6em;";
    $ans = "<div style='$style'></div><span>";
    return $ans;
   }
 }
 public function sthndl($xp,$el,$attribs) {

  if (preg_match('/^H.+$/',$el)) {
   // In general, don't display 'H1'. But MW has different
   if ($this->dict == 'mw') {
    // For mw, do display
    // However, don't display HxA, HxB, HxC (? see 'agre')
    if (preg_match('|^H[1-4]$|',$el)) {
     $this->row1 .= "($el)";
    }
   }else {
    // for other dictionaries, don't display 
   }
  } else if ($el == "s")  {
   $this->inSanskrit = true;
  } else if ($el == "key2"){
   $this->inkey2 = true;
  } else if ($el == "b"){ 
   $this->row .= "<strong>"; 
  } else if ($el == "graverse") {
   $this->row .= "<span style='font-size:smaller; font-weight:100'>";
  } else if ($el == "gralink") {
    $href = $attribs['href'];
    $tooltip = $attribs['n'];
    $style = 'text-decoration: none; border-bottom: 1px dotted #000;';
    $this->row .= "<a href='$href' title='$tooltip' style='$style' target='_rvlink'>";
  } else if ($el == "lanlink") {
    $href = $attribs['href'];
    # A work around.  Instead of real url parameter ('&page=...'),
    # we have, in basicadjust, put '_page=...'.  change back to '&page'
    $href = preg_replace('|_page|','&page',$href);
    # next so line number will appear in url of displayed page.
    $href = preg_replace('|_line|','&line',$href); 
    $tooltip = $attribs['n'];
    $target = $attribs['target'];
    $this->row .= "<a href='$href' title='$tooltip' target='$target'>";
  } else if ($el == "lex"){ // m. f., etc.
   $this->row .= "<strong>"; 
  } else if ($el == "i"){
   $this->row .= "<i>"; 
  } else if ($el == "br"){
   $this->row .= "<br/>";   
  } else if ($el == "h"){
  } else if ($el == "body"){
  } else if ($el == "tail"){
  } else if ($el == "L"){
  } else if ($el == "L1"){
   // for MW only, work done in chrhndl 
  } else if ($el == "s1") {
   // currently only MW.  This has an 'slp1' attribute which could be
   // used to replace the IAST text with Devanagari. However currently
   // we just display the IAST text, so do nothing with this element
  } else if ($el == "etym") {
    $this->row .= "<i>";
  } else if ($el == "info") { // mw no action
  } else if ($el == "pc"){
  } else if ($el == "info") { // mw no action
  } else if ($el == "to") { // mw no action
  } else if ($el == "ns") { // mw no action
  } else if ($el == "shortlong") { // mw no action
  } else if ($el == "srs") { // mw no action. Different from previous version.
  } else if ($el == "pcol") { // mw no action. Different from previous version.
  } else if ($el == "nsi") { // mw72 no action
  } else if ($el == "pb"){
   if ($this->dict == "mw") {
    # do nothing.
   }else if (in_array($this->dict,array("bur","stc"))) {
    # do nothing
   }else {
    $this->row .= "<br/>";
   }
  } else if ($el == "key1"){
  } else if ($el == "hom"){ // handled wholly in chrhndl
  } else if ($el == "F"){
   #$this->row .= "<br/>&nbsp;<span class='footnote'>[Footnote: ";
   $style = "font-weight:bold;";
   $this->row .= "<br/>[<span style='$style'>Footnote: </span><span>";
  } else if ($el == "symbol") {
  } else if ($el == "div") {
   $this->row .= $this->sthndl_div($attribs);
  } else if ($el == "alt") {
   // Alternate headword
   $style = "font-size:smaller";
   $this->row .= "<span style='$style'>(";
  } else if ($el == "hwtype") {
   // Ignore
  } else if ($el == "sup") {
   if (in_array($this->dict,array('gst','krm','mci'))) {
    $this->row .= '<sup style="font-weight:bold;">';
   } else {
    $this->row .= "<sup>";
   }
  } else if ($el == "lbinfo") {
    // empty tag.
  } else if ($el == "lang") {
    // nothing special here  Greek remains to be filled in
    // Depends on whether the text is filled in
    $n = $attribs['n'];
    if (in_array($this->dict,array('pwg','mw','pw','wil','md','yat','mw72','snp','stc','gra','lan','inm','bur','bop','ben','sch'))) {
     # nothing to do.  Greek (and other) unicode has been provided.
    }else {
     # put a placeholder where the greek, arabic, etc. needs to be provided.
     $this->row .= " ($n) ";
    }
  } else if ($el == "lb") {
    $this->row .= "<br/>";
  } else if ($el == "C") {
   $n = $attribs['n'];
   if ($this->dict == "vcp") {
    // vcp specific
    if ($n == '1') {
     $this->row .= "<br/>";
    }
   }
   $this->row .= "<strong>(C$n)</strong>"; // any dictionary
  } else if ($el == "edit"){ // vcp
    // no display
  } else if ($el == "ls") {
   if (isset($attribs['n'])) {
    $tooltip = $attribs['n'];
    $this->row .= "<span class='ls' title='$tooltip'>";   
    #$this->row .= "<span class='ls' title=\"$tooltip\">";   
   }else {
    $this->row .= "&nbsp;<span class='ls'>";   
   }
  } else if ($el == "span") {
   if (isset($attribs['class'])) {
    $class = $attribs['class'];
    $this->row .= "<span class='$class'>";
   } else if (isset($attribs['style'])) {
    $style = $attribs['style'];
    $this->row .= "<span style='$style'>";
   } else {
   $this->row .= "<span>";
   }
  } else if ($el == "lshead") {
   // pwg, pw
   $style = "color:blue; border-bottom: 1px dotted #000; text-decoration: none;";
   $style = "color:blue;";
   $this->row  .= "<span style='$style' class='ls'>";
  } else if ($el == "is") {
    //pwg, pw
   #$this->row .= "<span style='font-style: normal; color:teal'>";
   $this->row .= "<span style='letter-spacing:2px;'>"; # this is more like the text
  } else if ($el == "bot") {
   $this->row .= "<span style='color: brown'>";
  } else if ($el == "bio") {
   $this->row .= "<span style='color: brown'>";
  } else if ($el == "sic") {
   // no rendering
  } else if ($el == "ab"){
    if (isset($attribs['n'])) {
     $tran = $attribs['n'];
     #dbgprint(true," sthndl. ab. tran=$tran\n");
     #$this->row .= "<span title='$tran' style='text-decoration:underline'>";
     # this style provides a 'dotted underline'
     $style = "border-bottom: 1px dotted #000; text-decoration: none;";
     $this->row .= "<span title='$tran' style='$style'>";
    }else {
     $this->row .= "<span>";
    }
  } else if ($el == "vlex"){ // no display
  } else if ($el == "mark"){ 
   // skd. n = H,P
   $n = $attribs['n'];
   $row .= "<strong>($n) </strong>";   
  } else if ( ($el == "pic")&&($this->dict == "ben")) {
   $filename = $attribs['name'];
   $path = "../../web/images/$filename";
   $this->row .= "<img src='$path'/>";   
  } else if ($el == "note") {
   // no action currently. For krm.   
  } else if ($el == "Poem") {
   if ($this->dict == 'pe') {
    $style = "position:relative; left:3.0em;";
    $this->row .= "<br/><div style='$style'>";
   }else {
    // For krm.   
    $this->row .= "<br/>";    
   }
  } else if ($el == "type") {
    // displayed in chrhndl
  } else {
   // $this->row .= "<br/>&lt;$el&gt;";
   $a = array();
   foreach($attribs as $key=>$value) {
    $a[] = "$key='$value'";
   }
   $astring = join(" ",$a);
   $this->row .= "<$el $astring>";
  }

  $this->parentEl = $el;
}

 public function endhndl($xp,$el) {
  $this->parentEl = "";
  if ($el == "s") {
   $this->inSanskrit = false;
  } else if ($el == "F") {
   $this->row .= "]</span>&nbsp;<br/>";
  } else if ($el == "b"){ 
   $this->row .= "</strong>"; 
  } else if ($el == "graverse") {
   $this->row .= "</span>";
  } else if ($el == "gralink") {
   $this->row .= "</a>";
  } else if ($el == "lanlink") {
   $this->row .= "</a>";
  } else if ($el == "lex"){
   $this->row .= "</strong>"; 
  } else if ($el == "i"){
   $this->row .= "</i>"; 
  } else if ($el == "pb"){
   if ($this->dict == "mw") {
    # do nothing.
   }else if (in_array($this->dict,array("bur","stc"))) {
    # do nothing
   }else {
    $this->row .= "<br/>";
   }
  } else if ($el == "key2") {
   $this->inkey2 = false;
  } else if ($el == "symbol") {
  } else if ($el == "div") {
   if ($this->dict == "skd") {
    #$this->row .= " ( Footnote End)</strong>";
    $this->row .= "]</span>&nbsp;<br/>";
   }else {
   // close the div span
    $this->row .= "</span>";
   }
  } else if ($el == "alt") {
   // close the span, and introduce line break
   $this->row .= ")</span><br/>";
  } else if ($el == "sup") {
   $this->row .= "</sup>";
  } else if ($el == "ls") {
   $this->row .= "</span>&nbsp;";
  } else if ($el == "span") {
   $this->row .= "</span>";
  } else if ($el == "is") {
   $this->row .= "</span>";
  } else if ($el == "bot") {
   $this->row .= "</span>";
  } else if ($el == "bio") {
   $this->row .= "</span>";
  } else if ($el == "io") {
   $this->row .= "</span>";
  } else if ($el == "lshead") {
   $this->row .= "</span>";
  } else if ($el == "ab") {
   $this->row .= "</span>";
  } else if ($el == "etym") {
    $this->row .= "</i>";
  } else {
   $this->row .= "</$el>";
 }
}

 public function chrhndl($xp,$data) {
  $sdata = $this->sdata;
  if ($this->inkey2) {
   //$data = strtolower($data);
   if ($this->dict == 'mw') {
    // don't show
   }else {
    // 08-07-2020 also don't show for other dictionaries.
    /*
    if (in_array($this->dict,array('ae','mwe','bor'))) {
     // no transliteration of $key for English headword
     $this->row1 .= "&nbsp;<span class='$sdata'>$data</span>";
    }else {
     $this->row1 .= "&nbsp;<span class='$sdata'><SA>$data</SA></span>";
    }
    */
   }
  } else if ($this->parentEl == "key1"){ // nothing printed
  } else if ($this->parentEl == "pb") {
   if (true) { // (in_array($this->dict,array("pwg"))) {
    $hrefdata = $this->getHrefPage($data);
    $style = "font-size:smaller; font-weight:bold;";
    $this->row .= "<span style='$style'> $hrefdata</span>";   
   }
  } else if ($this->parentEl == "pc") {
   $hrefdata = $this->getHrefPage($data);
   $style = "font-size:normal; color:rgb(160,160,160);";
   $this->row1 .= "<span style='$style'> [Printed book page $hrefdata]</span>";
  } else if ($this->parentEl == "L") {
   $style = "font-size:normal; color:rgb(160,160,160);";
   $this->row1 .= "<span style='$style'> [Cologne record ID=$data]</span>";
  } else if ($this->parentEl == "L1") {
    // only applies to MW. L1 tag generated in basicadjust. 
   $style = "font-size:normal; color:rgb(160,160,160);";
   $this->row .= "<span class='lnum' style='$style'> [ID=$data]</span>";
  } else if ($this->parentEl == 's') {
   $this->row .= "<span class='$sdata'><SA>$data</SA></span>";
  } else if ($this->inSanskrit) {
   // probably not needed
   $this->row .= "<span class='$sdata'><SA>$data</SA></span>";
  } else if ($this->parentEl == "hom") {
   /* for some dictionaries, show hom elements*/
   if (in_array($this->dict,array('mw','pwkvn','md'))) {
    $this->row .= "<span class='hom' title='Homonym'>$data</span>";
   }
  } else if ($this->parentEl == 'div') { 
   $this->row .= $data;
  } else if ($this->parentEl == 'pb') { 
   if (in_array($this->dict,array("bur","stc"))) {
    # do nothing
   }else {
    $this->row .= $data;
   }
  } else if ($this->parentEl == "alt") {
   $this->row .= $data ;
  } else if ($this->parentEl == "lang") {
   // Greek typically uncoded
   //$data = $data . ' (greek)';
   if ($this->dict == "mw") {
    $this->row .= "<i>$data</i>"; # Greek italic for MW
   } else {
    $this->row .= $data;
   }
  } else if ($this->parentEl == "ab") {
   $this->row .= "$data";
   /* not used 12-14-2017
   $tran = getABdata($data);
   $dbg = false;
   dbgprint($dbg,"getABdata: $data -> $tran\n");
   if ($tran == "") {
   $this->row .= "$data";
   }else {
   $this->row .= "<span  title='$tran' style='text-decoration:underline'>";
   $this->row .= "$data";
   $this->row .= "</span>";
   }
   */
  }else if ($this->parentEl == "ls") { 
   #$data1 = format_ls($data);
   #$this->row .= $data1;
   $this->row .= $data;
  } else if ($this->parentEl == "type") {
    // 08-07-2020: Which dictionaries have 'type' tag?  SCH?
    // prepend to $row1, so it precedes key2
    // Note: $row1 is null in this routine.  change to $this->row1
    //$this->row1 = "<strong>$data</strong> " . $row1;
    $this->row1 = "<strong>$data</strong> " . $this->row1;
  } else { // Arbitrary other text
   $this->row .= $data;
  }
}
public function getHrefPage($data) {
/* getHrefPage generates markup for the link to a program which displays a pdf, as
 specified by the  input argument '$data'.
 In this implementation, the program which serves the pdf is
 $serve = ../webtc/servepdf.php.
 $data is assumed to be a string with a comma-delimited list of page numbers,
 only the first of which is used to generate a link.
 The markup returned for a given $lnum in the list $data is
   <a href='$serve?page=$lnum' target='_Blank'>$lnum</a>
 It is up to $serve to associate $lnum with a file.

*/
  $ans="";
 //$lnums = preg_split('/[,-]/',$data);
 $serve = $this->serve;
 $lnums = preg_split('/[,]/',$data);  //%{pfx}
 foreach($lnums as $lnum) {
  #list($page,$col) =  preg_split('/[-]/',$lnum);
  $page = $lnum; # this may be dictionary specific.
  if ($ans == "") {
   $dict = $this->dict;
   $args = "dict=$dict&page=$page";
   #$ans = "<a href='$serve?$args' target='_Blank'>$lnum</a>";
   $dictup = strtoupper($dict);
   $style = "color:rgb(130,130,130);";
   $ans = "<a href='$serve?$args' target='_$dictup' style='$style'>$lnum</a>";
  }else {
   $ans .= ",$lnum";
  }
 }
 return $ans;
}
public function mw_extra_line($line) {
 /* Currently only used in mw for links to Whitney and Westergaard.
  Based on <info whitneyroots="X"/> or <info westergaard="X"/>
 */
 include("dictinfowhich.php");
 $href0_whit_cologne = "//www.sanskrit-lexicon.uni-koeln.de/scans/csl-whitroot/disp/index.php";
 $href0_west_cologne = "//www.sanskrit-lexicon.uni-koeln.de/scans/csl-westergaard/disp/index.php";

 $href0_whit_xampp = "//localhost/cologne/csl-whitroot/disp/index.php";
 $href0_west_xampp = "//localhost/cologne/csl-westergaard/disp/index.php";
 
 if ($dictinfowhich == "cologne") {
  $href0_whit = $href0_whit_cologne;
  $href0_west = $href0_west_cologne;
 } else {
  // use local module if it exists. Otherwise, use Cologne
  // We are in cologne/xxx/web/webtc OR in cologne/csl-apidev/
  if (preg_match("|webtc$|",__DIR__)) {
   $href0_whit_rel = "../../../csl-whitroot/disp/index.php";
   $href0_west_rel = "../../../csl-westergaard/disp/index.php";
  }else {  
   // assume we are in cologne/csl-apidev
   $href0_whit_rel = "../csl-whitroot/disp/index.php";
   $href0_west_rel = "../csl-westergaard/disp/index.php";
  }
  if (file_exists($href0_whit_rel)) {
   $href0_whit = $href0_whit_xampp;
  } else {
   $href0_whit = $href0_whit_cologne;
  }
  if (file_exists($href0_west_rel)) {
   $href0_west = $href0_west_xampp;
  } else {
   $href0_west = $href0_west_cologne;
  }
 }
 $ans1=""; // whitney
 $ans2=""; // westergaard
 if (preg_match('|<info whitneyroots="(.*?)"/>|',$line,$matches)) {
  $x = $matches[1];
  $href0=$href0_whit;
  $results = preg_split("|;|",$x);
  $elts=array();
  foreach ($results as $rec) {
   list($whitkey,$whitpage) = preg_split("|,|",$rec);
   $href = "$href0" . "?page=$whitpage";
   $whitkey1 = $whitkey; 
   $whitkey2 = "";
   if (preg_match('|^([^1-9]*)([1-9]*)$|',$whitkey,$matches)) {
    $whitkey1 = $matches[1];
    $whitkey2 = $matches[2];
   }
   $sdata = $this->sdata;
   $elt = "<a href='$href' target='_Whitney'><span class='$sdata'><SA>$whitkey1</SA></span>$whitkey2</a>";
   $elts[] = $elt;
  }
  $ans1a = join(", ",$elts);
  $ans1 = "<em>Whitney Roots links:</em> " . $ans1a;
  #$ans1 = $ans1 . '  <br/>'; # dbg
  #dbgprint($dbg,"basicdisplay.php mw_extra_line: ans1=$ans1\n");
 }
 if (preg_match('|<info westergaard="(.*?)"/>|',$line,$matches)) {
  $x = $matches[1];
  $href0=$href0_west;
  $results = preg_split("|;|",$x);
  $elts=array();
  foreach ($results as $rec) {
   list($westkey,$westsutra,$madhaviyasutra) = preg_split("|,|",$rec);
   // westsutra is of form (section.rootnum)
   // our links require the section
   list($westsection,$westrootnum) = preg_split("|[.]|",$westsutra);
   $href = "$href0" . "?section=$westsection";
   $elt = "<a href='$href' target='_Westergaard'>$westsutra</a>";
   $elts[] = $elt;
  }
  $ans2a = join(", ",$elts);
  $ans2 = "<em>Westergaard Dhatupatha links:</em> " . $ans2a;
 }
 if (($ans1 != "") && ($ans2 != "")) {
  $ans = "$ans1&nbsp;&nbsp;&nbsp;&amp;&nbsp;$ans2";
 }else {
  $ans = "$ans1$ans2";
 }
 return $ans;
}
public function mci_extra_line($line) {
 /*
 display section name
 */
 $ans = "";
 if (preg_match('|<info section="(.*?)"/>|',$line,$matches)) {
  $x = $matches[1];
  $section = array();
  $section["1.1"] = "Names of Serpents, Birds, Animals etc.";
  $section["1.2"] = "Names of Missiles, Weapons, Bows etc.";
  $section["1.3"] = "Names of Literary Works, Parts of Works etc.";
  $section["1.4"] = "Names of Divisions of Time, Planets, Nakṣatras etc.";
  $section["1.5"] = "Names of Tīrthas, Rivers, Mountains, Forests etc.";
  $section["1.5A"] = "Names of Āśramas, Villages, Cities etc.";
  $section["1.6"] = "Names of Countries, Peoples, Islands etc.";
  $section["1.7"] =  "Miscellaneous Names";
  if (isset($section[$x])) {
   $name = $section[$x];
   $ans = "<b>$name</b>"; /* first option */
   $ans = "<i>($name)</i>"; /* second option */
   $x1 = substr($x,2);
   $ans = "<i>($x1. $name)</i>"; /* third option */
  }
 }
 return $ans;
}
} ## end of class 
?>
