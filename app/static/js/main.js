
$(document).on('ready', function() {
	new WOW({
		                      boxClass:     'wow',      // default
		                      animateClass: 'animated', // default
		                      offset:       200,
		                      mobile:       true,       // default
		                      live:         true        // default
	}).init();

	var rellax = new Rellax('.rellax');
	var hr = new Date().getHours();

	if (hr < 12) {
		/**
		 *	background: #8E2DE2;
		 *  background: -webkit-linear-gradient(to right, #4A00E0, #8E2DE2);
		 *  background: linear-gradient(to right, #4A00E0, #8E2DE2);
		**/
		$('body').css("background","-webkit-linear-gradient(to right, #ff5f6d, #ffc371)");
		$('body').css("background","linear-gradient(to right, #ff5f6d, #ffc371)");
		$('html').css("background","-webkit-linear-gradient(to right, #ff5f6d, #ffc371)");
		$('html').css("background","linear-gradient(to right, #ff5f6d, #ffc371)");
		color('#ffd000');

	}
	else if (hr >= 12 && hr < 19) {
		$('body').css("background","-webkit-linear-gradient(to right, #36d1dc, #5b86e5)");

		$('body').css("background","linear-gradient(to right, #36d1dc, #5b86e5)");
		$('html').css("background","-webkit-linear-gradient(to right, #36d1dc, #5b86e5)");

		$('html').css("background","linear-gradient(to right, #36d1dc, #5b86e5)");
		color('#00d8ff');

	}
	else {
		$('body').css("background","-webkit-linear-gradient(to right, #6441a5, #2a0845)");
		$('body').css("background","linear-gradient(to right, #6441a5, #2a0845)");
		$('html').css("background","-webkit-linear-gradient(to right, #6441a5, #2a0845)");
		$('html').css("background","linear-gradient(to right, #6441a5, #2a0845)");
		color('#6441a5');

	}
	$('.sidenav').sidenav();
	$('.tooltipped').tooltip();
	$(".card--content").click(function() {
		var content = '<div class="modal-content"><h1>'+$(this).attr("data-title")+'</h1><p>'+$(this).attr("data-message")+'</p></div>';
    $('#'+$(this).attr("data-str-title")).html(content);
    $('#'+$(this).attr("data-str-title")).modal();
	});
});


function color(c) {
    //	var theme = document.querySelector("meta[name=theme-color]");
    //	theme.setAttribute("content", c);
		elements = document.getElementsByClassName("theme-color");
		for (var i = 0; i < elements.length; i++) {
			elements[i].style.color=c;

		}

}
