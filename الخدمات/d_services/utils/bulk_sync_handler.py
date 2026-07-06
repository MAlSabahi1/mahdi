"""
Bulk Sync Handler - Generic handler for bulk create/update/delete operations
Handles the sync pattern used in prerequisites, workflow steps, and installment plans
"""
from typing import Dict, List, Set, Any, Type, Optional, Callable
from django.db import transaction
from django.db.models import Model
from django.core.exceptions import ValidationError

class BulkSyncResult:
    """Result of a bulk sync operation"""
    def __init__(self):
        self.created: List[Model] = []
        self.updated: List[Model] = []
        self.deleted_count: int = 0
    
    def to_dict(self) -> Dict:
        return {
            'created_count': len(self.created),
            'updated_count': len(self.updated),
            'deleted_count': self.deleted_count
        }


class BulkSyncHandler:
    """
    Generic handler for synchronizing a list of items with the database.
    Supports create, update, and delete operations based on incoming data.
    """
    
    @staticmethod
    def sync_by_id(
        model_class: Type[Model],
        parent_field: str,
        parent_instance: Model,
        items_data: List[Dict],
        field_mapping: Dict[str, str] = None,
        updatable_fields: List[str] = None,
        post_save_callback: Optional[Callable[[Model], None]] = None,
    ) -> BulkSyncResult:
        """
        Sync items using 'id' as the lookup field.
        - Items with existing ID: update
        - Items without ID: create new
        - Existing items not in the list: delete
        
        Args:
            model_class: Django model class to sync
            parent_field: Field name for the parent FK (e.g., 'fk_service')
            parent_instance: Parent model instance
            items_data: List of dicts with item data
            field_mapping: Dict mapping data keys to model fields (e.g., {'fk_stage': 'fk_stage_id'})
            updatable_fields: List of fields that can be updated
            post_save_callback: Optional callback to run after saving each item
        """
        result = BulkSyncResult()
        field_mapping = field_mapping or {}

        items_to_update: List[Model]=[]
        update_fields_set: Set[str] = set()
        with transaction.atomic():
            # Get existing items
            filter_kwargs = {parent_field: parent_instance, 'is_deleted': False}
            existing_items = {
                item.id: item 
                for item in model_class.objects.filter(**filter_kwargs)
            }
            sent_ids: Set[int] = set()
            for item_data in items_data:
                item_id = item_data.get('id')
                if item_id and item_id in existing_items:
                    # Update existing
                    sent_ids.add(item_id)
                    item = existing_items[item_id]
                    if updatable_fields:
                        for field in updatable_fields:
                            if field in item_data:
                                model_field = field_mapping.get(field, field)
                                value = item_data[field]
                                if isinstance(value, int) and hasattr(item, f'{model_field}_id'):
                                    setattr(item, f'{model_field}_id', value)
                                    update_fields_set.add(f'{model_field}_id')
                                else:
                                    setattr(item, model_field, value)
                                    update_fields_set.add(model_field)
                    items_to_update.append(item)
                    result.updated.append(item)
                else:
                    # Create new
                    item_data.pop('id', None)
                    create_kwargs = {parent_field: parent_instance}
                    for key, value in item_data.items():
                        model_field = field_mapping.get(key, key)
                        create_kwargs[model_field] = value
                    item = model_class.objects.create(**create_kwargs)
                    if post_save_callback:
                        post_save_callback(item)
                    result.created.append(item)
            # Delete items not in the list
            for item_id, item in existing_items.items():
                if item_id not in sent_ids:
                    item.delete(force_delete=True, is_main=True)
                    result.deleted_count += 1
            if items_to_update and update_fields_set:
                model_class.objects.bulk_update(items_to_update,list(update_fields_set))
                if post_save_callback:
                    for item in items_to_update:
                        post_save_callback(item)
        return result
    
    @staticmethod
    def sync_by_order(
        model_class: Type[Model],
        parent_field: str,
        parent_instance: Model,
        items_data: List[Dict],
        updatable_fields: List[str] = None,
    ) -> BulkSyncResult:
        """
        Sync items using 'order' as the lookup field.
        - Items with existing order: update
        - Items with new order: create new
        - Existing items with order not in list: delete
        
        Args:
            model_class: Django model class to sync
            parent_field: Field name for the parent FK
            parent_instance: Parent model instance
            items_data: List of dicts with item data
            updatable_fields: List of fields that can be updated
        """
        result = BulkSyncResult()
        
        with transaction.atomic():
            # Get existing items indexed by order
            filter_kwargs = {parent_field: parent_instance, 'is_deleted': False}
            existing_items = {
                item.order: item 
                for item in model_class.objects.filter(**filter_kwargs)
            }
            
            processed_orders: Set[int] = set()
            
            for item_data in items_data:
                order = item_data.get('order', 1)
                
                if order in existing_items:
                    # Update existing
                    processed_orders.add(order)
                    item = existing_items[order]
                    
                    if updatable_fields:
                        for field in updatable_fields:
                            if field in item_data:
                                setattr(item, field, item_data[field])
                    
                    item.save()
                    result.updated.append(item)
                else:
                    # Create new
                    processed_orders.add(order)
                    create_kwargs = {parent_field: parent_instance}
                    create_kwargs.update(item_data)
                    
                    item = model_class.objects.create(**create_kwargs)
                    result.created.append(item)
            
            # Delete items with orders not in the list
            for order, item in existing_items.items():
                if order not in processed_orders:
                    item.delete(force_delete=True, is_main=True)
                    result.deleted_count += 1
        
        return result
    
    @staticmethod
    def get_all_active(
        model_class: Type[Model],
        parent_field: str,
        parent_instance: Model,
        order_by: str = 'order'
    ):
        """Get all active (non-deleted) items for a parent, ordered"""
        filter_kwargs = {parent_field: parent_instance, 'is_deleted': False}
        return model_class.objects.filter(**filter_kwargs).order_by(order_by)
