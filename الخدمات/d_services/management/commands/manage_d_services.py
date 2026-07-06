import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.core import serializers
from django.apps import apps
from django.db import transaction

class Command(BaseCommand):
    help = 'Export or Import d_services data'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action to perform: export or import')
        parser.add_argument('--file', type=str, help='Path to the JSON file', default='d_services_data.json')

    def handle(self, *args, **options):
        action = options['action']
        file_path = options['file']

        if action == 'export':
            self.export_data(file_path)
        elif action == 'import':
            self.import_data(file_path)
        else:
            raise CommandError('Invalid action. Use "export" or "import".')

    def export_data(self, file_path):
        self.stdout.write(f'Exporting d_services data to {file_path}...')
        
        # Define models in order of dependency to ensure clean export/import
        models_to_export = [
            'WorkflowStage',
            'GrantSource',
            'Service',
            'ServiceVersion',
            'ServicePrerequisite',
            'ServiceWorkflowStep',
        ]
            # 'ServicePermission',
            # 'ServiceWorkflowStepPermission',
            # 'OrganizationServiceConfig',
            # 'ServiceInstallmentPlan',
            # 'GroupServicePermission',
            # 'StagePermission',
            # 'WorkflowStepChecklistTemplate',
            # 'ServiceRequest',
            # 'RequestAction',
            # 'StageChecklistItem',
            # 'RequestAttachment',
            # 'RequestInstallment',
            # 'RequestLog',
            # 'RequestReturnLog',

        all_objects = []
        for model_name in models_to_export:
            model = apps.get_model('d_services', model_name)
            objects = model.objects.all()
            all_objects.extend(list(objects))

        data = serializers.serialize('json', all_objects, indent=4, ensure_ascii=False)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully exported {len(all_objects)} objects to {file_path}'))

    @transaction.atomic
    def import_data(self, file_path):
        if not os.path.exists(file_path):
            raise CommandError(f'File {file_path} does not exist.')

        self.stdout.write(f'Importing d_services data from {file_path}...')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()

        try:
            objects = serializers.deserialize('json', data)
            count = 0
            for obj in objects:
                obj.save()
                count += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} objects from {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))
            raise e
