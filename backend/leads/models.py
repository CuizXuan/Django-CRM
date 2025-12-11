from django.db import models
from django.utils.translation import gettext_lazy as _

from common.base import AssignableMixin, BaseModel
from common.models import Org, Profile, Tags, Teams
from common.utils import (
    COUNTRIES,
    CURRENCY_CODES,
    INDCHOICES,
    LEAD_SOURCE,
    LEAD_STATUS,
)
from contacts.models import Contact


# Cleanup notes:
# - Removed 'created_from_site' flag (over-engineered)
# - Removed conversion tracking fields (converted_account, converted_contact,
#   converted_opportunity, conversion_date) - never populated, conversion just sets status
# - Removed 'created_on_arrow' property (frontend computes its own timestamps)


class Lead(AssignableMixin, BaseModel):
    """
    CRM线索模型 - 为现代销售工作流程优化
    基于 Twenty CRM 和 Salesforce 模式设计
    """

    # 核心线索信息
    title = models.CharField(
        _("标题"), max_length=255, blank=True, null=True,
        help_text="线索名称/主题（例如：'企业交易'、'网站咨询'）"
    )
    salutation = models.CharField(
        _("称谓"), max_length=64, blank=True, null=True,
        help_text="例如：先生、女士、小姐、博士"
    )
    first_name = models.CharField(_("名字"), null=True, max_length=255)
    last_name = models.CharField(_("姓氏"), null=True, max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(_("电话"), max_length=50, null=True, blank=True)
    job_title = models.CharField(
        _("职位"), max_length=255, blank=True, null=True,
        help_text="个人职位（例如：'销售副总裁'、'首席技术官'）"
    )
    website = models.CharField(_("网站"), max_length=255, blank=True, null=True)
    linkedin_url = models.URLField(
        _("LinkedIn URL"), max_length=500, blank=True, null=True
    )

    # 销售漏斗
    status = models.CharField(
        _("状态"), max_length=255, blank=True, null=True, choices=LEAD_STATUS
    )
    source = models.CharField(
        _("来源"), max_length=255, blank=True, null=True, choices=LEAD_SOURCE
    )
    industry = models.CharField(
        _("行业"), max_length=255, choices=INDCHOICES, blank=True, null=True
    )
    rating = models.CharField(
        _("评级"),
        max_length=10,
        blank=True,
        null=True,
        choices=[("HOT", "Hot"), ("WARM", "Warm"), ("COLD", "Cold")],
    )
    opportunity_amount = models.DecimalField(
        _("交易价值"), decimal_places=2, max_digits=12, blank=True, null=True
    )
    currency = models.CharField(
        _("货币"), max_length=3, choices=CURRENCY_CODES, blank=True, null=True
    )
    probability = models.IntegerField(
        _("获胜概率 %"), default=0, blank=True, null=True
    )
    close_date = models.DateField(_("预计成交日期"), default=None, null=True)

    # 地址
    address_line = models.CharField(_("地址"), max_length=255, blank=True, null=True)
    city = models.CharField(_("城市"), max_length=255, blank=True, null=True)
    state = models.CharField(_("州/省"), max_length=255, blank=True, null=True)
    postcode = models.CharField(_("邮政编码"), max_length=64, blank=True, null=True)
    country = models.CharField(
        _("国家"), max_length=3, choices=COUNTRIES, blank=True, null=True
    )

    # 分配
    assigned_to = models.ManyToManyField(Profile, related_name="lead_assigned_users")
    teams = models.ManyToManyField(Teams, related_name="lead_teams")

    # 活动跟踪
    last_contacted = models.DateField(_("Last Contacted"), blank=True, null=True)
    next_follow_up = models.DateField(_("Next Follow-up"), blank=True, null=True)
    description = models.TextField(_("备注"), blank=True, null=True)

    # 系统字段
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tags, related_name="lead_tags", blank=True)
    contacts = models.ManyToManyField(Contact, related_name="lead_contacts")
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="leads")
    company_name = models.CharField(
        _("公司名称"), max_length=255, blank=True, null=True
    )

    class Meta:
        verbose_name = "线索"
        verbose_name_plural = "线索"
        db_table = "lead"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["source"]),
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        name_parts = [self.salutation, self.first_name, self.last_name]
        return " ".join(part for part in name_parts if part) or f"Lead {self.id}"

