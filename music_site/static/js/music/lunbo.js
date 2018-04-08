var sliderData = [
        {
          title: '晴れ 时どき 雪',
          pic: '{{ img }}',
          url: './music/709386.html'
        },
        {
          title: 'Flower Dance',
          pic: 'http://img.zcool.cn/community/0109575540b83d0000017c946b5535.jpg',
          url: './music/406238.html'
        },
        {
          title: 'A Little Story - Valentin',
          pic: 'http://ww2.sinaimg.cn/large/67d25024gw1fb5h1swze9j20gq0b6acf.jpg',
          url: './music/857896.html'
        },
        {
          title: '桜花抄 - 天門',
          pic: 'http://ww4.sinaimg.cn/mw690/67d25024gw1fb5hbjl32jj21hc0u01dz.jpg',
          url: './music/528283.html'
        }
      ];

  $(function () {
    HBSlider.setConfig({
      autoPlay: true,
      delay: 5
    });
    HBSlider.setItems(sliderData);
    HBSlider.init();
    HBSlider.play();
  });