from django.db import models


AUTH_CHOICES = (
    ('none', 'None'),
    ('api_key', 'API Key'),
    ('other', 'Other'),
)


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class PublicAPI(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='apis'
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='apis'
    )

    auth = models.CharField(
        max_length=30,
        choices=AUTH_CHOICES,
        default='none'
    )
    
    meta_description = models.CharField(max_length=160)


    api_url = models.URLField()
    document_url = models.URLField()

    https_support = models.BooleanField(default=False)
    cors = models.BooleanField(default=False)

    auth_header = models.BooleanField(default=False)
    auth_query_param = models.BooleanField(default=False)
    auth_basic_auth = models.BooleanField(default=False)
    auth_cookie = models.BooleanField(default=False)
    auth_digest = models.BooleanField(default=False)

    is_free = models.BooleanField(default=False)

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('api:detail', kwargs={'slug': self.slug})
