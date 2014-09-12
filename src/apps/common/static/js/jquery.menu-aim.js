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
*/
(function($) {

    $.fn.menuAim = function(opts) {
        // Initialize menu-aim for all elements in jQuery collection
        this.each(function() {
            init.call(this, opts);
        });

        return this;
    };

    function init(opts) {
        var $menu = $(this),
            activeRow = null,
            mouseLocs = [],
            lastDelayLoc = null,
            timeoutId = null,
            options = $.extend({
                rowSelector: "> li",
                submenuSelector: "*",
                submenuDirection: "right",
                tolerance: 75,  // bigger = more forgivey when entering submenu
                enter: $.noop,
                exit: $.noop,
                activate: $.noop,
                deactivate: $.noop,
                exitMenu: $.noop
            }, opts);

        var MOUSE_LOCS_TRACKED = 3,  // number of past mouse locations to track
            DELAY = 1000;  // ms delay when user appears to be entering submenu

        /**
         * Keep track of the last few locations of the mouse.
         */
        var mousemoveDocument = function(e) {
                mouseLocs.push({x: e.pageX, y: e.pageY});

                if (mouseLocs.length > MOUSE_LOCS_TRACKED) {
                    mouseLocs.shift();
                }
            };

        /**
         * Cancel possible row activations when leaving the menu entirely
         */
        var mouseleaveMenu = function() {
                if (timeoutId) {
                    clearTimeout(timeoutId);
                }
         /**
         * close menu on mouse out
         **/
                options.exitMenu(this);
                // Deactivate the currently active row on menu exit.
                if (activeRow) {
                  options.deactivate(activeRow);
                }

                activeRow = null;
            };

        /**
         * Trigger a possible row activation whenever entering a new row.
         */
        var mouseenterRow = function() {
                if (timeoutId) {
                    // Cancel any previous activation delays
                    clearTimeout(timeoutId);
                }

                options.enter(this);
                possiblyActivate(this);
            },
            mouseleaveRow = function() {
                options.exit(this);
            };

        /*
         * Immediately activate a row if the user clicks on it.
         */
        var clickRow = function() {
                activate(this);
            };

        /**
         * Activate a menu row.
         */
        var activate = function(row) {
                if (row == activeRow) {
                    return;
                }

                if (activeRow) {
                    options.deactivate(activeRow);
                }

                options.activate(row);
                activeRow = row;
            };

        /**
         * Possibly activate a menu row. If mouse movement indicates that we
         * shouldn't activate yet because user may be trying to enter
         * a submenu's content, then delay and check again later.
         */
        var possiblyActivate = function(row) {
                var delay = activationDelay();

                if (delay) {
                    timeoutId = setTimeout(function() {
                        possiblyActivate(row);
                    }, delay);
                } else {
                    activate(row);
                }
            };

        /**
         * Return the amount of time that should be used as a delay before the
         * currently hovered row is activated.
         *
         * Returns 0 if the activation should happen immediately. Otherwise,
         * returns the number of milliseconds that should be delayed before
         * checking again to see if the row should be activated.
         */
        var activationDelay = function() {
                if (!activeRow || !$(activeRow).is(options.submenuSelector)) {
                    // If there is no other submenu row already active, then
                    // go ahead and activate immediately.
                    return 0;
                }

                var offset = $menu.offset(),
                    upperLeft = {
                        x: offset.left,
                        y: offset.top - options.tolerance
                    },
                    upperRight = {
                        x: offset.left + $menu.outerWidth(),
                        y: upperLeft.y
                    },
                    lowerLeft = {
                        x: offset.left,
                        y: offset.top + $menu.outerHeight() + options.tolerance
                    },
                    lowerRight = {
                        x: offset.left + $menu.outerWidth(),
                        y: lowerLeft.y
                    },
                    loc = mouseLocs[mouseLocs.length - 1],
                    prevLoc = mouseLocs[0];

                if (!loc) {
                    return 0;
                }

                if (!prevLoc) {
                    prevLoc = loc;
                }

                if (prevLoc.x < offset.left || prevLoc.x > lowerRight.x ||
                    prevLoc.y < offset.top || prevLoc.y > lowerRight.y) {
                    // If the previous mouse location was outside of the entire
                    // menu's bounds, immediately activate.
                    return 0;
                }

                if (lastDelayLoc &&
                        loc.x == lastDelayLoc.x && loc.y == lastDelayLoc.y) {
                    // If the mouse hasn't moved since the last time we checked
                    // for activation status, immediately activate.
                    return 0;
                }

                // Detect if the user is moving towards the currently activated
                // submenu.
                //
                // If the mouse is heading relatively clearly towards
                // the submenu's content, we should wait and give the user more
                // time before activating a new row. If the mouse is heading
                // elsewhere, we can immediately activate a new row.
                //
                // We detect this by calculating the slope formed between the
                // current mouse location and the upper/lower right points of
                // the menu. We do the same for the previous mouse location.
                // If the current mouse location's slopes are
                // increasing/decreasing appropriately compared to the
                // previous's, we know the user is moving toward the submenu.
                //
                // Note that since the y-axis increases as the cursor moves
                // down the screen, we are looking for the slope between the
                // cursor and the upper right corner to decrease over time, not
                // increase (somewhat counterintuitively).
                function slope(a, b) {
                    return (b.y - a.y) / (b.x - a.x);
                };

                var decreasingCorner = upperRight,
                    increasingCorner = lowerRight;

                // Our expectations for decreasing or increasing slope values
                // depends on which direction the submenu opens relative to the
                // main menu. By default, if the menu opens on the right, we
                // expect the slope between the cursor and the upper right
                // corner to decrease over time, as explained above. If the
                // submenu opens in a different direction, we change our slope
                // expectations.
                if (options.submenuDirection == "left") {
                    decreasingCorner = lowerLeft;
                    increasingCorner = upperLeft;
                } else if (options.submenuDirection == "below") {
                    decreasingCorner = lowerRight;
                    increasingCorner = lowerLeft;
                } else if (options.submenuDirection == "above") {
                    decreasingCorner = upperLeft;
                    increasingCorner = upperRight;
                }

                var decreasingSlope = slope(loc, decreasingCorner),
                    increasingSlope = slope(loc, increasingCorner),
                    prevDecreasingSlope = slope(prevLoc, decreasingCorner),
                    prevIncreasingSlope = slope(prevLoc, increasingCorner);

                if (decreasingSlope < prevDecreasingSlope &&
                        increasingSlope > prevIncreasingSlope) {
                    // Mouse is moving from previous location towards the
                    // currently activated submenu. Delay before activating a
                    // new menu row, because user may be moving into submenu.
                    lastDelayLoc = loc;
                    return DELAY;
                }

                lastDelayLoc = null;
                return 0;
            };

        /**
         * Hook up initial menu events
         */
        $menu
            .mouseleave(mouseleaveMenu)
            .find(options.rowSelector)
                .mouseenter(mouseenterRow)
                .mouseleave(mouseleaveRow)
                .click(clickRow);

        $(document).mousemove(mousemoveDocument);

    };
})(jQuery);

/* ========================================================================
 * Bootstrap: dropdown.js v3.1.0
 * http://getbootstrap.com/javascript/#dropdowns
 * ========================================================================
 * Copyright 2011-2014 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * ======================================================================== */


+function ($) {
  'use strict';

  // DROPDOWN CLASS DEFINITION
  // =========================

  var backdrop = '.dropdown-backdrop'
  var toggle   = '[data-toggle=dropdown]'
  var Dropdown = function (element) {
    $(element).on('click.bs.dropdown', this.toggle)
  }

  Dropdown.prototype.toggle = function (e) {
    var $this = $(this)

    if ($this.is('.disabled, :disabled')) return

    var $parent  = getParent($this)
    var isActive = $parent.hasClass('open')

    clearMenus()

    if (!isActive) {
      if ('ontouchstart' in document.documentElement && !$parent.closest('.navbar-nav').length) {
        // if mobile we use a backdrop because click events don't delegate
        $('<div class="dropdown-backdrop"/>').insertAfter($(this)).on('click', clearMenus)
      }

      var relatedTarget = { relatedTarget: this }
      $parent.trigger(e = $.Event('show.bs.dropdown', relatedTarget))

      if (e.isDefaultPrevented()) return

      $parent
        .toggleClass('open')
        .trigger('shown.bs.dropdown', relatedTarget)

      $this.focus()
    }

    return false
  }

  Dropdown.prototype.keydown = function (e) {
    if (!/(38|40|27)/.test(e.keyCode)) return

    var $this = $(this)

    e.preventDefault()
    e.stopPropagation()

    if ($this.is('.disabled, :disabled')) return

    var $parent  = getParent($this)
    var isActive = $parent.hasClass('open')

    if (!isActive || (isActive && e.keyCode == 27)) {
      if (e.which == 27) $parent.find(toggle).focus()
      return $this.click()
    }

    var desc = ' li:not(.divider):visible a'
    var $items = $parent.find('[role=menu]' + desc + ', [role=listbox]' + desc)

    if (!$items.length) return

    var index = $items.index($items.filter(':focus'))

    if (e.keyCode == 38 && index > 0)                 index--                        // up
    if (e.keyCode == 40 && index < $items.length - 1) index++                        // down
    if (!~index)                                      index = 0

    $items.eq(index).focus()
  }

  function clearMenus(e) {
    $(backdrop).remove()
    $(toggle).each(function () {
      var $parent = getParent($(this))
      var relatedTarget = { relatedTarget: this }
      if (!$parent.hasClass('open')) return
      $parent.trigger(e = $.Event('hide.bs.dropdown', relatedTarget))
      if (e.isDefaultPrevented()) return
      $parent.removeClass('open').trigger('hidden.bs.dropdown', relatedTarget)
    })
  }

  function getParent($this) {
    var selector = $this.attr('data-target')

    if (!selector) {
      selector = $this.attr('href')
      selector = selector && /#[A-Za-z]/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '') //strip for ie7
    }

    var $parent = selector && $(selector)

    return $parent && $parent.length ? $parent : $this.parent()
  }


  // DROPDOWN PLUGIN DEFINITION
  // ==========================

  var old = $.fn.dropdown

  $.fn.dropdown = function (option) {
    return this.each(function () {
      var $this = $(this)
      var data  = $this.data('bs.dropdown')

      if (!data) $this.data('bs.dropdown', (data = new Dropdown(this)))
      if (typeof option == 'string') data[option].call($this)
    })
  }

  $.fn.dropdown.Constructor = Dropdown


  // DROPDOWN NO CONFLICT
  // ====================

  $.fn.dropdown.noConflict = function () {
    $.fn.dropdown = old
    return this
  }


  // APPLY TO STANDARD DROPDOWN ELEMENTS
  // ===================================
/*
  $(document)
    .on('click.bs.dropdown.data-api', clearMenus)
    .on('click.bs.dropdown.data-api', '.dropdown form', function (e) { e.stopPropagation() })
    .on('mouseenter.bs.dropdown.data-api', toggle, Dropdown.prototype.toggle)
    .on('keydown.bs.dropdown.data-api', toggle + ', [role=menu], [role=listbox]', Dropdown.prototype.keydown)
*/
        jQuery('ul.nav li.dropdown').hover(function() {
          jQuery(this).find('.dropdown-menu').stop(true, true).delay(200).slideDown('fast');
          jQuery(this).addClass('open');
        }, function() {
          jQuery(this).find('.dropdown-menu').stop(true, true).delay(200).slideUp('fast');
          jQuery(this).removeClass('open');

        });

}(jQuery);
