<!DOCTYPE html>
<html>
 <head>
 <meta charset="UTF-8" />
  <title>Grassman Wörterbuch 1873 Advanced</title>
   <link rel="stylesheet" type="text/css" href="../webtc/main.css" media="screen" />
   <link rel="stylesheet" type="text/css" href="main.css" media="screen" />
   <link rel="stylesheet" href="../webtc/font.css" type="text/css">
  <script type="text/javascript" src="../js/jquery.min.js"></script>
  <script type="text/javascript" src="../js/jquery.cookie.js"></script>
  <script type="text/javascript" src="main.js"> </script>
<style>
#dictid {
 /*position:absolute;*/
 padding-top:15px;
 margin-left:10px;
 font-size:14pt;
 width:100%;
 text-align:left;
}
#querytable {
 /*position:absolute;*/
 top: 80px;
 left:5px;
}
#title {
font-family: verdana,arial,helvetica,sansserif;
font-size: 14pt;
}
</style>
</head>

 <body>
<div id="querydiv">
 <div id="dictid"> 
     <a href="//www.sanskrit-lexicon.uni-koeln.de/"
	style="background-color:#DBE4ED">
     <img id="unilogo" src="../images/cologne_univ_seal.gif"
            width="60" height="60" alt="University of Cologne"
	  title="Cologne Sanskrit Lexicon"></a>
     <span id="title">Grassmann Wörterbuch zum Rig Veda</span>
 </div>

<table id="querytable" border="0" cellpadding="3" cellspacing="1">
<tr>
<td >
Sanskrit Headword:
</td>
<td>
<input type="text" name="sword" id="sword" size="30" />
<select name="sregexp" id="sregexp">
     <option value="exact" selected="selected">exact</option>
     <option value="prefix">prefix</option>
     <option value="suffix">suffix</option>
     <option value="instring">infix</option>
     <option value="substring">substring</option>
    </select>
    <select name="transLit" id="transLit">
     <option value="hk" selected="selected">Kyoto-Harvard</option>
     <option value="slp1">SLP1</option>
     <option value="itrans">ITRANS</option>
     <option value="roman">Roman Unicode</option>
     <option value="deva">Devanagari Unicode</option>
    </select>

</td>
</tr>
<tr>
<td>
Text Word:
</td>
<td>
<input name="word" id="word" size="30" />

<select name="regexp" id="regexp">
     <option value="exact" selected="selected">exact</option>
     <option value="prefix">prefix</option>
     <option value="suffix">suffix</option>
     <option value="instring">infix</option>
     <option value="substring">substring</option>
    </select>
   <!--any case: -->
    <input type="checkbox" id="scase" name="scase" checked="checked" style="visibility:hidden;"/>

</td>
</tr>

<tr>
<td>Maximum:</td>
<td>
<select name="max" id="max">
<option  value="5">5</option>
<option value="20" selected="selected">20</option>
<option  value="50">50</option>
<option value="100">100</option>
<option value="200">200</option>
<option value="500">500</option>
<option value="1000">1000</option>
<!-- <option value="1000000">all</option> -->
</select> 
    &nbsp;output:
    <select name="filter" id="filter">
     <option value="deva" selected="selected">Devanagari Unicode</option>
     <option value="roman">Roman Unicode</option>
     <option value="hk">HK</option>
     <option value="slp1">SLP1</option>
     <option value="itrans">ITRANS</option>
    </select>

</td>
</tr>

<tr >
<!-- keep this element present, though undisplayed,
  as Javascript looks for 'outopt' element
-->
 <select name="outopt" id="outopt" style='display:none'>
  <option value="outopt4" selected="selected" >standard</option>
 </select>

<td>
    &nbsp;<a href="help.html">Help</a>
    &nbsp;&nbsp;
    <a href="/php/correction_form.php?dict=GRA" target="Corrections">Corrections</a>

</td>
<td>
<input type="button" onclick="getWord();" value="Search" id="searchbtn" />
<input type="button" onclick="getNext();" value="Next" id="nextbtn" />
<input type="button" value="working..." id="workbtn" />

</td>
</table>

  </div> <!-- end of querydiv -->
<!-- hidden, used with cookies -->
<input name="input" id="input_input" value="hk" style="visibility:hidden" /> 
<input name="output" id="input_output" value="deva" style="visibility:hidden" />
 <div id="disp">

 </div>
  <div id="data">
  </div>

</body>
</html>
