<?php
error_reporting(E_ALL & ~E_NOTICE & ~E_WARNING);
?>
<?php
/* 
Parameters:
 dict: one of the dictionary codes (case insensitive)
 page: a specific page of the dictionary.  In the form of the contents
       of a <pc> element
 08-31-2019 Refactored to do work in a ServepdfClass.
            
*/
require_once('servepdfClass.php');

function servepdfCall() {
  $temp = new ServepdfClass();
  $table1 = $temp->html;
  echo $table1;
}
servepdfCall();
?>
