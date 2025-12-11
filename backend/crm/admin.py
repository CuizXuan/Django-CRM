from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# 自定义 Admin 站点标题和头部
admin.site.site_title = _('CRM 管理')
admin.site.site_header = _('CRM 管理后台')
admin.site.index_title = _('欢迎使用 CRM 管理系统')