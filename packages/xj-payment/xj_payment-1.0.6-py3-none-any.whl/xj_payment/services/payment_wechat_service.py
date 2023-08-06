import logging

import requests
from lxml import etree as et
from pathlib import Path
from ..utils.wechat_utils import my_ali_pay
from main.settings import BASE_DIR
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from rest_framework import status
from django.http import HttpResponse

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

sub_appid = main_config_dict.wechat_merchant_app_id or module_config_dict.wechat_merchant_app_id or ""

sub_app_secret = main_config_dict.wechat_merchant_app_secret or module_config_dict.wechat_merchant_app_secret or ""

sub_mch_id = main_config_dict.wechat_merchant_mch_id or module_config_dict.wechat_merchant_mch_id or ""

trade_type = main_config_dict.wechat_trade_type or module_config_dict.wechat_trade_type or ""
# 交易类型，小程序取值：JSAPI

# 商品描述，商品简单描述
body = main_config_dict.wechat_body or module_config_dict.wechat_body or ""
# 标价金额，订单总金额，单位为分
total_fee = main_config_dict.wechat_total_fee or module_config_dict.wechat_total_fee or ""
# 通知地址，异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。
notify_url = main_config_dict.wechat_notify_url or module_config_dict.wechat_notify_url or ""

# 用户标识，trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识。
# print("<trade_type>", trade_type)

logger = logging.getLogger(__name__)


class PaymentWechatService:

    @staticmethod
    def get_user_info(code):
        # https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx0c2a8db23b2e7c28&redirect_uri=REDIRECT_URI&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect
        req_params = {
            'appid': sub_appid,
            'secret': sub_app_secret,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        user_info = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=req_params, timeout=3,
                                 verify=False)
        return user_info.json()

    @staticmethod
    def payment_applets_pay(params):
        pay = my_ali_pay()
        order = pay.order.create(
            trade_type=trade_type,  # 交易类型，小程序取值：JSAPI
            body=body,  # 商品描述，商品简单描述
            total_fee=params['total_fee'],  # 标价金额，订单总金额，单位为分
            notify_url=notify_url,  # 通知地址，异步接收微信支付结果通知的回调地址，通知url必须为外网可访问的url，不能携带参数。
            sub_mch_id=sub_mch_id,
            sub_appid=sub_appid,
            sub_user_id=params['openid']  # 用户标识，trade_type=JSAPI，此参数必传，用户在商户appid下的唯一标识。
        )
        wxpay_params = pay.jsapi.get_jsapi_params(order['prepay_id'])
        return wxpay_params

    @staticmethod
    def callback(_xml):
        # _xml = request.body
        # 拿到微信发送的xml请求 即微信支付后的回调内容
        xml = str(_xml, encoding="utf-8")
        return_dict = {}
        tree = et.fromstring(xml)
        # xml 解析
        return_code = tree.find("return_code").text
        try:
            if return_code == 'FAIL':
                # 官方发出错误
                # return_dict['message'] = '支付失败'
                logging.error("微信支付失败")
                # return Response(return_dict, status=status.HTTP_400_BAD_REQUEST)
            elif return_code == 'SUCCESS':
                # 拿到自己这次支付的 out_trade_no
                _out_trade_no = tree.find("out_trade_no").text
                # TODO 这里省略了 拿到订单号后的操作 看自己的业务需求
                return_dict['message'] = '支付成功'
                logging.info("微信支付成功")
        except Exception as e:
            pass
        finally:
            return return_dict
