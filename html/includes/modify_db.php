<?php
$host="localhost";
$username="root";
$password="hearmeout";
$databasename="thebat";

$connect=mysql_connect($host,$username,$password);
$db=mysql_select_db($databasename);
if(isset($_POST['save_exit']))
{
	$exitId = $_POST['exit_val'];
	mysql_query("UPDATE currentUser SET `Exit`='$exitId'")or die("Query Failed: " . mysql_error());
	echo "success";
	exit();
}
if(isset($_POST['edit_map']))
{
	$row=$_POST['row_id'];
	$location=$_POST['loc_val'];
	$lat=$_POST['lat_val'];
	$long=$_POST['long_val'];
	$alt=$_POST['alt_val'];
	$oldlocation=$_POST['old_loc'];
	mysql_query("UPDATE maps SET Name='$location', Latitude='$lat', Longitude='$long', Altitude='$alt' WHERE id='$row'");
	if($location!=$oldlocation)
		mysql_query("UPDATE coordinates SET Map='$location' WHERE Map='$oldlocation'"); //update all the coordinates that had old map name to the new map name.
	echo "success";
	exit();
}
if(isset($_POST['edit_row']))
{
	$row=$_POST['row_id'];
	if(isset($_POST['label_val']))
	{
		$label=$_POST['label_val'];
		$clat=$_POST['clat_val'];
		$clong=$_POST['clong_val'];
		$map=$_POST['map_val'];
		$toNode=$_POST['toNode_val'];
		$isExit=$_POST['isExit'];
		
		foreach($toNode as $value) //go through all nodes to see which are postive and negative (Positive = Connected, Negative = Not Connected)
		{
			if($value > 0) //Find distance between FromNode and ToNode and store it into dijkstra
			{
				$query = "SELECT * FROM coordinates WHERE id ='$value'";
				$result = mysql_query($query) or die($query."<br/><br/>".mysql_error());
				$nodeRow = mysql_fetch_array($result);
				$distance = haversine($clat,$clong,$nodeRow['Latitude'],$nodeRow['Longitude']);
				$id=$row . $value; //easy way to have unique but identifiable ID by concatenating two IDs together.
				mysql_query("REPLACE INTO dijkstra VALUES('$id', '$row', '$value', '$distance', '$map')");

			}
			else //if value is unchecked then delete it from dijkstra
			{
				$value = $value * -1; //value was negative when sent, turn it back to postive and find that id in dijkstra to delete it.
				$id=$row . $value; //easy way to have unique but identifiable ID by concatenating two IDs together.
				mysql_query("DELETE FROM dijkstra WHERE id='$id'");
			}
				
		}
		//Update Weights in dijkstra when a node is changed.
		$updateResult=mysql_query("SELECT * FROM dijkstra WHERE FromNode='$row' OR ToNode = '$row'");
		while($updateWeight = mysql_fetch_array($updateResult))
		{
			if($updateWeight['FromNode']==$row)
			{
				$toNodeID = $updateWeight['ToNode'];
				$id=$row . $toNodeID; //easy way to have unique but identifiable ID by concatenating two IDs together.
				$weightToQuery = mysql_query("SELECT * FROM coordinates WHERE id='$toNodeID'");
				$weightTo = mysql_fetch_array($weightToQuery);
				$newWeight = haversine($clat,$clong,$weightTo['Latitude'],$weightTo['Longitude']);
			}
			else
			{
				$fromNodeID = $updateWeight['FromNode'];
				$id=$fromNodeID . $row; //easy way to have unique but identifiable ID by concatenating two IDs together.
				$weightFromQuery = mysql_query("SELECT * FROM coordinates WHERE id='$fromNodeID'");
				$weightFrom = mysql_fetch_array($weightFromQuery);
				$newWeight = haversine($clat,$clong,$weightFrom['Latitude'],$weightFrom['Longitude']);
			}
			mysql_query("UPDATE dijkstra SET Weight='$newWeight' WHERE id='$id'");
		}
		//Update coordinates
		mysql_query("UPDATE coordinates SET Label='$label', Latitude='$clat', Longitude='$clong', isExit='$isExit' WHERE id='$row'");
	}
	echo "success";
	exit();
}
if(isset($_POST['delete_map']))
{
	$row_no=$_POST['row_id'];
	$map=$_POST['loc_value'];
	mysql_query("DELETE FROM maps WHERE id='$row_no'");
	mysql_query("DELETE FROM coordinates WHERE Map='$map'"); //delete all labels that were under the map that was just deleted
	echo "success";
	exit();
}
if(isset($_POST['delete_row']))
{
	$row_no=$_POST['row_id'];
	mysql_query("DELETE FROM coordinates WHERE id='$row_no'");
	//Delete All nodes that rely on the label that was deleted
	mysql_query("DELETE FROM dijkstra WHERE FromNode='$row_no' OR ToNode='$row_no'");
	echo "success";
	exit();
}
if(isset($_POST['insert_map']))
{
	$lat=$_POST['lat_val'];
	$long=$_POST['long_val'];
	$map=$_POST['map_val'];
	$alt=$_POST['alt_val'];
	mysql_query("INSERT INTO maps VALUES ('','$map','$lat','$long','$alt')");
	echo mysql_insert_id();
	exit();
}
if(isset($_POST['insert_row']))
{
	$label=$_POST['label_val'];
	$lat=$_POST['lat_val'];
	$long=$_POST['long_val'];
	$map=$_POST['map_val'];
	$toNode=$_POST['toNode_val'];
	$isExit=$_POST['isExit'];
	mysql_query("INSERT INTO coordinates VALUES ('','$map','$label','$lat','$long','$isExit')");
	$fromNode = mysql_insert_id();
	foreach($toNode as $value)
	{
		if($value > 0) //Add new nodes to dijkstra
		{
			$query = "SELECT * FROM coordinates WHERE id ='$value'";
			$result = mysql_query($query) or die($query."<br/><br/>".mysql_error());
			$nodeRow = mysql_fetch_array($result);
			$distance = haversine($clat,$clong,$nodeRow['Latitude'],$nodeRow['Longitude']);
			$id = $fromNode . $value;
			mysql_query("INSERT INTO dijkstra VALUES ('$id','$fromNode','$value','$distance','$map')");
		}
	}
	echo mysql_insert_id();
	exit();
}
function haversine($latFrom,$longFrom,$latTo,$longTo) //Haversine formula to find distance between two points
{
	$latFrom = deg2rad($latFrom);
	$longFrom = deg2rad($longFrom);
	$latTo = deg2rad($latTo);
	$longTo = deg2rad($longTo);
	$latDelta = $latTo - $latFrom;
	$longDelta = $longTo - $longFrom;
	$radiusOfEarth = 6371000;	
	$angle = 2 * asin(sqrt(pow(sin($latDelta /2), 2) +
		cos($latFrom) * cos($latTo) * pow(sin($longDelta / 2), 2)));
	return $angle * $radiusOfEarth;
	
}
?>


