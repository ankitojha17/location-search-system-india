import time
from django.core.management.base import BaseCommand
from service.models.search_log_model import SearchLog
from service.models.location_model import Location
from service.external_location_api import WikipediaAPI
from django.core.cache import cache

class Command(BaseCommand):
    help = 'Always-on background worker for Wikipedia processing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Worker Started: Listening for requests ---"))
        
        while True:  
            pending_tasks = SearchLog.objects.filter(is_processed=False, status='PENDING')

            if not pending_tasks.exists():
            
                time.sleep(0.5)
                continue

            for task in pending_tasks:
                self.stdout.write(f"Scraping Wikipedia for: {task.query}")
                
                wiki_data = WikipediaAPI.fetch_city_data(task.query)

                if wiki_data:
                
                    location, _ = Location.objects.get_or_create(
                        name=wiki_data['name'],
                        defaults={
                            'state': wiki_data['state'],
                            'description': wiki_data['description']
                        }
                    )
                    task.status = 'FOUND'
                    
                    cache_key = f"loc_{task.query.lower().replace(' ', '_')}"
                    cache.set(cache_key, location, 3600)
                    self.stdout.write(self.style.SUCCESS(f"Saved: {wiki_data['name']}"))
                else:
                    task.status = 'NOT_FOUND'
                    self.stdout.write(self.style.WARNING(f"Not found: {task.query}"))
                
                task.is_processed = True
                task.save()

            time.sleep(1)