from django.db import models
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from accounts.models import Account
from common.base import AssignableMixin, BaseModel
from common.models import Org, Profile, Tags, Teams
from common.utils import CURRENCY_CODES, OPPORTUNITY_TYPES, SOURCES, STAGES
from contacts.models import Contact


class Opportunity(AssignableMixin, BaseModel):
    """
    CRM商机模型 - 销售漏斗管理
    基于 Twenty CRM 和 Salesforce 模式设计
    """

    # 核心商机信息
    name = models.CharField(_("商机名称"), max_length=255)
    account = models.ForeignKey(
        Account,
        related_name="opportunities",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    stage = models.CharField(
        _("阶段"), max_length=64, choices=STAGES, default="PROSPECTING"
    )
    opportunity_type = models.CharField(
        _("类型"), max_length=64, choices=OPPORTUNITY_TYPES, blank=True, null=True
    )

    # 财务信息
    currency = models.CharField(
        _("货币"), max_length=3, choices=CURRENCY_CODES, blank=True, null=True
    )
    amount = models.DecimalField(
        _("金额"), decimal_places=2, max_digits=12, blank=True, null=True
    )
    probability = models.IntegerField(
        _("概率 (%)"), default=0, blank=True, null=True
    )
    closed_on = models.DateField(_("预计成交日期"), blank=True, null=True)

    # 来源与上下文
    lead_source = models.CharField(
        _("线索来源"), max_length=255, choices=SOURCES, blank=True, null=True
    )

    # 关系
    contacts = models.ManyToManyField(Contact, related_name="opportunity_contacts")

    # 分配
    assigned_to = models.ManyToManyField(
        Profile, related_name="opportunity_assigned_users"
    )
    teams = models.ManyToManyField(Teams, related_name="opportunity_teams")
    closed_by = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="opportunity_closed_by",
    )

    # 标签
    tags = models.ManyToManyField(Tags, related_name="opportunity_tags", blank=True)

    # 备注
    description = models.TextField(_("备注"), blank=True, null=True)

    # 系统字段
    is_active = models.BooleanField(default=True)
    org = models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        related_name="opportunities",
    )

    class Meta:
        verbose_name = "商机"
        verbose_name_plural = "商机"
        db_table = "opportunity"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["stage"]),
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.name}"

    @property
    def created_on_arrow(self):
        return timesince(self.created_at) + " ago"
