<?php
function dbgprint($dbg,$text) {
 if (!$dbg) {return;}
 $filename = "dbg_apidev.txt";
 $fp1 = fopen($filename,"a");
 fwrite($fp1,"$text");
 fclose($fp1);
}
?>
