/* document.getElementsBySelector(selector)
   - returns an array of element objects from the current document
     matching the CSS selector. Selectors can contain element names, 
     class names and ids and can be nested. For example:
     
       elements = document.getElementsBySelect('div#main p a.external')
     
     Will return an array of all 'a' elements with 'external' in their 
     class attribute that are contained inside 'p' elements that are 
     contained inside the 'div' element which has id="main"

   New in version 0.4: Support for CSS2 and CSS3 attribute selectors:
   See http://www.w3.org/TR/css3-selectors/#attribute-selectors

   Version 0.4 - Simon Willison, March 25th 2003
   -- Works in Phoenix 0.5, Mozilla 1.3, Opera 7, Internet Explorer 6, Internet Explorer 5 on Windows
   -- Opera 7 fails 
*/function getAllChildren(e){return e.all?e.all:e.getElementsByTagName("*")}document.getElementsBySelector=function(e){if(!document.getElementsByTagName)return new Array;var t=e.split(" "),n=new Array(document);for(var r=0;r<t.length;r++){token=t[r].replace(/^\s+/,"").replace(/\s+$/,"");if(token.indexOf("#")>-1){var i=token.split("#"),s=i[0],o=i[1],u=document.getElementById(o);if(!u||s&&u.nodeName.toLowerCase()!=s)return new Array;n=new Array(u);continue}if(token.indexOf(".")>-1){var i=token.split("."),s=i[0],a=i[1];s||(s="*");var f=new Array,l=0;for(var c=0;c<n.length;c++){var h;if(s=="*")h=getAllChildren(n[c]);else try{h=n[c].getElementsByTagName(s)}catch(p){h=[]}for(var d=0;d<h.length;d++)f[l++]=h[d]}n=new Array;var v=0;for(var m=0;m<f.length;m++)f[m].className&&f[m].className.match(new RegExp("\\b"+a+"\\b"))&&(n[v++]=f[m]);continue}if(token.match(/^(\w*)\[(\w+)([=~\|\^\$\*]?)=?"?([^\]"]*)"?\]$/)){var s=RegExp.$1,g=RegExp.$2,y=RegExp.$3,b=RegExp.$4;s||(s="*");var f=new Array,l=0;for(var c=0;c<n.length;c++){var h;s=="*"?h=getAllChildren(n[c]):h=n[c].getElementsByTagName(s);for(var d=0;d<h.length;d++)f[l++]=h[d]}n=new Array;var v=0,w;switch(y){case"=":w=function(e){return e.getAttribute(g)==b};break;case"~":w=function(e){return e.getAttribute(g).match(new RegExp("\\b"+b+"\\b"))};break;case"|":w=function(e){return e.getAttribute(g).match(new RegExp("^"+b+"-?"))};break;case"^":w=function(e){return e.getAttribute(g).indexOf(b)==0};break;case"$":w=function(e){return e.getAttribute(g).lastIndexOf(b)==e.getAttribute(g).length-b.length};break;case"*":w=function(e){return e.getAttribute(g).indexOf(b)>-1};break;default:w=function(e){return e.getAttribute(g)}}n=new Array;var v=0;for(var m=0;m<f.length;m++)w(f[m])&&(n[v++]=f[m]);continue}s=token;var f=new Array,l=0;for(var c=0;c<n.length;c++){var h=n[c].getElementsByTagName(s);for(var d=0;d<h.length;d++)f[l++]=h[d]}n=f}return n};