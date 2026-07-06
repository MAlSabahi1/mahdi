from decimal import Decimal
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from d_services.models.ServiceRequest import ServiceRequest
from d_services.choices.choices import PaymentStatusChoice


class CalculationHandler:
    @staticmethod
    def generate_request_number(organization, org_config) -> str:
        prefix = org_config.request_prefix if org_config and org_config.request_prefix else 'REQ'
        year = timezone.now().year
        
        last_request = ServiceRequest.objects.filter(
            fk_organization=organization,
            request_number__startswith=f"{prefix}-{year}"
        ).only('request_number').order_by('-id').first()
        
        if last_request:
            try:
                last_num = int(last_request.request_number.split('-')[-1])
                next_num = last_num + 1
            except (ValueError, IndexError):
                next_num = 1
        else:
            next_num = 1
            
        return f"{prefix}-{year}-{next_num:06d}"
    
    @staticmethod
    def calculate_fees(service, org_config, organization, requester_id=None) -> dict:
        fees = {
            'total_fee': 0,
            'discounted_fee': 0,
            'remaining_amount': 0,
            'amount_paid': 0,
            'payment_status': PaymentStatusChoice.FREE
        }
        
        if not org_config.is_paid:
            return fees
        
        free_count = ServiceRequest.objects.filter(
            requester_id=requester_id,
            fk_service=service,
            fk_organization=organization,
            total_fee=0,
            requested_at__year=timezone.now().year
            ).count()
        
        fee_amount = org_config.fee_amount or 0
        
        if free_count < (org_config.free_limit_per_year or 0):
            fees = {
                'total_fee': fee_amount,
                'discounted_fee': 0,
                'remaining_amount': 0,
                'amount_paid': 0,
                'discounted_fee_reason': _("الخدمة مجانية للمره %s") % (org_config.free_limit_per_year - free_count),
                'payment_status': PaymentStatusChoice.FREE
            }
            return fees

        fees['total_fee'] = fee_amount
        fees['discounted_fee'] = 0
        fees['discounted_fee_reason'] = None
        fees['remaining_amount'] = fee_amount
        fees['payment_status'] = PaymentStatusChoice.UNPAID
        fees['amount_paid'] = 0
        
        return fees
    
    @staticmethod
    def update_payment_status(instance) -> None:
        instance.remaining_amount = (
            instance.total_fee -
            instance.discount_amount -
            instance.grant_amount -
            instance.amount_paid
        )
        
        if instance.remaining_amount < 0:
            instance.remaining_amount = 0
        
        has_grant = instance.grant_amount > 0
        has_discount = instance.discount_amount > 0
        has_payment = instance.amount_paid > 0
        is_fully_paid = instance.remaining_amount == 0
        
        if instance.total_fee == 0:
            instance.payment_status = PaymentStatusChoice.FREE
            return
        
        if is_fully_paid:
            if has_grant and has_discount:
                instance.payment_status = PaymentStatusChoice.PAID_BY_GRANT_DISCOUNT
            elif has_grant:
                instance.payment_status = PaymentStatusChoice.PAID_BY_GRANT
            elif has_discount:
                instance.payment_status = PaymentStatusChoice.PAID_BY_DISCOUNT
            elif has_payment:
                instance.payment_status = PaymentStatusChoice.PAID
            else:
                instance.payment_status = PaymentStatusChoice.FREE
        else:
            if has_grant and has_discount:
                instance.payment_status = PaymentStatusChoice.PARTIAL_GRANT_DISCOUNT
            elif has_grant:
                instance.payment_status = PaymentStatusChoice.PARTIAL_GRANT
            elif has_discount:
                instance.payment_status = PaymentStatusChoice.PARTIAL_DISCOUNT
            elif has_payment:
                instance.payment_status = PaymentStatusChoice.PARTIAL
            else:
                instance.payment_status = PaymentStatusChoice.UNPAID
