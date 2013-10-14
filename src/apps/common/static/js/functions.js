$(function() {

    $(document).on('focusin', '.field, textarea', function () {
		if(this.title==this.value) {
			this.value = '';
		}
	}).on('focusout', '.field, textarea', function(){
		if(this.value=='') {
			this.value = this.title;
		}
	});

	//$('#ddlState').c2Selectbox();
    if ($('#top-bar').length) {
        var callBox = $('#phone-hdr').offset().top;
		$(window).scroll(function(){
			var scrollTop = $(window).scrollTop();
			
			if( scrollTop > callBox ){
				$('#top-bar').css('top', 0);
			}else{
				console.log('v1111ariable');
				$("#top-bar").css('top', -200);
			}
		})
	}


});