$(function() {
	if( $('#top-bar').length ){
		var callBox = $('#bar').offset().top;
		$(window).scroll(function(){
			var scrollTop = $(window).scrollTop();
			
			if( scrollTop > callBox ){
				$('#top-bar').css('top', 0);
			}else{
				console.log('v1111ariable');
				$("#top-bar").css('top', -90);
				
				console.log('v1111ariable');
				$('#quotePulldown').hide();
				$('.close').hide();
			}
		})
	}
});

$(document).ready(function () {
		$('.show_hide').on('click', function(event) {
			event.preventDefault();
			if($('#quotePulldown').css('display') == 'block') {
				$('#quotePulldown').hide();
				$('.close').hide();
			} else {
				$('#quotePulldown').slideDown();
				$('.close').show();
			}
		});
	});
	
