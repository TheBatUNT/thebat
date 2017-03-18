<script src="includes/modify_db.js"></script>
<script src="bower_components/jquery/dist/jquery.min.js"></script>
<?php

$conn =mysql_connect('localhost','root','hearmeout');
	if(!$conn)
	{
	?>
		<div>
			Connection to Database Failed
		</div><?php
	}
	$db = mysql_select_db('thebat');
	if(!$db)
	{
		die('Can\'t use thebat: '.mysql_error());
	}
	$exitcounter = 0;
	$query = "SELECT * FROM maps";
	$maps = mysql_query($query) or die($query."<br/><br/>".mysql_error());
	$query = "SELECT * FROM currentUser"; //get users current location from DB
	$currentUser = mysql_query($query) or die($query."<br/><br/>".mysql_error());
	$currentLoc = mysql_fetch_array($currentUser);
	$mindist = -1;
	while($row = mysql_fetch_array($maps))
	{
		//Haversine Formula to find closest map to the User
		$radiusOfEarth = 6371000;
		$latFrom = deg2rad($currentLoc['Latitude']);
		$longFrom = deg2rad($currentLoc['Longitude']);
		$latTo = deg2rad($row['Latitude']);
		$longTo = deg2rad($row['Longitude']);
		
		$latDelta = $latTo - $latFrom;
		$longDelta = $longTo - $longFrom;
		
		$angle = 2 * asin(sqrt(pow(sin($latDelta /2), 2) +
			cos($latFrom) * cos($latTo) * pow(sin($longDelta / 2), 2)));
		$distance = $angle * $radiusOfEarth;
		if($mindist == -1 or $distance < $mindist)
		{
			$mindist = $distance;
			$mapname = $row['Name'];
		}
	}
	//get all coordinates from the closest map.
	$query = "SELECT * FROM coordinates WHERE Map ='$mapname' AND isExit=1";
	$exits = mysql_query($query) or die($query."<br/><br/>".mysql_error());
	while($exitrow = mysql_fetch_array($exits))
	{
		$exitcounter++;	?>
		<button type="button" onclick="save_exit('<?php echo $exitrow['id']; ?>');" class="ext" id="<?php echo $exitrow['Label']; ?>" alt="Navigate to <?php echo $exitrow['Label']; ?> for <?php echo $mapname; ?>"><?php echo $exitrow['Label']; ?></button>
	<?php
	}
	//change the height of button so they take up screen
	$height = 100 / $exitcounter;
?>
<html>
	<body>

	</body>
</html>
<style>
.ext{
	color: white;
	font-size: 50px;
	background-color: red;
	border-color: black;
	width: 100%;
	height: <?php echo $height; ?>%;
}
</style>

