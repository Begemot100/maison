function galleryModal() {
  return {
    showModal: false,
    selectedImages: [],
    selectedCategoryName: '',
    galleryData: {
      'Manicure': [
        'images_webp/portfolio_webp/man.webp',
        'images_webp/portfolio_webp/man1.webp',
        'images_webp/portfolio_webp/man2.webp',
        'images_webp/portfolio_webp/man3.webp',
        'images_webp/portfolio_webp/man4.webp',
        'images_webp/portfolio_webp/man5.webp',


      ],
      'Pedicure': [
        'images_webp/portfolio_webp/manped.webp',
        'images_webp/portfolio_webp/manped1.webp',
        'images_webp/portfolio_webp/ped.webp',



      ],
      'Lashes': [
         'images_webp/portfolio_webp/brow.webp',
        'images_webp/portfolio_webp/brow1.webp',
        'images_webp/portfolio_webp/brow2.webp',
        'images_webp/portfolio_webp/brow3.webp',




      ],
      'Hair': [
        'images/portfolio/haircover.JPG',
        'images/portfolio/hair1.png',
        'images/portfolio/hair2.JPG',
        'images/portfolio/hair3.JPG',
         'images/portfolio/hair4.JPG',



      ],
      'Brows': [
        'images/portfolio/b.JPG',
        'images/portfolio/b1.JPG',
        'images/portfolio/b2.JPG',


      ],

      'Clients': [
        'images/portfolio/cli/cli.JPG',
        'images/portfolio/cli/cli1.JPG',
        'images/portfolio/cli/cli2.JPG',
        'images/portfolio/cli/cli3.JPG',
      ],

      'Endosphera': [
        'images/endo/endos1.jpg',
        'images/endo/endos2.jpg',
        'images/endo/endos3.jpg',
        'images/endo/endos4.jpg',

      ],
    },
    openCategory(name) {
      this.selectedCategoryName = name;
      this.selectedImages = this.galleryData[name] || [];
      this.showModal = true;
    }
  };
}

