/*! Sphinx-Seeta-Theme | Copyright (c) 2017-present, SeetaTech, Co.,Ltd. */

(function($) {
$(document).ready(function() {
  // Add Note, Warning to Bootstrap style
  $(".admonition")
      .addClass("alert alert-info")
      .filter(".warning, .caution")
      .removeClass("alert-info")
      .addClass("alert-warning")
      .end()
      .filter(".error, .danger")
      .removeClass("alert-info")
      .addClass("alert-danger alert-error")
      .end();

  // Inline code styles to Bootstrap style
  $("tt.docutils.literal").not(".xref").each(function(i, e) {
    // ignore references
    if (!$(e).parent().hasClass("reference")) {
      $(e).replaceWith(function() {
        return $("<code/>").html($(this).html());
      });
    }
  });

  // Patch table to Bootstrap style
  $("table.docutils")
      .removeClass("docutils")
      .addClass("table")
      .attr("border", 0);

  // Fix the wrong offset of href with fixed navbar
  let smoothedScrollBody = function(target, offset, time) {
    if (target && target.offset()) {
      $("html,body")
          .animate(
              {scrollTop : target.offset().top - offset}, time, function() {});
    }
  };
  if ($(location.href.split("#")[1])) {
    let target = $(document.getElementById(location.href.split("#")[1]));
    smoothedScrollBody(target, 70, 300);
  }
  $(".headerlink").click(function() {
    let target = $(document.getElementById($(this).attr('href').split("#")[1]));
    smoothedScrollBody(target, 70, 100);
  });
  $(".doc-container .reference").click(function() {
    let target = $(document.getElementById($(this).attr('href').split("#")[1]));
    smoothedScrollBody(target, 70, 100);
  });

  // Enhance the navbar
  // 1) Make a responsive search form
  // 2) Change the icon color on click
  let navbar_form = $(".navbar-form .form-control")
  navbar_form.focus(function() {
    let form = $(this).parent().parent();
    let expand_width = form.parent().width() - 48;
    form.siblings().css("z-index", -1);
    $(this).animate({"min-width" : expand_width}, "fast", "swing");
  });
  navbar_form.blur(function() {
    $(this).parent().parent().siblings().css("z-index", "");
    $(this).animate({"min-width" : ""}, "fast", "swing");
  });
  $(".navbar-toggle").click(function() {
    let icon;
    let icons = $(this).find("span");
    for (let i = 0; i < icons.length; i++) {
      icon = icons.eq(i);
      if (icon.css("background-color") === "rgb(255, 255, 255)") {
        icon.css("background-color", "rgb(179, 179, 179)");
      } else {
        icon.css("background-color", "rgb(255, 255, 255)");
      }
    }
  });

  // Enhance the sidebar-nav
  // 1) Fixed to the window height
  // 2) Change the icon on click
  let sidebar_nav = $(".sidebar-nav")
  if (sidebar_nav.length > 0) {
      sidebar_nav.css("height", $(window).height());
      $(window).resize(function() {
        sidebar_nav.css("height", $(window).height());
      });
    $(".sidebar-nav-toggle").click(function() {
      if ($(this).hasClass("fa-arrow-left")) {
        $(this).removeClass("fa-arrow-left").addClass("fa-close");
      } else {
        $(this).removeClass("fa-close").addClass("fa-arrow-left");
      }
    });
  } else {
    $(".sidebar-nav-toggle").remove();
  }

  // Enhance the sidebar-toc
  // 1) To be responsive to the scroll of main content
  // 2) Limit the max height between header and footer
  if ($(".sidebar-toc").length > 0) {
    let findNextSection = function(arr, key, offset) {
      let i = arr.length - 1;
      for (; i >= 1; i--) {
        if (key + offset > arr[i]) return i;
      }
      return i;
    };
    let anchor_spacing = 150;
    let section_spacing = $("#navbar").height() + 32;
    let bar_init_height = $('.sidebar-toc').height();
    let bar_shrink = false;
    let section_tops = [], anchor_tops = [];
    let sections = $(".section"), anchors = $(".sidebar-toc a");
    let last_section = 0, next_section;
    for (let i = 0; i < sections.length; i++) {
      section_tops.push(sections.eq(i).offset().top);
      anchor_tops.push(anchors.eq(i).position().top);
      if (anchors.eq(i).hasClass("current")) last_section = i;
    }
    $(window).scroll(function() {
      next_section =
          findNextSection(section_tops, $("html").scrollTop(), section_spacing);
      let bar = $('.sidebar-toc');
      let max_height = $('.footer').offset().top - bar.offset().top - 30;
      // Shrink or restore
      if (bar_init_height > max_height) {
        bar_shrink = true;
        let bonus_scroll = bar_init_height - max_height;
        bar.height(max_height);
        bar.scrollTop(bar.scrollTop() + bonus_scroll);
      } else if (bar_shrink) {
        bar.height(bar_init_height);
      }
      if (next_section !== last_section) {
        anchors.eq(next_section).addClass("current");
        if (next_section > last_section) {
          let anchor_offset = anchor_tops[next_section] + anchor_spacing;
          if (anchor_offset > (bar.height() + bar.scrollTop())) {
            bar.scrollTop(anchor_offset - bar.height()); // ScrollDown
          }
        } else {
          let anchor_offset = anchor_tops[next_section];
          if (anchor_offset < bar.scrollTop()) {
            bar.scrollTop(anchor_offset); // ScrollUp
            console.log(anchor_offset);
          }
        }
        anchors.eq(last_section).removeClass("current");
      }
      last_section = next_section;
    });
  }
});
}(window.$jqTheme || window.jQuery));
