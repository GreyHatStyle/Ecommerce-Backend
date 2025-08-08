import csv
from typing import List

from django.core.management.base import BaseCommand, CommandParser

from shopping.models import Product
from shopping.utils import ProductRecommendationUtil


class Command(BaseCommand):
    help = "Fill Product table from given CSV file"
    
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to csv file",
        )
        
    def handle(self, *args, **kwargs) -> str | None:
        csv_file = kwargs['csv_file']
        util = ProductRecommendationUtil()
        
        
        if csv_file is None:
            self.stderr.write(self.style.ERROR("Path to csv file not given"))
            return
        
        try:
            products_to_create: List[Product] = []
            
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    cluster = util.predict_cluster_number(row['description'])
                    product = Product(
                        title=row['title'],
                        description=row['description'],
                        price=row['price'],
                        stock=row['stocks'],
                        recommendation_cluster=cluster,
                    )
                    
                    products_to_create.append(product)
                    
            Product.objects.bulk_create(products_to_create)
                
            self.stdout.write(self.style.SUCCESS('Products imported in table Successfully'))
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))