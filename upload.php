<?php

// new filename
$filename = 'pic_'.date('YmdHis') . '.jpeg';
print($filename);
$url = '';
if( move_uploaded_file($_FILES['webcam']['tmp_name'],'pictures/'.$filename) ){
 $url = 'http://' . $_SERVER['HTTP_HOST'] . dirname($_SERVER['REQUEST_URI']) . '/upload/' . $filename;
}

// Return image url
echo $url;