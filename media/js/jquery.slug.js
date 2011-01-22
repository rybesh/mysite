jQuery.fn.slug = function(options) {
  var settings = { slug: '#id_slug' };
	
  if(options) {
    jQuery.extend(settings, options);
  }
	
  $this = $(this);

  makeSlug = function() {
    var slug = jQuery.trim($this.val()) // Trimming recommended by Brooke Dukes - http://www.thewebsitetailor.com/2008/04/jquery-slug-plugin/comment-page-1/#comment-23
      .replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase() // See http://www.djangosnippets.org/snippets/1488/ 
      .replace(/\-{2,}/g,'-'); // If we end up with any 'multiple hyphens', replace with just one. Temporary bugfix for input 'this & that'=>'this--that'
    $('input' + settings.slug).val(slug);
  }
		
  $(this).keyup(makeSlug);
		
  return $this;
};
