📋 Django-CRM 项目中文翻译需求统计

  一、后端翻译需求（共23处）

  1. 接口返回提示和错误信息（12处）

  - accounts/views.py:
    客户创建/更新/删除成功、权限错误、邮件发送相关提示
  - common/utils.py: 需要修正和补充的行业选择、任务状态等翻译

  2. 模型字段和选择项（11处）

  - tasks/models.py:
    - BoardMember的ROLE_CHOICES（所有者、管理员、成员）
    - BoardTask的PRIORITY_CHOICES（低、中、高、紧急）
    - Task的STATUS_CHOICES和PRIORITY_CHOICES

  二、前端翻译需求（共47处）

  1. 布局和导航组件（15处）

  - AppSidebar.svelte: 侧边栏标题、菜单项、用户信息等
  - CrmDrawer.svelte: 抽屉组件文本

  2. 过滤器和搜索组件（12处）

  - FilterBar.svelte: 清除、筛选等按钮文本
  - SearchInput.svelte: 搜索占位符
  - SelectFilter.svelte: 选择占位符、全部标签
  - DateRangeFilter.svelte: 日期范围选项（今天、最近7天等）

  3. 表格和表单组件（10处）

  - CrmTable.svelte: 空数据提示
  - leads/+page.svelte: 表单占位符、来源选项
  - contacts/+page.svelte: 列标题

  4. 页面组件（10处）

  - login/+page.svelte: 登录页面标题和描述
  - dashboard组件: 仪表盘各面板文本

  三、特别需要注意的文件

  1. 分页组件 - Pagination.svelte
  2. 发票页面 - invoices/+page.svelte
  3. 工单页面 - cases/+page.svelte
  4. 任务页面 - tasks/+page.svelte
  5. 商机页面 - opportunities/+page.svelte

  四、实施建议

  1. 创建翻译文件结构:

    - Django后端：在 backend/crm/locale/zh_CN/LC_MESSAGES/
  创建翻译文件
    - 前端：配置Svelte i18n或使用国际化库
  2. 优先级排序:

    - 🚨 高优先级：用户界面直接可见的文本（按钮、标签、菜单）
    - ⚠️ 中优先级：表单验证和错误消息
    - 💡 低优先级：日志和系统内部消息
  3. 翻译文件生成:
  # Django后端生成翻译文件
  python manage.py makemessages -l zh_CN

  # 前端配置i18n
  npm install svelte-i18n

  总计需要翻译的文本内容：70处