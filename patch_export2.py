import os

filepath = '/home/mahdi/Desktop/n/mahdi/Backend/systems/services/application/services/export_service.py'
with open(filepath, 'r') as f:
    content = f.read()

# Replace meta data writing
old_meta = """        forces = list(ForceType.objects.values_list('name', flat=True))
        quals = list(Qualification.objects.values_list('name', flat=True))
        statuses = list(ServiceStatus.objects.values_list('name', flat=True))
        
        # Write to sheet"""

new_meta = """        forces = list(ForceType.objects.values_list('name', flat=True))
        quals = list(Qualification.objects.values_list('name', flat=True))
        
        status_objs = list(ServiceStatus.objects.all())
        statuses = [s.name for s in status_objs]
        status_class_displays = [s.get_classification_display() for s in status_objs]
        
        classifications = [
            'قوة عاملة فعلية',
            'قوة عاملة غير فعلية',
            'قوة غير عاملة مؤقتاً',
            'قوة غير عاملة نهائياً'
        ]
        
        # Write to sheet"""
content = content.replace(old_meta, new_meta)

old_ranges = """            'نوع الحالة': _write_column(6, statuses),
            'الحالة': _write_column(6, statuses),  # Same reference
        }
        
        meta_ws.hide() # إخفاء ورقة البيانات بعد تنشيط ورقة أخرى لكي تعمل بنجاح"""

new_ranges = """            'نوع الحالة': _write_column(6, statuses),
            'الحالة': _write_column(7, classifications),
        }
        
        _write_column(8, statuses)         # Col I (index 8)
        _write_column(9, status_class_displays) # Col J (index 9)
        self.status_count = len(statuses)
        
        meta_ws.hide() # إخفاء ورقة البيانات بعد تنشيط ورقة أخرى لكي تعمل بنجاح"""
content = content.replace(old_ranges, new_ranges)

# Replace writing loop in _write_sheet
old_loop = """            for r_idx, row_dict in enumerate(sheet_data, 1):
                for c_idx, col_name in enumerate(headers):
                    val = row_dict.get(col_name, '')
                    is_locked_col = col_name in self.protected_columns
                    if is_locked_col:
                        worksheet.write(r_idx + 2, c_idx, val, fmts['locked_data'])
                    else:
                        worksheet.write(r_idx + 2, c_idx, val, fmts['editable_data'])
                        if col_name in self.meta_ranges and self.meta_ranges[col_name]:
                            worksheet.data_validation(
                                r_idx + 2, c_idx, r_idx + 2, c_idx,
                                {
                                    'validate': 'list',
                                    'source': f"={self.meta_ranges[col_name]}",
                                    'show_error': False,
                                    'error_title': 'قيمة غير صالحة',
                                    'error_message': 'الرجاء اختيار قيمة من القائمة المنسدلة'
                                }
                            )"""

new_loop = """            type_col_name = 'نوع الحالة'
            type_col_idx = headers.index(type_col_name) if type_col_name in headers else -1
            type_col_letter = xlsxwriter.utility.xl_col_to_name(type_col_idx) if type_col_idx >= 0 else ''

            for r_idx, row_dict in enumerate(sheet_data, 1):
                for c_idx, col_name in enumerate(headers):
                    val = row_dict.get(col_name, '')
                    is_locked_col = col_name in self.protected_columns
                    
                    if col_name == 'الحالة' and type_col_letter:
                        row_num = r_idx + 3
                        max_status = max(1, getattr(self, 'status_count', 100))
                        formula = f'=IFERROR(VLOOKUP({type_col_letter}{row_num}, SystemData!$I$1:$J${max_status}, 2, FALSE), "{val}")'
                        if is_locked_col:
                            worksheet.write_formula(r_idx + 2, c_idx, formula, fmts['locked_data'], value=val)
                        else:
                            worksheet.write_formula(r_idx + 2, c_idx, formula, fmts['editable_data'], value=val)
                        continue
                        
                    if is_locked_col:
                        worksheet.write(r_idx + 2, c_idx, val, fmts['locked_data'])
                    else:
                        worksheet.write(r_idx + 2, c_idx, val, fmts['editable_data'])
                        if col_name in self.meta_ranges and self.meta_ranges[col_name]:
                            worksheet.data_validation(
                                r_idx + 2, c_idx, r_idx + 2, c_idx,
                                {
                                    'validate': 'list',
                                    'source': f"={self.meta_ranges[col_name]}",
                                    'show_error': False,
                                    'error_title': 'قيمة غير صالحة',
                                    'error_message': 'الرجاء اختيار قيمة من القائمة المنسدلة'
                                }
                            )"""

content = content.replace(old_loop, new_loop)

with open(filepath, 'w') as f:
    f.write(content)
