from rest_framework import serializers # type: ignore
from .models import Category, Product, ProductVariant, Person, Position, COLORS, SIZES, STYLES

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    
    name = serializers.CharField(
        max_length=100, 
        label="Product name"
    )
    
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False,
        label="Category"
    )
    
    description = serializers.CharField(
        style={'base_template': 'textarea.html'},
        help_text="Complete product description"
    )
    
    material = serializers.CharField(
        max_length=50,
        default="Organic cotton",
        help_text="Main product material/fabric",
        required=False
    )
    
    base_price = serializers.DecimalField(
        max_digits=6, 
        decimal_places=2
    )
    
    is_featured = serializers.BooleanField(
        default=False, 
        label="Is featured on the main page?",
        required=False
    )

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.material = validated_data.get('material', instance.material)
        instance.base_price = validated_data.get('base_price', instance.base_price)
        instance.is_featured = validated_data.get('is_featured', instance.is_featured)
        
        instance.save()
        return instance
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active']


class ProductVariantSerializer(serializers.ModelSerializer):
    current_price = serializers.DecimalField(
        source='get_price', 
        max_digits=6, 
        decimal_places=2, 
        read_only=True
    )

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'product', 'color', 'size', 'style', 
            'sku', 'stock_quantity', 'price_override', 'current_price'
        ]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name', 'description']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'surname', 'gender', 'position', 'created']
        read_only_fields = ['id', 'created']

    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Imię może zawierać tylko litery.")
        
        if not value.istitle():
            raise serializers.ValidationError("Imię musi zaczynać się wielką literą, a reszta liter musi być mała (np. 'Anna').")
        
        return value

    def validate_surname(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Nazwisko może zawierać tylko litery.")
        
        if not value.istitle():
            raise serializers.ValidationError("Nazwisko musi zaczynać się wielką literą, a reszta liter musi być mała (np. 'Nowak').")
        
        return value
    
# http://127.0.0.1:8000/persons/?nazwisko=a