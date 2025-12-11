# Python imports
import uuid

# Django imports
from common.models import models


class TimeAuditModel(models.Model):
    """记录创建和最后修改的时间"""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    class Meta:
        abstract = True


class UserAuditModel(models.Model):
    """记录创建和最后修改的用户"""

    created_by = models.ForeignKey(
        "common.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        verbose_name="创建人",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        "common.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        verbose_name="最后修改人",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class AuditModel(TimeAuditModel, UserAuditModel):
    """记录创建和最后修改的时间和用户"""

    class Meta:
        abstract = True
