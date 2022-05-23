import sys

import exifread
import os
from geopy.geocoders import Nominatim
import requests
import json
import fake_useragent
ua = fake_useragent.UserAgent()

html_head = """
<!DOCTYPE html>

<html class="no-js"  lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no">
<link rel="shortcut icon" href="images/bitbug_favicon.ico" type="image/x-icon">
<title>:: 逍遥 & 月月子 :: Personal photo album</title>
<embed autostart="true" loop="-1" controls="ControlPanel" width="0" height="0" src="music/pinfan.mp3">
<!-- Normalize -->

<link rel="stylesheet" href="css/assets/normalize.css" type="text/css">

<!-- Bootstrap -->

<link href="css/assets/bootstrap.min.css" rel="stylesheet" type="text/css">

<!-- Font-awesome.min -->

<link href="css/font-awesome.min.css" rel="stylesheet" type="text/css">

<!-- Effet -->

<link rel="stylesheet" href="css/gallery/foundation.min.css"  type="text/css">
<link rel="stylesheet" type="text/css" href="css/gallery/set1.css" />

<!-- Main Style -->

<link rel="stylesheet" href="css/main.css" type="text/css">

<!-- Responsive Style -->

<link href="css/responsive.css" rel="stylesheet" type="text/css">

<!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->

<!--[if lt IE 9]>

      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>

      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>

    <![endif]-->

<script src="js/assets/modernizr-2.8.3.min.js" type="text/javascript"></script>
</head>

<body>

<!-- header -->

<header id="header" class="header">
  <div class="container-fluid">
    <hgroup> 
      
      <!-- logo -->
      
      <h1> <a href="index.html" title="逍遥 & 月月子">逍遥 & 月月子</a> </h1>
      
      <!-- logo --> 
      
      <!-- nav -->
      
      <nav>
        <div class="menu-expanded">
          <div class="nav-icon">
            <div id="menu" class="menu"></div>
            <p>menu</p>
          </div>
          <div class="cross"> <span class="linee linea1"></span> <span class="linee linea2"></span> <span class="linee linea3"></span> </div>
          <div class="main-menu">
            <ul>
              <li class="active"><a href="index.html">Home</a></li>
              <li><a>Waiting for me</a></li>
              <li><a>Waiting for me</a></li>
              <li><a>Waiting for me</a></li>
            </ul>
          </div>
        </div>
      </nav>
      
      <!-- nav --> 
      
    </hgroup>
  </div>
</header>

<!-- header -->
<div class="copyrights">Collect from <a href="#" >Xiaoyao & Yueyue の Life </a></div>

<main class="main-wrapper" id="container"> 
  
  <!-- image Gallery -->
  
  <div class="wrapper">
    <div class="">
      <ul class="small-block-grid-2 medium-block-grid-3 large-block-grid-3 masonry">
"""
html_footer = """
</ul>
    </div>
  </div>
</main>

<!-- Image Gallery --> 

<!-- footer -->

<footer class="footer">
  <h3>Stay connected with me</h3>
  <div class="container footer-bot">
    <div class="row"> 
      
      <!-- logo -->
      
      <div class="col-xs-12 col-sm-6 col-md-3 col-lg-3"> <img  alt="Picxa" title="Picxa"/>
        <p class="copy-right">&copy; Reserved 逍遥 & 月月子 2020.</p>
      </div>
      
     
      
      <!-- social -->
      
      <div class="col-xs-12 col-sm-6 col-md-3 col-lg-3 padding-top">
        <ul class="social">
          <li><a href="#"><i class="fa fa-wechat" aria-hidden="true"></i></a></li>
          <li><a href="#"><i class="fa fa-qq" aria-hidden="true"></i></a></li>
          <li><a href="#"><i class="fa fa-weibo" aria-hidden="true"></i></a></li>
          <li><a href="#"><i class="fa fa-github" aria-hidden="true"></i></a></li>
          <li><a href="#"><i class="fa fa-twitter" aria-hidden="true"></i></a></li>
          <li><a href="#"><i class="fa fa-facebook" aria-hidden="true"></i></a></li>
        </ul>
        
        <p> 
      </div>
      
      <!-- social --> 
      
    </div>
  </div>
</footer>

<!-- footer --> 

<!-- jQuery --> 

<script src="js/jquery.min.js"></script> 
<script>window.jQuery || document.write('<script src="js/assets/jquery.min.js"><\/script>')</script> 
<script src="js/assets/plugins.js" type="text/javascript"></script> 
<script src="js/assets/bootstrap.min.js" type="text/javascript"></script> 

<script src="js/maps.js" type="text/javascript"></script> 
<script src="js/custom.js" type="text/javascript"></script> 
<script src="js/jquery.contact.js" type="text/javascript"></script> 
<script src="js/main.js" type="text/javascript"></script> 
<script src="js/gallery/masonry.pkgd.min.js" type="text/javascript"></script> 
<script src="js/gallery/imagesloaded.pkgd.min.js" type="text/javascript"></script> 
<script src="js/gallery/jquery.infinitescroll.min.js" type="text/javascript"></script> 
<script src="js/gallery/main.js" type="text/javascript"></script> 
<script src="js/jquery.nicescroll.min.js" type="text/javascript"></script>
</body>
</html>
"""


def format_lati_long(data):  # list2float
    list_tmp = str(data).replace('[', '').replace(']', '').split(',')
    # print(list_tmp)
    l = [ele.strip() for ele in list_tmp]
    if int(l[-1].split('/')[1]) == 0:
        return 0

    data_sec = int(l[-1].split('/')[0]) / (int(l[-1].split('/')[1]) * 3600)  # 秒的值
    data_minute = int(l[1]) / 60
    data_degree = int(l[0])
    result = data_degree + data_minute + data_sec
    # print(result)
    # result = round(data_degree + data_minute + data_sec,6)
    return result


all_path = ['pic/' + x for x in os.listdir('./pic')]
info_list = []
count = 0


def getINfo(path):
    if not path.endswith(".jpg"):
        return
    img = exifread.process_file(open(path, 'rb'))

    name = path[path.find("/")+1:path.find(".")]
    if name.find("-") > 1:
        name = name[0:name.find("-")]

    # try:
    #     time = str(img['Image DateTime']).split(' ')[0].replace(':', '.')
    # except (KeyError, IndexError, TypeError):
    #     time = ''
    time = "{0}.{1}.{2}".format(name[0:4], name[4:6], name[6:])

    # info_list.append([path, time, "", name])
    print(name)
    global count
    count += 1
    # return

    # print('拍摄时间',time)
    try:
        latitude = format_lati_long(str(img['GPS GPSLatitude']))
        # print(latitude)
        lat_direction = img['GPS GPSLatitudeRef']

        longitude = format_lati_long(str(img['GPS GPSLongitude']))
        # print(longitude)
        long_direction = img['GPS GPSLongitudeRef']

        # #geopy get position:
        # geolocator = Nominatim(user_agent='demo_of_gnss_help')
        # position0 = geolocator.reverse('%s,%s'%(latitude,longitude))#字符格式才显示中国
        # print(position0.address.split(',')[-1][3:])
        # 高德
        api_key = 'f84cbb2dc078c087c6dc37b6ae74ab85'
        url_get_position = 'https://restapi.amap.com/v3/geocode/regeo?output=JSON&location={}&key={}&radius=1000&extensions=base'
        resp = requests.get(url_get_position.format(f'{longitude},{latitude}', api_key))
        location_data = json.loads(resp.text)
        address = location_data.get('regeocode').get('formatted_address')
    except (KeyError, IndexError, TypeError):
        address = ''
    # print('拍摄地点：',address)
    info_list.append([path, time, address, name])


if __name__ == '__main__':
    for each in all_path:
        getINfo(each)
    print(count)
    print(info_list)
    info_list.sort(key=lambda x: int(x[3]), reverse=True)
    # print(info_list)
    # sys.exit(0)
    html_list = []
    for each in info_list:
        s = requests.session()
        # s.headers = {"User-Agent": ua.random}
        s.headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Cookie': '__vtins__JLvourAu9qIUtWYT=%7B%22sid%22%3A%20%22d808d1eb-cd4d-5525-9c23-a4b84bfee362%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201653299238015%2C%20%22ct%22%3A%201653297438015%7D; __51uvsct__JLvourAu9qIUtWYT=1; __51vcke__JLvourAu9qIUtWYT=50a79f61-7a17-5226-95a2-c8650d36005d; __51vuft__JLvourAu9qIUtWYT=1653297438019; wzws_cid=d80c633fb63f2e390ef11c3eaebe8802109fab5a368c645d4c2e60b6e4fa06eb5634c9acb16e25b979bd9ce6619dcbd6707c249dc1effb90d6c2cfecb2f1f2753d3c0a8629ffaecca1aaf907636f4263', 'Host': 'api.vvhan.com', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"'}
        s.headers['User-Agent'] = ua.random
        # url = "https://api.ghser.com/qinghua/?type=json"
        url = "https://api.vvhan.com/api/love?type=json"
        r = s.get(url)
        qinghua = r.json()['ishan']
        # qinghua = requests.get('https://api.ghser.com/qinghua?type=json', timeout=10).json()["ishan"]
        html_str = """     
        <li class="masonry-item grid">
            <figure class="effect-sarah"> <img src="{0}" alt="" />
                <figcaption>
                <h2>摄于 <span>{1}</span></h2>
                <p>{2}</p>
                <p class="description">{3}</p>
            </figure>
            </li>   
        """.format(each[0], each[1], each[2], qinghua)
        html_list.append(html_str)
        print(f'{each[0]} finished!')
    # print()        
    with open('index.html', 'w') as f:
        f.write(html_head + ' '.join(html_list).replace('\n', '') + html_footer)
