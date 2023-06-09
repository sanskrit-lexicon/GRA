<?php
/* dictinfo.php. 
 06-28-2018
*/
class DictInfo {
 public $dict;
 public $dictupper;
 # $english is flag indicating whether to transcode headwords
 # false means 'yes, transcode'; true means 'no, do not transcode'
 public $english;  
 # $webpath is relative path to the 'web' directory for this dictionary
 public $webpath;
 public $webparent;
 public $sqlitedir;
 #public $sqlitefile;  // path to primary sqlite data (e.g. gradb.sqlite)
 #public $abfile;      // path to abbreviation sqlite file (e.g.graab.sqlite)
 #public $bibfile;     // path to bibliography file for pw, pwg
 public $advsearchfile;  // path to query_dump file used by webtc2 display.
 public $transcodefile; // path to transcoder.php
 public $year = '2020';  # template variable used in get_cologne_webPath method
 public function __construct($dict) {
  $this->dict=strtolower($dict);
  $this->dictupper=strtoupper($dict);
  $this->english = in_array($this->dictupper,array("AE","MWE","BOR"));
  $dir = dirname(__FILE__); //directory containing this php file
  $dir1 = "$dir/"; # Note: $dir does not end in '/'
  $this->webpath = realpath("$dir/../");
  $this->webparent = realpath("$dir/../../");
  # go from webparent to web. This for dev convenience.
  # Suppose a dev version of 'web' is installed in 'web1', and that
  # web1 and web are siblings.
  # Suppose web1 does not have the sqlite and webtc2 data files.
  # Then, the next formulations use these files from the 'web' directory.
  #  
  #$this->sqlitefile = "{$this->webpath}/sqlite/{$this->dict}.sqlite";
  #$this->sqlitefile = "{$this->webparent}/web/sqlite/{$this->dict}.sqlite";
  $this->sqlitedir = "{$this->webparent}/web/sqlite";
  $this->advsearchfile = "{$this->webparent}/web/webtc2/query_dump.txt";
  #$this->abfile = "{$this->webparent}/web/sqlite/{$this->dict}ab.sqlite";
  #$this->bibfile = "{$this->webparent}/web/sqlite/{$this->dict}bib.sqlite";
  $this->transcodefile = "{$this->webpath}/utilities/transcoder.php";
 }
 public function get_parent_dirpfx($base) {
  $dirpfx = "../../"; // apidev  Not portable
  #$ds = DIRECTORY_SEPARATOR;
  for($i=1;$i<10;$i++) {
   $d = dirname(__FILE__,$i);
   $b = basename($d);
   if ($b == $base) {
    $d = dirname(__FILE__,$i+1);
    $dirpfx = "$d/";
    break;
   }
  }
  return $dirpfx;
 }
 public function get_cologne_webPath() {
  // 04-17-2018
  // used by servepdf.php
  // Cologne scan directory 
  $cologne_scandir = "//www.sanskrit-lexicon.uni-koeln.de/scans";
  $path = $cologne_scandir . "/{$this->dictupper}Scan/{$this->year}/web";
  return $path;
 }
 public function get_year() {
  return $this->year;
 }
 public function get_webPath() {
  return $this->webpath;
 }
 public function get_pdfpages_url() {
  /* Assume this method called only from servepdf, which is in web/webtc folder
  */
  $dbg=false;
  include("dictinfowhich.php");
  $cologne_url = $this->get_cologne_pdfpages_url();
  if ($dictinfowhich == 'cologne') {
   return $cologne_url;
  }
  // otherwise, $dictinfowhich == 'xampp'
  // Try relative url, either in web directory, or parent of web directory
  // 10-26-2019 First choice is cologne/scans/xxx/pdfpages; relative to where
  // We are (in cologne/xxx/web/webtc); so rel path is ../../../scans/xxx/pdfpages
  // dictionary code xxx is available as $this->dict
  // Use relative url if it is a non-empty directory.

  $dict = $this->dict;
  $testpaths = array ( "../../../scans/$dict/pdfpages", "../pdfpages",   "../../pdfpages" );
  foreach($testpaths as $testpath) {
   if (!$this->dir_is_empty($testpath)) {
    return $testpath;
   }
  }
  // Use Cologne url as a fallback
  return $cologne_url;
 } 

 public function dir_is_empty($dir) {
  /* ref: https://stackoverflow.com/questions/7497733/how-can-i-use-php-to-check-if-a-directory-is-empty
   Note this is just a function. Put into this class for convenience of this
   application.  Currently used only by get_pdfpages_dir()
  */
  if (! is_dir($dir)) { 
   return TRUE; 
  }
  $handle = opendir($dir);
  while (false !== ($entry = readdir($handle))) {
    if ($entry != "." && $entry != "..") {
      closedir($handle);
      return FALSE;
    }
  }
  closedir($handle);
  return TRUE;
}
 public function get_cologne_pdfpages_url() {
 /* These urls are current as of 08-31-2019
 */
 $cologne_pdfpages_urls = array(
  "ACC"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/ACCScan/2014/web/pdfpages" ,
  "AE"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/AEScan/2014/web/pdfpages" ,
  "AP"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/APScan/2014/web/pdfpages" ,
  "AP90"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/AP90Scan/2014/web/pdfpages" ,
  "BEN"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/BENScan/2014/web/pdfpages" ,
  "BHS"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/BHSScan/2014/web/pdfpages" ,
  "BOP"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/BOPScan/2014/web/pdfpages" ,
  "BOR"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/BORScan/2014/web/pdfpages" ,
  "BUR"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/BURScan/2013/web/pdfpages" ,
  "CAE"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/CAEScan/2014/web/pdfpages" ,
  "CCS"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/CCSScan/2014/web/pdfpages" ,
  "GRA"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/GRAScan/2014/web/pdfpages" ,
  "GST"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/GSTScan/2014/web/pdfpages" ,
  "IEG"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/IEGScan/2014/web/pdfpages" ,
  "INM"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/INMScan/2013/web/pdfpages" ,
  "KRM"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/KRMScan/2014/web/pdfpages" ,
  "MCI"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/MCIScan/2014/web/pdfpages" ,
  "MD"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/MDScan/2014/web/pdfpages" ,
  #"MW"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2014/web/pdfpages" ,
  "MW"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/MWScanpdf" ,
  "MW72"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/MW72Scan/2014/web/pdfpages" ,
  "MWE"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/MWEScan/2013/web/pdfpages" ,
  "PD"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/PDScan/2014/web/pdfpages" ,
  "PE"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/PEScan/2014/web/pdfpages" ,
  "PGN"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/PGNScan/2014/web/pdfpages" ,
  "PUI"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/PUIScan/2014/web/pdfpages" ,
  "PWG"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/PWGScan/2013/web/pdfpages" ,
  "PW"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/PWScan/2014/web/pdfpages" ,
  "SCH"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/SCHScan/2014/web/pdfpages" ,
  "SHS"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/SHSScan/2014/web/pdfpages" ,
  "SKD"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/SKDScan/2013/web/pdfpages" ,
  "SNP"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/SNPScan/2014/web/pdfpages" ,
  "STC"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/STCScan/2013/web/pdfpages" ,
  "VCP"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/VCPScan/2013/web/pdfpages" ,
  "VEI"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/VEIScan/2014/web/pdfpages" ,
  "WIL"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/WILScan/2014/web/pdfpages" ,
  "YAT"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/YATScan/2014/web/pdfpages" ,
  "LAN"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/LANScan/2019/web/pdfpages" ,
  "ARMH"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/ARMHScan/2020/web/pdfpages" ,
  "PWKVN"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/PWScan/2014/web/pdfpages" ,
  "LRV"=>"//www.sanskrit-lexicon.uni-koeln.de/scans/LRVScan/pdfpages" ,
 );
 $url = $cologne_pdfpages_urls[$this->dictupper];
 return $url;
 }
}

?>
