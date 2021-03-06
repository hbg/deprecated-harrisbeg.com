original = document.title;
$(document).on('ready', function() {
	$('#splash-screen').fadeOut().delay(1);
	var rellax = new Rellax('.rellax');
	var hr = new Date().getHours();
	var sw = 0;
	if (/*hr < 12*/ false) {
		/*
		$('body').css("background","-webkit-linear-gradient(to right, #fc466b, #3f5efb)");
		$('body').css("background","linear-gradient(to right, #fc466b, #3f5efb)");
		$('html').css("background","-webkit-linear-gradient(to right, #fc466b, #3f5efb)");
		*/
		$('.roll-cell').css("background","linear-gradient(to right, #fc466b, #3f5efb)");
		sw = 0;
		color(0);

	}
	else if (/*hr < 18*/ true) {
		/*
		$('body').css("background","-webkit-linear-gradient(to right,  #dc2430, #7b4397)");
		$('body').css("background","linear-gradient(to right, #dc2430, #7b4397)");
		$('html').css("background","-webkit-linear-gradient(to right, #dc2430, #7b4397)");
		*/
		//$('.roll-cell').css("background","linear-gradient(to right, #dc2430, #7b4397)");
		sw = 1;
		color(1);

	}
	else {
		/*
		$('body').css("background","-webkit-linear-gradient(to right, #ee0979, #ff6a00)");
		$('body').css("background","linear-gradient(to right,  #ee0979, #ff6a00)");
		$('html').css("background","-webkit-linear-gradient(to right, #ee0979, #ff6a00)");
		*/
		$('td').css("background","linear-gradient(to right, #ee0979, #ff6a00)");

		sw = 2;
		color(2);
	}

	$('.sidenav').sidenav();
	$('.tooltipped').tooltip();
	$(".card--content").click(function() {
		var content = '<div class="modal-content"><h1>'+$(this).attr("data-title")+'</h1><p>'+$(this).attr("data-message")+'</p><p class="grey-text lighten-2">'+$(this).attr("data-date")+'</p></div>';
    $('#'+(this).attr("data-str-title")).html(content);
    $('#'+(this).attr("data-str-title")).modal();

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
	//	counter($(".counter"), 6);
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
 * @param c Time of day {0,1,2}
 * @return Theme color changed
 */
function color(c) {
    //	var theme = document.querySelector("meta[name=theme-color]");
    //	theme.setAttribute("content", c);

		let elements = document.getElementsByClassName("theme-color");
		for (let i = 0; i < elements.length; i++) {
			switch (c) {
				case 0:
					$(elements[i]).css("background", "-webkit-linear-gradient(left, #fc466b, #3f5efb)");
					break;
				case 1:
					$(elements[i]).css("background", "-webkit-linear-gradient(left, #dc2430, #7b4397)");
					break;
				case 2:
					$(elements[i]).css("background", "-webkit-linear-gradient(left, #ee0979, #ff6a00)");
					break;
			}
  			$(elements[i]).css("-webkit-background-clip", "text");
  			$(elements[i]).css("-webkit-text-fill-color","transparent");

		}
}

$(window).focus(function() {
    document.title = original;
});

$(window).blur(function() {
    document.title = "Please don't leave...";
});
