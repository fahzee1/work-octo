(function(e){e.extend(e,{placeholder:{browser_supported:function(){return this._supported!==undefined?this._supported:this._supported="placeholder"in e('<input type="text">')[0]},shim:function(t){var n={color:"#888",cls:"placeholder",selector:"input[placeholder], textarea[placeholder]"};e.extend(n,t);return!this.browser_supported()&&e(n.selector)._placeholder_shim(n)}}});e.extend(e.fn,{_placeholder_shim:function(t){function n(t){var n=e(t).offsetParent().offset(),r=e(t).offset();return{top:r.top-n.top,left:r.left-n.left,width:e(t).width()}}return this.each(function(){var r=e(this);if(r.is(":visible")){if(r.data("placeholder")){var i=r.data("placeholder");i.css(n(r));return!0}var s={};!r.is("textarea")&&r.css("height")!="auto"&&(s={lineHeight:r.css("height"),whiteSpace:"nowrap"});var o=e("<label />").text(r.attr("placeholder")).addClass(t.cls).css(e.extend({position:"absolute",display:"inline","float":"none",overflow:"hidden",textAlign:"left",color:t.color,cursor:"text",paddingTop:r.css("padding-top"),paddingRight:r.css("padding-right"),paddingBottom:r.css("padding-bottom"),paddingLeft:r.css("padding-left"),fontSize:r.css("font-size"),fontFamily:r.css("font-family"),fontStyle:r.css("font-style"),fontWeight:r.css("font-weight"),textTransform:r.css("text-transform"),backgroundColor:"transparent",zIndex:99},s)).css(n(this)).attr("for",this.id).data("target",r).click(function(){e(this).data("target").focus()}).insertBefore(this);r.data("placeholder",o).focus(function(){o.hide()}).blur(function(){o[r.val().length?"hide":"show"]()}).triggerHandler("blur");e(window).resize(function(){var e=o.data("target");o.css(n(e))})}})}})})(jQuery);jQuery(document).add(window).bind("ready load",function(){jQuery.placeholder&&jQuery.placeholder.shim()});