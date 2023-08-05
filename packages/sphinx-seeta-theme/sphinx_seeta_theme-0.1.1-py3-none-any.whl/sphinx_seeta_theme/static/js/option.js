/*! Sphinx-Seeta-Theme | Copyright (c) 2017-present, SeetaTech, Co.,Ltd. */

$(document).ready(function () {
  let opt_groups = $(".opt-group");
  if (opt_groups.length > 0) {
    function label(lbl) {
      return lbl.replace(/[ .]/g, '-').toLowerCase();
    }
    function showContent() {
      let active_keys_map = new Map();
      $('.opt-group .active').each(function() {
        let key;
        const filters = $(this).attr("filter").split('-');
        for (let i = 0; i < filters.length; i++) {
          key = filters[i];
          if (!active_keys_map.has(key))
            active_keys_map.set(key, []);
          active_keys_map.get(key).push(label($(this).text()));
        }
      });
      let sections = $(".section");
      for (let i = 0; i < sections.length; i++) {
        const sec_id = sections.eq(i).attr("id");
        let is_display = true;
        active_keys_map.forEach(function(value, key) {
          if (sec_id.indexOf(key) !== -1) {
            for (let j = 0; j < value.length; j++) {
              if (sec_id.indexOf(value[j]) === -1) {
                is_display = false;
                break;
              }
            }
            let title = sections.eq(i).children().first();
            let option_start = title.text().indexOf(".withOption");
            if (option_start !== -1) {
              sections.eq(i).children().first().text(
                title.text().substr(0, option_start));
            }
          }
        });
        if (is_display) {
          sections.eq(i).show();
        } else {
          sections.eq(i).hide();
        }
      }
    }
    showContent();
    opt_groups.on('click', '.opt', function setContent() {
      let el = $(this);
      el.siblings().removeClass('active');
      el.addClass('active');
      showContent();
    });
  }
});
