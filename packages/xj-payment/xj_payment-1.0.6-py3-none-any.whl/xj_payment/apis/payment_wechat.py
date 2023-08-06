from django.http import JsonResponse
from rest_framework import request
from rest_framework.views import APIView
from ..services.payment_wechat_service import PaymentWechatService


class PaymentWechat(APIView):
    # 获取唯一标识
    def get_user_info(self):
        code = self.GET.get('code', 0)  # 保留俩位小数  前端传回的金额数据
        wxpay_params = PaymentWechatService.get_user_info(code)

        return JsonResponse(wxpay_params)

    # 小程序支付
    def payment_applets_pay(self):
        params = self.POST
        wxpay_params = PaymentWechatService.payment_applets_pay(params)

        return JsonResponse(wxpay_params)

    # 回调接口
    def callback(self):
        _xml = self.body
        wxpay_params = PaymentWechatService.callback(_xml)
        return JsonResponse(wxpay_params)
