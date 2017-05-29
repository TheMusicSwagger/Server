<?php
    try {
		$db=new PDO('mysql:dbname=themusicswagger_db;host=localhost;port=3306;charset=utf8','notroot','', array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
	}catch (PDOException $e) {
		die("Impossible de se connecter : " . $e->getMessage());
	}

	if(isset($_POST["config"])){
		$arr=json_decode($_POST["config"], true);
		$links=$arr["LINKS"];
		$boxes=$arr["BOXES"];
	}
	else{
		die("You must provide the configuration !");
	}
    $db->query("DELETE FROM links");
    $db->query("DELETE FROM boxes");
    $db->query("DELETE FROM update_number");
    $db->query("INSERT INTO update_number (ID) VALUES (NULL);");

    
	for($i=0;$i<count($links);$i++){
		$entry=$links[$i];
		$BOX_ID_OUT=$entry["BOX_ID_OUT"];
		$LINK_ID_OUT=$entry["LINK_ID_OUT"];
		$BOX_ID_IN=$entry["BOX_ID_IN"];
		$LINK_ID_IN=$entry["LINK_ID_IN"];
		$db->query("INSERT INTO links(BOX_ID_OUT, LINK_ID_OUT, BOX_ID_IN, LINK_ID_IN) VALUES ('$BOX_ID_OUT','$LINK_ID_OUT','$BOX_ID_IN','$LINK_ID_IN')");
	}
	for($i=0;$i<count($boxes);$i++){ 
		$entry=$boxes[$i];
		$TYPE=$entry["TYPE"];
		$BOX_ID=$entry["BOX_ID"];
		$SPEC_PARAM=$entry["SPEC_PARAM"];
		$db->query("INSERT INTO boxes(TYPE, BOX_ID, SPEC_PARAM) VALUES ('$TYPE','$BOX_ID','$SPEC_PARAM')");
	}
?>
