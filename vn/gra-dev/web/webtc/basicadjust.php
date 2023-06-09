<?php
error_reporting(E_ALL & ~E_NOTICE & ~E_WARNING);
?>
<?php 
/*basicadjust.php
BasicAdjust class  Takes a parameter object
   and a list of xml records from the dictionary database,
   and adjust each of these records so it is ready for the BasicDisplay.
   This was formerly done by the BasicDisplay class in line_adjust function.
   The hope is to have dictionary specific code in this BasicAdjust class,
   and to have the BasicDisplay class to be identical for all dictionaries.
*/
require_once('dal.php');
require_once('dbgprint.php');
class BasicAdjust {
 public $getParms;
 public $adjxmlrecs;
 public $dal_ab, $dal_auth; // 
 public $accent;
 public $dbg;
 public $pagecol;
 public $dict;
 public function __construct($getParms,$xmlrecs) {
  $this->accent = $getParms->accent;
  $dict = $getParms->dict;
  $this->dict = $dict;
  $key = $getParms->key;
  $this->dbg=false;
  $this->dal_ab = new Dal($dict,"ab");
  if (in_array($dict,array('pwg','pw','pwkvn'))) {
   $this->dal_auth = new Dal($dict,"bib");  # pwgbib
   dbgprint(false,"basicadjust: bib file open? " . $this->dal_auth->status ."\n");
  }else if (in_array($dict,array('mw','ap90','ben','sch'))){
   $this->dal_auth = new Dal($dict,"authtooltips");
  }else {
   $this->dal_auth = null;
  }
 
  $this->getParms = $getParms;
  $this->adjxmlrecs = array();
  #$i = 0;
  foreach($xmlrecs as $line) {
   $this->pagecol = '';
   $line1 = $this->line_adjust($line);
   $this->adjxmlrecs[] = $line1;
   #$i = $i + 1;
   dbgprint($this->dbg,"basicadjust: line=\n$line\n\nadjline=$line1\n");
  }
  
 }
 public function line_adjust($line) {
 $dbg = false;
 $line = preg_replace('/¦/',' ',$line);
 $line = preg_replace_callback('|<chg +type="(.*?)" +n="(.*?)" src="(.*?)">(.*?)</chg>|',"BasicAdjust::chg_markup",$line);
 $line = preg_replace_callback('|<info vn="(.*?)"/>|',"BasicAdjust::infovn_markup",$line);
           
$line = preg_replace_callback('|<s>(.*?)</s>|','BasicAdjust::s_callback',$line);
 $line = preg_replace_callback('|<key2>(.*?)</key2>|','BasicAdjust::key2_callback',$line);
 //$line = preg_replace("|\[Page.*?\]|",  "<pb>$0</pb>",$line);
 $line = preg_replace("|\[(Page.*?)\]|",  "<pb>$1</pb>",$line);

 $line = preg_replace('/<pc>Page(.*)<\/pc>/',"<pc>\\1</pc>",$line);

 if (preg_match('/<pc>(.*)<\/pc>/',$line,$matches)){
  if($this->pagecol == $matches[1]){
   $line = preg_replace('/<pc>(.*)<\/pc>/','',$line);
  }else {$this->pagecol = $matches[1];}
 }
 /*  Replace the 'title' part of a known ls with its capitalized form
     This is probably particular to pwg and/or pw
 */
 if (in_array($this->getParms->dict,array('pw','pwg','pwkvn'))) {
  $line = preg_replace_callback('|<ls(.*?)>(.*?)</ls>|',
      "BasicAdjust::ls_callback_pwg",$line);
  
      
 }else if (in_array($this->getParms->dict,array('mw','ap90','ben','sch'))){
  $line = preg_replace_callback('|<ls(.*?)>(.*?)</ls>|',
      "BasicAdjust::ls_callback_mw",$line);

  $line = preg_replace('|<ls>ib[.]|','<ls><ab>ib.</ab>',$line);    
 }
 /* 12-14-2017
  'local' abbreviation handled here. Generate an n attribute if one
   is not present
 */
 $line = preg_replace_callback('|<ab(.*?)>(.*?)</ab>|',"BasicAdjust::abbrv_callback",$line);
 
 // Revised 04-05-2021, 04-09-2021 for AV
 $dbg=false;
 dbgprint($dbg,"BasicAdjust dict={$this->getParms->dict}\n");
 if ($this->getParms->dict == 'gra') {
  dbgprint($dbg,"BasicAdjust before rgveda, avveda: $line\n");
  $line = preg_replace_callback('|[{](AV[.] .*?)[}]|',"BasicAdjust::avveda_verse_callback",$line);
  $line = preg_replace_callback('|[{](.*?)[}]|',"BasicAdjust::rgveda_verse_callback",$line);
  dbgprint($dbg,"BasicAdjust after rgveda: $line\n");
 }
 if ($this->getParms->dict == 'lan') {
  #$dbg=true; ###11-20
  /* Two types: <ls n="lan,16,4">16^4^</ls>
      <ls n="wg,1235">1235b</ls>
  */
  dbgprint($dbg,"BasicAdjust before lanman link: $line\n");
  $line = preg_replace_callback('|<ls n="(.*?)">(.*?)</ls>|',"BasicAdjust::lanman_link_callback",$line);
  dbgprint($dbg,"BasicAdjust after lanman_link: $line\n");
 }

 //$line = preg_replace('|- <br/>|','',$line);
 //$line = preg_replace('|<br/>|',' ',$line);
 // 2018-07-07  Handle lex tag.  
 $line = preg_replace_callback('|<lex(.*?)>(.*?)</lex>|',"BasicAdjust::add_lex_markup",$line);
 
  if (in_array($this->getParms->dict, array("mw","md"))) {
   $line = $this->move_L_mw($line);
   # remove <hom>X</hom> within head portion
   $line = preg_replace("|<key2>(.*?)<hom>.*?</hom>(.*?<body>)|","<key2>$1$2",$line); 
   # remove space after sqrt 
   $line = preg_replace("|√ |u","√",$line); # experiment of 12/25/2019
  }
  else if ($this->getParms->dict == "ap90") {
   /*  ap90.xml has a line break '<lb/>' according to the printed edition.
     In the display, these are not recognized.
     Further, the display attempts to rejoin hyphenation due to line breaks.
     Finally, the pattern '<b>--X</b>' is treated as a division that generates
     a line break.
   */
   #dbgprint(true,"line before <lb> changes\n$line\n");
   $line = preg_replace('|- *<lb/>|','',$line);
   $line = preg_replace('|-</s> <lb/><s>|','',$line);
   $line = preg_replace('|<lb/>|','',$line);
   /* moved into make_xml.py 04-21-2020
   # now reintroduce some line breaks, and replace '--' with '&mdash;'
   # tech note on php:  when html entity &mdash; is used, then there is
   # an error in the xml parser in basicdisplay.php.  However, when we use 
   # the numerical code, '&#x2014;', the error disappears.
   # It might be better to do this logic (including the em-dash) in
   # make_xml.py or even in ap90.txt. E.g., change
   # <b>--X</b> to <div n="1"/><b>—X</b>
   $line = preg_replace('|<b>--|','<div n="1"/><b>&#x2014; ',$line);
   # also, there are seven instances of "<P/>". Replace with a div
   $line = preg_replace('|<P/>|','<div n="P"/>',$line);
   # remove '-' after <s> 04-11-2021
   # $line = preg_replace('|<s>--|','<div n="1"/><b>&#x2014;</b> <s>-',$line);
   $line = preg_replace('|<s>--|','<div n="1"/><b>&#x2014;</b> <s>',$line);
   // 04-11-2021.  Add line breaks at two additional patterns
   // at start of italics (about 2000 cases)
   $line = preg_replace('|<i>--|','<div n="1"/><i>&#x2014; ',$line);
   // preceding small Roman numerals (about 360 case, in verbs)
   $line = preg_replace('|--([IV]+[.])|','<div n="1"/>&#x2014; \1',$line);
   #dbgprint(true,"line after <lb> changes\n$line\n");
   // any remaining -- to mdash
   $line = preg_replace('|--|','&#x2014; ',$line);
   */
  }
  else if ($this->getParms->dict == "ap") {
   // replace -- with mdash : perhaps should be part of ap.txt
   $line = preg_replace('/--/','&#8212;',$line);
   // 03-12-2017.  Put 'b' (bold) tag around the first word of a div
   $line = preg_replace('|(<div[^>]*>)(\(<i>.</i>\))|','\\1<b>\\2</b>',$line);
   // 11-29-2018.  Also pattern '<s>--X</b>' 
   $line = preg_replace('|(<div[^>]*>)([0-9]+)|','\\1<b>\\2</b>',$line);
   // Remove <root/> tag -- it plays no part in display
   $line = preg_replace('|<root/>|','',$line);
  }
  else if ($this->getParms->dict == "yat") {
   $line = preg_replace('|- <br/>|','',$line);
   $line = preg_replace('|<br/>|',' ',$line);
   $line = preg_replace('/--/','&#8212;',$line);  # emdash
  }
  else if ($this->getParms->dict == "shs") {
   $line = preg_replace('|- <lb/>|','',$line);
   $line = preg_replace('|<lb/>|',' ',$line);
   $line = preg_replace('/--/','&#8212;',$line);  # emdash
  } else if ($this->getParms->dict == "ben") {
   $line = preg_replace('/--/','&#8212;',$line);  # emdash
   $line = preg_replace('|<g></g>|','<lang n="greek"></lang>',$line);
   $line = preg_replace('|<P/>|','<div n="P"/>',$line);
  } else if ($this->getParms->dict == "bor") {
   /* Put bold tag around first word of <div n="1"> or <div n="I"> 
      Sometimes there is no space character in the div. Remedy this by always
      putting a space before a closing div </div>.
   */
   $line = preg_replace('|</div>|',' </div>',$line);
   $line = preg_replace('|<div n="([1I])">([^ ]*)|','<div n="\1"><b>\2</b>',$line);
  } else if ($this->getParms->dict == "mw72") {
   # removed 10-31-2019, since Greek text now provided in mw72.
   #$line = preg_replace('|></lang>|'," empty='yes'></lang>",$line);
  } else if ($this->getParms->dict == "inm") {
   # Greek text in inm is italic
   $line = preg_replace('|<lang n="greek">|','<i><lang n="greek">',$line);
   $line = preg_replace('|</lang>|','</lang></i>',$line);
  } else if ($this->getParms->dict == "sch") {
   // this conversion now present in sch.txt
   // $line = preg_replace('|\^(.)|',"<sup>\\1</sup>",$line);
  } else if ($this->getParms->dict == "acc") {
   # this should have been done in acc.txt or acc.xml
   $line = preg_replace('|\^([a-d02th]+)|',"<sup>\\1</sup>",$line);
   $line = preg_replace('/--/','&#8212;',$line);  # emdash
   # also, remove breaks.  This is a display choice, maybe not for acc.txt,xml
   $line = preg_replace('|- <br/>|','',$line);
   $line = preg_replace('|<br/>|',' ',$line);
  }
  if ($this->getParms->dict == "mw")  {
   /* 11-13-2018 make bold abbreviations following <div n="vp">
   */
  $line = preg_replace('|(<div n="vp"/> *)(<ab.*?</ab>)|',"\\1<b>\\2</b>",$line);
  }


 return $line;
}

 public function ls_matchabbr($fieldname,$fieldidx,$data) {
  $dbg = false;
  $table = $this->dal_auth->tabname;
  dbgprint($dbg,"ls_matchabbr: data=$data\n");
  //dbgprint($dbg,"  table=$table\n");
  $ans = array();  // default return value
  // Use $data. Variant of getgeneral
  if (!$this->dal_auth->file_db) {
   return $ans;
  }
  // 
  if (!preg_match("|^([^ .,']+)|",$data,$matches)) {
   return $ans;
  }
  //$tabid = 'code'; // pw, pwg, pwkvn
  $key = $matches[1];
  $key1 = $key . '%';
  $sql = "select * from $table where $fieldname LIKE '$key1'";
  dbgprint($dbg,"ls_matchabbr: sql=$sql\n");
  $result = $this->dal_auth->file_db->query($sql);
  $ansarr = array();
  $max = -1;
  $ansmax = null;
  foreach($result as $m) {
   $code0 = $m[$fieldidx];
   if (strpos($data,$code0) === 0) {
    // this is a candidate. is it the longest?
    $n = strlen($code0);
    if ($n > $max) {
     $ansmax = $m;
     $max = $n;
    }
   }
  }
  if ($ansmax == null) {
   // probably could not happen. Return default answer
   return $ans;
  }
  $ans = array($ansmax);
  return $ans;
 }
 public function ls_callback_pwg($matches) {
 // for pw, pwg
 // Two situations envisioned:
 // <ls>X</ls>  
 // <ls n="C">Y</ls>
 $dbg=false;
 $ans = $matches[0];
 $ndata = $matches[1];  // empty string or ' n="C"'
 $data0 = $matches[2];
 if (preg_match('|n="(.*?)"|',$ndata,$matchesn)) {
  $n = $matchesn[1]; //
  // $data = "$n $data0";  // controversial.
  $data1 = "$n $data0";
  $data = $data0;
 } else{
  $n = '';
  $data1 = $data0;
  $data = $data0;
 }
 dbgprint($dbg,"ls_callback_pwg BEGIN: ndata=$ndata, n=$n, data0=$data0, data1=$data1\n");
 dbgprint($dbg,"ls_callback_pwg : n=$n, data=$data\n");
 if (!$this->dal_auth->status) {
  return $ans;
 }
 $fieldname = 'code';
 $fieldidx = 1;
 $result = $this->ls_matchabbr($fieldname,$fieldidx,$data1);
 if (count($result) == 0) {
  return $ans; // failure
 }
  $rec = $result[0];
  list($n0,$code,$codecap,$text) = $rec;
  // 12-26-2017. pwg. Add lshead, so as to be able to style
  $ncode = strlen($code); // use substr_replace in case $code has parens
  if ($n != '') {
   //$datanew = preg_replace("/^$code/","<lshead></lshead>",$data);
   $datanew = $data;
   dbgprint($dbg,"pwg lshead 1: n=$n: datanew=$datanew\n");
  } else {
   //$datanew = preg_replace("/^$code/","<lshead>$codecap</lshead>",$data);
   $datanew = substr_replace($data,"<lshead>$codecap</lshead>",0,$ncode);
   dbgprint($dbg,"lshead 2: n=$n: datanew=$datanew\n");
  }
  # be sure there is no xml in the text
  $text = preg_replace('/<.*?>/',' ',$text);
  //dbgprint($dbg," ls_callback_pwg. text after removing tags: \n$text\n");
  # convert special characters to html entities
  # for instance, this handles cases when $tran has single (or double) quotes
  $tooltip = $this->htmlspecial($text);
  $tip0 = mb_substr($tooltip,0,10) . "...";
  //dbgprint($dbg," ls_callback_pwg code=$code,  codecap=$codecap, tooltip=$tip0\n");
 // 04-14-2021.  Use 'gralink' for certain values of 'code'
  //$linkcodes = array('ṚV.','AV.','P');
  $href = $this->ls_callback_pwg_href($code,$data1);
  dbgprint($dbg,"ls_callback_pwg. code=$code, data1=$data1, href=$href\n");
  if ($href != null) {
   // link
   //$ans = "<gralink href='$href' n='$tooltip'><ls>$datanew</ls></gralink>";
   $datanew1 = preg_replace("|</lshead>(.*)$|",'</lshead><span class="ls">${1}</span>',$datanew);
   //dbgprint(true,"datanew=$datanew\n");
   //dbgprint(true,"datanew1=$datanew1\n");
   if ($n == '') {
    $ans = "<gralink href='$href' n='$tooltip'><span class='ls'>$datanew1</span></gralink>";
    //dbgprint(true,"ans1=$ans\n");
   } else { // currently the same
    $ans = "<gralink href='$href' n='$tooltip'><span class='ls'>$datanew1</span></gralink>";    
    //dbgprint(true,"ans2=$ans\n");
   }
  }else {
   //$ans = "<ls n='$tooltip'>$datanew</ls>";
   $ans = "<ls n='$tooltip'><span class='dotunder ls'>$datanew</span></ls>";
  }
  dbgprint($dbg,"ls_callback_pwg: ans=$ans\n");
 
 return $ans;
}
public function ls_callback_pwg_href($code,$data) {
 $href = null; // default if no success
 $dbg = false;
 dbgprint($dbg,"ls_callback_pwg_href. data=$data\n");
 if (preg_match('|^(Spr[.]) ([0-9]+)|',$data,$matches)) {
  if (in_array($this->dict,array('pw'))) {
   // Indische Sprüche in pw
   $pfx = $matches[1];
   $verse = $matches[2];
   $href = "https://funderburkjim.github.io/boesp-prep/web1/boesp.html?$verse";
   dbgprint($dbg,"Spr: href=$href\n");
   return $href;
  }
  if ($this->dict == 'pwg') {
   // This is a reference to 1st edition of Indische Spruche in pwg.
   // Link to boesp as above is not correct.
   return $href;
  }
 }
 if (preg_match('|^(Spr[.]) \(II\) ([0-9]+)|',$data,$matches)) {
  // Indische Sprüche in pwg (2nd edition)
  $pfx = $matches[1];
  $verse = $matches[2];
  $href = "https://funderburkjim.github.io/boesp-prep/web1/boesp.html?$verse";
  dbgprint($dbg,"Spr: href=$href\n");
  return $href;
 }
 if (preg_match('|^(MBH[.]) *([0-9]+) *, *([0-9]+)[.]?$|',$data,$matches)) {
  // Mahabharata, Calcutta edition for pwg.
  // Some PW refs to MBH are different, using 3 parameters (Bombay)
  $pfx = $matches[1];
  $parvan = $matches[2];
  $verse = $matches[3];
  $href = "https://sanskrit-lexicon-scans.github.io/mbhcalc?$parvan.$verse";
  dbgprint($dbg,"$pfx: href=$href\n");
  return $href;
 }
 if (preg_match('|^(HARIV[.]) *([0-9]+)[.]?$|',$data,$matches)) {
  // Mahabharata, Calcutta edition for harivamsa
  $pfx = $matches[1];
  $verse = $matches[2];
  $href = "https://sanskrit-lexicon-scans.github.io/hariv?$verse";
  dbgprint($dbg,"$pfx: href=$href\n");
  return $href;
 }
 
 if (preg_match('|^(Chr[.]) *([0-9]+)|',$data,$matches)) {
  // Boehtlingk Chrestomathie, 2nd edition.
  if (! in_array($this->dict,array('pw'))) {
   // PWG refers under N. (Nalopakhyana), maybe others.
   // Not yet handled.
   return $href;
  }
  $pfx = $matches[1];
  $verse = $matches[2]; // page
  $href = "https://sanskrit-lexicon-scans.github.io/bchrest/index.html?$verse";
  dbgprint($dbg,"$pfx: href=$href\n");
  return $href;
 }

 if (!preg_match('|^(.*?)[.] *([0-9]+)[ ,]+([0-9]+)[ ,]+([0-9]+)(.*)$|',$data,$matches)) {
  return $href;
 }
 // links for Rigveda, Atharvaveda, or Panini,
 // Ramayana Gorresio, Ramayana Schlegel
 $code_to_pfx = array('ṚV.' => 'rv', 'AV.' => 'av', 'P.' => 'p',
  'Spr.' => 'Spr',
  'R. GORR.' => 'rgorr', 'R. ed. GORR.' => 'rgorr', 'GORR.' => 'rgorr',
  'R.' => 'rschl','R. SCHL.' => 'rschl');
 if (!isset($code_to_pfx[$code])) {
  return $href;
 }
 $pfx = $code_to_pfx[$code];
 $code0 = $matches[1];
 $imandala = (int)$matches[2]; 
 $ihymn = (int)$matches[3];
 $iverse = (int)$matches[4];
 dbgprint($dbg,"ls_callback_pwg_href. $code0, $imandala, $ihymn, $iverse\n");
 $rest = $matches[5];
 if (in_array($pfx,array('rv','av'))) {
  $hymnfilepfx = sprintf("%s%02d.%03d",$pfx,$imandala,$ihymn);
  $hymnfile = "$hymnfilepfx.html";
  $versesfx = sprintf("%02d",$iverse);
  $anchor = "$hymnfilepfx.$versesfx";
  $versesfx = sprintf("%02d",$iverse);
  $anchor = "$hymnfilepfx.$versesfx";
  $dir = sprintf("https://sanskrit-lexicon.github.io/%slinks/%shymns",$pfx,$pfx);
  $href = "$dir/$hymnfile#$anchor";
 }else if ($pfx == "p") {  // P.  = Panini
  $dir = "https://ashtadhyayi.com/sutraani";
  $href = "$dir/$imandala/$ihymn/$iverse";
 }else if (in_array($pfx,array('rgorr'))) { 
  $dir = "https://sanskrit-lexicon-scans.github.io/ramayanagorr";
  $href = "$dir/?$imandala,$ihymn,$iverse";
  return $href;
 }else if (in_array($pfx,array('rschl'))) {
  /* 06-13-2022. rschl is appropriate when $imandala is 1 or 2
  Otherwise ($imandala 3,4,5,6,7)rschl should change to rgorr
   This is known to be appropriate for pwg dictionary.
  */
  if (in_array($imandala,array(1,2))) {
   $dir = "https://sanskrit-lexicon-scans.github.io/ramayanaschl";
  }else {
   $dir = "https://sanskrit-lexicon-scans.github.io/ramayanagorr";
  }
  $href = "$dir/?$imandala,$ihymn,$iverse";
  return $href;
 }
 dbgprint($dbg,"href=$href\n");
 return $href; 
}

public function ls_callback_mw($matches) {
 // Try to also handle ap90, ben
 // Two situations envisioned:
 // <ls>X</ls>  
 // <ls n="C">Y</ls>
 $dbg=false;
 $ans = $matches[0];
 $ndata = $matches[1];  // empty string or ' n="C"'
 $data0 = $matches[2];
 if (preg_match('|n="(.*?)"|',$ndata,$matchesn)) {
  $n = $matchesn[1]; //
  $data1 = "$n $data0";  // controversial.
  $data = $data0; //10-07
 } else{
  $n = '';
  $data1 = $data0;
  $data = $data0;
 }
 dbgprint($dbg,"\nls_callback_mw BEGIN: ndata=$ndata, n=$n, data0=$data0, data1=$data1\n");
 if (!$this->dal_auth->status) {
  return $ans;
 }
 // --------------------------------------------------------------
 // Tooltip for name of work
 $fieldname = 'key';
 if ($this->dict == 'mw') {
  $fieldidx = 1;
 }else { // ap90, ben
  $fieldidx = 0;
 }
 $result = $this->ls_matchabbr($fieldname,$fieldidx,$data1);
 if (count($result) == 0) {
  dbgprint($dbg,"ls_callback_mw : ls_matchabbr returns no results\n");
  return $ans; // failure
 }
  $rec = $result[0];
  if ($this->dict == 'mw') {
   list($cid,$code,$title,$type) = $rec;
   $text = "$title ($type)";
   dbgprint($dbg,"ls_matchabbr returns: cid=$cid, code=$code, title=$title, type=$type\n");
  } else if (in_array($this->dict,array('ap90','ben','sch'))) {
   list($code,$text) = $rec;
  }
  # Add lshead, so as to be able to style
  // for mw and ap90, codecap = code
  dbgprint($dbg,"ls_callback_mw : n=$n, data=$data\n");
  $codecap = $code;
  $ncode = strlen($code); // use substr_replace in case $code has parens
  if ($n != '') {
   //$datanew = substr_replace($data,"<lshead>$data</lshead>",0);
   $datanew = $data;
   dbgprint($dbg,"lshead 1: n=$n: datanew=$datanew\n");
  } else {
   $datanew = substr_replace($data,"<lshead>$codecap</lshead>",0,$ncode);
   dbgprint($dbg,"lshead 2: n=$n: datanew=$datanew\n");
  }
  # be sure there is no xml in the text
  $text = preg_replace('/<.*?>/',' ',$text);
  # convert special characters to html entities
  # for instance, this handles cases when $tran has single (or double) quotes
  $tooltip = $this->htmlspecial($text);
  // --------------------------------------------------------------
  $href = null;
  //dbgprint(true,"before ls_callback_mw_href, dict=" . $this->dict . "\n");
  if ($this->dict == 'mw') {
   $href = $this->ls_callback_mw_href($code,$n,$data);
  }else if ($this->dict == 'ap90') {
   $href = $this->ls_callback_ap90_href($code,$n,$data);
  }else if ($this->dict == 'sch') {
   $href = $this->ls_callback_sch_href($code,$n,$data);
  }
  dbgprint($dbg,"ls_callback_mw: href=$href\n");
  if ($href != null) {
   // link
   //$ans = "<gralink href='$href' n='$tooltip'><ls>$datanew</ls></gralink>";
   dbgprint($dbg,"ls_callback_mw: n=$n, datanew=$datanew\n");
   if ($n == '') {
    $datanew1 = preg_replace("|</lshead>(.*)$|",'</lshead><span class="ls">${1}</span>',$datanew);
   }else {
    $datanew1 = '<span class="ls">' . $datanew . '</span>';
   }
   //dbgprint(true,"datanew1=$datanew1\n");
   $ans = "<gralink href='$href' n='$tooltip'><span class='ls'>$datanew1</span></gralink>";
  }else {
   $ans = "<ls n='$tooltip'><span class='dotunder ls'>$datanew</span></ls>";
  }
  dbgprint($dbg,"ls_callback_mw: ans=$ans\n");
 return $ans;
}
public function ls_callback_mw_href($code,$n,$data) {
 $href = null; // default if no success
 $dbg = false;
 dbgprint($dbg,"ls_callback_mw_href. code=$code, n='$n', data='$data'\n");
 $code_to_pfx = array('RV.' => 'rv', 'AV.' => 'av', 'Pāṇ.' => 'p',
  'MBh.' => 'MBH.','Hariv.' => 'hariv',
  'MBh. (ed. Calc.)' => 'MBHC', 'MBh. (ed. Bomb.)' => 'MBHB',
  'R.' => 'R', 'R. G.' => 'R', 'R. (G)' => 'R', 'R. (G.)' => 'R', 'R. [G]' => 'R',
  'R. ed. Gorresio' => 'R');
 //hrefs for MBHC, MBHB not implemented. MBHC is same as MBH.(?)
 if (!isset($code_to_pfx[$code])) {
  dbgprint($dbg,"ls_callback_mw_href. Code is unknown:'$code'\n");
  return $href;
 }
 $pfx = $code_to_pfx[$code];
 dbgprint($dbg,"ls_callback_mw_href: code=$code, pfx=$pfx\n");
 if ($n == '') {
  $data1 = $data;
 }else {
  $data1 = "$n $data";
 }
 if (in_array($pfx,array('rv','av'))) {
  if (preg_match('|^(.*?)[.] *([^ ,]+)[ ,]+([0-9]+)[ ,]+([0-9]+)(.*)$|',$data1,$matches)) {
   $code0 = $matches[1];
   $mandala = $matches[2];  // in lower-case roman numerals for mw
   $imandala = $this->roman_int($mandala);
   $ihymn = (int)$matches[3];
   $iverse = (int)$matches[4];
   dbgprint($dbg,"ls_callback_mw_href. $code0, $mandala, $ihymn, $iverse\n");
   $rest = $matches[5];
   $hymnfilepfx = sprintf("%s%02d.%03d",$pfx,$imandala,$ihymn);
   $hymnfile = "$hymnfilepfx.html";
   $versesfx = sprintf("%02d",$iverse);
   $anchor = "$hymnfilepfx.$versesfx";
   $versesfx = sprintf("%02d",$iverse);
   $anchor = "$hymnfilepfx.$versesfx";
   $dir = sprintf("https://sanskrit-lexicon.github.io/%slinks/%shymns",$pfx,$pfx);
   $href = "$dir/$hymnfile#$anchor";
   return $href;
  }else if (preg_match('|^(.*?)[.] *([^ ,]+)[ ,]+([0-9]+)(.*)$|',$data1,$matches))
  { // two parameter version. Supply verse number = 1
   $code0 = $matches[1];
   $mandala = $matches[2];  // in lower-case roman numerals for mw
   $imandala = $this->roman_int($mandala);
   if ($imandala == 0) {return $href;}
   $ihymn = (int)$matches[3];
   $iverse = 1;  // line to verse 1.
   dbgprint($dbg,"ls_callback_mw_href. $code0, $mandala, $ihymn, $iverse\n");
   $rest = $matches[5];
   $hymnfilepfx = sprintf("%s%02d.%03d",$pfx,$imandala,$ihymn);
   $hymnfile = "$hymnfilepfx.html";
   $versesfx = sprintf("%02d",$iverse);
   $anchor = "$hymnfilepfx.$versesfx";
   $versesfx = sprintf("%02d",$iverse);
   $anchor = "$hymnfilepfx.$versesfx";
   $dir = sprintf("https://sanskrit-lexicon.github.io/%slinks/%shymns",$pfx,$pfx);
   $href = "$dir/$hymnfile#$anchor";
   return $href;
  }else {
   return $href; // failure to match
  }
 } // end for rv, av
 if (in_array($pfx,array('p'))) {
  //if(! preg_match('|^(.*?)[.] *([0-9]+)-([0-9]+)[ ,]+([0-9]+)(.*)$|',$data1,$matches)) 
  // Panini for mw.   10-07-2021
  if(! preg_match('|^(.*?)[.] *([iv]+)[ ,]+([0-9]+)[ ,]+([0-9]+)(.*)$|',$data1,$matches)) {
    return $href;
   }
   $code0 = $matches[1];
   //$ic = (int)$matches[2];
   $romanlo = $matches[2];
   $ic = $this->roman_int($romanlo); 
   $is = (int)$matches[3];
   $iv = (int)$matches[4];
   $dir = "https://ashtadhyayi.com/sutraani";
   $href = "$dir/$ic/$is/$iv";
   return $href;
 }
 if (in_array($pfx,array('R'))) {
  // Ramayana, Goressio. Similar to 'p' (Panini), except for '$dir'
  dbgprint($dbg,"ls_callback_mw_href: data1=$data1\n");
  // data1 = code + data2.
  $data2 = substr_replace($data1,"",0,strlen($code));
  //$data2 = trim($data2);
  dbgprint($dbg,"ls_callback_mw_href: data2=$data2\n");
  if(! preg_match('| *([iv]+)[ ,]+([0-9]+)[ ,]+([0-9]+)(.*)$|',$data2,$matches)) {
    return $href;
   }
   $romanlo = $matches[1];
   $ic = $this->roman_int($romanlo); 
   $is = (int)$matches[2];
   $iv = (int)$matches[3];
   $dir = "https://sanskrit-lexicon-scans.github.io/ramayanagorr";
   $href = "$dir/?$ic,$is,$iv";
   return $href;
 }
 dbgprint($dbg,"ls_callback_mw_href: data1=$data1\n");
 if (preg_match('|^(MBh[.]) *([^ ,]+) *, *([0-9]+)[.]?$|',$data1,$matches)) {
  // Mahabharata, Calcutta edition for mw.
  $pfx = $matches[1];
  $parvan_roman = $matches[2];
  $parvan = $this->roman_int($parvan_roman);
  $verse = $matches[3];
  $href = "https://sanskrit-lexicon-scans.github.io/mbhcalc?$parvan.$verse";
  dbgprint($dbg,"ls_callback_mw_href: $pfx: href=$href\n");
  return $href;
 }
 if (preg_match('|^(Hariv[.]) *([0-9]+)[.]?$|',$data,$matches)) {
  // Mahabharata, Calcutta edition for harivamsa. For MW.
  $pfx = $matches[1];
  $verse = $matches[2];
  $href = "https://sanskrit-lexicon-scans.github.io/hariv?$verse";
  dbgprint($dbg,"$pfx: href=$href\n");
  return $href;
 }

 return $href; 
}
public function ls_callback_sch_href($code,$n,$data) {
 $href = null; // default if no success
 $dbg = false;
 dbgprint($dbg,"ls_callback_sch_href. code=$code, n=$n, data=$data\n");
 if (preg_match('|^(Spr[.]) ([0-9]+)|',$data,$matches)) {
   // Indische Sprüche in sch is assumed to be volume 2
   $pfx = $matches[1];
   $verse = $matches[2];
   $href = "https://funderburkjim.github.io/boesp-prep/web1/boesp.html?$verse";
   dbgprint($dbg,"Spr: href=$href\n");
   return $href;
  }
 $code_to_pfx = array('ṚV.' => 'rv', 'AV.' => 'av', 'P.' => 'p', 'Hariv.' => 'hariv', 'R. Gorr.' => 'rgorr','R.' => 'rschl');
 if (!isset($code_to_pfx[$code])) {
  return $href;
 }
 $pfx = $code_to_pfx[$code];
 if ($n == '') {
  $data1 = $data;
 }else {
  $data1 = "$n $data";
 }
 if (in_array($pfx,array('rv','av'))) {
  // #, #, #  (three decimal numbers, separated by commas)
  if (!preg_match('|^(.*?)[.] *([0-9]+)[,] +([0-9]+)[,] +([0-9]+)(.*)$|',$data1,$matches)) {
   return $href;
  }
  $code0 = $matches[1];
  $imandala = (int)$matches[2];
  $ihymn = (int)$matches[3];
  $iverse = (int)$matches[4];
  dbgprint($dbg,"ls_callback_ap90_href. $code0, $mandala, $ihymn, $iverse\n");
  $rest = $matches[5];
  $hymnfilepfx = sprintf("%s%02d.%03d",$pfx,$imandala,$ihymn);
  $hymnfile = "$hymnfilepfx.html";
  $versesfx = sprintf("%02d",$iverse);
  $anchor = "$hymnfilepfx.$versesfx";
  $versesfx = sprintf("%02d",$iverse);
  $anchor = "$hymnfilepfx.$versesfx";
  $dir = sprintf("https://sanskrit-lexicon.github.io/%slinks/%shymns",$pfx,$pfx);
  $href = "$dir/$hymnfile#$anchor";
  return $href;
 } // end for rv, av
 if (in_array($pfx,array('p'))) {
  // #, #, # (three decimal numbers, separated by commas)
  if(!preg_match('|^(.*?)[.] *([0-9]+)[,] +([0-9]+)[,] +([0-9]+)(.*)$|',$data1,$matches)) {
    return $href;
   }
   $code0 = $matches[1];
   $ic = (int)$matches[2];
   $is = (int)$matches[3];
   $iv = (int)$matches[4];
   $dir = "https://ashtadhyayi.com/sutraani";
   $href = "$dir/$ic/$is/$iv";
   return $href;
 }
 if (in_array($pfx,array('hariv'))) {
  // ## one decimal numbers
  if(!preg_match('|^(.*?)[.] *([0-9]+)(.*)$|',$data1,$matches)) {
    return $href;
   }
  // Mahabharata, Calcutta edition for harivamsa
  $pfx = $matches[1];
  $verse = $matches[2];
  $href = "https://sanskrit-lexicon-scans.github.io/hariv?$verse";
  dbgprint($dbg,"$pfx: href=$href\n");
  return $href;
 }
 if (in_array($pfx,array('rgorr'))) {
  // #, #, # (three decimal numbers, separated by commas)
  if(!preg_match('|^(.*?)[.] *([0-9]+)[,] +([0-9]+)[,] +([0-9]+)(.*)$|',$data1,$matches)) {
    return $href;
   }
   $code0 = $matches[1];
   $ic = (int)$matches[2];
   $is = (int)$matches[3];
   $iv = (int)$matches[4];
   $dir = "https://sanskrit-lexicon-scans.github.io/ramayanagorr";
   $href = "$dir/?$ic,$is,$iv";
   return $href;
 }
 if (in_array($pfx,array('rschl'))) {
  // #, #, # (three decimal numbers, separated by commas)
  if(!preg_match('|^(.*?)[.] *([0-9]+)[,] +([0-9]+)[,] +([0-9]+)(.*)$|',$data1,$matches)) {
    return $href;
   }
   $code0 = $matches[1];
   $ic = (int)$matches[2];
   $is = (int)$matches[3];
   $iv = (int)$matches[4];
   $dir = "https://sanskrit-lexicon-scans.github.io/ramayanaschl";
   $href = "$dir/?$ic,$is,$iv";
   return $href;
 }
 return $href; 
}
public function ls_callback_ap90_href($code,$n,$data) {
 $href = null; // default if no success
 $dbg = false;
 dbgprint($dbg,"ls_callback_ap90_href. code=$code, n=$n, data=$data\n");
 $code_to_pfx = array('Rv.' => 'rv', 'Av.' => 'av', 'P.' => 'p');
 if (!isset($code_to_pfx[$code])) {
  return $href;
 }
 $pfx = $code_to_pfx[$code];
 if ($n == '') {
  $data1 = $data;
 }else {
  $data1 = "$n $data";
 }
 if (in_array($pfx,array('rv','av'))) {
  // #. #. #  (three numbers,
  if (!preg_match('|^(.*?)[.] *([0-9]+)[.] +([0-9]+)[.] +([0-9]+)(.*)$|',$data1,$matches)) {
   return $href;
  }
  $code0 = $matches[1];
  //$mandala = $matches[2];  // in 
  //$imandala = $this->roman_int($mandala);
  $imandala = (int)$matches[2];
  $ihymn = (int)$matches[3];
  $iverse = (int)$matches[4];
  dbgprint($dbg,"ls_callback_ap90_href. $code0, $mandala, $ihymn, $iverse\n");
  $rest = $matches[5];
  $hymnfilepfx = sprintf("%s%02d.%03d",$pfx,$imandala,$ihymn);
  $hymnfile = "$hymnfilepfx.html";
  $versesfx = sprintf("%02d",$iverse);
  $anchor = "$hymnfilepfx.$versesfx";
  $versesfx = sprintf("%02d",$iverse);
  $anchor = "$hymnfilepfx.$versesfx";
  $dir = sprintf("https://sanskrit-lexicon.github.io/%slinks/%shymns",$pfx,$pfx);
  $href = "$dir/$hymnfile#$anchor";
  return $href;
 } // end for rv, av
 if (in_array($pfx,array('p'))) {
  // I. 2. 3
  if(!preg_match('|^(.*?)[.] *([IV]+)[.] +([0-9]+)[.] +([0-9]+)(.*)$|',$data1,$matches)) {
    return $href;
   }
   $code0 = $matches[1];
   $roman = $matches[2];  // upper-case
   $romanlo = strtolower($roman);
   $ic = $this->roman_int($romanlo);
   $is = (int)$matches[3];
   $iv = (int)$matches[4];
   $dir = "https://ashtadhyayi.com/sutraani";
   $href = "$dir/$ic/$is/$iv";
   return $href;
 }
 return $href; 
}

 public function abbrv_callback($matches) {
 /* <ab n="{tran>}">{data}</ab>
  <ab{attrib}>{data)</ab>
 */
 $x = $matches[0]; // full string
 $a = $matches[1];
 $data = $matches[2];
 $dbg=false;
 dbgprint($dbg,"abbrv_callback: a=$a, data=$data\n");
 if(preg_match('/n="(.*?)"/',$a,$matches1)) {
  dbgprint($dbg," abbrv_callback case 1\n");
  $ans = $x;
 }else if (preg_match('|^br|',$a)) {
  // <abbr> is used in chg_markup. Don't change it!
  return $x;
 }else {
  $tran = $this->getABdata($data);  
  # convert special characters to html entities
  # for instance, this handles cases when $tran has single (or double) quotes
  $tran = htmlspecialchars($tran,ENT_QUOTES);
  $ans = "<ab n='$tran'>$data</ab>";
  dbgprint($dbg," abbrv_callback case 2\n");
 }
 dbgprint($dbg," abbrv_callback returns $ans\n");
 return $ans;
}

 public function getABdata($key) {
 // abbreviation tool tips from Xab.sqlite
 $ans="";
 #$table = "{$this->getParms->dict}ab";
 $table = $this->dal_ab->tabname;
 $result = $this->dal_ab->getgeneral($key,$table);
 $dbg=false;
 dbgprint($dbg,"getABdata: length of result=" . count($result) . "\n");
 if (count($result) == 1) {
  list($key1,$data) = $result[0];
  if (preg_match('/<disp>(.*?)<\/disp>/',$data,$matches)) {
   $ans = $matches[1];
   /*  This taken from mw code; but is probably obsolete.
     It permitted <s>X</s> coding within the abbreviation expansion
     and conversion to the user's choice of 'filter'
   global $dispfilter;
   $temp = strtolower($dispfilter);
   $filterflag = (preg_match('/deva/',$temp) || preg_match('/roman/',$temp));
   if ($filterflag) {
	$ans = preg_replace('/<s>/','<SA>',$ans);
	$ans = preg_replace('/<\/s>/','</SA>',$ans);
   }
   */
  }
 }
 return $ans;
}
 public function add_lex_markup($matches) {
 /* <lex{attrib}|>{data}</lex> ignore attrib
   Turn it into an abbreviation.
   This function current just for cae dictionary.
 */
 if ($this->getParms->dict == "mw") {
  //Something more complex required for MW.
  return  $this->add_lex_markup_mw($matches);
 }
 $x = $matches[0]; // full <lex>X</lex> string
 $a = $matches[1]; # attributes
 $data = $matches[2]; # {data}
 $dbg=false;
 dbgprint($dbg,"add_lex_markup: a=$a, data=$data\n");
 if(preg_match('/n="(.*?)"/',$a,$matches1)) {
  dbgprint($dbg," add_lex_markup case 1\n");
  $ans = $x;
 }else {
  $tran = $this->getABdata($data);  
  # what if $tran is not present as an abbreviation
  if (!$tran) {
   $tran = "substantive information";
  }
  # convert special characters to html entities
  # for instance, this handles cases when $tran has single (or double) quotes
  $tran = htmlspecialchars($tran,ENT_QUOTES);
  $ans = "<ab n='$tran'>$data</ab>";
  dbgprint($dbg," add_lex_markup case 2\n");
 }
 dbgprint($dbg," add_lex_markup returns $ans\n");
 return $ans;
}
 public function add_lex_markup_mw($matches) {
 /* <lex{attrib}>{data}</lex> ignore attrib
   For mw, {data} is more complex. For display purposes, we want
   to identify the genders and mark as abbreviations.
   This is originally done in BasicDisplay class with an XML Parser.
   That seems to be the only way to do it here.
   So we make a special LexParser class for this purpose
 */
 $dbg=false;
 
 $x = $matches[0]; // full <lex>X</lex> string
 $lexparser = new BasicAdjustLexParser($x,$this);
 if ($lexparser->status) {
  $ans = $lexparser->result;
 } else {
  dbgprint($dbg,"basicadjust error in BasicAdjustLexParser\n");
  $ans = $x;
 }
 dbgprint($dbg," add_lex_markup_mw returns $ans\n");
 return $ans;
}

 public function s_callback($matches) {
/* remove accent if needed
   remove <srs/>
*/
 $x = $matches[0];
 if ($this->accent != "yes") {
  // remove accent characters from slp1 text:  /,^,\
  $y = $matches[1];    // $x = <s>$y</s>
  $y = $this->remove_slp1_accent($y);
  $x = "<s>$y</s>";
 }
 return $x;
}
public function key2_callback($matches) {
/* remove accent if needed
*/
 $x = $matches[0];
 if ($this->accent != "yes") {
  // remove accent characters from slp1 text:  /,^,\
  // Assume no closing xml tag within text.
  $y = $matches[1];    // $x = <key2>$y</key2>
  $y = $this->remove_slp1_accent($y);
  $x = "<key2>$y</key2>";
 }
 return $x;
}
public function remove_slp1_accent($y) {
  #$y = preg_replace('|[\/\^\\\]|','',$y);
  # udatta accent is '/'.  But '/' also used in xml tags (empty or closing)
  # preadjust $y to replace these instances of '/' with '_'
  #  assumes no tag name starts with '_', a safe assumption in this xml
  $y = preg_replace('|</|','<_',$y);  
  $y = preg_replace('|/>|','_>',$y);
  $y = preg_replace('|[\/\^\\\]|','',$y);
  # restore the '/' used in xml tags
  $y = preg_replace('|<_|','</',$y);
  $y = preg_replace('|_>|','/>',$y);
  return $y;
}
 public function rgveda_verse_modern($gra) {
 /*Github user SergeA
  $gra is called 'mandala' in rgveda_verse_callback
  https://github.com/sanskrit-lexicon/Cologne/issues/223#issuecomment-390369526
 */
 $data = [
  [1,191,1,1,191],
  [192,234,2,1,43],
  [235,295,3,1,62],
  [297,354,4,1,58],
  [355,441,5,1,87],
  [442,516,6,1,75],
  [517,620,7,1,104],
  [621,668,8,1,48],
  [1018,1028,8,59,59], //Vālakhilya hymns 1—11
  [669,712,8,60,103],
  [713,826,9,1,114],
  [827,1017,10,1,191]
 ];
 for($i=0;$i<count($data);$i++) {
  list($gra1,$gra2,$mandala,$hymn1,$hymn2) = $data[$i];
  if (($gra1 <= $gra) && ($gra<=$gra2)) {
   $hymn = $hymn1 + ($gra - $gra1);
   $x = "$mandala.$hymn";
   return $x;
  }
 }
 return "?"; // algorithm failed
}
public function rgveda_link($gra1,$gra2) {
 /* gra1 = mandala.hymn, gra2 = verse
 */ 
 $dbg=false;
 dbgprint($dbg,"rgveda_link: gra1=$gra1, gra2=$gra2\n");
 list($mandala,$hymn) = explode(".",$gra1);
 $imandala = (int)$mandala;
 $ihymn = (int)$hymn;
 $hymnfilepfx = sprintf("rv%02d.%03d",$imandala,$ihymn);
 $hymnfile = "$hymnfilepfx.html";
 $iverse = (int)$gra2;
 $versesfx = sprintf("%02d",$iverse);
 $anchor = "$hymnfilepfx.$versesfx";
 dbgprint($dbg,"rgveda_link: hymnfile=$hymnfile, anchor=$anchor\n");
 return array($hymnfile,$anchor);
}
public function rgveda_verse_callback($matches0) {
/* 
    Adds 'gralink' element to xml. These need
    to be converted to html in basicdisplay.php
*/
 $dbg=false;
 $x0 = $matches0[0];
 $x1 = $matches0[1];
 if(! preg_match('|^([0-9]+)[ ,]+([0-9]+)(.*)$|',$x1,$matches)) {
  dbgprint($dbg,"rgveda_verse_callback: error. x1=$x1\n");
  return $x0;
 }
 $gra1 = $matches[1];  // mandala
 $gra2 = $matches[2];  // hymn
 $gra3 = $matches[3];  // rest of stuff before closing }
 dbgprint($dbg,"rgveda_verse_callback: gra1=$gra1, gra2=$gra2, gra3=$gra3\n");
 $modern = $this->rgveda_verse_modern((int)$gra1);
 # This version provides a link
 list($rvfile,$rvanchor) = $this->rgveda_link($modern,$gra2);
 # 2018-08-30  use github location
 $dir = "https://sanskrit-lexicon.github.io/rvlinks/rvhymns";
 $href = "$dir/$rvfile#$rvanchor";
 $modern1 = "$modern.$gra2";
 //$tooltip = "=$modern1 (mandala,hymn,verse)";
 $tooltip = "Rg Veda $modern1 (mandala,hymn,verse)";
 // 04-03-2021
 $x = "<gralink href='$href' n='$tooltip'>$gra1,$gra2$gra3</gralink>";
 return $x;
}
public function avveda_verse_callback($matches0) {
/* 
    Adds 'gralink' elements to xml. These need
    to be converted to html in basicdisplay.php
*/
 $dbg=false;
 $x0 = $matches0[0];
 $x1 = $matches0[1];
 if(! preg_match('|^AV[.] ([0-9]+),([0-9]+),([0-9]+)(.*)$|',$x1,$matches)) {
  dbgprint($dbg,"avveda_verse_callback: error. x1=$x1\n");
  return $x0;
 }
 $gra1 = $matches[1];  // mandala
 $gra2 = $matches[2];  // hymn
 $gra3 = $matches[3];  // verse
 $gra4 = $matches[4];  // rest of stuff before closing }
 dbgprint($dbg,"avveda_verse_callback: gra1=$gra1, gra2=$gra2, gra3=$gra3\n");

 $imandala = (int)$gra1;
 $ihymn = (int)$gra2;
 $hymnfilepfx = sprintf("av%02d.%03d",$imandala,$ihymn);
 $hymnfile = "$hymnfilepfx.html";
 $iverse = (int)$gra3;
 $versesfx = sprintf("%02d",$iverse);
 $anchor = "$hymnfilepfx.$versesfx";

 # 2018-08-30  use github location
 $dir = "https://sanskrit-lexicon.github.io/avlinks/avhymns";
 $href = "$dir/$hymnfile#$anchor";
 $tooltip = sprintf("Atharva Veda %02d.%03d.%02d",$imandala,$ihymn,$iverse);
 // 04-03-2021
 $x = "<gralink href='$href' n='$tooltip'>$x1</gralink>";
 return $x;
}

public function roman_int($roman) {
 $a = array("i" => 1,"ii" => 2,"iii" => 3,"iv" => 4,"v" => 5,"vi" => 6,"vii" => 7,"viii" => 8,"ix" => 9,"x" => 10,
"xi" => 11,"xii" => 12,"xiii" => 13,"xiv" => 14,"xv" => 15,"xvi" => 16,"xvii" => 17,"xviii" => 18,"xix" => 19,"xx" => 20 ); 
 try {
  if(isset($a[$roman])) {
   return $a[$roman];
  }else {
   return 0;
  }
 } catch (exception $e)  {
 return 0; // error
 }
 return 0;
}
public function lanman_link_callback($matches) {
/* 
    Adds 'lanlink' or 'wglink'  elements to xml. These need
    to be converted to html in basicdisplay.php
*/
 $x0 = $matches[0];
 $n0 = $matches[1]; # lan,16,4   or wg,1235
 $txt = $matches[2]; # text of <ls> tag}
 $parts = explode(",",$n0);
 if ($parts[0] == "lan") {
  $page = $parts[1];
  $linenum = $parts[2];
  $url = 'https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/servepdf.php?dict=LAN'; #&page=111-a
  # This ampersand causes problems in basicdisplay parsing!
  #$href = "$url" . "&page=$page";
  $href = "$url" . "_page=$page";
  # It is useful to also have the line number visible in the url of the displayed url
  $href = "$href" . "_line=$linenum";
  $tooltip = "Lanman Sanskrit Reader, page $page, line $linenum";
  $x = "<lanlink href='$href' n='$tooltip' target='_lanlink'>$txt</lanlink>";
 }else if ($parts[0] == "wg") {
  // https://funderburkjim.github.io/WhitneyGrammar/step1/pages2c.html#section_1234
  $section = $parts[1];
  $url = 'https://funderburkjim.github.io/WhitneyGrammar/step1/pages2c.html';
  $href = "$url#section_$section";
  $tooltip = "Whitney Grammar, section $section";
  $x = "<lanlink href='$href' n='$tooltip' target='_wglink'>$txt</lanlink>";
 }else { // $n0 mal-formed
  $x = $x0; // return unchanged
 }
 return $x;
}
public function move_L_mw($line) {
 /* 04-12-2018. For MW. Logic to place Cologne record ID at END
  of displays for <H1X> records. This acomplished by changing the
  name of the <L> tag to <L1>
 */
 $dbg=false;
 dbgprint($dbg,"basicadjust.move_L_mw enter: line=\n$line\n");
 if (preg_match('|<(H[1-4].)>.*(<L>.*?</L>)|',$line,$matches)) {
  $H = $matches[1];
  $Ltag = $matches[2];
  // remove L element
  $line = preg_replace("|$Ltag|","",$line);
  // construct L1 tag
  $L1tag = preg_replace("|L>|","L1>",$Ltag);
  #dbgprint(true,"Ltag=$Ltag,  L1tag=$L1tag\n");
  // Insert L1tag before end of tail -- so at end of display
  $line = preg_replace("|</tail>|","$L1tag</tail>",$line);
 }
 dbgprint($dbg,"basicadjust.move_L_mw leave: line=\n$line\n");
 return $line;
}
public function htmlspecial($text) {
 // First, use the php function to convert quotes to html entities:
 // This converts single quote to &#039;
 $tooltip = htmlspecialchars($text,ENT_QUOTES);
 // since the result is parsed again with xml_parser, and xml_parser
 // autoconverts (apparently) &#039; back to single quote,
 // and then generates a parse error if this single quote occurs
 //  within an atribute value expresses as <x attr='y'>  (i.e. y has a
 //  single quote).
 // Because of this we change &#039; to &#8217;  -- which xml_parser
 // apparently leaves unchanged, and generates no error.
 $tooltip = preg_replace('/&#039;/','&#8217;',$tooltip);
 return $tooltip;
}
 public function infovn_markup($matches) {
  /* As of 5-2-2023, only present in 'gra' dictionary
   <info vn="X"/>
    [vn X]
  */
  $vn = $matches[1];
  $ans = "<span style='color:red;'>[vn $vn]</span>";
  return $ans;
 }
 public function chg_markup($matches) {
 /* <chg type="TYPE" n="CHGID" src="SRC">{chgdata}</chg>
   attrib:  ' type="TYPE" n="CHGID" src="SRC"
 */
 $dbg = false;
 $x = $matches[0]; // full <chg>Z</chg> string
 $type = $matches[1];
 $chgid = $matches[2];
 $src = $matches[3];
 $chgdata = $matches[4];
 dbgprint($dbg,"chg_markup: type=$type, chgid=$chgid, src=$src\n  chgdata=$chgdata\n");
 if ($type == 'chg') {
  // $anshead = "CHG type=$type, chgid=$chgid, src=$src";
  $anshead = '';
  if (preg_match('|<old>(.*?)</old> *<new>(.*?)</new>|',$chgdata,$matches1)) {
   $old = $matches1[1];
   $new = $matches1[2];
   $styleold = 'text-decoration:line-through;';
   $ansold = "<span style='$styleold'>$old</span>";
   $stylenew = 'color:green;';
   $msgstyle = "color:red; display:inline; text-decoration:underline red dotted;";
   $ansnew = "<abbr title='source=$src' style='$msgstyle'>[Correction: </abbr><span style='$stylenew'>$new</span><span style='color:red;'>]</span>";
   $ans = "$anshead : $ansold $ansnew";
   dbgprint($dbg,"ansold=$ansold\nansnew=$ansnew\n");
   return $ans;
  }else {
   return $x; // form not recognized
  }
 }else  if ($type == 'del') {
  // $anshead = "CHG type=$type, chgid=$chgid, src=$src";
  $anshead = '';
  if (preg_match('|<old>(.*?)</old>|',$chgdata,$matches1)) {
   $old = $matches1[1];
   $styleold = 'text-decoration:line-through;';

   $msgstyle = "color:red; display:inline;";
   $ansold = "<abbr title='source=$src' style='$msgstyle'>Deletion: </abbr><span style='$styleold'>$old</span><span style='color:red;'>]</span>";
   $ans = "$ansold";
   dbgprint($dbg,"Deletion: ansold=$ansold\n");
   return $ans;
  }else {
   return $x; // form not recognized
  }
 }else { // unknown type
  return $x; 
 }
 $dbg=false;
 }

}

class BasicAdjustLexParser{
 public $parentEl, $row, $status, $result, $dbg, $basicadj;
 public $parents; # array, treated as stack of elements
 public function __construct($line,$basicadj) {
 // $line is a <lex>X</lex> string
 // $basicadj is the calling instance of Basicadjust class;
 //    used to call getABdata
 $this->basicadj = $basicadj;
 $dbg=false;
 $this->dbg=false;
 dbgprint($dbg,"BasicAdjustLexParser: line=$line\n");
  $p = xml_parser_create('UTF-8');
  xml_set_element_handler($p,array($this,'sthndl'),array($this,'endhndl'));
  xml_set_character_data_handler($p,array($this,'chrhndl'));
  xml_parser_set_option($p,XML_OPTION_CASE_FOLDING,FALSE);
  $this->row="";
  # 09-27-2018. Due to error in 'double-parsing' of '&amp;'
  #   This parser for adding abbreviations in <lex> markup
  #   Also converts &amp; to &.   Since the result is parsed a 
  #   second time (in basicdisplay.php) the naked '&' causes a parsing error.
  #   This rare even was noticed in hw=caRqa (L=70905) and
  #   in hw=aruRa (L=15417).
  $this->parents=array();
  $line1 = preg_replace("/&amp;/","<amp/>",$line); # 09-27-2018
  if (!xml_parse($p,$line1)) {
   dbgprint(true,"BasicAdjustLexParser: xml parse error\n");
   dbgprint(true,"line1=$line1\n");
   $this->result = $line;
   $this->status = false;
   return;
  }
  $this->status = true;
  $this->result = $this->row;
  dbgprint($dbg,"BasicAdjustLexParser: result={$this->result}\n");
 }
 
 public function sthndl($xp,$el,$attribs) {
  if ($el == "lex") {
   // nothing.  don't output the lex tag to html
  }else if ($el == "amp") {
   // nothing
  }else {
   // output the element tag and its attributes
   $this->row .= "<$el";
   foreach($attribs as $name=>$value) {
    $this->row .= " $name='$value'";
   }
   $this->row .= ">";
  }
  $this->parentEl = $el;
  $this->parents[] = $el;  
 }
 public function endhndl($xp,$el) {
  #$this->parentEl = "";
  array_pop($this->parents);
  if ($el == "lex") {
   // nothing.  don't output the ending lex tag to html
  }else if ($el == "amp") {
   // nothing
  }else {
   // close the tag
   $this->row .= "</$el>";
  }
 }
 public function chrhndl($xp,$data) {
  // get parent from top of stack
  $this->parentEl = array_pop($this->parents);
  // restore top of stack
  $this->parents[]=$this->parentEl;
  if ($this->parentEl == "lex") {
   // $data is a text node within lex convert to abbreviation if possible
   $tran = $this->basicadj->getABdata($data);  
   // try some adjustments if abbreviation not found 
   if ($tran == "") {
    $data1 = trim($data); // remove spaces at ends
    $data1 = preg_replace('|[.]|','',$data1);
    $data1 = preg_replace('|\(.*$|','',$data1);
    $data1 = "$data1."; # add period
    $tran = $this->basicadj->getABdata($data1);
   }
   if ($tran == "") {
    $data1 = trim($data); // remove spaces at ends
    $data1 = preg_replace('|[.]|','',$data1);
    $data1 = preg_replace('|^.*\)|','',$data1);
    $data1 = "$data1."; //add period at end 
    $tran = $this->basicadj->getABdata($data1);
   }
   dbgprint($this->dbg,"BasicAdjustLexParser. lex chrhndl. data=$data, tran=$tran\n");
   if ($tran == "")  {
    // No translation found
    $this->row .= $data;
   }else {
    # convert special characters to html entities
    # for instance, this handles cases when $tran has single (or double) quotes
    $tran = htmlspecialchars($tran,ENT_QUOTES);  
    $this->row .= "<ab n='$tran'>$data</ab>";
   }
  }else {
   // some other tag. just return $data unchanged
   $this->row .= $data;
   dbgprint($this->dbg,"BasicAdjustLexParser. lex chrhndl. parent={$this->parentEl}, data=$data\n");
  }

 }
public function htmlspecial($text) {
 // we need this function in this class also
 // First, use the php function to convert quotes to html entities:
 // This converts single quote to &#039;
 $tooltip = htmlspecialchars($text,ENT_QUOTES);
 // since the result is parsed again with xml_parser, and xml_parser
 // autoconverts (apparently) &#039; back to single quote,
 // and then generates a parse error if this single quote occurs
 //  within an atribute value expresses as <x attr='y'>  (i.e. y has a
 //  single quote).
 // Because of this we change &#039; to &#8217;  -- which xml_parser
 // apparently leaves unchanged, and generates no error.
 $tooltip = preg_replace('/&#039;/','&#8217;',$tooltip);
 return $tooltip;
}
}
?>
