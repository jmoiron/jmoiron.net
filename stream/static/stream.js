/* stream.js
 * written by @jmoiron for jmoiron.net
 */

$(function() {
  $('.gh-files .expander a').click(function(e) {
    e.preventDefault();
    var $this = $(this);
    var $li = $this.parents(".modified");
    var $diff = $li.find(".diff");
    if ($diff.is(":visible")) {
      $diff.slideUp(300, function() {
        $li.css({paddingBottom: '0'});
      });
    } else {
      $diff.slideDown(300, function() {
        $li.css({paddingBottom: '.5em'});    
      });
    }
  });
});

