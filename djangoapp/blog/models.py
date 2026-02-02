from django.db import models
from utils.rands import slugify_new


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=30)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=30,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = "Categorias"

    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=50,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True,
        default="",
        null=False,
        blank=True,
        max_length=255,
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Marque esse campo para que a página '
            'seja exibida publicamente.'
            ),
        )
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
