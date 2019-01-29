
$(document).on('ready', function() {


	var rellax = new Rellax('.rellax');
	var hr = new Date().getHours();
	$('.fixed-action-btn').floatingActionButton();

	if (hr < 12) {
		/**
		 *	background: #8E2DE2;
		 *  background: -webkit-linear-gradient(to right, #4A00E0, #8E2DE2);
		 *  background: linear-gradient(to right, #4A00E0, #8E2DE2);
		**/
		$('body').css("background","-webkit-linear-gradient(to right, #fc466b, #3f5efb)");
		$('body').css("background","linear-gradient(to right, #fc466b, #3f5efb)");
		$('html').css("background","-webkit-linear-gradient(to right, #fc466b, #3f5efb)");
		$('html').css("background","linear-gradient(to right, #fc466b, #3f5efb)");
		color('#3f5efb');

	}
	else if (hr < 18) {
		$('body').css("background","-webkit-linear-gradient(to right,  #dc2430, #7b4397)");
		$('body').css("background","linear-gradient(to right, #dc2430, #7b4397)");
		$('html').css("background","-webkit-linear-gradient(to right, #dc2430, #7b4397)");
		$('html').css("background","linear-gradient(to right, #dc2430, #7b4397)");
		color('#7b4397');

	}
	else {
		$('body').css("background","-webkit-linear-gradient(to right, #ee0979, #ff6a00)");
		$('body').css("background","linear-gradient(to right,  #ee0979, #ff6a00)");
		$('html').css("background","-webkit-linear-gradient(to right, #ee0979, #ff6a00)");
		$('html').css("background","linear-gradient(to right, #ee0979, #ff6a00)");
		color('#ff6a00');


	}
	$('.sidenav').sidenav();
	$('.tooltipped').tooltip();
	$(".card--content").click(function() {
		var content = '<div class="modal-content"><h1>'+$(this).attr("data-title")+'</h1><p>'+$(this).attr("data-message")+'</p><p class="grey-text lighten-2">'+$(this).attr("data-date")+'</p></div>';
    $('#'+$(this).attr("data-str-title")).html(content);
    $('#'+$(this).attr("data-str-title")).modal();
	});
	var geojson = {
  type: 'FeatureCollection',
  features: [{
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates: [-117.1611,32.7157]
    },
    properties: {
      title: 'Mapbox',
      description: 'Washington, D.C.'
    }
  },
  {
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates: [-122.414, 37.776]
    },
    properties: {
      title: 'Mapbox',
      description: 'San Francisco, California'
    }
  }]
};
geojson.features.forEach(function(marker) {

  // create a HTML element for each feature
  var el = document.createElement('div');
  el.className = 'marker';

  // make a marker for each feature and add to the map
  new mapboxgl.Marker(el)
  .setLngLat(marker.geometry.coordinates)
  .addTo(map);
});
	new WOW({
		                      boxClass:     'wow',      // default
		                      animateClass: 'animated', // default
		                      offset:       200,
		                      mobile:       true,       // default
		                      live:         true        // default
	}).init();

});


/**
 * @param  {String}
 * @return {void}
 */
function color(c) {
    //	var theme = document.querySelector("meta[name=theme-color]");
    //	theme.setAttribute("content", c);
		elements = document.getElementsByClassName("theme-color");
		for (var i = 0; i < elements.length; i++) {
			elements[i].style.color=c;

		}

}
