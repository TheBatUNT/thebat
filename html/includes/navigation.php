<script src="bower_components/jquery/dist/jquery.min.js"></script>
<script src="includes/modify_db.js"></script>
<?php
/**
*
* Display Navigation Settings
* Dynamic add, edit, and delete maps, and labels.
*
*/
function DisplayNavigation(){
	$conn =mysql_connect('localhost','root','hearmeout');
	if(!$conn)
	{
	?>
		<div class="alert alert-warning alert-dismissable">
			Connection to Database Failed
			<button type="button" class="close" data-dismiss="alert" aria-hidden="true">x</button>
		</div><?php
	}
	$db = mysql_select_db('thebat');
	if(!$db)
	{
		die('Can\'t use thebat: '.mysql_error());
	}
	$query = "SELECT * FROM maps";
	$result = mysql_query($query) or die($query."<br/><br/>".mysql_error());
	?>
	<div class="alert alert-success alert-dismissable">
		Connected to Database successfully
		<button type="button" class="close" data-dismiss="alert" aria-hidden="true">x</button>
	</div>
	  <div class="row">
		<div class="col-lg-12">
		  <div class="panel panel-primary">
			<div class="panel-heading"><i class="fa fa-map-marker fa-fw"></i> Navigation Settings</div>
			<!-- /.panel-heading -->
				<div class="panel-body">
			  <form role="form" action="" method="POST">
				<!-- Nav tabs -->
				<ul class="nav nav-tabs">
				<?php
				while($row = mysql_fetch_array($result))
				{
					//Need to change this so it is dynamic, currently sets the first map as active
					if($row['id'] == 1)
						echo "<li class='active'><a href='#".$row['id']."'data-toggle='tab'>".$row['Name']."</a></li>";
					else
						echo "<li><a href='#".$row['id']."'data-toggle='tab'>".$row['Name']."</a></li>";
				}?>
					<li><a href='#new' data-toggle='tab'>New Map</a></li>
				</ul>
				<!-- Tab panes -->
				<div class="tab-content">
				<?php
				$result = mysql_query($query) or die($query."<br/><br/>".mysql_error());
				$coordID = 1;
				while($row = mysql_fetch_array($result))
				{ 
					//Same as above, need to change to make dynamic
					if($row['id'] == 1)
						echo "<div class='tab-pane fade in active' id='".$row['id']."'>";
					else
						echo "<div class='tab-pane fade' id='".$row['id']."'>";
					?><div class="table-responsive">
					   <table class="table table-hover" id="myTable<?php echo $row['id'];?>"><th>Location</th><th>Latitude</th><th>Longitude</th><th>Altitude/Nodes</th><th>Save/Delete/Is Exit</th>
							<tr id="row<?php echo $row['id'];?>">
									<td><input type='text' class='form-control' id="loc<?php echo $row['id'];?>" value="<?php echo $row['Name'];?>"/></td>
									<td><input type='text' class='form-control' id="lat<?php echo $row['id'];?>" value="<?php echo $row['Latitude'];?>"/></td>
									<td><input type='text' class='form-control' id="long<?php echo $row['id'];?>" value="<?php echo $row['Longitude'];?>"/></input></td>
									<td><input type='text' class='form-control' id="alt<?php echo $row['id'];?>" value="<?php echo $row['Altitude'];?>"/></input></td>
									<td><div class="btn-group"><input type='button' class="btn btn-success" id="save_button<?php echo $row['id'];?>" value="Save" onclick="save_map('<?php echo $row['id'];?>');">
									<input type='button' class="btn btn-danger" id="delete_button<?php echo $row['id'];?>" value="Delete" onclick="delete_map('<?php echo $row['id'];?>');"></div></td>
								</tr><?php
						$rowID = $row['id'];
						$rowname = $row['Name'];?>
						<input type='hidden' id="map<?php echo $row['id'];?>" value="<?php echo $rowname;?>"/><?php
						$query1 = "SELECT * FROM coordinates WHERE Map ='$rowname'";
						$coordresult = mysql_query($query1) or die($query1."<br/><br/>".mysql_error());
						while($coordRow = mysql_fetch_array($coordresult))
						{
							?>
							<tr id="row<?php echo $coordRow['id'];?>">
										<td><input type='text' class='form-control' id="label<?php echo $coordRow['id'];?>" value="<?php echo $coordRow['Label'];?>"/></td>
										<td><input type='text' class='form-control' id="clat<?php echo $coordRow['id'];?>" value="<?php echo $coordRow['Latitude'];?>"></input></td>
										<td><input type='text' class='form-control' id="clong<?php echo $coordRow['id'];?>" value="<?php echo $coordRow['Longitude'];?>"></input></td>
										<td><div class="multiselect">
											<div class="selectBox" multiple onclick="showCheckboxes(<?php echo $coordRow['id'];?>)">
												<select class='form-control'>
													<option>Select connecting Nodes</option>
												</select>
												<div class="overSelect"></div>
											</div>
											<div class="checkboxes" id="checkboxes<?php echo $coordRow['id'];?>">
												<?php $query2 = "SELECT * FROM coordinates WHERE Map ='$rowname'";
												$checkresult = mysql_query($query2) or die($query2."<br/><br/>".mysql_error());
												while($checkRow = mysql_fetch_array($checkresult)) //Create checkboxes
												{
													if($checkRow['id'] != $coordRow['id']) //Do not create one that is equal to the current node.
													{
														$id = $coordRow['id'] . $checkRow['id'];
														$dijkstraResult = mysql_query("SELECT * FROM dijkstra WHERE id ='$id'");
														$dijkstraResult = mysql_fetch_array($dijkstraResult);
														if($dijkstraResult['id'] == $id) //Set the checkbox to Checked if it is already connected in DB
														{?>
															<label for="check<?php echo $id;?>">
																<input type="checkbox" id="check<?php echo $id;?>" value="<?php echo $checkRow['id'];?>" checked /><?php echo $checkRow['Label'];?></label>
														<?php
														}	
														else
														{?>
															<label for="check<?php echo $id;?>">
																<input type="checkbox" id="check<?php echo $id;?>" value="<?php echo $checkRow['id'];?>"/><?php echo $checkRow['Label'];?></label>
														<?php
														}?>	
													<?php
													}
												}
												?>
											</div>
										</div></td>
										<td><div class="btn-group">
										<input type='button' class="btn btn-success" id="save_button<?php echo $coordRow['id'];?>" value="Save" onclick="save_row('<?php echo $coordRow['id'];?>','<?php echo $rowname;?>');"/>
										<input type='button' class="btn btn-danger" id="delete_button<?php echo $coordRow['id'];?>" value="Delete" onclick="delete_row('<?php echo $coordRow['id'];?>');"/></div>
										<?php
										if($coordRow['isExit']==1)
										{?>	<label>
											<input type="checkbox" id="exit<?php echo $coordRow['id'];?>" checked />Is Exit?</label></td>
										<?php 
										}
										else 
										{?>	<label>
											<input type="checkbox" id="exit<?php echo $coordRow['id'];?>" />Is Exit?</label></td>
										<?php
										} ?>
							</tr>

					<?php
						}
					?>
						<tr id ="new_row">
							<td><input type="text" class="form-control" id="new_label<?php echo $rowID;?>"></td>
							<td><input type="text" class="form-control" id="new_latitude<?php echo $rowID;?>"></td>
							<td><input type="text" class="form-control" id="new_longitude<?php echo $rowID;?>"></td>
							<td><div class="multiselect">
									<div class="selectBox" onclick="newShowCheckboxes(<?php echo $rowID;?>)">
										<select class='form-control'>
											<option>Select connecting Nodes</option>
										</select>
										<div class="overSelect"></div>
									</div>
									<div class="checkboxes" id="newcheckboxes<?php echo $rowID;?>">
										<?php $query2 = "SELECT * FROM coordinates WHERE Map ='$rowname'";
										$checkresult = mysql_query($query2) or die($query2."<br/><br/>".mysql_error());
										while($checkRow = mysql_fetch_array($checkresult)) //Show all nodes to connect when making a new label.
										{?>
												<label for="check<?php echo $checkRow['id'];?>">
													<input type="checkbox" id="check<?php echo $checkRow['id'];?>" value="<?php echo $checkRow['id'];?>"/><?php echo $checkRow['Label'];?></label>
										<?php
										}
										?>
									</div>
							</div></td>
							<td><input type="button" class="btn btn-success" value="Insert Row" onclick="insert_row('<?php echo $row['id'];?>');">
							<label><input type="checkbox" id="new_exit<?php echo $rowID;?>"/>Is Exit?</label></td>
						</tr>
						</table>
						</div>
				
				</div>
				<?php
				} ?>
				<div class='tab-pane fade' id='new'>
					<table class="table table-hover table-responsive">
						<th>Location</th><th>Latitude</th><th>Longitude</th><th>Altitude</th>
						<tr id ="new_map">
							<td><input type="text" class="form-control" id="new_location"></td>
							<td><input type="text" class="form-control" id="new_latitude"></td>
							<td><input type="text" class="form-control" id="new_longitude"></td>
							<td><input type="text" class="form-control" id="new_altitude"></td>
							<td><input type="button" class="btn btn-success" value="Insert Map" onclick="insert_map();"></td>
						</tr>
					</table>
			</div><!-- ./ Panel body -->
				<input type="button" class="btn btn-success" value="Refresh" onclick="document.location.reload(true)" />
			  </form>
			</div><!-- /.panel-primary -->
		  <div class="panel-footer"> Information provided by Database</div>
		</div><!-- /.col-lg-12 -->
	  </div><!-- /.row -->
<?php
}
?>
<script>
var expanded = false;

function showCheckboxes(id) {
	var checkboxes = document.getElementById("checkboxes"+id);
	if (!expanded) {
		checkboxes.style.display = "block";
		expanded = true;
	} else {
		checkboxes.style.display = "none";
		expanded = false;
	}
}
function newShowCheckboxes(id) {
	var checkboxes = document.getElementById("newcheckboxes"+id);
	if (!expanded) {
		checkboxes.style.display = "block";
		expanded = true;
	} else {
		checkboxes.style.display = "none";
		expanded = false;
	}
}
</script>
<style>
.selectBox {
  position: relative;
}

.selectBox select {
  width: 100%;
  font-weight: bold;
}

.overSelect {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
}

.checkboxes {
  display: none;
  border: 1px #dadada solid;
}

.checkboxes label {
  display: block;
}

.checkboxes label:hover {
  background-color: #1e90ff;
}
</style>



