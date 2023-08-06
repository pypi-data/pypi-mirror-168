from django.contrib import admin

# 引入用户平台
from .models import *


class PaymentOrderAdmin(admin.ModelAdmin):

    fields = ('id', 'app_id', 'order_no', 'transact_no', 'transact_id', 'user_id', 'subject', 'total_amount', 'buyer_pay_amount', 'point_amount', 'invoice_amount', 'price_off_amount', 'pay_mode',)
    list_display = ('app_id', 'order_no', 'transact_no', 'transact_id', 'user_id', 'subject', 'total_amount', 'buyer_pay_amount', 'point_amount', 'invoice_amount', 'price_off_amount', 'pay_mode',)
    readonly_fields = ['id']


admin.site.register(PaymentOrder, PaymentOrderAdmin)
