
from django.core.management.base import BaseCommand
from django.db import connection
from pymongo import MongoClient
import os

class Command(BaseCommand):
    help = 'Test MongoDB connection'

    def handle(self, *args, **options):
        try:
            # Test Django connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(
                self.style.SUCCESS('Django-MongoDB connection successful!')
            )
            
            # Test direct PyMongo connection
            client = MongoClient(os.getenv('MONGODB_HOST', 'mongodb://localhost:27017'))
            db = client[os.getenv('MONGODB_NAME', 'leetcode_clone')]
            
            # Test write operation
            test_collection = db.test_connection
            test_collection.insert_one({"test": "connection"})
            test_collection.delete_one({"test": "connection"})
            
            self.stdout.write(
                self.style.SUCCESS('Direct PyMongo connection successful!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'MongoDB connection failed: {str(e)}')
            )