from django.db import models

# Create your models here.
from django.utils.html import format_html


class Proxy(models.Model):
    """
        可用代理ip信息
        """
    PROTOCOL = (
        (-1, '未验证'),
        (0, '未知'),
        (1, 'http'),
        (2, 'https'),
        (3, 'http + https')
    )
    ANONYMITYS = (
        (-1, '未验证'),
        (0, '未知'),
        (1, '高匿'),
        (2, '普匿'),
        (3, '透明')
    )
    HTTP=(
        (-1, '未验证'),
        (0, '不支持'),
        (1, '支持')
    )
    protocol = models.SmallIntegerField(choices=PROTOCOL, default=-1, verbose_name='代理类型')
    anonymity = models.SmallIntegerField(choices=ANONYMITYS, default=-1, verbose_name='匿名程度')
    ip = models.CharField(max_length=16, null=True, unique=True, verbose_name='ip')
    port = models.CharField(max_length=12, null=True, verbose_name='端口号')

    http = models.SmallIntegerField(default=-1, choices=HTTP, verbose_name="HTTP")
    https = models.SmallIntegerField(default=-1, choices=HTTP, verbose_name="HTTPS")

    speed = models.CharField(max_length=12, null=True, verbose_name='响应速度')
    area = models.CharField(max_length=64, null=True, verbose_name='ip地址')
    verify_time = models.DateTimeField(default=None, null=True, verbose_name='最后验证时间')
    source = models.CharField(max_length=35, null=True, verbose_name='来源')

    class Meta:
        verbose_name = "代理"
        verbose_name_plural = verbose_name


    def html_http(self):
        colors = ["#999966", "#CC3333", "#009966"]
        # print(self.http)
        ret = '<font color="{}">{}</font>'.format(colors[self.http+1], self.HTTP[self.http+1][1])
        return format_html(ret)
    def html_https(self):
        colors = ["#999966", "#CC3333", "#009966"]
        # print(self.https)
        ret = '<font color="{}">{}</font>'.format(colors[self.https+1], self.HTTP[self.https+1][1])
        return format_html(ret)
    def html_anonymity(self):
        colors = ["#999966", "#999966", "#009966", "#339933", "#99CC00"]
        # print(self.anonymity)
        ret = '<font color="{}">{}</font>'.format(colors[self.anonymity+1], self.ANONYMITYS[self.anonymity+1][1])
        return format_html(ret)
    def html_speed(self):
        # 绿到浅
        colors = ["#339933", "#99CC33", "#CC3333",]
        # print(self.anonymity)
        color = ""
        speed = None
        if self.speed!=None:
            speed = float(self.speed)
            if speed<1:
                color = colors[0]
            elif speed<3.6:
                color = colors[1]
            else:
                color = colors[2]
        else:
            color = ""
            speed = "-"
        ret = '<font color="{}">{}</font>'.format(color, speed)
        return format_html(ret)
    html_http.short_description= "HTTP"
    html_https.short_description= "HTTPS"
    html_anonymity.short_description= "匿名性"
    html_speed.short_description= "速度"