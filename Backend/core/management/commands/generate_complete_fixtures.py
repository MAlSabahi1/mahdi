"""
Management command to generate complete fixtures for Phase 1
"""
import json
from datetime import datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate complete fixtures for all lookup tables'

    def handle(self, *args, **options):
        self.stdout.write('Generating complete fixtures...')
        
        # Generate Job Titles (100+)
        self.generate_job_titles()
        
        # Generate Positions
        self.generate_positions()
        
        self.stdout.write(self.style.SUCCESS('Successfully generated all fixtures'))

    def generate_job_titles(self):
        """Generate all 100+ job titles"""
        
        # Category IDs: 1=إداري, 2=ميداني, 3=فني, 4=تخصصي, 5=حرفي
        
        job_titles = [
            # إداري (25)
            (1, 1, "إداري"),
            (2, 1, "كاتب"),
            (3, 1, "مؤرشف"),
            (4, 1, "أمين صندوق"),
            (5, 1, "خطاط"),
            (6, 1, "مغلف"),
            (7, 1, "مراسل"),
            (8, 1, "تسجيل جنائي"),
            (9, 1, "محاسب"),
            (10, 1, "مراجع"),
            (11, 1, "جامع بيانات شخصية"),
            (12, 1, "قيم جامع"),
            (13, 1, "موثق"),
            (14, 1, "مستلم بلاغات"),
            (15, 1, "معلم"),
            (16, 1, "مرشد توعوي"),
            (17, 1, "صحفي"),
            (18, 1, "مذيع"),
            (19, 1, "رئيس وحدة"),
            (20, 1, "إحصاء بيانات"),
            (21, 1, "مترجم"),
            (22, 1, "مدير مكتب"),
            