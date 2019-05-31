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

var blueIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [ 25, 41 ],
	iconAnchor: [ 12, 41 ],
	popupAnchor: [ 1, -34 ],
	shadowSize: [ 41, 41 ]
});

var greenIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [ 25, 41 ],
	iconAnchor: [ 12, 41 ],
	popupAnchor: [ 1, -34 ],
	shadowSize: [ 41, 41 ]
});

var redIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [ 25, 41 ],
	iconAnchor: [ 12, 41 ],
	popupAnchor: [ 1, -34 ],
	shadowSize: [ 41, 41 ]
});

var orangeIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [ 25, 41 ],
	iconAnchor: [ 12, 41 ],
	popupAnchor: [ 1, -34 ],
	shadowSize: [ 41, 41 ]
});

var yellowIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [ 25, 41 ],
	iconAnchor: [ 12, 41 ],
	popupAnchor: [ 1, -34 ],
	shadowSize: [ 41, 41 ]
});

var violetIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [ 25, 41 ],
	iconAnchor: [ 12, 41 ],
	popupAnchor: [ 1, -34 ],
	shadowSize: [ 41, 41 ]
});

var greyIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-grey.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [ 25, 41 ],
	iconAnchor: [ 12, 41 ],
	popupAnchor: [ 1, -34 ],
	shadowSize: [ 41, 41 ]
});

var blackIcon = new L.Icon({
	iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png',
	shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	iconSize: [ 25, 41 ],
	iconAnchor: [ 12, 41 ],
	popupAnchor: [ 1, -34 ],
	shadowSize: [ 41, 41 ]
});

var icons = [ blueIcon, greenIcon, redIcon, orangeIcon, yellowIcon, violetIcon, greenIcon, blackIcon ];

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
	//remove os pontos do mapa
	//pega a qtd de pontos do mapa
	var number_of_markers = Object.keys(markers).length;
	if (Object.keys(markers).length != 0) {
		for (var i = 0; i < number_of_markers; i++) {
			if (markers.hasOwnProperty(Object.keys(markers)[0])) {
				if (Object.keys(markers)[0] != 'selected') {
					map.removeLayer(markers[Object.keys(markers)[0]]);
					delete markers[Object.keys(markers)[0]];
				}
			}
		}
	}

	$.ajax({
		url: 'http://localhost:5000/housing',
		crossDomain: true,
		type: 'POST',
		dataType: 'html',
		data: $('#form').serialize(),
		success: function(response) {
			//cria o elemento com a tabela de resulta
			//passa de string para elemento (objeto)
			table = createElementFromHTML(response);
			if (document.getElementById('table')) {
				//remove a tabela de resultado anterior, se existir
				$('#table').remove();
			}
			//adiciona a tabela de resultado
			document.body.appendChild(table[0]);
			//console.log(document.getElementById('table'));
			//chamar função para passar a tabela de resultados para JSON
			resultJson = tableToJson(document.getElementById('table'));

			//colocar os pontos no mapa
			//passa por cada linha do resultado
			resultJson.forEach((row, index) => {
				//pega latitude e longitude do resultado
				var lat = row['latitude'];
				var lng = row['longitude'];

				//Para as cores se repetirem quando chegar na ultima cor
				if ((index % icons.length == 0) | (index > icons.length - 1)) {
					index = index % icons.length;
				}
				//adicione o marcador no mapa, com ID sendo o ID do resultado, usando os icones cadastrados
				markers[row['']] = L.marker([ lat, lng ], { icon: icons[index] }).addTo(map);
			});
		},
		error: function(error) {
			//captura erro no código
			console.log(error);
		}
	});
});

function createElementFromHTML(htmlString) {
	var div = document.createElement('div');
	div.innerHTML = htmlString.trim();
	// Change this to div.childNodes to support multiple top-level nodes
	return div.childNodes;
}

function tableToJson(table) {
	var data = [];
	// first row needs to be headers
	var headers = [];
	for (var i = 0; i < table.rows[0].cells.length; i++) {
		headers[i] = table.rows[0].cells[i].innerHTML.toLowerCase().replace(/ /gi, '');
	}
	// go through cells
	for (var i = 1; i < table.rows.length; i++) {
		var tableRow = table.rows[i];
		var rowData = {};
		for (var j = 0; j < tableRow.cells.length; j++) {
			rowData[headers[j]] = tableRow.cells[j].innerHTML;
		}
		data.push(rowData);
	}
	return data;
}
