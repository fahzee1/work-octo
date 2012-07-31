function setCookie(c_name,value,exdays)
{
var exdate=new Date();
exdate.setDate(exdate.getDate() + exdays);
var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
document.cookie=c_name + "=" + c_value;
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

jQuery(document).ajaxSend(function(event, xhr, settings) {
        function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

function initiate_popup() {
    element_id = 'popup-wrapper';
    if($('#' + element_id)) {

        setTimeout(
            "load_popup($('#"+element_id+"'));",
            120000);

    }
}
function load_popup(element) {
    
    var cookie = getCookie('popup_offer');
    if(cookie == null || cookie == '' || cookie == undefined) {
        cookie = getCookie('lead_id');
    }
    // var refer_id = getCookie('refer_id');
    // refer_id = refer_id.toLowerCase();
    // var agent_ids = ['a02815']
    // for(var i in agent_ids) {
    //    if(agent_ids[i] == refer_id) {
    //        return false;
    //    }
    // }
    if(cookie == null || cookie == '' || cookie == undefined) {
        $(document).ready(function () {
            var interval = 1; //sec
            var max_time = 300;
            _COUNTDOWN = max_time;
            $('div#popup-timer span').html('05:00');
            var _interval = setInterval(function () {
                var t = _COUNTDOWN -  interval;
                if(t > 0) {
                    var minutes = Math.floor(t / 60);
                    var seconds = t - (minutes * 60);
                    $('div#popup-timer span').html('0'+minutes+':'+(seconds>9?'':'0')+seconds);
                    _COUNTDOWN = t;
                } else {
                    clearInterval(_interval);
                    element.hide();
                }
            }
            , interval * 1000);
        }
        );
        element.show();
        setCookie('popup_offer', 'true', 999)
    }
}
jQuery('#popup-close').live('click', function() {
    $(this).parent().parent().hide();
});
initiate_popup();