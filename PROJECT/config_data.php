<?php 
error_reporting(E_ALL);

class Config {
	public $ipAddress;
	public $sampleTime;
	public $maxNumOfSamples;
	public $apiVersion;
}


$ConfigTestFile = 'config_test_file.json';

$config = new Config();
$config->ipAddress = $_POST['IP_address'];		
$config->sampleTime = $_POST['Sample_time'];		
$config->maxNumOfSamples = $_POST['Max_number_of_samples'];		
$config->apiVersion = $_POST['API_version'];		


$toJSON = json_encode($config);
file_put_contents($ConfigTestFile, $toJSON);

echo "DONE!";

?>