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
        objekte = [
            Supplier(
                supplier_id=row['Verkäufer-ID'], 
                willingness_to_pay=row['ZB_S'],
                preference=row['Präferenz'],
            )
            for _, row in df_suppliers.iterrows()
        ]
        Supplier.objects.bulk_create(objekte, batch_size=200)
        self.stdout.write(self.style.SUCCESS(f'{len(objekte)} Verkäufer wurden importiert!'))

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
        Buyer.objects.bulk_create(buyer_objs, batch_size=200)
        self.stdout.write(self.style.SUCCESS(f'{len(buyer_objs)} Käufer wurden importiert!'))