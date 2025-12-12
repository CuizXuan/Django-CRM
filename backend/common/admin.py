from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from common.models import Address, Comment, CommentFiles, SessionToken, User

# Register your models here.

admin.site.register(User)
admin.site.register(Address)


class CommentAdminForm(forms.ModelForm):
    """自定义评论表单，将对象ID改为下拉选择"""

    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
            'object_id': forms.Select(),  # 将object_id改为下拉选择
        }
        field_classes = {
            'object_id': forms.UUIDField,
        }

    def clean(self):
        """自定义验证逻辑"""
        cleaned_data = super().clean()

        # 如果选择了content_type但没有选择object_id，报错
        content_type = cleaned_data.get('content_type')
        object_id = cleaned_data.get('object_id')

        # 只有当选择了content_type时，object_id才是必填的
        if content_type and not object_id:
            raise forms.ValidationError({
                'object_id': '请选择具体的对象。'
            })

        # 如果没有选择content_type，清除object_id的值（避免无效的UUID）
        if not content_type and object_id:
            cleaned_data['object_id'] = None

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 动态设置object_id字段的required属性
        # 默认情况下，object_id不是必填的（除非选择了content_type）
        self.fields['object_id'].required = False

        # 如果是编辑现有实例，显示对应的对象
        if self.instance and self.instance.pk:
            # 检查是否有content_type
            if hasattr(self.instance, 'content_type_id') and self.instance.content_type_id:
                try:
                    # 直接通过content_type_id获取ContentType
                    from django.contrib.contenttypes.models import ContentType
                    content_type = ContentType.objects.get(pk=self.instance.content_type_id)
                    self._update_object_id_choices(content_type)

                    # 确保当前选中的值在下拉列表中
                    if self.instance.object_id:
                        object_id_str = str(self.instance.object_id)
                        current_choices = [choice[0] for choice in self.fields['object_id'].choices]
                        if object_id_str not in current_choices:
                            # 如果不在列表中，添加它
                            self.fields['object_id'].choices.append(
                                (object_id_str, f'当前选择: {object_id_str}')
                            )
                            # 同时更新widget的choices
                            self.fields['object_id'].widget.choices = self.fields['object_id'].choices
                except Exception as e:
                    # 如果出错，记录日志并显示错误信息
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"编辑评论时加载对象失败: {str(e)}", exc_info=True)
                    self.fields['object_id'].choices = [('', f'加载失败: {str(e)}')]
                    self.fields['object_id'].widget.choices = [('', f'加载失败: {str(e)}')]
            else:
                # 没有content_type的情况
                self.fields['object_id'].choices = [('', '请选择内容类型')]
                self.fields['object_id'].widget.choices = [('', '请选择内容类型')]
        else:
            # 新建实例时的处理
            content_type_id = None

            # 从POST数据中获取content_type
            if hasattr(self, 'data') and self.data and 'content_type' in self.data:
                content_type_id = self.data.get('content_type')
            # 从initial中获取
            elif hasattr(self, 'initial') and 'content_type' in self.initial:
                content_type_id = self.initial.get('content_type')
            # 从URL参数中获取（在get_form中处理）
            elif 'content_type' in self.fields:
                content_type_id = self.fields['content_type'].initial

            if content_type_id:
                # 如果有content_type，加载对应的对象
                try:
                    content_type = ContentType.objects.get(pk=content_type_id)
                    self._update_object_id_choices(content_type)

                    # 自动选择第一个有效对象（因为object_id是必填的）
                    if self.fields['object_id'].choices and len(self.fields['object_id'].choices) > 1:
                        # 选择第一个非空选项
                        first_choice = self.fields['object_id'].choices[1][0]
                        self.initial['object_id'] = first_choice

                        # 如果是POST请求，更新data字典
                        if hasattr(self, 'data') and self.data:
                            # 将QueryDict转换为可修改的字典
                            data_copy = self.data.copy()
                            data_copy['object_id'] = first_choice
                            self.data = data_copy
                except (ContentType.DoesNotExist, ValueError):
                    self.fields['object_id'].choices = [('', '无效的内容类型')]
                    self.fields['object_id'].widget.choices = [('', '无效的内容类型')]
                    self.initial['object_id'] = ''
            else:
                # 没有content_type时的默认显示
                self.fields['object_id'].choices = [('', '请先选择内容类型')]
                self.fields['object_id'].widget.choices = [('', '请先选择内容类型')]
                self.initial['object_id'] = ''

    def _update_object_id_choices(self, content_type):
        """根据选择的content_type更新object_id的选择项"""
        if not content_type:
            if 'object_id' in self.fields:
                self.fields['object_id'].choices = [('', '---------')]
                self.fields['object_id'].widget.choices = [('', '---------')]
            return

        try:
            # 确保object_id字段存在
            if 'object_id' not in self.fields:
                return

            model_class = content_type.model_class()
            if model_class:
                # 限制查询数量，避免数据过多时性能问题
                try:
                    if content_type.model == 'user':
                        # 对于用户模型，按邮箱排序
                        objects = model_class.objects.order_by('email')[:100]
                    else:
                        # 其他模型按创建时间排序
                        objects = model_class.objects.order_by('-created_at')[:100]
                except Exception:
                    # 如果排序失败，使用默认排序
                    objects = model_class.objects.all()[:100]

                # 构建选择项列表
                choices = [('', '---------')]  # 默认空选项

                for obj in objects:
                    # 确保对象有有效的pk
                    if not obj.pk:
                        continue

                    # 尝试获取对象的显示名称
                    try:
                        if hasattr(obj, 'email') and obj.email:
                            # 对于用户，显示邮箱
                            display_name = f"{obj.email} - {str(obj)}"
                        elif hasattr(obj, 'name') and obj.name:
                            display_name = obj.name
                        elif hasattr(obj, 'subject') and obj.subject:
                            display_name = obj.subject
                        elif hasattr(obj, 'title') and obj.title:
                            display_name = obj.title
                        else:
                            display_name = str(obj)

                        # 如果显示名称太长，截断它
                        if len(display_name) > 100:
                            display_name = display_name[:100] + '...'

                        choices.append((str(obj.pk), display_name))
                    except Exception:
                        # 如果获取显示名称失败，使用pk作为显示
                        choices.append((str(obj.pk), f'对象 {obj.pk}'))

                # 更新object_id字段的选择项，同时更新widget
                self.fields['object_id'].choices = choices
                self.fields['object_id'].widget.choices = choices

                # 如果有选中的值，确保它在选择项中
                if self.instance and hasattr(self.instance, 'object_id') and self.instance.object_id:
                    object_id_str = str(self.instance.object_id)
                    if object_id_str not in [choice[0] for choice in choices]:
                        # 如果当前值不在新选择项中（可能是对象被删除或超过100条限制）
                        choices.append((object_id_str, f'对象ID: {object_id_str}'))
                        self.fields['object_id'].choices = choices
                        self.fields['object_id'].widget.choices = choices
            else:
                self.fields['object_id'].choices = [('', '无效的模型类型')]
                self.fields['object_id'].widget.choices = [('', '无效的模型类型')]
        except Exception as e:
            # 如果出现错误，提供空的选择项
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"加载对象列表失败: {str(e)}", exc_info=True)
            if 'object_id' in self.fields:
                self.fields['object_id'].choices = [('', f'加载失败: {str(e)}')]
                self.fields['object_id'].widget.choices = [('', f'加载失败: {str(e)}')]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """自定义评论管理界面

    使用说明：
    1. 先选择"内容类型"
    2. 保存表单（此时会自动加载对应类型的对象列表到"对象ID"下拉框）
    3. 编辑评论，从下拉列表中选择具体的对象
    4. 填写评论内容并保存
    """
    form = CommentAdminForm

    # 列表显示字段
    list_display = (
        'content_type',
        'get_object_display',
        'comment',
        'commented_by',
        'commented_on',
        'org',
    )

    class Media:
        """添加CSS样式"""
        css = {
            'all': ('admin/css/comment-admin.css',)
        }

    # 列表过滤器
    list_filter = (
        'content_type',
        'commented_on',
        'org',
    )

    # 搜索字段
    search_fields = (
        'comment',
        'commented_by__user__email',
    )

    # 只读字段
    readonly_fields = ('commented_on',)

    # 字段分组显示
    fieldsets = (
        (_('基本信息'), {
            'fields': ('content_type', 'object_id', 'org'),
            'description': '使用说明：1. 先选择"内容类型"；2. 保存表单后会加载对应对象列表；3. 重新编辑可选择具体的对象。'
        }),
        (_('评论内容'), {
            'fields': ('comment', 'commented_by', 'commented_on'),
        }),
    )

    def get_object_display(self, obj):
        """在列表中显示关联的对象"""
        if obj.content_object:
            return str(obj.content_object)[:50]  # 限制显示长度
        return f"对象ID: {obj.object_id}"
    get_object_display.short_description = '关联对象'

    def get_form(self, request, obj=None, **kwargs):
        """重写get_form以传递当前用户信息"""
        try:
            form = super().get_form(request, obj, **kwargs)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"创建表单失败: {str(e)}", exc_info=True)
            raise

        # 如果是新建评论，可以预设评论者
        if not obj and hasattr(request, 'user'):
            try:
                from common.models import Profile
                profile = Profile.objects.filter(user=request.user).first()
                if profile and 'commented_by' in form.base_fields:
                    form.base_fields['commented_by'].initial = profile
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"设置默认评论者失败: {str(e)}")

        # 如果有org参数，预设组织
        if not obj and 'org' in request.GET:
            try:
                org_id = request.GET.get('org')
                if org_id and 'org' in form.base_fields:
                    form.base_fields['org'].initial = org_id
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"设置默认组织失败: {str(e)}")

        # 如果有URL中的content_type参数，设置初始值
        if not obj and 'content_type' in request.GET:
            try:
                content_type_id = request.GET.get('content_type')
                if content_type_id and 'content_type' in form.base_fields:
                    # 验证content_type_id是否是有效的整数
                    try:
                        content_type_id = int(content_type_id)
                        # 设置content_type的初始值
                        form.base_fields['content_type'].initial = content_type_id

                        # 加载对应的对象列表
                        content_type = ContentType.objects.get(pk=content_type_id)
                        form._update_object_id_choices(content_type)
                    except (ValueError, ContentType.DoesNotExist) as e:
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.warning(f"加载内容类型失败: {str(e)}")
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"处理content_type参数时出错: {str(e)}", exc_info=True)

        return form


admin.site.register(CommentFiles)


@admin.register(SessionToken)
class SessionTokenAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "token_jti_short",
        "is_active",
        "expires_at",
        "last_used_at",
        "created_at",
    )
    list_filter = ("is_active", "expires_at", "created_at")
    search_fields = ("user__email", "token_jti", "ip_address")
    raw_id_fields = ("user",)
    readonly_fields = (
        "token_jti",
        "refresh_token_jti",
        "created_at",
        "last_used_at",
        "revoked_at",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    actions = ["revoke_tokens", "cleanup_expired"]

    def token_jti_short(self, obj):
        return f"{obj.token_jti[:16]}..."

    token_jti_short.short_description = "Token JTI"

    def revoke_tokens(self, request, queryset):
        for token in queryset:
            token.revoke()
        self.message_user(request, f"{queryset.count()} tokens revoked successfully.")

    revoke_tokens.short_description = "Revoke selected tokens"

    def cleanup_expired(self, request, queryset):
        count, _ = SessionToken.cleanup_expired()
        self.message_user(request, f"{count} expired tokens cleaned up.")

    cleanup_expired.short_description = "Cleanup expired tokens"
