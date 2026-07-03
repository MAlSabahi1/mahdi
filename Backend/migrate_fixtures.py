import os
import django
from django.apps import apps
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

# Models
GeoGovernorate = apps.get_model('core', 'GeoGovernorate')
SecurityAdministration = apps.get_model('core', 'SecurityAdministration')
CentralDepartment = apps.get_model('core', 'CentralDepartment')
JobCategory = apps.get_model('core', 'JobCategory')
JobTitle = apps.get_model('core', 'JobTitle')
Rank = apps.get_model('core', 'Rank')
ServiceStatus = apps.get_model('core', 'ServiceStatus')
Qualification = apps.get_model('core', 'Qualification')
Position = apps.get_model('core', 'Position')
ForceType = apps.get_model('core', 'ForceType')

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'fixtures')

def load_governorates():
    print("Loading Governorates...")
    filepath = os.path.join(FIXTURES_DIR, 'governorates_directorates.json')
    if not os.path.exists(filepath): return

    with open(filepath, 'r', encoding='utf-8') as f:
        for item in json.load(f):
            if item['model'] == 'core.governorate':
                fields = item['fields']
                name = fields.get('name', '')
                region_name = name.replace('إدارة أمن محافظة ', '').replace('إدارة أمن ', '')
                geo, _ = GeoGovernorate.objects.get_or_create(
                    name_ar=region_name,
                    defaults={'name_en': fields.get('code', ''), 'is_active': fields.get('is_active', True)}
                )
                SecurityAdministration.objects.get_or_create(
                    geo_governorate=geo,
                    defaults={'name': name, 'code': fields.get('code', ''), 'is_active': fields.get('is_active', True)}
                )

def load_job_titles():
    print("Loading Job Titles and Categories...")
    cat_filepath = os.path.join(FIXTURES_DIR, 'qualifications_categories.json')
    if os.path.exists(cat_filepath):
        with open(cat_filepath, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                if item['model'] == 'core.jobcategory':
                    JobCategory.objects.get_or_create(id=item['pk'], defaults={'name': item['fields']['name']})
                elif item['model'] == 'core.qualification':
                    Qualification.objects.get_or_create(id=item['pk'], defaults={'name': item['fields']['name'], 'order': item['pk']})

    job_filepath = os.path.join(FIXTURES_DIR, 'job_titles_complete.json')
    if os.path.exists(job_filepath):
        with open(job_filepath, 'r', encoding='utf-8') as f:
            try:
                for item in json.load(f):
                    if item['model'] == 'core.jobtitle':
                        fields = item['fields']
                        cat_id = fields.get('category')
                        if cat_id:
                            cat, _ = JobCategory.objects.get_or_create(id=cat_id, defaults={'name': f'Category {cat_id}'})
                            try:
                                JobTitle.objects.get_or_create(name=fields.get('name', ''), defaults={'category': cat, 'description': fields.get('description', '')})
                            except Exception: pass
            except Exception: pass

def load_departments():
    print("Loading Departments...")
    filepath = os.path.join(FIXTURES_DIR, 'departments.json')
    if not os.path.exists(filepath): return
    
    # Needs a default SecurityAdmin and GeoGovernorate to attach CentralDepartments to
    default_geo, _ = GeoGovernorate.objects.get_or_create(name_ar='أخرى', defaults={'name_en': 'OTHER', 'is_active': True})
    default_admin, _ = SecurityAdministration.objects.get_or_create(name='الإدارة العامة الافتراضية', defaults={'code': 'DEFAULT', 'geo_governorate': default_geo})

    with open(filepath, 'r', encoding='utf-8') as f:
        for item in json.load(f):
            if item['model'] == 'core.department':
                fields = item['fields']
                try:
                    CentralDepartment.objects.get_or_create(
                        name=fields.get('name', ''),
                        security_admin=default_admin,
                        defaults={'code': fields.get('code', ''), 'is_active': fields.get('is_active', True)}
                    )
                except Exception: pass

def load_ranks_and_statuses():
    print("Loading Ranks and Statuses...")
    # Ranks (often in initial_data or state_transition_rules)
    rank_filepath = os.path.join(FIXTURES_DIR, 'initial_data.json')
    if os.path.exists(rank_filepath):
        with open(rank_filepath, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                if item['model'] == 'core.rank':
                    fields = item['fields']
                    Rank.objects.get_or_create(name=fields.get('name', ''), defaults={'order': item['pk'], 'is_officer': fields.get('is_officer', False)})

    status_filepath = os.path.join(FIXTURES_DIR, 'service_statuses.json')
    if os.path.exists(status_filepath):
        with open(status_filepath, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                if item['model'] == 'core.servicestatus':
                    fields = item['fields']
                    # old classification might differ, map it safely
                    class_val = fields.get('classification', 'active_full')
                    if class_val not in ['active_full', 'active_part', 'inactive_temp', 'inactive_perm']:
                        class_val = 'active_full'
                    ServiceStatus.objects.get_or_create(
                        name=fields.get('name', ''),
                        defaults={'classification': class_val, 'receives_salary': fields.get('receives_salary', True)}
                    )

def load_positions_and_force_types():
    print("Loading Positions and Force Types...")
    pos_filepath = os.path.join(FIXTURES_DIR, 'positions.json')
    if os.path.exists(pos_filepath):
        with open(pos_filepath, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                if item['model'] == 'core.position':
                    fields = item['fields']
                    try:
                        Position.objects.get_or_create(
                            name=fields.get('name', ''),
                            defaults={'level': fields.get('level', 5)}
                        )
                    except Exception: pass

    force_filepath = os.path.join(FIXTURES_DIR, 'force_types.json')
    if os.path.exists(force_filepath):
        with open(force_filepath, 'r', encoding='utf-8') as f:
            for item in json.load(f):
                if item['model'] == 'core.forcetype':
                    fields = item['fields']
                    ForceType.objects.get_or_create(
                        name=fields.get('name', ''),
                        defaults={'code': fields.get('code', str(item['pk'])), 'category': fields.get('category', 'basic'), 'rank_type': fields.get('rank_type', 'both')}
                    )

def main():
    print("Starting comprehensive migration...")
    load_governorates()
    load_job_titles()
    load_departments()
    load_ranks_and_statuses()
    load_positions_and_force_types()
    print("Comprehensive Migration completed!")

if __name__ == '__main__':
    main()
