from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from accounts.models import Account
from common.base import AssignableMixin, BaseModel
from common.models import Org, Profile, Tags, Teams
from common.utils import CASE_TYPE, PRIORITY_CHOICE, STATUS_CHOICE
from contacts.models import Contact


# 清理说明：
# - 删除了 Case 和 Solution 的 'created_on_arrow' 属性（前端自行计算时间戳）
# - 修复了 case_type 的默认值从 "" 改为 None（空字符串对于可为空的字段来说是不好的默认值）


class Case(AssignableMixin, BaseModel):
    name = models.CharField(pgettext_lazy(_("案例名称"), "Name"), max_length=64)
    status = models.CharField(choices=STATUS_CHOICE, max_length=64)
    priority = models.CharField(choices=PRIORITY_CHOICE, max_length=64)
    case_type = models.CharField(
        choices=CASE_TYPE, max_length=255, blank=True, null=True, default=None
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="accounts_cases",
    )
    contacts = models.ManyToManyField(Contact, related_name="case_contacts")
    closed_on = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(Profile, related_name="case_assigned_users")
    is_active = models.BooleanField(default=True)
    teams = models.ManyToManyField(Teams, related_name="cases_teams")
    tags = models.ManyToManyField(Tags, related_name="case_tags", blank=True)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="cases")

    class Meta:
        verbose_name = "案例"
        verbose_name_plural = "案例"
        db_table = "case"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.name}"


class Solution(BaseModel):
    """
    知识库解决方案

    解决方案是可以链接到案例的可重用答案/指南。
    它们构成了常见问题和解决方案的知识库。
    """

    title = models.CharField(max_length=255)
    description = models.TextField()

    STATUS_CHOICES = [
        ("draft", "草稿"),
        ("reviewed", "已审核"),
        ("approved", "已批准"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    is_published = models.BooleanField(default=False)

    # 组织关系
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="solutions")

    # 使用此解决方案的案例
    cases = models.ManyToManyField(Case, related_name="solutions", blank=True)

    class Meta:
        verbose_name = "解决方案"
        verbose_name_plural = "解决方案"
        db_table = "solution"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["is_published"]),
            models.Index(fields=["org"]),
        ]

    def __str__(self):
        return self.title

    def publish(self):
        """发布解决方案（必须先批准）"""
        if self.status == "approved":
            self.is_published = True
            self.save()

    def unpublish(self):
        """取消发布解决方案"""
        self.is_published = False
        self.save()
