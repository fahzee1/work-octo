/**
 * menu-aim is a jQuery plugin for dropdown menus that can differentiate
 * between a user trying hover over a dropdown item vs trying to navigate into
 * a submenu's contents.
 *
 * menu-aim assumes that you have are using a menu with submenus that expand
 * to the menu's right. It will fire events when the user's mouse enters a new
 * dropdown item *and* when that item is being intentionally hovered over.
 *
 * __________________________
 * | Monkeys  >|   Gorilla  |
 * | Gorillas >|   Content  |
 * | Chimps   >|   Here     |
 * |___________|____________|
 *
 * In the above example, "Gorillas" is selected and its submenu content is
 * being shown on the right. Imagine that the user's cursor is hovering over
 * "Gorillas." When they move their mouse into the "Gorilla Content" area, they
 * may briefly hover over "Chimps." This shouldn't close the "Gorilla Content"
 * area.
 *
 * This problem is normally solved using timeouts and delays. menu-aim tries to
 * solve this by detecting the direction of the user's mouse movement. This can
 * make for quicker transitions when navigating up and down the menu. The
 * experience is hopefully similar to amazon.com/'s "Shop by Department"
 * dropdown.
 *
 * Use like so:
 *
 *      $("#menu").menuAim({
 *          activate: $.noop,  // fired on row activation
 *          deactivate: $.noop  // fired on row deactivation
 *      });
 *
 *  ...to receive events when a menu's row has been purposefully (de)activated.
 *
 * The following options can be passed to menuAim. All functions execute with
 * the relevant row's HTML element as the execution context ('this'):
 *
 *      .menuAim({
 *          // Function to call when a row is purposefully activated. Use this
 *          // to show a submenu's content for the activated row.
 *          activate: function() {},
 *
 *          // Function to call when a row is deactivated.
 *          deactivate: function() {},
 *
 *          // Function to call when mouse enters a menu row. Entering a row
 *          // does not mean the row has been activated, as the user may be
 *          // mousing over to a submenu.
 *          enter: function() {},
 *
 *          // Function to call when mouse exits a menu row.
 *          exit: function() {},
 *
 *          // Selector for identifying which elements in the menu are rows
 *          // that can trigger the above events. Defaults to "> li".
 *          rowSelector: "> li",
 *
 *          // You may have some menu rows that aren't submenus and therefore
 *          // shouldn't ever need to "activate." If so, filter submenu rows w/
 *          // this selector. Defaults to "*" (all elements).
 *          submenuSelector: "*",
 *
 *          // Direction the submenu opens relative to the main menu. Can be
 *          // left, right, above, or below. Defaults to "right".
 *          submenuDirection: "right"
 *      });
 *
 * https://github.com/kamens/jQuery-menu-aim
*/(function(e){function t(t){var n=e(this),r=null,i=[],s=null,o=null,u=e.extend({rowSelector:"> li",submenuSelector:"*",submenuDirection:"right",tolerance:75,enter:e.noop,exit:e.noop,activate:e.noop,deactivate:e.noop,exitMenu:e.noop},t),a=3,f=1e3,l=function(e){i.push({x:e.pageX,y:e.pageY});i.length>a&&i.shift()},c=function(){o&&clearTimeout(o);u.exitMenu(this);r&&u.deactivate(r);r=null},h=function(){o&&clearTimeout(o);u.enter(this);m(this)},p=function(){u.exit(this)},d=function(){v(this)},v=function(e){if(e==r)return;r&&u.deactivate(r);u.activate(e);r=e},m=function(e){var t=g();t?o=setTimeout(function(){m(e)},t):v(e)},g=function(){function d(e,t){return(t.y-e.y)/(t.x-e.x)}if(!r||!e(r).is(u.submenuSelector))return 0;var t=n.offset(),o={x:t.left,y:t.top-u.tolerance},a={x:t.left+n.outerWidth(),y:o.y},l={x:t.left,y:t.top+n.outerHeight()+u.tolerance},c={x:t.left+n.outerWidth(),y:l.y},h=i[i.length-1],p=i[0];if(!h)return 0;p||(p=h);if(p.x<t.left||p.x>c.x||p.y<t.top||p.y>c.y)return 0;if(s&&h.x==s.x&&h.y==s.y)return 0;var v=a,m=c;if(u.submenuDirection=="left"){v=l;m=o}else if(u.submenuDirection=="below"){v=c;m=l}else if(u.submenuDirection=="above"){v=o;m=a}var g=d(h,v),y=d(h,m),b=d(p,v),w=d(p,m);if(g<b&&y>w){s=h;return f}s=null;return 0};n.mouseleave(c).find(u.rowSelector).mouseenter(h).mouseleave(p).click(d);e(document).mousemove(l)}e.fn.menuAim=function(e){this.each(function(){t.call(this,e)});return this}})(jQuery);+function(e){"use strict";function i(r){e(t).remove();e(n).each(function(){var t=s(e(this)),n={relatedTarget:this};if(!t.hasClass("open"))return;t.trigger(r=e.Event("hide.bs.dropdown",n));if(r.isDefaultPrevented())return;t.removeClass("open").trigger("hidden.bs.dropdown",n)})}function s(t){var n=t.attr("data-target");if(!n){n=t.attr("href");n=n&&/#[A-Za-z]/.test(n)&&n.replace(/.*(?=#[^\s]*$)/,"")}var r=n&&e(n);return r&&r.length?r:t.parent()}var t=".dropdown-backdrop",n="[data-toggle=dropdown]",r=function(t){e(t).on("click.bs.dropdown",this.toggle)};r.prototype.toggle=function(t){var n=e(this);if(n.is(".disabled, :disabled"))return;var r=s(n),o=r.hasClass("open");i();if(!o){"ontouchstart"in document.documentElement&&!r.closest(".navbar-nav").length&&e('<div class="dropdown-backdrop"/>').insertAfter(e(this)).on("click",i);var u={relatedTarget:this};r.trigger(t=e.Event("show.bs.dropdown",u));if(t.isDefaultPrevented())return;r.toggleClass("open").trigger("shown.bs.dropdown",u);n.focus()}return!1};r.prototype.keydown=function(t){if(!/(38|40|27)/.test(t.keyCode))return;var r=e(this);t.preventDefault();t.stopPropagation();if(r.is(".disabled, :disabled"))return;var i=s(r),o=i.hasClass("open");if(!o||o&&t.keyCode==27){t.which==27&&i.find(n).focus();return r.click()}var u=" li:not(.divider):visible a",a=i.find("[role=menu]"+u+", [role=listbox]"+u);if(!a.length)return;var f=a.index(a.filter(":focus"));t.keyCode==38&&f>0&&f--;t.keyCode==40&&f<a.length-1&&f++;~f||(f=0);a.eq(f).focus()};var o=e.fn.dropdown;e.fn.dropdown=function(t){return this.each(function(){var n=e(this),i=n.data("bs.dropdown");i||n.data("bs.dropdown",i=new r(this));typeof t=="string"&&i[t].call(n)})};e.fn.dropdown.Constructor=r;e.fn.dropdown.noConflict=function(){e.fn.dropdown=o;return this};jQuery("ul.nav li.dropdown").hover(function(){jQuery(this).find(".dropdown-menu").stop(!0,!0).delay(200).slideDown("fast");jQuery(this).addClass("open")},function(){jQuery(this).find(".dropdown-menu").stop(!0,!0).delay(200).slideUp("fast");jQuery(this).removeClass("open")})}(jQuery);