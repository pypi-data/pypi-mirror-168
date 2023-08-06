from django.db import models


class Type4(models.Model):
    """
    <h3>Welcome to <strong>Tempo</strong></h3>
    <h1>We're Creative Agency</h1>
    <h2>We are team of talented designers making websites with Bootstrap</h2>
    <a href="#about" class="btn-get-started scrollto">Get Started</a>
    """
    modal_title = models.CharField('modal_title', default="EVENT", max_length=20, blank=True)
    h3 = models.CharField('h3', max_length=20, help_text="강조 : strong tag")
    h1 = models.CharField('h1', max_length=40)
    h2 = models.TextField('h2', help_text="줄넘기기 : br tag, 강조 : strong tag")
    link_url = models.URLField('link_url', blank=True, help_text="공란 가능")
    link_text = models.CharField('link_text', default="Get Started", max_length=20)
    bg = models.ImageField(upload_to=f'images/popup/type4')
    activate = models.BooleanField(default=False, help_text="활성창 1개만 가능")

    def __str__(self):
        return self.h1


class Type3(models.Model):
    """
    <h2 data-aos="fade-up">Enjoy Your Healthy<br>Delicious Food</h2>
    <p data-aos="fade-up" data-aos-delay="100">Sed autem laudantium dolores. Voluptatem itaque ea consequatur eveniet. Eum quas beatae cumque eum quaerat.</p>
    <div class="d-flex" data-aos="fade-up" data-aos-delay="200">
      <a href="#book-a-table" class="btn-book-a-table">Book a Table</a>
      <a href="https://www.youtube.com/watch?v=LXb3EKWsInQ" class="glightbox btn-watch-video d-flex align-items-center"><i class="bi bi-play-circle"></i><span>Watch Video</span></a>
    </div>
    """
    modal_title = models.CharField('modal_title', default="EVENT", max_length=20, blank=True)
    h2 = models.CharField('h2', max_length=40, help_text="줄넘기기 : br tag")
    p = models.TextField('p', help_text="줄넘기기 : br tag, 강조 : strong tag")
    link_url = models.URLField('link_url', blank=True, help_text="공란 가능")
    link_text = models.CharField('link_text', default="Book a Table", max_length=20)
    link_video_url = models.URLField('link_video_url', blank=True, help_text="공란 가능")
    link_video_text = models.CharField('link_video_text', default="Watch Video", max_length=20)
    img = models.ImageField(upload_to=f'images/popup/type3')
    activate = models.BooleanField(default=False, help_text="활성창 1개만 가능")

    def __str__(self):
        return self.h2


class Type2(models.Model):
    """
    <h2 data-aos="fade-up">Focus On What Matters</h2>
    <blockquote data-aos="fade-up" data-aos-delay="100">
      <p>Lorem ipsum dolor, sit amet consectetur adipisicing elit. Perspiciatis cum recusandae eum laboriosam voluptatem repudiandae odio, vel exercitationem officiis provident minima. </p>
    </blockquote>
    <div class="d-flex" data-aos="fade-up" data-aos-delay="200">
      <a href="#about" class="btn-get-started">Get Started</a>
      <a href="https://www.youtube.com/watch?v=LXb3EKWsInQ" class="glightbox btn-watch-video d-flex align-items-center"><i class="bi bi-play-circle"></i><span>Watch Video</span></a>
    </div>
    """
    modal_title = models.CharField('modal_title', default="EVENT", max_length=20, blank=True)
    h2 = models.CharField('h2', max_length=40)
    p = models.TextField('p', help_text="줄넘기기 : br tag, 강조 : strong tag")
    link_url = models.URLField('link_url', blank=True, help_text="공란 가능")
    link_text = models.CharField('link_text', default="Get Started", max_length=20)
    link_video_url = models.URLField('link_video_url', blank=True, help_text="공란 가능")
    link_video_text = models.CharField('link_video_text', default="Watch Video", max_length=20)
    bg = models.ImageField(upload_to=f'images/popup/type2')
    activate = models.BooleanField(default=False, help_text="활성창 1개만 가능")

    def __str__(self):
        return self.h2


class Type1(models.Model):
    """
    <div class="col-lg-6 text-center">
      <h2 data-aos="fade-down">행사 <span>UpConstruction</span></h2>
      <p data-aos="fade-up">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
      <a data-aos="fade-up" data-aos-delay="200" href="#get-started" class="btn-get-started">Get Started</a>
    </div>
    """
    modal_title = models.CharField('modal_title', default="EVENT", max_length=20, blank=True)
    h2 = models.CharField('h2', max_length=40, help_text="줄넘기기 : br tag, 강조 : span tag")
    p = models.TextField('p', help_text="줄넘기기 : br tag")
    link_url = models.URLField('link_url', blank=True, help_text="공란 가능")
    link_text = models.CharField('link_text', default="Get Started", max_length=20)
    bg = models.ImageField(upload_to=f'images/popup/type1')
    bg2 = models.ImageField(blank=True, upload_to=f'images/popup/type1')
    bg3 = models.ImageField(blank=True, upload_to=f'images/popup/type1')
    activate = models.BooleanField(default=False, help_text="활성창 1개만 가능")

    def __str__(self):
        return self.h2