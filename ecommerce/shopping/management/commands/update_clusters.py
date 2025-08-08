from typing import Any

from django.core.management.base import BaseCommand

from shopping.models import Product
from shopping.utils import ProductRecommendationUtil


class Command(BaseCommand):
    
    help = "Update cluster values for existing products"
    
    def handle(self, *args: Any,**kwargs: Any) -> str | None:
        
        util = ProductRecommendationUtil()
        products = Product.objects.filter(recommendation_cluster__isnull = True)
        success_count = 0
        product_count = products.count()
        
        
        for product in products:
            id = product.id
            try:
                if product.description:
                    product.recommendation_cluster = util.predict_cluster_number(product.description)
                    product.save()
                    success_count += 1
                    
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error saving id:[{id}] product\nMessage:{e}"))
                

        if product_count != success_count:
            self.stderr.write(self.style.ERROR(f"Successful saves: {success_count} out of {product_count}"))
            return
        
        self.stdout.write(self.style.SUCCESS(f"Successfully saved {success_count} clusters!!"))
            