
from django.core.management.base import BaseCommand
from pymongo import MongoClient
import os

class Command(BaseCommand):
    help = 'Set up MongoDB indexes'

    def handle(self, *args, **options):
        client = MongoClient(os.getenv('MONGODB_HOST', 'mongodb://localhost:27017'))
        db = client[os.getenv('MONGODB_NAME', 'leetcode_clone')]
        
        # Create indexes
        db.problems_problem.create_index([("title", 1)])
        db.problems_problem.create_index([("difficulty", 1)])
        db.submissions_submission.create_index([("user_id", 1)])
        db.submissions_submission.create_index([("problem_id", 1)])
        db.submissions_submission.create_index([("submitted_at", -1)])
        
        self.stdout.write(
            self.style.SUCCESS('Indexes created successfully!')
        )