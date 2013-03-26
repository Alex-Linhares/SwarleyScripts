<?php

/*
htaccess_protected_file_downloader.php
Copyright (C) 2013  Ian Thomas

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// PARAMETERS ==================================================================

$filename = "example.tar.gz";
$parent_url = "https://www.server.com/path";
$username = "user";
$password = "password";

// MAIN ========================================================================

// ensure PHP has enough memory allocated to cache the entire download...
ini_set('memory_limit', '128M');

$curl = curl_init();

curl_setopt($curl, CURLOPT_URL, $parent_url . "/" . $filename);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
curl_setopt($curl, CURLOPT_USERPWD, "$username:$password");

// reference: http://www.php.net/manual/en/function.curl-setopt.php#98164
// extra options to work with SSL...
curl_setopt($curl, CURLOPT_SSLVERSION, 3);
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);

// other options - not usually required...
// curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, 2);
// curl_setopt($curl, CURLOPT_HEADER, true);
// curl_setopt($curl, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)");
// curl_setopt($curl, CURLOPT_CONNECTTIMEOUT, $timeout);

// download the file contents from the host...
$data = curl_exec($curl);

if ( $data === false || curl_errno($curl) )
{
    die("Download error: " . curl_error($curl) );
}

$info = curl_getinfo($curl);
curl_close($curl);

// check for authentication error...
if ( $info['http_code'] == 401 )
{
    die("Password authentication error");
}

// prepare file download for client browser...
header('Content-Description: File Transfer');
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename=' . $filename);
header('Content-Transfer-Encoding: binary');
header('Expires: 0');
header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
header('Pragma: public');
header('Content-Length: ' . strlen($data));
ob_clean();
flush();
echo $data;
flush();

?>
