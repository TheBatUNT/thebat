function save_exit(id)
{
	$.ajax
	({
		type:'post',
		url:'includes/modify_db.php',
		data:{
			save_exit:'save_exit',
			exit_val:id
		},
		success:function(response) {
			if(response=="success")
			{
				window.location.href="index.php";
			}
		}
	});
}
function save_map(id)
{
		var location=document.getElementById("loc"+id).value;
		var latitude=document.getElementById("lat"+id).value;
		var longitude=document.getElementById("long"+id).value;
		var altitude=document.getElementById("alt"+id).value;
		var oldlocation=document.getElementById("map"+id).value;
	$.ajax
	({
		type:'post',
		url:'includes/modify_db.php',
		data:{
			edit_map:'edit_map',
			row_id:id,
			loc_val:location,
			lat_val:latitude,
			long_val:longitude,
			alt_val:altitude,
			old_loc:oldlocation
		},
		success:function(response) {
			if(response=="success")
			{
				document.getElementById("loc"+id).value=location;
				document.getElementById("lat"+id).value=latitude;
				document.getElementById("long"+id).value=longitude;
				document.getElementById("alt"+id).value=altitude;
			}
		}
	});
}
function save_row(id,map)
{
		var label=document.getElementById("label"+id).value;
		var clat=document.getElementById("clat"+id).value;
		var clong=document.getElementById("clong"+id).value;
		var checkboxes=document.getElementById("checkboxes"+id).getElementsByTagName('input');
		var toNode = []; //create empty array to store all nodes
		if(document.getElementById("exit"+id).checked)
			var exit = 1;
		else
			var exit = 0;
		for(var i = 0;i < checkboxes.length; i++)
		{
			
			if(checkboxes[i].checked) //check to see if box is checked.
				toNode[i] = checkboxes[i].value;
			else
				toNode[i] = checkboxes[i].value * -1; //turn id to negative so I can identify it as unselected
		}
	$.ajax
	({
		type:'post',
		url:'includes/modify_db.php',
		data:{
			edit_row:'edit_row',
			row_id:id,
			label_val:label,
			clat_val:clat,
			clong_val:clong,
			map_val:map,
			toNode_val:toNode,
			isExit:exit
		},
		success:function(response) {
			if(response=="success")
			{
				document.getElementById("label"+id).value=label;
				document.getElementById("clat"+id).value=clat;
				document.getElementById("clong"+id).value=clong;
			}
		}
	});
}
function delete_map(id)
{
	if(confirm('Are you sure you want to delete everything under this map?'))
	{
		var location = document.getElementById("loc"+id).value;
		$.ajax
		({
			type:'post',
			url:'includes/modify_db.php',
			data:{
				delete_map:'delete_map',
				row_id:id,
				loc_value:location
			},
			success:function(response) {
				if(response=="success")
				{
					var row=document.getElementById("row"+id);
					row.parentNode.removeChild(row);
					location.reload();
				}
			}
		});
	}
}
function delete_row(id)
{
	if(confirm('Are you sure you want to delete this label?'))
	{
		$.ajax
		({
			type:'post',
			url:'includes/modify_db.php',
			data:{
				delete_row:'delete_row',
				row_id:id,
			},
			success:function(response) {
				if(response=="success")
				{
					var row=document.getElementById("row"+id);
					row.parentNode.removeChild(row);
				}
			}
		});
	}
}
function insert_map()
{
	var map=document.getElementById("new_location").value;
	var longitude=document.getElementById("new_longitude").value;
	var latitude=document.getElementById("new_latitude").value;
	var altitude=document.getElementById("new_altitude").value;
	$.ajax
	({
		type:'post',
		url:'includes/modify_db.php',
		data:{
			insert_map:'insert_map',
			map_val:map,
			lat_val:latitude,
			long_val:longitude,
			alt_val:altitude
		},
		success:function(response) {
			if(response!="")
			{
				document.getElementById("new_map").value="";
				document.getElementById("new_latitude").value="";
				document.getElementById("new_longitude").value="";
				document.getElementById("new_altitude").value="";
				location.reload();				
			}
		}
	});
}
function insert_row(tableid)
{
	var label=document.getElementById("new_label"+tableid).value;
	var map=document.getElementById("map"+tableid).value;
	var longitude=document.getElementById("new_longitude"+tableid).value;
	var latitude=document.getElementById("new_latitude"+tableid).value;
	var checkboxes=document.getElementById("newcheckboxes"+tableid).getElementsByTagName('input');
	var toNode = []; //empty array to store all nodes
	if(document.getElementById("new_exit"+tableid).checked)
		var exit = 1;
	else
		var exit = 0;
	for(var i = 0;i < checkboxes.length; i++)
	{
		if(checkboxes[i].checked) //don't worry about not connected because once user saves this moves to edit_row function
			toNode[i] = checkboxes[i].value;
	}
	$.ajax
	({
		type:'post',
		url:'includes/modify_db.php',
		data:{
			insert_row:'insert_row',
			label_val:label,
			lat_val:latitude,
			long_val:longitude,
			map_val:map,
			toNode_val:toNode,
			isExit: exit
		},
		success:function(response) {
			if(response!="")
			{
				var id=response; //get id that new row was put into in DB
				var table=document.getElementById("myTable"+tableid);
				var table_len=(table.rows.length)-1;
				//create the row and append to bottom of table and fill out data.
				if(exit==1)
					var row = table.insertRow(table_len).outerHTML="<tr id='row"+id+"'><td><input type='text' class='form-control' id='label"+id+"' value="+label+"></td><td><input type='text' class='form-control' id='clat"+id+"' value="+latitude+"></td><td><input type='text' class='form-control' id='clong"+id+"' value="+longitude+"></td><td><input type='button' class='btn btn-success' value='Refresh' onclick='document.location.reload(true);'/><label><input type='checkbox' id='exit"+id+"'checked />Is Exit?</label></td></tr>";
				else
					var row = table.insertRow(table_len).outerHTML="<tr id='row"+id+"'><td><input type='text' class='form-control' id='label"+id+"' value="+label+"></td><td><input type='text' class='form-control' id='clat"+id+"' value="+latitude+"></td><td><input type='text' class='form-control' id='clong"+id+"' value="+longitude+"></td><td><input type='button' class='btn btn-success' value='Refresh' onclick='document.location.reload(true);'/><label><input type='checkbox' id='exit"+id+"'/>Is Exit?</label></td></tr>";
				document.getElementById("new_label"+tableid).value=""; //set values back to empty
				document.getElementById("new_latitude"+tableid).value="";
				document.getElementById("new_longitude"+tableid).value="";
			}
		}
	});
}

