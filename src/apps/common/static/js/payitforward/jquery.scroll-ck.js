/* ===========================================================
 * jquery-onepage-scroll.js v1.2
 * ===========================================================
 * Copyright 2013 Pete Rojwongsuriya.
 * http://www.thepetedesign.com
 *
 * Create an Apple-like website that let user scroll
 * one page at a time
 *
 * Credit: Eike Send for the awesome swipe event
 * https://github.com/peachananr/onepage-scroll
 * 
 * License: GPL v3
 *
 * ========================================================== */!function(e){var t={sectionContainer:"section",easing:"ease",animationTime:600,pagination:!0,updateURL:!1,keyboard:!0,beforeMove:null,afterMove:null,loop:!0,responsiveFallback:767};e.fn.swipeEvents=function(){return this.each(function(){function i(e){var i=e.originalEvent.touches;if(i&&i.length){t=i[0].pageX;n=i[0].pageY;r.bind("touchmove",s)}}function s(e){var i=e.originalEvent.touches;if(i&&i.length){var o=t-i[0].pageX,u=n-i[0].pageY;o>=50&&r.trigger("swipeLeft");o<=-50&&r.trigger("swipeRight");u>=50&&r.trigger("swipeUp");u<=-50&&r.trigger("swipeDown");(Math.abs(o)>=50||Math.abs(u)>=50)&&r.unbind("touchmove",s)}}var t,n,r=e(this);r.bind("touchstart",i)})};e.fn.onepage_scroll=function(n){function o(){if(e(window).width()<r.responsiveFallback){e("body").addClass("disabled-onepage-scroll");e(document).unbind("mousewheel DOMMouseScroll");i.swipeEvents().unbind("swipeDown swipeUp")}else{if(e("body").hasClass("disabled-onepage-scroll")){e("body").removeClass("disabled-onepage-scroll");e("html, body, .wrapper").animate({scrollTop:0},"fast")}i.swipeEvents().bind("swipeDown",function(t){e("body").hasClass("disabled-onepage-scroll")||t.preventDefault();i.moveUp()}).bind("swipeUp",function(t){e("body").hasClass("disabled-onepage-scroll")||t.preventDefault();i.moveDown()});e(document).bind("mousewheel DOMMouseScroll",function(e){e.preventDefault();var t=e.originalEvent.wheelDelta||-e.originalEvent.detail;u(e,t)})}}function u(e,t){deltaOfInterest=t;var n=(new Date).getTime();if(n-lastAnimation<quietPeriod+r.animationTime){e.preventDefault();return}deltaOfInterest<0?i.moveDown():i.moveUp();lastAnimation=n}var r=e.extend({},t,n),i=e(this),s=e(r.sectionContainer);total=s.length,status="off",topPos=0,lastAnimation=0,quietPeriod=500,paginationList="";e.fn.transformPage=function(t,n,r){e(this).css({"-webkit-transform":"translate3d(0, "+n+"%, 0)","-webkit-transition":"all "+t.animationTime+"ms "+t.easing,"-moz-transform":"translate3d(0, "+n+"%, 0)","-moz-transition":"all "+t.animationTime+"ms "+t.easing,"-ms-transform":"translate3d(0, "+n+"%, 0)","-ms-transition":"all "+t.animationTime+"ms "+t.easing,transform:"translate3d(0, "+n+"%, 0)",transition:"all "+t.animationTime+"ms "+t.easing});e(this).one("webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend",function(e){typeof t.afterMove=="function"&&t.afterMove(r)})};e.fn.moveDown=function(){var t=e(this);index=e(r.sectionContainer+".active").data("index");current=e(r.sectionContainer+"[data-index='"+index+"']");next=e(r.sectionContainer+"[data-index='"+(index+1)+"']");if(next.length<1){if(r.loop!=1)return;pos=0;next=e(r.sectionContainer+"[data-index='1']")}else pos=index*100*-1;typeof r.beforeMove=="function"&&r.beforeMove(current.data("index"));current.removeClass("active");next.addClass("active");if(r.pagination==1){e(".onepage-pagination li a[data-index='"+index+"']").removeClass("active");e(".onepage-pagination li a[data-index='"+next.data("index")+"']").addClass("active")}e("body")[0].className=e("body")[0].className.replace(/\bviewing-page-\d.*?\b/g,"");e("body").addClass("viewing-page-"+next.data("index"));if(history.replaceState&&r.updateURL==1){var n=window.location.href.substr(0,window.location.href.indexOf("#"))+"#"+(index+1);history.pushState({},document.title,n)}t.transformPage(r,pos,index)};e.fn.moveUp=function(){var t=e(this);index=e(r.sectionContainer+".active").data("index");current=e(r.sectionContainer+"[data-index='"+index+"']");next=e(r.sectionContainer+"[data-index='"+(index-1)+"']");if(next.length<1){if(r.loop!=1)return;pos=(total-1)*100*-1;next=e(r.sectionContainer+"[data-index='"+total+"']")}else pos=(next.data("index")-1)*100*-1;typeof r.beforeMove=="function"&&r.beforeMove(current.data("index"));current.removeClass("active");next.addClass("active");if(r.pagination==1){e(".onepage-pagination li a[data-index='"+index+"']").removeClass("active");e(".onepage-pagination li a[data-index='"+next.data("index")+"']").addClass("active")}e("body")[0].className=e("body")[0].className.replace(/\bviewing-page-\d.*?\b/g,"");e("body").addClass("viewing-page-"+next.data("index"));if(history.replaceState&&r.updateURL==1){var n=window.location.href.substr(0,window.location.href.indexOf("#"))+"#"+(index-1);history.pushState({},document.title,n)}t.transformPage(r,pos,index)};e.fn.moveTo=function(t){current=e(r.sectionContainer+".active");next=e(r.sectionContainer+"[data-index='"+t+"']");if(next.length>0){typeof r.beforeMove=="function"&&r.beforeMove(current.data("index"));current.removeClass("active");next.addClass("active");e(".onepage-pagination li a.active").removeClass("active");e(".onepage-pagination li a[data-index='"+t+"']").addClass("active");e("body")[0].className=e("body")[0].className.replace(/\bviewing-page-\d.*?\b/g,"");e("body").addClass("viewing-page-"+next.data("index"));pos=(t-1)*100*-1;i.transformPage(r,pos,t);if(r.updateURL==0)return!1}};i.addClass("onepage-wrapper").css("position","relative");e.each(s,function(t){e(this).css({position:"absolute",top:topPos+"%"}).addClass("section").attr("data-index",t+1);topPos+=100;r.pagination==1&&(paginationList+="<li><a data-index='"+(t+1)+"' href='#"+(t+1)+"'></a></li>")});i.swipeEvents().bind("swipeDown",function(t){e("body").hasClass("disabled-onepage-scroll")||t.preventDefault();i.moveUp()}).bind("swipeUp",function(t){e("body").hasClass("disabled-onepage-scroll")||t.preventDefault();i.moveDown()});if(r.pagination==1){e("<ul class='onepage-pagination'>"+paginationList+"</ul>").prependTo("body");posTop=i.find(".onepage-pagination").height()/2*-1;i.find(".onepage-pagination").css("margin-top",posTop)}if(window.location.hash!=""&&window.location.hash!="#1"){init_index=window.location.hash.replace("#","");e(r.sectionContainer+"[data-index='"+init_index+"']").addClass("active");e("body").addClass("viewing-page-"+init_index);r.pagination==1&&e(".onepage-pagination li a[data-index='"+init_index+"']").addClass("active");next=e(r.sectionContainer+"[data-index='"+init_index+"']");if(next){next.addClass("active");r.pagination==1&&e(".onepage-pagination li a[data-index='"+init_index+"']").addClass("active");e("body")[0].className=e("body")[0].className.replace(/\bviewing-page-\d.*?\b/g,"");e("body").addClass("viewing-page-"+next.data("index"));if(history.replaceState&&r.updateURL==1){var a=window.location.href.substr(0,window.location.href.indexOf("#"))+"#"+init_index;history.pushState({},document.title,a)}}pos=(init_index-1)*100*-1;i.transformPage(r,pos,init_index)}else{e(r.sectionContainer+"[data-index='1']").addClass("active");e("body").addClass("viewing-page-1");r.pagination==1&&e(".onepage-pagination li a[data-index='1']").addClass("active")}r.pagination==1&&e(".onepage-pagination li a").click(function(){var t=e(this).data("index");if(!e(this).hasClass("active")){current=e(r.sectionContainer+".active");next=e(r.sectionContainer+"[data-index='"+t+"']");if(next){current.removeClass("active");next.addClass("active");e(".onepage-pagination li a.active").removeClass("active");e(".onepage-pagination li a[data-index='"+t+"']").addClass("active");e("body")[0].className=e("body")[0].className.replace(/\bviewing-page-\d.*?\b/g,"");e("body").addClass("viewing-page-"+next.data("index"))}pos=(t-1)*100*-1;i.transformPage(r,pos,t)}if(r.updateURL==0)return!1});e(document).bind("mousewheel DOMMouseScroll",function(t){t.preventDefault();var n=t.originalEvent.wheelDelta||-t.originalEvent.detail;e("body").hasClass("disabled-onepage-scroll")||u(t,n)});if(r.responsiveFallback!=0){e(window).resize(function(){o()});o()}r.keyboard==1&&e(document).keydown(function(t){var n=t.target.tagName.toLowerCase();if(!e("body").hasClass("disabled-onepage-scroll"))switch(t.which){case 38:n!="input"&&n!="textarea"&&i.moveUp();break;case 40:n!="input"&&n!="textarea"&&i.moveDown();break;default:return}t.preventDefault()});return!1}}(window.jQuery);