<?php
 /* dictinfowhich is used so we know how to construct
    paths to various files.  There are assumed to be two
    file structures: one like that at Cologne sanskrit-lexicon-uni-koeln.de
    web site, and another simpler structure based on that devised for 
    use on other servers, such as xampp or a typical Linux php setup.
    Note: this is copied from repository csl_apidev.
*/
 if (preg_match("|^/[an]fs/|",dirname(__DIR__))) {
  $dictinfowhich = "cologne"; 
  #require_once('dbgprint.php');
  #dbgprint(true,"dictinfowhich: " .dirname(__DIR__)  . "  $dictinfowhich\n");
 }else {
  $dictinfowhich = "xampp";
 }
?>