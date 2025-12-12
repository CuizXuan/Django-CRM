import binascii
import datetime
import os
import time
import uuid

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _
from common.base import BaseModel
from common.utils import (
    COUNTRIES,
    CURRENCY_CODES,
    ROLES,
    is_document_file_audio,
    is_document_file_code,
    is_document_file_image,
    is_document_file_pdf,
    is_document_file_sheet,
    is_document_file_text,
    is_document_file_video,
    is_document_file_zip,
)

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, db_index=True, primary_key=True
    )
    email = models.EmailField(_("邮箱地址"), blank=True, unique=True)
    profile_pic = models.CharField(max_length=1000, null=True, blank=True, verbose_name="头像")
    activation_key = models.CharField(max_length=150, null=True, blank=True, verbose_name="激活密钥")
    key_expires = models.DateTimeField(null=True, blank=True, verbose_name="密钥过期时间")
    is_active = models.BooleanField(default=True, verbose_name="是否活跃")
    is_staff = models.BooleanField(_("管理员状态"), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        db_table = "users"
        ordering = ("-is_active",)

    def __str__(self):
        return self.email


class Address(BaseModel):
    address_line = models.CharField(
        _("地址"), max_length=255, blank=True, default=""
    )
    street = models.CharField(_("街道"), max_length=55, blank=True, default="")
    city = models.CharField(_("城市"), max_length=255, blank=True, default="")
    state = models.CharField(_("省份"), max_length=255, blank=True, default="")
    postcode = models.CharField(
        _("邮政编码"), max_length=64, blank=True, default=""
    )
    country = models.CharField(_("国家"),max_length=3, choices=COUNTRIES, blank=True, default="")
    org = models.ForeignKey(
        "Org",
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name="组织"
    )

    class Meta:
        verbose_name = "地址"
        verbose_name_plural = "地址"
        db_table = "address"
        ordering = ("-created_at",)

    def __str__(self):
        return self.city if self.city else ""


def generate_unique_key():
    return str(uuid.uuid4())


class Org(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True,verbose_name="姓名")
    api_key = models.TextField(default=generate_unique_key, unique=True, editable=False,verbose_name="API密钥")
    is_active = models.BooleanField(default=True, verbose_name="是否活跃")

    # 本地化设置
    default_currency = models.CharField(
        max_length=3, choices=CURRENCY_CODES, default="USD"
    )
    default_country = models.CharField(
        max_length=2, choices=COUNTRIES, blank=True, null=True
    )

    class Meta:
        verbose_name = "组织"
        verbose_name_plural = "组织"
        db_table = "organization"
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.name)


class Tags(BaseModel):
    """用于分类 CRM 实体（客户、线索、商机）的标签"""

    name = models.CharField(max_length=20,verbose_name="姓名")
    slug = models.CharField(max_length=20, blank=True, verbose_name="别名")
    org = models.ForeignKey(
        "Org",
        on_delete=models.CASCADE,
        related_name="tags",
        verbose_name="组织")

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"
        db_table = "tags"
        ordering = ("-created_at",)
        unique_together = ["slug", "org"]

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Profile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profiles", verbose_name="用户")
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="profiles", verbose_name="组织")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="电话")
    alternate_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="备用电话")
    address = models.ForeignKey(
        Address,
        related_name="address_users",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="地址"
    )
    role = models.CharField(max_length=50, choices=ROLES, default="USER", verbose_name="角色")
    has_sales_access = models.BooleanField(default=False, verbose_name="销售权限")
    has_marketing_access = models.BooleanField(default=False, verbose_name="营销权限")
    is_active = models.BooleanField(default=True, verbose_name="是否活跃")
    is_organization_admin = models.BooleanField(default=False, verbose_name="是否组织管理员")
    date_of_joining = models.DateField(null=True, blank=True, verbose_name="入职日期")

    class Meta:
        verbose_name = "个人资料"
        verbose_name_plural = "个人资料"
        db_table = "profile"
        ordering = ("-created_at",)
        unique_together = [["user", "org"], ["phone", "org"]]

    def __str__(self):
        return f"{self.user.email} <{self.org.name}>"

    @property
    def is_admin(self):
        return self.is_organization_admin

    @property
    def user_details(self):
        return {
            "email": self.user.email,
            "id": self.user.id,
            "is_active": self.user.is_active,
            "profile_pic": self.user.profile_pic,
            "last_login": self.user.last_login,
        }


class Comment(BaseModel):
    """
    使用 ContentType 框架的通用评论模型。
    可以附加到任何模型（客户、线索、联系人、商机、案例、任务、发票、个人资料）。
    """

    # 通用关系到任何模型
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="内容类型"
    )
    object_id = models.UUIDField(verbose_name="对象ID")
    content_object = GenericForeignKey("content_type", "object_id")

    comment = models.CharField(max_length=255, verbose_name="评论内容")
    commented_on = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    commented_by = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="评论者"
    )
    org = models.ForeignKey(
        "Org",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="组织"
    )

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        db_table = "comment"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.comment}"

    def clean(self):
        """
        验证评论的组织与内容对象的组织匹配。

        安全性：这可以防止跨组织数据引用，其中 org_a 中的评论可能引用 org_b 中的对象。
        """
        from django.core.exceptions import ValidationError

        if self.content_object and hasattr(self.content_object, "org"):
            if self.content_object.org_id != self.org_id:
                raise ValidationError(
                    {
                        "org": "评论的组织必须与被引用对象的组织匹配。"
                    }
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CommentFiles(BaseModel):
    """
    评论的文件附件。
    安全性：添加 org 字段以实现 RLS 保护和组织级隔离。
    """

    comment = models.ForeignKey(Comment,verbose_name="评论", on_delete=models.CASCADE)
    comment_file = models.FileField(
        _("文件"), upload_to="CommentFiles", null=True, blank=True
    )
    # 安全修复：添加 org 字段以实现 RLS 保护
    org = models.ForeignKey(
        "Org",
        on_delete=models.CASCADE,
        related_name="comment_files",
        null=True,  # 迁移期间暂时可为空
        blank=True,
        verbose_name="组织"
    )

    class Meta:
        verbose_name = "评论文件"
        verbose_name_plural = "评论文件"
        db_table = "commentFiles"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.comment.comment}"

    def save(self, *args, **kwargs):
        # 如果未设置，自动从父评论填充 org
        if not self.org_id and self.comment_id:
            self.org_id = self.comment.org_id
        super().save(*args, **kwargs)


class Attachments(BaseModel):
    """
    使用 ContentType 框架的通用附件模型。
    可以附加到任何模型（客户、线索、联系人、商机、案例、任务、发票）。
    """

    # 通用关系到任何模型
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="attachments"
    )
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    file_name = models.CharField(max_length=60)
    attachment = models.FileField(max_length=1001, upload_to="attachments/%Y/%m/")
    org = models.ForeignKey(
        "Org",
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    class Meta:
        verbose_name = "附件"
        verbose_name_plural = "附件"
        db_table = "attachments"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.file_name}"

    def file_type(self):
        name_ext_list = self.attachment.url.split(".")
        if len(name_ext_list) > 1:
            ext = name_ext_list[int(len(name_ext_list) - 1)]
            if is_document_file_audio(ext):
                return ("audio", "fa fa-file-audio")
            if is_document_file_video(ext):
                return ("video", "fa fa-file-video")
            if is_document_file_image(ext):
                return ("image", "fa fa-file-image")
            if is_document_file_pdf(ext):
                return ("pdf", "fa fa-file-pdf")
            if is_document_file_code(ext):
                return ("code", "fa fa-file-code")
            if is_document_file_text(ext):
                return ("text", "fa fa-file-alt")
            if is_document_file_sheet(ext):
                return ("sheet", "fa fa-file-excel")
            if is_document_file_zip(ext):
                return ("zip", "fa fa-file-archive")
            return ("file", "fa fa-file")
        return ("file", "fa fa-file")

    def clean(self):
        """
        验证附件的组织与内容对象的组织匹配。

        安全性：这可以防止跨组织数据引用，其中 org_a 中的附件可能引用 org_b 中的对象。
        """
        from django.core.exceptions import ValidationError

        if self.content_object and hasattr(self.content_object, "org"):
            if self.content_object.org_id != self.org_id:
                raise ValidationError(
                    {
                        "org": "附件的组织必须与被引用对象的组织匹配。"
                    }
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


def document_path(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("docs", hash_, filename)


class Document(BaseModel):

    DOCUMENT_STATUS_CHOICE = (("active", "活跃"), ("inactive", "不活跃"))

    title = models.TextField(blank=True, null=True)
    document_file = models.FileField(upload_to=document_path, max_length=5000)
    status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default="active"
    )
    shared_to = models.ManyToManyField(Profile, related_name="document_shared_to")
    teams = models.ManyToManyField("Teams", related_name="document_teams")
    org = models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    class Meta:
        verbose_name = "文档"
        verbose_name_plural = "文档"
        db_table = "document"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title}"

    def file_type(self):
        name_ext_list = self.document_file.url.split(".")
        if len(name_ext_list) > 1:
            ext = name_ext_list[int(len(name_ext_list) - 1)]
            if is_document_file_audio(ext):
                return ("audio", "fa fa-file-audio")
            if is_document_file_video(ext):
                return ("video", "fa fa-file-video")
            if is_document_file_image(ext):
                return ("image", "fa fa-file-image")
            if is_document_file_pdf(ext):
                return ("pdf", "fa fa-file-pdf")
            if is_document_file_code(ext):
                return ("code", "fa fa-file-code")
            if is_document_file_text(ext):
                return ("text", "fa fa-file-alt")
            if is_document_file_sheet(ext):
                return ("sheet", "fa fa-file-excel")
            if is_document_file_zip(ext):
                return ("zip", "fa fa-file-archive")
            return ("file", "fa fa-file")
        return ("file", "fa fa-file")


def generate_key():
    # Security: Increased from 8 bytes (64 bits) to 32 bytes (256 bits)
    return binascii.hexlify(os.urandom(32)).decode()


class APISettings(BaseModel):
    title = models.TextField()
    # 安全性：增加 max_length 以容纳 32 字节密钥（64 个十六进制字符）
    apikey = models.CharField(max_length=64, blank=True)
    website = models.URLField(max_length=255, null=True)
    lead_assigned_to = models.ManyToManyField(
        Profile, related_name="lead_assignee_users"
    )
    tags = models.ManyToManyField(Tags, blank=True)
    org = models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        related_name="api_settings",
    )

    class Meta:
        verbose_name = "API设置"
        verbose_name_plural = "API设置"
        db_table = "apiSettings"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.apikey or self.apikey is None or self.apikey == "":
            self.apikey = generate_key()
        super().save(*args, **kwargs)


# Phase 3: JWT Token Tracking


class SessionToken(BaseModel):
    """跟踪活跃的 JWT 会话以实现安全性"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="session_tokens",
        verbose_name="用户"
    )
    token_jti = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="令牌ID")  # JWT ID
    refresh_token_jti = models.CharField(
        max_length=255, unique=True, db_index=True, null=True, blank=True, verbose_name="刷新令牌ID"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP地址")
    user_agent = models.TextField(blank=True, null=True, verbose_name="用户代理")
    expires_at = models.DateTimeField(verbose_name="过期时间")
    is_active = models.BooleanField(default=True, verbose_name="是否活跃")
    revoked_at = models.DateTimeField(null=True, blank=True, verbose_name="撤销时间")
    last_used_at = models.DateTimeField(auto_now=True, verbose_name="最后使用时间")

    class Meta:
        verbose_name = "会话令牌"
        verbose_name_plural = "会话令牌"
        db_table = "session_token"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["token_jti"]),
            models.Index(fields=["expires_at"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.token_jti[:8]}..."

    def revoke(self):
        """撤销此会话令牌"""
        from django.utils import timezone

        self.is_active = False
        self.revoked_at = timezone.now()
        self.save()

    @classmethod
    def cleanup_expired(cls):
        """删除过期的令牌（通过 cron/celery 调用）"""
        from django.utils import timezone

        return cls.objects.filter(expires_at__lt=timezone.now()).delete()


# Activity Tracking for Recent Activities Dashboard


class Activity(BaseModel):
    """跟踪所有 CRM 实体中的用户活动"""

    ACTION_CHOICES = (
        ("CREATE", "创建"),
        ("UPDATE", "更新"),
        ("DELETE", "删除"),
        ("VIEW", "查看"),
        ("COMMENT", "评论"),
        ("ASSIGN", "分配"),
    )

    ENTITY_TYPE_CHOICES = (
        ("Account", "客户"),
        ("Lead", "线索"),
        ("Contact", "联系人"),
        ("Opportunity", "商机"),
        ("Case", "案例"),
        ("Task", "任务"),
        ("Invoice", "发票"),
        ("Event", "事件"),
        ("Document", "文档"),
        ("Team", "团队"),
    )

    user = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities",
        verbose_name="用户"
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="操作")
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE_CHOICES, verbose_name="实体类型")
    entity_id = models.UUIDField(verbose_name="实体ID")
    entity_name = models.CharField(max_length=255, blank=True, default="", verbose_name="实体名称")
    description = models.TextField(blank=True, default="", verbose_name="描述")
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="activities", verbose_name="组织")

    class Meta:
        verbose_name = "活动"
        verbose_name_plural = "活动"
        db_table = "activity"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["org", "-created_at"]),
            models.Index(fields=["entity_type", "entity_id"]),
        ]

    def __str__(self):
        return f"{self.user} {self.get_action_display()} {self.entity_type}: {self.entity_name}"

    @property
    def created_on_arrow(self):
        return timesince(self.created_at) + " ago"


class Teams(BaseModel):
    name = models.CharField(max_length=100, verbose_name="名称")
    description = models.TextField(verbose_name="描述")
    users = models.ManyToManyField(Profile, related_name="user_teams", verbose_name="用户")
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="teams", verbose_name="组织")

    class Meta:
        verbose_name = "团队"
        verbose_name_plural = "团队"
        db_table = "teams"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name}"

    def get_users(self):
        return ",".join(
            [str(_id) for _id in list(self.users.values_list("id", flat=True))]
        )


class ContactFormSubmission(BaseModel):
    """
    网站联系表单提交。
    通过联系表单存储潜在客户的咨询。
    不受组织范围限制，因为这些是平台级别的提交。
    """

    name = models.CharField(max_length=255, verbose_name="姓名")
    email = models.EmailField(verbose_name="邮箱")
    message = models.TextField(verbose_name="消息")
    reason = models.CharField(
        max_length=100,
        choices=[
            ("general", "General Inquiry"),
            ("sales", "Sales Question"),
            ("support", "Technical Support"),
            ("partnership", "Partnership Opportunity"),
            ("other", "Other"),
        ],
        default="general",
        verbose_name="原因"
    )

    # Tracking fields
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP地址")
    user_agent = models.TextField(null=True, blank=True, verbose_name="用户代理")
    referrer = models.URLField(max_length=500, null=True, blank=True, verbose_name="来源页面")

    # Status tracking
    STATUS_CHOICES = [
        ("new", "New"),
        ("read", "Read"),
        ("replied", "Replied"),
        ("closed", "Closed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="状态")
    replied_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contact_replies",
        verbose_name="回复人"
    )
    replied_at = models.DateTimeField(null=True, blank=True, verbose_name="回复时间")

    class Meta:
        verbose_name = "Contact Form Submission"
        verbose_name_plural = "Contact Form Submissions"
        db_table = "contact_form_submission"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.email} ({self.reason})"


# Import SecurityAuditLog so Django discovers it for migrations
from common.audit_log import SecurityAuditLog
