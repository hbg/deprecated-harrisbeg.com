

$(document).on('ready', function() {
	new WOW({
		                      boxClass:     'wow',      // default
		                      animateClass: 'animated', // default
		                      offset:       200,
		                      mobile:       true,       // default
		                      live:         true        // default
	}).init();
	$('.tooltipped').tooltip();

	var rellax = new Rellax('.rellax');
	var hr = new Date().getHours() - 8;
	if (hr < 12) {
		/**
		 *	background: #8E2DE2;
		 *  background: -webkit-linear-gradient(to right, #4A00E0, #8E2DE2);
		 *  background: linear-gradient(to right, #4A00E0, #8E2DE2);
		**/
		$('body').css("background","-webkit-linear-gradient(to right, #ff5f6d, #ffc371)");
		$('body').css("background","-webkit-linear-gradient(to right, #ff5f6d, #ffc371)");

	}
	else if (hr >= 12 && hr < 19) {
		$('body').css("background","-webkit-linear-gradient(to right, #36d1dc, #5b86e5)");

		$('body').css("background","linear-gradient(to right, #36d1dc, #5b86e5)");
	}
	else {
		$('body').css("background","-webkit-linear-gradient(to right, #6441a5, #2a0845)");

		$('body').css("background","linear-gradient(to right, #6441a5, #2a0845)");
	}
});
