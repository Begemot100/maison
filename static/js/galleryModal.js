function galleryModal() {
  return {
    showModal: false,
    selectedImages: [],
    selectedCategoryName: '',
    lastTap: 0,
    tapTimeout: null,
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
//    init() {
//      console.log('galleryModal initialized');
//      console.log('galleryData:', this.galleryData);
//      if (!this.galleryData || Object.keys(this.galleryData).length === 0) {
//        console.error('galleryData is empty or undefined');
//      }
//    },
    openCategory(name) {
        this.selectedCategoryName = name;
        this.selectedImages = this.galleryData[name] || [];
        this.showModal = true;
      },

//      openFullImage(imgPath) {
//        window.open(`/static/${imgPath}`, '_blank');
//      },

      closeModal() {
        this.showModal = false;
      },
    handleDoubleTap() {
        const now = Date.now();
        const interval = 300; // мс
        if (now - this.lastTap < interval) {
          clearTimeout(this.tapTimeout);
          this.closeModal();
        } else {
          // сбросим lastTap через interval, если второго тапа не было
          this.tapTimeout = setTimeout(() => {
            this.lastTap = 0;
          }, interval);
        }
        this.lastTap = now;
      },
    };
  }

//  -