# 应用名称
from django.urls import re_path

from xj_payment.apis import alipay, transaction_inquiry, wechat_payment
from .apis import payment_alipay
from .apis import payment_wechat
from .apis import payment_unionpay
from .apis import data

app_name = 'payment'

urlpatterns = [
    # re_path(r'^alipay_payment/?$', alipay.Payment.as_view(), ),
    # re_path(r'^alipay_payment/?$', alipay.Payment.test)
    # re_path(r'^get_pay_url/?$', alipay.Payment.get_pay_url),  # 获取支付宝支付链接
    re_path(r'^get_pay_url/?$', payment_alipay.PaymentAlipay.get_pay_url),  # 获取支付宝支付链接
    # re_path(r'^get_result/?$', alipay.Payment.pay_result),  # 支付宝处理完成后同步回调通知
    re_path(r'^get_result/?$', payment_alipay.PaymentAlipay.pay_result),  # 支付宝处理完成后同步回调通知
    re_path(r'^update_order/?$', alipay.Payment.update_order),  # 支付宝处理完成后支付宝服务器异步回调通知
    re_path(r'^refund/?$', alipay.Payment.refund),  # 支付宝退款
    re_path(r'^close/?$', alipay.Payment.close),  # 关闭订单

    re_path(r'^refund_inquiry/?$', transaction_inquiry.query.refund_inquiry),  # 支付宝退款查询
    re_path(r'^trade_query/?$', transaction_inquiry.query.trade_query),  # 支付宝下单查询

    re_path(r'^get_user_info/?$', payment_wechat.PaymentWechat.get_user_info),  # 获取用户标识接口
    re_path(r'^applets_pay/?$', payment_wechat.PaymentWechat.payment_applets_pay),  # 小程序支付接口
    re_path(r'^callback/?$', payment_wechat.PaymentWechat.callback),  # 回调接口

    re_path(r'^unipay/?$', payment_unionpay.PaymentUnionPay.unipay),

    re_path(r'^list_table/?$', data.Data.list_table),
    re_path(r'^list_col/?$', data.Data.list_col),
    re_path(r'^consolidation/?$', data.Data.consolidation),
    # re_path(r'^pay/?$', wechat_payment.WeChatPayment.pay),
    # re_path(r'^pay/?$', wechat.WeChatPayment.pay),
    # 支付结果回调
    # re_path(r'^payNotify/', views.WeChatPayNotifyViewSet.as_view(), name='pay_notify'),

]
