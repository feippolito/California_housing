var tileLayer = new L.TileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
	attribution:
		'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
});

var map = new L.Map('map', {
	center: [ 37, -119 ],
	zoom: 6,
	layers: [ tileLayer ]
});

var myId = 'selected';

var markers = {};

//on map click
map.on('click', function(e) {
	if (markers.hasOwnProperty(myId)) {
		map.removeLayer(markers[myId]);
	}
	markers[myId] = L.marker(e.latlng).addTo(map);
	var lat = e.latlng['lat'];
	var lng = e.latlng['lng'];
	$('#lat').val(lat);
	$('#lng').val(lng);
});

//on button click
$('#button_submit').click(function() {
	$.ajax({
		url: 'http://localhost:5000/housing',
		crossDomain: true,
		type: 'POST',
		dataType: 'html',
		data: $('#form').serialize(),
		success: function(response) {
			table = createElementFromHTML(response);
			document.body.appendChild(table[0]);
		},
		error: function(error) {
			console.log(error);
		}
	});
	//console.log('cliquei');
});

function createElementFromHTML(htmlString) {
	var div = document.createElement('div');
	div.innerHTML = htmlString.trim();

	// Change this to div.childNodes to support multiple top-level nodes
	return div.childNodes;
}
