from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Account
from common.base import AssignableMixin, BaseModel
from common.models import Org, Profile, Tags, Teams
from contacts.models import Contact


# Cleanup notes:
# - Removed 'created_on_arrow' property from Task model (frontend computes its own timestamps)


class Board(BaseModel):
    """Kanban Board"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="owned_boards"
    )
    members = models.ManyToManyField(
        Profile, through="BoardMember", related_name="boards"
    )
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="boards")
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = "看板"
        verbose_name_plural = "看板"
        db_table = "board"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        return self.name


class BoardMember(BaseModel):
    """Board membership with roles"""

    ROLE_CHOICES = (
        ("owner", _("所有者")),
        ("admin", _("管理员")),
        ("member", _("成员")),
    )

    board = models.ForeignKey(
        Board, on_delete=models.CASCADE, related_name="memberships"
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="board_memberships"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    org = models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        related_name="board_members",
    )

    class Meta:
        verbose_name = "看板成员"
        verbose_name_plural = "看板成员"
        db_table = "board_member"
        unique_together = ("board", "profile")
        indexes = [
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.profile} - {self.board} ({self.role})"

    def save(self, *args, **kwargs):
        if not self.org_id and self.board_id:
            self.org_id = self.board.org_id
        super().save(*args, **kwargs)


class BoardColumn(BaseModel):
    """Column in a board (e.g., To Do, In Progress, Done)"""

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=7, default="#6B7280")  # Hex color
    limit = models.PositiveIntegerField(null=True, blank=True)  # WIP limit
    org = models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        related_name="board_columns",
    )

    class Meta:
        verbose_name = "看板列"
        verbose_name_plural = "看板列"
        db_table = "board_column"
        ordering = ("order",)
        unique_together = ("board", "name")
        indexes = [
            models.Index(fields=["org", "order"]),
        ]

    def __str__(self):
        return f"{self.board.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.org_id and self.board_id:
            self.org_id = self.board.org_id
        super().save(*args, **kwargs)


class BoardTask(BaseModel):
    """Task/Card in a board column"""

    PRIORITY_CHOICES = (
        ("low", _("低")),
        ("medium", _("中")),
        ("high", _("高")),
        ("urgent", _("紧急")),
    )

    column = models.ForeignKey(
        BoardColumn, on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    assigned_to = models.ManyToManyField(
        Profile, related_name="assigned_board_tasks", blank=True
    )
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Link to CRM entities (optional)
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="board_tasks",
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="board_tasks",
    )
    opportunity = models.ForeignKey(
        "opportunity.Opportunity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="board_tasks",
    )
    org = models.ForeignKey(
        Org,
        on_delete=models.CASCADE,
        related_name="board_tasks",
    )

    class Meta:
        verbose_name = "看板任务"
        verbose_name_plural = "看板任务"
        db_table = "board_task"
        ordering = ("order",)
        indexes = [
            models.Index(fields=["org", "order"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.org_id and self.column_id:
            self.org_id = self.column.board.org_id
        super().save(*args, **kwargs)

    @property
    def is_completed(self):
        return self.completed_at is not None

    @property
    def is_overdue(self):
        from django.utils import timezone

        if self.due_date and not self.is_completed:
            return timezone.now() > self.due_date
        return False



class Task(AssignableMixin, BaseModel):

    STATUS_CHOICES = (
        ("New", _("新建")),
        ("In Progress", _("进行中")),
        ("Completed", _("已完成")),
    )

    PRIORITY_CHOICES = (("Low", _("低")), ("Medium", _("中")), ("High", _("高")))

    title = models.CharField(_("title"), max_length=200)
    status = models.CharField(_("status"), max_length=50, choices=STATUS_CHOICES)
    priority = models.CharField(_("priority"), max_length=50, choices=PRIORITY_CHOICES)
    due_date = models.DateField(blank=True, null=True)
    description = models.TextField(_("Notes"), blank=True, null=True)
    account = models.ForeignKey(
        Account,
        related_name="accounts_tasks",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    opportunity = models.ForeignKey(
        "opportunity.Opportunity",
        related_name="opportunity_tasks",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    case = models.ForeignKey(
        "cases.Case",
        related_name="case_tasks",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    lead = models.ForeignKey(
        "leads.Lead",
        related_name="lead_tasks",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    contacts = models.ManyToManyField(Contact, related_name="task_contacts")

    assigned_to = models.ManyToManyField(Profile, related_name="task_assigned_users")
    teams = models.ManyToManyField(Teams, related_name="tasks_teams")
    tags = models.ManyToManyField(Tags, related_name="task_tags", blank=True)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = "任务"
        db_table = "task"
        ordering = ("-due_date",)
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["due_date"]),
            models.Index(fields=["org", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.title}"

    def clean(self):
        """Validate that task has at most one parent entity."""
        super().clean()
        parent_fields = ["account", "opportunity", "case", "lead"]
        set_parents = [
            field for field in parent_fields if getattr(self, f"{field}_id", None)
        ]
        if len(set_parents) > 1:
            raise ValidationError(
                {
                    "account": _(
                        "A task can only be linked to one parent entity "
                        "(Account, Opportunity, Case, or Lead). "
                        f"Currently linked to: {', '.join(set_parents)}"
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
