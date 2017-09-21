from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from transliterate import translit, get_available_language_codes


class UserProfile(models.Model):
    user = models.OneToOneField(User)


class PostCategory(models.Model):
    category_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    # slug = models.SlugField(verbose_name="перевод", null=True)

    def __str__(self):
        return "%s" % self.category_name

    class Meta:
        verbose_name = 'Категория статьи'
        verbose_name_plural = 'Категории статей'


class Post(models.Model):
    author = models.ForeignKey(User, related_name='poster')
    category = models.ForeignKey(PostCategory, null=True, blank=True, default=None)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    views = models.IntegerField(default=0, verbose_name="Просмотры")
    likes = models.IntegerField(default=0, verbose_name="Понравилось")
    dislikes = models.IntegerField(default=0, verbose_name="Не понравилось")
    
    likedone = models.ManyToManyField(User, blank=True, related_name='userlikes')

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ["-created_date", "-updated_date"]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

class Comment(models.Model):
    commentator = models.ForeignKey(User, blank=True, related_name='commentator')
    text = models.TextField(verbose_name="Оставьте Ваш комментарий")
    post = models.ForeignKey(Post, blank=True, null=True, default=None)


    created_date = models.DateTimeField(default=timezone.now)
    # published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text


def create_slug(instance, new_slug=None):
    slug = slugify(translit(instance.title, 'ru' ,reversed=True))
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)









