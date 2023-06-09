<?php
error_reporting( error_reporting() & ~E_NOTICE & ~E_WARNING);
?>
<!DOCTYPE html>
<?php init_inputs(); ?>
<html>
 <head>
 <meta charset="UTF-8" />
 <title>Grassman Wörterbuch 1873 Mobile</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"> 
  <link rel="stylesheet" href="//code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.css" />
  <script src="//code.jquery.com/jquery-1.8.2.min.js"></script>
  <script src="//code.jquery.com/mobile/1.2.0/jquery.mobile-1.2.0.min.js"></script>
   <link rel="stylesheet" href="../webtc/main.css" type="text/css">
   <link rel="stylesheet" href="main.css" type="text/css">
   <link rel="stylesheet" href="../webtc/font.css" type="text/css">
  <script type="text/javascript" src="../js/jquery.cookie.js"></script>

  <script type="text/javascript" src="../webtc/main_webtc.js"></script>

</head> 
<body> 

<div data-role="page" id="one">

  <div data-role="header" data-position="fixed" data-theme="b">

  <table style="left:1px">
   <tr>
   <td>
    <a href="//www.sanskrit-lexicon.uni-koeln.de/" 
      style="background-color:#5e87b0;">  
    <img id="unilogo" src="../images/cologne_univ_seal.gif"
           title="Cologne Sanskrit Lexicon" width="40" height="40"/>
    </a>
   </td>
   <td>
   </td>
   <td> 
    <span>Grassmann Wörterbuch zum Rig Veda</span>
   </td>
   </tr>
  </table>

  </div><!-- /header -->

  <div data-role="content" >  
<?php
 echo init_citation_pref();
?>
   <div id="disp" ></div>
  </div><!-- /content -->
<!-- /footer -->   
 </div> <!-- page one -->

<div data-role="page" id="two" data-theme="a">
 <div data-role="header" data-theme="e">
  <h1>Preferences</h1>
 </div><!-- /header, two-->
 <div data-role="content" data-theme="d">

<?php
echo init_preferences();
?>
 <p><a href="#one" data-rel="back" data-role="button" data-inline="true" data-icon="back">OK</a></p>	
 </div> <!-- content, two -->
</div> <!-- page two -->

<div data-role="page" id="winlw" data-theme = "a">
 
</div>

</body>
</html>
<?php 
function init_inputs_key() {
 // word = citation.
 $ans = "";
 if (isset($_GET['word'])) {
  $x = $_GET['word'];
 }else if (isset($_GET['citation'])) {
  $x = $_GET['citation'];
 }else if (isset($_GET['key'])) {
  $x = $_GET['key'];
 }else {
  $x = "";
 }
 $invalid_characters = array("$", "%", "#", "<", ">", "=", "(", ")");
 $ans = str_replace($invalid_characters, "", $x);
 return $ans;
}
function init_inputs() {
// from GET/POST parameters, initialize $inithash
global $inithash;
$inithash=array();
 $inithash['word'] = init_inputs_key();

 // translit = input
 $x = $_REQUEST['translit'];
 if (!$x) {$x = $_REQUEST['input'];}
 if (!$x) {$x = "";}
 $translit0 = $x;
 // filter = output
 $x = $_REQUEST['filter'];
 if (!$x) {$x = $_REQUEST['output'];}
 if (!$x) {$x = "";}
 $filter0=$x;

 // normalization of translit and filter.
 // translit0 may have substrings HK,SLP,IT which are converted
 // to translit = hk,slp1,itrans
 // filter0 may have substring HK,SLP2,IT,DEVA,ROMAN, which are converted
 // to filter = hk,slp1,itrans,deva,roman
 $x = strtoupper($translit0);
 if (preg_match('/HK/',$x)) {
  $x="hk";
 }else if (preg_match('/IT/',$x)) {
  $x="itrans";
 }else if (preg_match('/DE/',$x)) {
  $x="deva";
 }else if (preg_match('/RO/',$x)) {
  $x="roman";
 }else {
  $x="slp1";
 }
 $translit = $x;
 // normalization of filter, using old parameters
 // slp1 is default
 $x = strtoupper($filter0);
 if (preg_match('/HK/',$x)) {
  $x="hk";
 }else if (preg_match('/IT/',$x)) {
  $x="itrans";
 }else if (preg_match('/DEVA/',$x)) {
  $x="deva";
 }else if (preg_match('/ROMAN/',$x)) {
  $x="roman";
 }else {
  $x="slp1";
 }
 $filter = $x;
// 
 // initializing $inithash
 $inithash['translit'] = $translit;
 $inithash['filter'] = $filter;

}

 function output_option ($value,$display,$initvalue) {
  $ans= "  <option value='$value'";
  if ($initvalue == $value) {
   $ans .= " selected='selected'";
  }
  $ans .= ">$display</option>
";
  return $ans;
}
function init_translit() {
global $inithash;
 $init=$inithash['translit'];
 $hk = output_option("hk","Kyoto-Harvard",$init);
 $slp1= output_option("slp1","SLP1",$init);
 $itrans=output_option("itrans","ITRANS",$init);
 $roman=output_option("roman","Roman Unicode",$init);
 $deva=output_option("deva","Devanagri Unicode",$init);
 $ans=<<<FORM
 <table >
 <tr>
 <td><span>input</span>
 </td>
 <td>
 <select name="transLit" id="transLit" >
 $hk
 $slp1
 $itrans
 $roman
 $deva
 </select>
 </td>
 </tr>
</table>
FORM;

 return $ans;
}
function init_filter() {
global $inithash;
 $init=$inithash['filter'];
 $deva=output_option("deva","Devanagari Unicode",$init);
 $roman=output_option("roman","Roman Unicode",$init);
 $hk = output_option("hk","Kyoto-Harvard",$init);
 $slp1= output_option("slp1","SLP1",$init);
 $itrans=output_option("itrans","ITRANS",$init);
 $ans=<<<FORM
 <table>
 <tr>
 <td><span>output</span>
 </td>
 <td>
 <select name="filter" id="filter">
 $deva
 $roman
 $hk
 $slp1
 $itrans
 </select>
 </td>
 </tr>
</table>
FORM;

 return $ans;
}
function init_citation_pref() {
global $inithash;
 $init=$inithash['word'];
$ans = <<<FORM
<table>
 <tr>
<!--
  <td>citation:&nbsp;
  </td>
-->
  <td> <a onclick="getWord();" data-role="button" data-icon="search"
   data-iconpos="notext">Search</a>
  </td>
  <td><input type="text" name="key" size="20" id="key" value="$init" />
  </td>
  <td><a href="#two" data-role="button" data-rel="dialog" 
   data-transition="pop" data-icon="info" data-iconpos="notext">Preferences</a>
  </td>
 </tr>
</table>
FORM;

 return $ans;
}

function init_indexcaller() {
 // set invisible 'indexcaller' 
 $x = $_GET['translit'];
 if (!$x) {$x = $_GET['input'];}
 $y = $_GET['filter'];
 if (!$y) {$y = $_GET['output'];}
 if ($x ||$y) {
  $val="YES";
 }else {
  $val="NO";
 }
 $id = "indexcaller";
 $ans = <<<FORM
 <input name="$id"  id="$id" value="$val"  style="visibility:hidden" />
FORM;
 return $ans;
}
function init_preferences(){
$translit = init_translit();
$filter = init_filter();
$indexcaller = init_indexcaller();
$ans = <<<FORM
   <input name="input" id="input_input" value="hk" style="visibility:hidden" /> 
   <input name="output" id="input_output" value="deva" style="visibility:hidden" />
$translit
$filter
$indexcaller
FORM;

return $ans;
}
?>
