(function(e){e.fn.prepopulate=function(t,n){return this.each(function(){var r=e(this);r.data("_changed",!1);r.change(function(){r.data("_changed",!0)});var i=function(){if(r.data("_changed")!=1){var i=[];e.each(t,function(t,n){e(n).val().length>0&&i.push(e(n).val())});r.val(URLify(i.join(" "),n))}};e(t.join(",")).keyup(i).change(i).focus(i)})}})(django.jQuery);