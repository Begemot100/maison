function galleryModal() {
  return {
    showModal: false,
    selectedImages: [],
    selectedCategoryName: '',
    galleryData: {
      'Manicure': [
        'images/portfolio/man.JPG',
        'images/portfolio/man1.jpeg',
        'images/portfolio/man2.PNG',
        'images/portfolio/man3.PNG',
        'images/portfolio/man4.JPG',
        'images/portfolio/man5.JPG',


      ],
      'Pedicure': [
        'images/portfolio/manped.PNG',
        'images/portfolio/manped1.JPG',
        'images/portfolio/ped.JPG',

      ],
      'Lashes': [
        'images/portfolio/brow.JPG',
        'images/portfolio/brow1.JPG',
        'images/portfolio/brow2.JPG',
        'images/portfolio/brow3.JPG',


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

