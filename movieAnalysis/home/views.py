import json

from django.db import connection
from django.shortcuts import render,HttpResponse
from django.template.defaulttags import register
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from movieManager.models import Movie


def index(request):
    return render(request, 'home/index.html')

def movieList(request):
    movie_count = Movie.objects.count()
    size = 15
    ret_content = {
        "m_count": movie_count,
        "page_size": size
    }
    return render(request, 'home/movieList.html', context=ret_content)


def scoreContrast(request):
    return render(request, "home/scoreContrast.html")
































data = '''

port: 7890
socks-port: 7891
redir-port: 7892
allow-lan: false
mode: Rule
log-level: info
external-controller: 127.0.0.1:9090
secret: ""
cfw-bypass:
  - localhost
  - 127.*
  - 10.*
  - 172.16.*
  - 172.17.*
  - 172.18.*
  - 172.19.*
  - 172.20.*
  - 172.21.*
  - 172.22.*
  - 172.23.*
  - 172.24.*
  - 172.25.*
  - 172.26.*
  - 172.27.*
  - 172.28.*
  - 172.29.*
  - 172.30.*
  - 172.31.*
  - 192.168.*
  - <local>
cfw-latency-timeout: 3000
cfw-latency-url: http://www.gstatic.com/generate_204
cfw-conn-break-strategy:
  proxy: none
  profile: true
  mode: false
cfw-child-process: []
Proxy:
  - name: galan
    type: vmess
    server: galan.1690036618.site
    port: "443"
    uuid: 773bf377-a039-4ba7-8729-1d3222e982aa
    alterId: "233"
    cipher: auto
    tls: true
    skip-cert-verify: true
    network: ws
    ws-path: /spider
Proxy Group:
  - name: Proxies
    proxies:
      - galan
    type: select
Rule:
  - MATCH,Proxies


'''

@register.filter
def get_range(value):
    return range(value)



@csrf_exempt
def mapJson(request):
    return HttpResponse(open("static/map/js/china.js", encoding='utf-8'), content_type="application/json")

def myCustomSQL(sql):
    row = None
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()
    return row
@csrf_exempt
def getMapData(request,mothod, movie_id):
    print(mothod, movie_id)
    if mothod=="map":
        sql = 'select v.city, v.dx, l.longitude, l.latitude from pluging_location as l, ' \
              '(select v.city, count(*) as dx from moviemanager_viewer as v, ' \
              '(select * from moviemanager_comment where movie_id=77) as c where c.viewer_id=v.id group by city) as v ' \
              'where v.city=l.name;'
        rs = myCustomSQL(sql=sql)
        ret = {}
        data = []
        for r in rs:
            data.append({
                "name": r[0],
                "value": [r[2], r[3], r[1]]
            })
        ret["data"] = data
        return HttpResponse(json.dumps(ret), content_type="application/json")
    elif mothod=="mapdis":
        sql =  'select l.province, sum(v.dx) as dx from pluging_location as l,'\
               '(select v.city, count(*) as dx from moviemanager_viewer as v,'\
               '(select * from moviemanager_comment where movie_id=2) as c where '\
               'c.viewer_id=v.id group by city) as v where v.city=l.name ' \
               'group by l.province order by dx DESC;'
        rs = myCustomSQL(sql)
        data_name = []
        data_value = []
        for r in rs:
            print(r)
            data_name.append(r[0])
            data_value.append(int(r[1]))
        ret = {
            "name": data_name,
            "value": data_value
        }
        print(ret)
        return HttpResponse(json.dumps(ret), content_type="application/json")

    return HttpResponse(json.dumps({
        "data": "参数错误"
    }), content_type="application/json")



def clash(request):
    return HttpResponse(data)


def total(request):
    return render(request, 'home/total.html')


def proxy(request):
    print(request)
    print(request.headers)
    return HttpResponse("S")