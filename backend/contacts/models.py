from django.db import models
from django.utils.translation import gettext_lazy as _

from common.base import AssignableMixin, BaseModel
from common.models import Org, Profile, Tags, Teams
from common.utils import COUNTRIES


class Contact(AssignableMixin, BaseModel):
    """
    CRM联系人模型 - 为现代销售工作流程优化
    基于 Twenty CRM 和 Salesforce 模式设计
    """

    # 核心联系人信息
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone = models.CharField(_("电话"), max_length=20, null=True, blank=True)

    # 专业信息
    organization = models.CharField(_("公司"), max_length=255, blank=True, null=True)
    title = models.CharField(_("职位"), max_length=255, blank=True, null=True)
    department = models.CharField(
        _("部门"), max_length=255, blank=True, null=True
    )

    # 沟通偏好
    do_not_call = models.BooleanField(_("请勿致电"), default=False)
    linkedin_url = models.URLField(_("LinkedIn URL"), blank=True, null=True)

    # 地址信息（类似 Lead 模型的扁平字段）
    address_line = models.CharField(_("地址"), max_length=255, blank=True, null=True)
    city = models.CharField(_("城市"), max_length=255, blank=True, null=True)
    state = models.CharField(_("州/省"), max_length=255, blank=True, null=True)
    postcode = models.CharField(_("邮政编码"), max_length=64, blank=True, null=True)
    country = models.CharField(
        _("国家"), max_length=3, choices=COUNTRIES, blank=True, null=True
    )

    # 分配
    assigned_to = models.ManyToManyField(Profile, related_name="contact_assigned_users")
    teams = models.ManyToManyField(Teams, related_name="contact_teams")

    # 标签
    tags = models.ManyToManyField(Tags, related_name="contact_tags", blank=True)

    # 备注
    description = models.TextField(_("备注"), blank=True, null=True)

    # 系统字段
    is_active = models.BooleanField(default=True)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="contacts")

    # 账户关系（可选 - 联系人可以独立存在，不关联账户）
    account = models.ForeignKey(
        "accounts.Account",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_contacts",
        help_text="该联系人所属的主要账户",
    )

    class Meta:
        verbose_name = "联系人"
        verbose_name_plural = "联系人"
        db_table = "contacts"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        return self.first_name
