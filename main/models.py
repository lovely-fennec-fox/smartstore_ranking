from django.db import models


class Product(models.Model) :
    name = models.CharField('상품이름', max_length=256, null=False, unique=True )
    address = models.CharField('상품주소', max_length=256, null=False, default='-')
    num = models.CharField('상품번호', max_length=30, null=False, default='-')

    def __str__(self):
        return f'{self.name}'


class Keyword(models.Model):
    name = models.CharField('키워드', max_length=30)
    number = models.PositiveSmallIntegerField('번호', null=False, default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='keywords', null=False)

    class Meta:
        unique_together = [('product', 'number')]

    def __str__(self):
        return f'{self.name}'


class Rank(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name='rank', null=False)
    date_searched = models.DateTimeField(auto_now_add=True)
    rank = models.CharField('랭킹', max_length=5)

    def __str__(self):
        return f'{self.rank}.{self.keyword.name}/{self.product.name}'
