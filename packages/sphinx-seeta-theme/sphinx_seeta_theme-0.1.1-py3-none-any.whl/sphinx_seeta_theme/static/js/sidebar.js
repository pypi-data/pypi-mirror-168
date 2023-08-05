/*! Sphinx-Seeta-Theme | Copyright (c) 2017-present, SeetaTech, Co.,Ltd. */

$(document).ready(function() {
  function addToggle(toc_class) {
    $(toc_class + " .sidebar-nav-wrapper").children("ul").first()
        .css({"margin-top" : "6px", "margin-left" : "3px"});
    let all_entries = $(toc_class + " .sidebar-nav-wrapper li");
    all_entries.each(function() {
      let child_ul = $(this).find("ul");
      if (child_ul.length && child_ul.first().children().length) {
        let anchor = $(this).children("a").first();
        if (typeof(anchor.attr("href")) != "undefined") {
          let parent_li = anchor.parent().clone();
          parent_li.addClass("leaf");
          parent_li.find("ul").remove();
          parent_li.find("a").text("Overview");
          child_ul.first().prepend(parent_li);
          anchor.attr("href_v2", anchor.attr("href"));
          anchor.removeAttr("href");
        }
        $(this).addClass("closed");
        child_ul.first().hide();
      } else {
        $(this).addClass("leaf");
      }
    });
  }

  function autoExpand(elem) {
    if (elem.parent().hasClass("closed")) {
      elem.parent().removeClass("closed").addClass("opened");
      elem.parent().children("ul").first().slideDown("fast");
    } else if (elem.parent().hasClass("opened")) {
      elem.parent().removeClass("opened").addClass("closed");
      elem.parent().children("ul").first().slideUp("fast");
    }
  }

  function getUrlAnchor(url) {
    let url_array = url.split("#");
    if (url_array.length === 2) return "#" + url_array[url_array.length - 1];
    return undefined;
  }

  function keepExpand() {
    let current_entry;
    let entry_list = $('.sidebar-nav li');
    let local_anchor = getUrlAnchor(location.href);
    let has_local_anchor = false;
    for (let i = entry_list.length - 1; i >= 0; --i) {
      let anchor = entry_list.eq(i).find('a').first();
      let entry_url = anchor.attr('href');
      if (!entry_url) entry_url = anchor.attr('href_v2');
      if (!current_entry && entry_url === "#") {
        current_entry = entry_list.eq(i);
      } else if (local_anchor && entry_url === local_anchor) {
        current_entry = entry_list.eq(i);
        has_local_anchor = true;
      }
    }
    let all_entries = $(".sidebar-nav .sidebar-nav-wrapper li");
    all_entries.each(function() {
      let anchor = $(this).children("a").first();
      anchor.click(function() {
        autoExpand(anchor);
      });
    });
    if (current_entry) {
      current_entry.children("ul").first().show();
      if (!current_entry.hasClass('leaf')) {
        current_entry.removeClass("closed").addClass("opened");
      } else {
        if (!has_local_anchor) {
          current_entry.removeClass("opened").addClass("focused");
        }
      }
      while (current_entry.parent().is('ul') &&
             current_entry.parent().parent().is('li')) {
        current_entry = current_entry.parent().parent();
        current_entry.removeClass("closed").addClass("opened");
        current_entry.children("ul").first().show();
      }
    }
  }

  function rewriteTOC() {
    let anchors = $(".sidebar-toc a");
    let title_anchor = anchors.first();
    let items_list = title_anchor.siblings().first();
    title_anchor.removeClass().addClass("sidebar-title reference").text("Contents");
    title_anchor.parent().parent().css("margin-left", 2);
    title_anchor.parent().parent().append(items_list.children());
    items_list.remove();
    anchors.each(function() {
      $(this).on("click", function() {
        for (let i = 0; i < anchors.length; i++) {
          anchors.eq(i).removeClass("current");
        }
        $(this).addClass("current")
      });
    });
  }

  addToggle(".sidebar-nav");
  keepExpand();
  rewriteTOC();

  // Scroll to center the current focused entry
  let current_last = $(".sidebar-nav .current").last();
  if (current_last.length > 0) {
    $(".sidebar-nav").scrollTop(current_last.position().top - $(window).height() / 2);
  }
});
