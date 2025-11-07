from django.db import models


COLORS = (
    ('BLK', 'Black'),
    ('GRY', 'Gray'),
    ('NVY', 'Navy'),
    ('WHT', 'White'),
    ('PNK', 'Pink'),
)

SIZES = (
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
)

STYLES = (
    ('F', 'Female'),
    ('U', 'Unisex'),
)

GENDERS = models.IntegerChoices(
    'Gender',
    'Female Male Other'
)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Category")
    description = models.TextField(
        blank=True,
        help_text="Short category description, visible on the category page"
    )
    is_active = models.BooleanField(default=True, verbose_name="Visible in the shop?")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product name")
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Category"
    )
    description = models.TextField(help_text="Complete product description")
    material = models.CharField(
        max_length=50,
        default="Organic cotton",
        help_text="Main product material/fabric"
    )
    base_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Base price"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Featured on the main page?")
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name="Product parent"
    )
    color = models.CharField(max_length=3, choices=COLORS, default='BLK', verbose_name="Color")
    size = models.CharField(max_length=3, choices=SIZES, default='M', verbose_name="Size")
    style = models.CharField(max_length=3, choices=STYLES, default='U', verbose_name="Style/cut")
    sku = models.CharField(
        max_length=20,
        unique=True,
        help_text="Catalogue number (SKU)"
    )
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Stock quantity")
    price_override = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="If empty, uses base price"
    )

    class Meta:
        unique_together = ('product', 'color', 'size', 'style')
        verbose_name = "Product variant"
        verbose_name_plural = "Product variants"

    def get_price(self):
        return self.price_override if self.price_override is not None else self.product.base_price

    def __str__(self):
        color_display = dict(COLORS).get(self.color)
        size_display = dict(SIZES).get(self.size)
        style_display = dict(STYLES).get(self.style)
        return f"{self.product.name} - {size_display}, {color_display}, {style_display}"
    

class Position(models.Model):  
    name = models.CharField(max_length=70, blank=False, null=False)
    description = models.TextField(blank = False, null = True)

    def  __str__(self):
        return f"{self.name}"

class Person(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    surname =  models.CharField(max_length=100, blank=False, null=False)
    gender = models.IntegerField(choices=GENDERS.choices, default=GENDERS.Female)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ['surname']

    def __str__(self):
        return f"{self.name} {self.surname}"

