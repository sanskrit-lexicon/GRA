<!DOCTYPE html>
<html>
<head>
 <meta charset="UTF-8" />
 <title>GRA</title>
 <!--<link rel="stylesheet" href="webtc/main.css" type="text/css" />-->
 <style>
body {
color: black; background-color: #DBE4ED;
font-size: 14pt;
}
#disp {
  position:absolute;
  left: 1%;
  width: 98%;
 background-color: white;
 overflow-y:auto;
 overflow-x:hidden;
 height: 400px;
}
#title {
font-family: verdana,arial,helvetica,sansserif;
font-size: 14pt;
text-align:left;
}
 </style>
</head>
<body>
   <table width="100%"> 
     <tr><td width="10%">
      <a href="//www.sanskrit-lexicon.uni-koeln.de/">
      <img id="unilogo" src="images/cologne_univ_seal.gif"
           alt="University of Cologne" width="60" height="60"
	   title="Cologne Sanskrit Lexicon"/>
      </a>
      </td>
      <td><span id="title">Grassmann Wörterbuch zum Rig Veda</span></td>
      </tr>
    </table>
 <div id="disp" class="disp">
 <ol><b>Available displays</b>
  <li><a href="webtc/indexcaller.php">Basic display</a></li>
  <li><a href="webtc1/index.php">List display</a></li>
  <li><a href="webtc2/index.php">Advanced Search</a></li>
  <li><a href="mobile1/index.php">Mobile-friendly display</a></li>

 </ol>
 <ol>
  <a href="webtc/download.html">Downloads</a>
 </ol>
 
 <ol ><b>Related material</b>
<?php
require_once('webtc/dictinfowhich.php');
$href_fm_cologne="//www.sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/gra.html";
if ($dictinfowhich == "cologne") {
 $href_fm = $href_fm_cologne;
}else {
 // for xampp installation
 $dir_web = dirname(__DIR__); // directory continaing this program
 $testpath = "../../csl-doc";
 if ( is_dir($testpath)) {
  // use local installation csl-doc
  $href_fm = "$testpath/build/dictionaries/gra.html";
 } else {
  // local installation not available, use Cologne
  $href_fm = $href_fm_cologne;
 }
}
echo("<li><a href='$href_fm'>Front Matter</a></li>\n");
?>
  
  <li><a href="graheader.xml">License of Digital Edition</a></li>
  <li><a href="https://www.worldcat.org/title/worterbuch-zum-rig-veda/oclc/184798352">WorldCat reference</a></li>
  <li>Bibliographic entry: GRASSMANN, H. G. (1873). Worterbuch zum Rig-veda. Wiesbaden, O. Harrassowitz.</li>
 </ol>

 </div>

</body>
</html>
