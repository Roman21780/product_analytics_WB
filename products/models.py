from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена со скидкой")
    rating = models.FloatField(verbose_name="Рейтинг")
    review_count = models.IntegerField(verbose_name="Количество отзывов")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"