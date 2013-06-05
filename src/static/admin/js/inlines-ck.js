/**
 * Django admin inlines
 *
 * Based on jQuery Formset 1.1
 * @author Stanislaus Madueke (stan DOT madueke AT gmail DOT com)
 * @requires jQuery 1.2.6 or later
 *
 * Copyright (c) 2009, Stanislaus Madueke
 * All rights reserved.
 *
 * Spiced up with Code from Zain Memon's GSoC project 2009
 * and modified for Django by Jannis Leidel
 *
 * Licensed under the New BSD License
 * See: http://www.opensource.org/licenses/bsd-license.php
 */(function(e){e.fn.formset=function(t){var n=e.extend({},e.fn.formset.defaults,t),r=function(t,n,r){var i=new RegExp("("+n+"-(\\d+|__prefix__))"),s=n+"-"+r;e(t).attr("for")&&e(t).attr("for",e(t).attr("for").replace(i,s));t.id&&(t.id=t.id.replace(i,s));t.name&&(t.name=t.name.replace(i,s))},i=e("#id_"+n.prefix+"-TOTAL_FORMS").attr("autocomplete","off"),s=parseInt(i.val()),o=e("#id_"+n.prefix+"-MAX_NUM_FORMS").attr("autocomplete","off"),u=o.val()==""||o.val()-i.val()>0;e(this).each(function(t){e(this).not("."+n.emptyCssClass).addClass(n.formCssClass)});if(e(this).length&&u){var a;if(e(this).attr("tagName")=="TR"){var f=this.eq(0).children().length;e(this).parent().append('<tr class="'+n.addCssClass+'"><td colspan="'+f+'"><a href="javascript:void(0)">'+n.addText+"</a></tr>");a=e(this).parent().find("tr:last a")}else{e(this).filter(":last").after('<div class="'+n.addCssClass+'"><a href="javascript:void(0)">'+n.addText+"</a></div>");a=e(this).filter(":last").next().find("a")}a.click(function(){var t=e("#id_"+n.prefix+"-TOTAL_FORMS"),i=e("#"+n.prefix+"-empty"),u=i.clone(!0);u.removeClass(n.emptyCssClass).addClass(n.formCssClass).attr("id",n.prefix+"-"+s);u.is("tr")?u.children(":last").append('<div><a class="'+n.deleteCssClass+'" href="javascript:void(0)">'+n.deleteText+"</a></div>"):u.is("ul")||u.is("ol")?u.append('<li><a class="'+n.deleteCssClass+'" href="javascript:void(0)">'+n.deleteText+"</a></li>"):u.children(":first").append('<span><a class="'+n.deleteCssClass+'" href="javascript:void(0)">'+n.deleteText+"</a></span>");u.find("*").each(function(){r(this,n.prefix,t.val())});u.insertBefore(e(i));e(t).val(parseInt(t.val())+1);s+=1;o.val()!=""&&o.val()-t.val()<=0&&a.parent().hide();u.find("a."+n.deleteCssClass).click(function(){var t=e(this).parents("."+n.formCssClass);t.remove();s-=1;n.removed&&n.removed(t);var i=e("."+n.formCssClass);e("#id_"+n.prefix+"-TOTAL_FORMS").val(i.length);(o.val()==""||o.val()-i.length>0)&&a.parent().show();for(var u=0,f=i.length;u<f;u++){r(e(i).get(u),n.prefix,u);e(i.get(u)).find("*").each(function(){r(this,n.prefix,u)})}return!1});n.added&&n.added(u);return!1})}return this};e.fn.formset.defaults={prefix:"form",addText:"add another",deleteText:"remove",addCssClass:"add-row",deleteCssClass:"delete-row",emptyCssClass:"empty-row",formCssClass:"dynamic-form",added:null,removed:null}})(django.jQuery);