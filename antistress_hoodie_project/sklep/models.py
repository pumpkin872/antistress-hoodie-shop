from django.db import models

from django.db import models

# Lista wyboru popularnych kolorów
COLORS = (
    ('BLK', 'Black'),
    ('GRY', 'Gray'),
    ('NVY', 'Navy'),
    ('WHT', 'White'),
    ('AUT', 'Warm autumn beige'),
)

SIZES = (
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Category")
    slug = models.SlugField(unique=True, help_text="Short description of the cut")
    description = models.TextField(
        blank=True,
        help_text="Krótki opis kategorii, widoczny na stronie kategorii."
    )
    is_active = models.BooleanField(default=True, verbose_name="Czy aktywna w sklepie")

    class Meta:
        verbose_name_plural = "Kategorie"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Model reprezentujący podstawowy produkt (Antistress Hoodie)."""
    name = models.CharField(max_length=100, verbose_name="Nazwa Produktu")
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Kategoria"
    )
    description = models.TextField(help_text="Pełny opis produktu i jego 'antystresowych' cech.")
    material = models.CharField(
        max_length=50,
        default="Bawełna organiczna",
        help_text="Główny materiał wykonania bluzy."
    )
    base_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Podstawowa cena sugerowana (warianty mogą mieć inną)."
    )
    is_featured = models.BooleanField(default=False, verbose_name="Wyróżniony na stronie głównej")
    
    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """Model reprezentujący konkretny wariant produktu (np. L, Czarny)."""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name="Produkt Matka"
    )
    color = models.CharField(max_length=3, choices=COLORS, default='BLK', verbose_name="Kolor")
    size = models.CharField(max_length=3, choices=SIZES, default='M', verbose_name="Rozmiar")
    sku = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unikalny kod magazynowy (Stock Keeping Unit)."
    )
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Stan Magazynowy")
    price_override = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Jeśli puste, używa ceny podstawowej produktu."
    )

    class Meta:
        unique_together = ('product', 'color', 'size')
        verbose_name = "Wariant Produktu"
        verbose_name_plural = "Warianty Produktu"

    def get_price(self):
        """Zwraca rzeczywistą cenę wariantu."""
        return self.price_override if self.price_override is not None else self.product.base_price

    def __str__(self):
        color_display = dict(COLORS).get(self.color)
        size_display = dict(SIZES).get(self.size)
        return f"{self.product.name} - {size_display}, {color_display}"