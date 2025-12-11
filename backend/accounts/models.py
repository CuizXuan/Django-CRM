from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from common.base import AssignableMixin, BaseModel
from common.models import Org, Profile, Tags, Teams
from common.utils import COUNTRIES, CURRENCY_CODES, INDCHOICES
from contacts.models import Contact


# 清理说明：
# - 删除了 'created_on_arrow' 属性（前端自行计算时间戳）
# - 删除了 'contact_values' 属性（未使用）


class Account(AssignableMixin, BaseModel):
    """
    CRM 客户模型 - 为现代销售工作流程优化
    基于 Twenty CRM 和 Salesforce 模式
    """

    # 核心客户信息
    name = models.CharField(_("客户名称"), max_length=255)
    email = models.EmailField(_("邮箱"), blank=True, null=True)
    phone = models.CharField(_("电话"), max_length=20, null=True, blank=True)
    website = models.URLField(_("网站"), blank=True, null=True)

    # 商业信息
    industry = models.CharField(
        _("行业"), max_length=255, choices=INDCHOICES, blank=True, null=True
    )
    number_of_employees = models.PositiveIntegerField(
        _("员工数量"), blank=True, null=True
    )
    annual_revenue = models.DecimalField(
        _("年营收"), max_digits=15, decimal_places=2, blank=True, null=True
    )
    currency = models.CharField(
        _("货币"), max_length=3, choices=CURRENCY_CODES, blank=True, null=True
    )

    # 地址（类似 Lead 和 Contact 模型的扁平字段）
    address_line = models.CharField(_("地址"), max_length=255, blank=True, null=True)
    city = models.CharField(_("城市"), max_length=255, blank=True, null=True)
    state = models.CharField(_("省份"), max_length=255, blank=True, null=True)
    postcode = models.CharField(_("邮政编码"), max_length=64, blank=True, null=True)
    country = models.CharField(
        _("国家"), max_length=3, choices=COUNTRIES, blank=True, null=True
    )

    # 分配
    assigned_to = models.ManyToManyField(Profile, related_name="account_assigned_users")
    teams = models.ManyToManyField(Teams, related_name="account_teams")
    contacts = models.ManyToManyField(
        "contacts.Contact", related_name="account_contacts"
    )

    # 标签
    tags = models.ManyToManyField(Tags, related_name="account_tags", blank=True)

    # 备注
    description = models.TextField(_("备注"), blank=True, null=True)

    # 系统字段
    is_active = models.BooleanField(default=True)
    org = models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    class Meta:
        verbose_name = "客户"
        verbose_name_plural = "客户"
        db_table = "accounts"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["industry"]),
            models.Index(fields=["org", "-created_at"]),
        ]
        permissions = [
            ("can_add_account", "可以添加客户"),
            ("can_change_account", "可以修改客户"),
            ("can_delete_account", "可以删除客户"),
        ]

    def __str__(self):
        return f"{self.name}"


class AccountEmail(BaseModel):
    from_account = models.ForeignKey(
        Account, related_name="sent_email", on_delete=models.SET_NULL, null=True
    )
    recipients = models.ManyToManyField(Contact, related_name="recieved_email")
    message_subject = models.TextField(null=True)
    message_body = models.TextField(null=True)
    timezone = models.CharField(max_length=100, default="UTC")
    scheduled_date_time = models.DateTimeField(null=True)
    scheduled_later = models.BooleanField(default=False)
    from_email = models.EmailField()
    rendered_message_body = models.TextField(null=True)
    org = models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        related_name="account_emails",
    )

    class Meta:
        verbose_name = "客户邮件"
        verbose_name_plural = "客户邮件"
        db_table = "account_email"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.message_subject}"

    def save(self, *args, **kwargs):
        """
        确保组织遵循父级客户；如果失败则回退到第一个收件人的组织。

        这可以防止缺少组织分配，这会违反多租户隔离。
        """
        if not self.org_id:
            if self.from_account and self.from_account.org_id:
                self.org_id = self.from_account.org_id
            else:
                # 对于未保存的 m2m，收件人可能在保存后才可用
                recipient = self.recipients.first() if self.pk else None
                if recipient and recipient.org_id:
                    self.org_id = recipient.org_id
        if not self.org_id:
            raise ValidationError(_("客户邮件需要组织"))
        super().save(*args, **kwargs)


class AccountEmailLog(BaseModel):
    """此模型用于跟踪邮件是否已发送"""

    email = models.ForeignKey(
        AccountEmail, related_name="email_log", on_delete=models.SET_NULL, null=True
    )
    contact = models.ForeignKey(
        Contact, related_name="contact_email_log", on_delete=models.SET_NULL, null=True
    )
    is_sent = models.BooleanField(default=False)
    org = models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        related_name="account_email_logs",
    )

    class Meta:
        verbose_name = "邮件日志"
        verbose_name_plural = "邮件日志"
        db_table = "emailLogs"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.email.message_subject}"

    def save(self, *args, **kwargs):
        """
        将日志组织与父级邮件（优先）或联系人组织对齐。
        """
        if not self.org_id:
            if self.email and self.email.org_id:
                self.org_id = self.email.org_id
            elif self.contact and self.contact.org_id:
                self.org_id = self.contact.org_id
        if not self.org_id:
            raise ValidationError(_("邮件日志需要组织"))
        super().save(*args, **kwargs)
