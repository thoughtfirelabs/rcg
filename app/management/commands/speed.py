from django.core.management.base import BaseCommand, CommandError
from app.modules.fund_module import fund
import cProfile as profile
import pandas as pd

class Command(BaseCommand):
    help = 'Speed Test for Fund Module'

    def add_arguments(self, parser):
        pass

    def test(self):
        fund_id = 'LGWXBOK7'
        date = '02/08/2017'
        date = pd.to_datetime(date)
        f = fund(fund_id, date)
        f.run()

    def handle(self, *args, **options):
        profile.runctx('self.test()',globals(),locals(),'test.txt')
        import pstats
        p = pstats.Stats('test.txt')
        p.sort_stats('cumulative').print_stats(100)

