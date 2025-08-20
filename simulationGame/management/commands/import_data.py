from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from simulationGame.models import Supplier, Buyer

class Command(BaseCommand):
    help = 'Importiert Daten aus der Excel-Datei in Django-Modell'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str)
        parser.add_argument('--sheet1', type=str, default='ZB_Verkäufer2')
        parser.add_argument('--sheet2', type=str, default='ZB_Käufer2')

    def handle(self, *args, **options):
        df_suppliers = pd.read_excel(options['excel_file'], sheet_name='ZB_Verkäufer2')
        supplier_objs = [
            Supplier(
                supplier_id=row['Verkäufer-ID'], 
                willingness_to_pay=row['ZB_S'],
                preference=row['Präferenz'],
            )
            for _, row in df_suppliers.iterrows()
        ]
        Supplier.objects.all().delete()
        Supplier.objects.bulk_create(supplier_objs, batch_size=200)
        self.stdout.write(self.style.SUCCESS(f'{len(supplier_objs)} Verkäufer wurden importiert!'))

        df_buyers = pd.read_excel(options['excel_file'], sheet_name='ZB_Käufer2')
        buyer_objs = [
            Buyer(
                buyer_id=row['Käufer-ID'], 
                willingness_to_pay=row['ZB_B'],
                preference=row['Preference'],
                out_door_pf=row['Outdoor'],
                in_door_pf=row['Indoor'],
            )
            for _, row in df_buyers.iterrows()
        ]
        Buyer.objects.all().delete()
        Buyer.objects.bulk_create(buyer_objs, batch_size=200)
        self.stdout.write(self.style.SUCCESS(f'{len(buyer_objs)} Käufer wurden importiert!'))