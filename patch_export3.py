import os

filepath = '/home/mahdi/Desktop/n/mahdi/Backend/systems/services/application/services/export_service.py'
with open(filepath, 'r') as f:
    content = f.read()

old_block = """            if self.raw_columns:
                all_arabic = self.protected_columns + self.editable_columns
                for i, raw_col in enumerate(self.raw_columns):
                    if i < len(all_arabic):
                        val = getattr(person, raw_col, '')
                        if val is None:
                            val = ''
                        elif hasattr(val, 'name'):
                            val = val.name
                        elif isinstance(val, date):
                            val = val.strftime('%Y-%m-%d')
                        person_dict[all_arabic[i]] = str(val)"""

new_block = """            from datetime import date
            if self.raw_columns:
                all_arabic = self.ordered_columns if getattr(self, 'ordered_columns', None) else (self.protected_columns + self.editable_columns)
                for i, raw_col in enumerate(self.raw_columns):
                    if i < len(all_arabic):
                        if raw_col == '__UNIT__':
                            val = person.security_admin.name if getattr(person, 'security_admin', None) else ''
                        elif raw_col == '__DEPT_BRANCH__':
                            val = person.central_department.name if getattr(person, 'central_department', None) else (
                                person.branch.name if getattr(person, 'branch', None) else (
                                    person.district_police.name if getattr(person, 'district_police', None) else ''
                                )
                            )
                        elif raw_col == '__DISTRICT_DIVISION__':
                            val = person.division.name if getattr(person, 'division', None) else ''
                        elif raw_col == '__STATUS_TYPE__':
                            val = person.current_status.get_classification_display() if getattr(person, 'current_status', None) else ''
                        else:
                            val = getattr(person, raw_col, '')

                        if val is None:
                            val = ''
                        elif hasattr(val, 'name'):
                            val = val.name
                        elif isinstance(val, date):
                            val = val.strftime('%Y-%m-%d')
                        person_dict[all_arabic[i]] = str(val)"""

content = content.replace(old_block, new_block)

with open(filepath, 'w') as f:
    f.write(content)
