var tileLayer = new L.TileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',{
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
});

var map = new L.Map('map', {
  'center': [37, -119],
  'zoom': 6,
  'layers': [tileLayer]
});

var myId = 'selected';  

var markers = {}

map.on('click', function (e) {
  if (markers.hasOwnProperty(myId)) {
    map.removeLayer(markers[myId]);
  }
  markers[myId] = L.marker(e.latlng).addTo(map);
});
