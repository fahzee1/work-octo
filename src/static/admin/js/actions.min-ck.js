(function(e){e.fn.actions=function(t){var n=e.extend({},e.fn.actions.defaults,t),r=e(this),i=!1;checker=function(t){t?showQuestion():reset();e(r).attr("checked",t).parent().parent().toggleClass(n.selectedClass,t)};updateCounter=function(){var t=e(r).filter(":checked").length;e(n.counterContainer).html(interpolate(ngettext("%(sel)s of %(cnt)s selected","%(sel)s of %(cnt)s selected",t),{sel:t,cnt:_actions_icnt},!0));e(n.allToggle).attr("checked",function(){if(t==r.length){value=!0;showQuestion()}else{value=!1;clearAcross()}return value})};showQuestion=function(){e(n.acrossClears).hide();e(n.acrossQuestions).show();e(n.allContainer).hide()};showClear=function(){e(n.acrossClears).show();e(n.acrossQuestions).hide();e(n.actionContainer).toggleClass(n.selectedClass);e(n.allContainer).show();e(n.counterContainer).hide()};reset=function(){e(n.acrossClears).hide();e(n.acrossQuestions).hide();e(n.allContainer).hide();e(n.counterContainer).show()};clearAcross=function(){reset();e(n.acrossInput).val(0);e(n.actionContainer).removeClass(n.selectedClass)};e(n.counterContainer).show();e(this).filter(":checked").each(function(){e(this).parent().parent().toggleClass(n.selectedClass);updateCounter();e(n.acrossInput).val()==1&&showClear()});e(n.allToggle).show().click(function(){checker(e(this).attr("checked"));updateCounter()});e("div.actions span.question a").click(function(t){t.preventDefault();e(n.acrossInput).val(1);showClear()});e("div.actions span.clear a").click(function(t){t.preventDefault();e(n.allToggle).attr("checked",!1);clearAcross();checker(0);updateCounter()});lastChecked=null;e(r).click(function(t){t||(t=window.event);var i=t.target?t.target:t.srcElement;if(lastChecked&&e.data(lastChecked)!=e.data(i)&&t.shiftKey==1){var s=!1;e(lastChecked).attr("checked",i.checked).parent().parent().toggleClass(n.selectedClass,i.checked);e(r).each(function(){if(e.data(this)==e.data(lastChecked)||e.data(this)==e.data(i))s=s?!1:!0;s&&e(this).attr("checked",i.checked).parent().parent().toggleClass(n.selectedClass,i.checked)})}e(i).parent().parent().toggleClass(n.selectedClass,i.checked);lastChecked=i;updateCounter()});e("form#changelist-form table#result_list tr").find("td:gt(0) :input").change(function(){i=!0});e('form#changelist-form button[name="index"]').click(function(){if(i)return confirm(gettext("You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost."))});e('form#changelist-form input[name="_save"]').click(function(){var t=!1;e("div.actions select option:selected").each(function(){e(this).val()&&(t=!0)});if(t)return i?confirm(gettext("You have selected an action, but you haven't saved your changes to individual fields yet. Please click OK to save. You'll need to re-run the action.")):confirm(gettext("You have selected an action, and you haven't made any changes on individual fields. You're probably looking for the Go button rather than the Save button."))})};e.fn.actions.defaults={actionContainer:"div.actions",counterContainer:"span.action-counter",allContainer:"div.actions span.all",acrossInput:"div.actions input.select-across",acrossQuestions:"div.actions span.question",acrossClears:"div.actions span.clear",allToggle:"#action-toggle",selectedClass:"selected"}})(django.jQuery);