$(function() {
	if( $('#top-bar').length ){
		var callBox = $('#bar').offset().top;
		$(window).scroll(function(){
			var scrollTop = $(window).scrollTop();
			
			if( scrollTop > callBox ){
				$('#top-bar').css('top', 0);
			}else{
				console.log('v1111ariable');
				$("#top-bar").css('top', -100);
			}
		})
	}
});
