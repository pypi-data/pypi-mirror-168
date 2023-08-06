require([
  '++resource++camcomskin.padova.javascripts/slick.js',
  '++resource++camcomskin.padova.javascripts/ellipsed.js',
  'mockup-patterns-modal',
], function(slick, ellipsed, Modal) {
  var ellipsis = ellipsed.ellipsis;

  var options = {
    initialSlide: 0,
    slidesToShow: 4,
    slidesToScroll: 1,
    arrows: true,
    dots: true,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
        },
      },
    ],
  };

  $('.collectionTile.carousel .pat-slider').slick(options);

  setTimeout(function() {
    ellipsis('.tile-collection .collectionItemDescription', 4, {
      responsive: true,
    });
    ellipsis('.news-highlight .news-description', 4, { responsive: true });
    ellipsis('.news-two-rows-collection .collectionItemTitle h3', 3, {
      responsive: true,
    });
    ellipsis('.paired-collection .collectionItemTitle h3', 3, {
      responsive: true,
    });
  }, 0);

  const handleVideoModals = function() {
    $('a.video-renderer-modal').each(function() {
      var videoModal = new Modal($(this), {
        position: 'center middle',
        loadLinksWithinModal: false,
      });
      videoModal.on('after-render', function() {
        document.querySelectorAll('iframe').forEach(function(iframe) {
          var src = iframe.dataset.ccSrc;
          var name = iframe.dataset.ccName;
          var placeholder = iframe.previousElementSibling;
          if (placeholder && src) {
            if (window.cc.isAccepted(name)) {
              iframe.setAttribute('src', src);
              iframe.removeAttribute('hidden');
              placeholder.setAttribute('hidden', true);
            } else {
              iframe.setAttribute('src', '');
              iframe.setAttribute('hidden', true);
              placeholder.removeAttribute('hidden');
            }
          }
        });
      });
    });
  };

  $(document).ready(function() {
    if ($('body').hasClass('userrole-anonymous')) {
      handleVideoModals();
    } else {
      handleVideoModals();
    }
  });
});
