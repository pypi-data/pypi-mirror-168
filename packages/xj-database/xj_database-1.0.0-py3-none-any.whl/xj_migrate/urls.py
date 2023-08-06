# 应用名称
from django.urls import re_path

from xj_payment.apis import alipay, transaction_inquiry, wechat_payment
from .apis import data_migration

app_name = 'database'

urlpatterns = [

    re_path(r'^list_table/?$', data_migration.Data.list_table),
    re_path(r'^list_col/?$', data_migration.Data.list_col),
    re_path(r'^consolidation/?$', data_migration.Data.consolidation),

]
