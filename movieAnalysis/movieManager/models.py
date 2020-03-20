from django.db import models

# Create your models here.

class Identity(models.Model):
    name = models.CharField(max_length=10, unique=True)
    class Meta:
        verbose_name = '身份'
        verbose_name_plural = verbose_name

class Category(models.Model):
    name = models.CharField(max_length=10, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name

class Person(models.Model):
    GENDER_CHOICE = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    user_id = models.CharField(max_length=15, unique=True, null=False, blank=False)
    name = models.CharField(max_length=40, verbose_name='名字')
    image = models.ImageField(upload_to='uploadtemp', default='person/default.png')
    foreign_name = models.CharField(max_length=40, verbose_name='国外名')
    birth_place = models.CharField(max_length=45, null=True, blank=True, verbose_name='出身地')
    gender = models.SmallIntegerField(choices=GENDER_CHOICE, default=0, verbose_name='性别')
    # 1 男 2 女 0未知
    national = models.CharField(max_length=15, null=True, blank=True, verbose_name='名族')
    nationality = models.CharField(max_length=15, null=True, blank=True, verbose_name='国籍')
    identity = models.ManyToManyField(Identity, related_name="person")
    introduce = models.TextField(null=True, blank=True, verbose_name='介绍')
    def __str__(self):
        return self.name
    class Meta:
        # abstract=True
        verbose_name = "人物"
        verbose_name_plural = verbose_name



class Awards(models.Model):
    awards_name = models.CharField(max_length=100)
    prize = models.CharField(max_length=540, null=True, blank=True)
    nominate = models.CharField(max_length=540, null=True, blank=True)
    class Meta:
        verbose_name = '奖项'
        verbose_name_plural = verbose_name



class Movie(models.Model):
    movie_id = models.IntegerField(unique=True, null=False, blank=False)
    movie_name = models.CharField(max_length=24)
    image = models.ImageField(upload_to='uploadtemp', default='movie/default.png')
    category = models.ManyToManyField(Category, related_name="ccategory_movie")
    actor = models.ManyToManyField(Person, related_name="actor_movie")
    lead_director = models.ManyToManyField(Person, related_name="lead_director_movie")
    vice_director = models.ManyToManyField(Person, related_name="vice_director_movie")
    awards = models.ManyToManyField(Awards, related_name="awards_movie")
    score = models.FloatField(default=0.0)
    introduce = models.TextField(null=True, blank=True)
    release_time = models.DateField()
    release_area = models.CharField(max_length=15, null=True, blank=True, default="")
    def __str__(self):
        return self.movie_name

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = verbose_name



class Viewer(models.Model):
    user_id = models.CharField(max_length=20, unique=True,)
    user_level = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=18, null=True, blank=True)
    gender = models.SmallIntegerField(default=0,)  # 1 男 2 女 0未知
    vipInfo = models.CharField(max_length=19, default="")
    vipType = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.user_id
    class Meta:
        verbose_name = "评论者"
        verbose_name_plural = verbose_name



class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_comment')
    comment_id = models.CharField(max_length=20, unique=True,)
    start_time = models.DateTimeField()
    content = models.TextField()
    score = models.FloatField()
    viewer = models.ForeignKey(Viewer, on_delete=models.CASCADE, related_name='viewer_comment')
    def __str__(self):
        return self.comment_id
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name