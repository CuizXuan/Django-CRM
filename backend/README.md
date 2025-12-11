BottleCRM 后端 - Django REST API
BottleCRM 的后端系统，一个基于 Django REST Framework 构建的多租户 CRM 平台。

技术栈
Django 4.2.1 - Web 框架

Django REST Framework 3.14.0 - API 工具包

PostgreSQL - 数据库 (psycopg2-binary 2.9.11)

Celery 5.5.3 - 异步任务队列

Redis 4.6.0 - Celery 的消息代理

djangorestframework-simplejwt 5.2.2 - JWT 认证

drf-spectacular 0.26.2 - OpenAPI/Swagger 文档

django-ses 3.5.0 - AWS SES 邮件后端

Sentry SDK 1.24.0 - 错误追踪

Django 应用
应用	描述
common	用户、组织、个人资料、评论、附件、文档模型
accounts	客户账户管理
leads	线索跟踪和转化
contacts	联系人管理
opportunity	销售管道和交易跟踪
cases	客户支持工单
tasks	任务管理
invoices	发票系统
events	日历事件
teams	团队管理
emails	邮件处理
planner	计划事件
boards	看板系统
marketing	新闻稿和联系表单
先决条件
Python 3.8+

PostgreSQL

Redis (用于 Celery)

virtualenv

安装
1. 创建并激活虚拟环境
bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
2. 安装依赖
bash
pip install -r requirements.txt
3. 配置环境变量
在 backend/ 目录中创建 .env 文件：

env
# Django
SECRET_KEY=你的密钥
ENV_TYPE=dev

# 数据库
DBNAME=bottlecrm
DBUSER=postgres
DBPASSWORD=root
DBHOST=localhost
DBPORT=5432

# 邮件
DEFAULT_FROM_EMAIL=noreply@bottlecrm.com
ADMIN_EMAIL=admin@bottlecrm.com

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# 域名
DOMAIN_NAME=http://localhost:8000
SWAGGER_ROOT_URL=http://localhost:8000
4. 设置数据库
bash
# 创建 PostgreSQL 数据库
sudo -u postgres psql
CREATE DATABASE bottlecrm WITH OWNER = postgres;
ALTER USER postgres WITH PASSWORD 'root';
\q

# 运行迁移
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser
5. 运行开发服务器
bash
python manage.py runserver
API 将在 http://localhost:8000 可用

运行 Celery
对于后台任务（邮件、通知），运行 Celery worker：

bash
celery -A crm worker --loglevel=INFO
API 文档
Swagger UI: http://localhost:8000/swagger-ui/

ReDoc: http://localhost:8000/api/schema/redoc/

Django 管理后台: http://localhost:8000/admin/

生成 Schema
要生成 OpenAPI schema 文件：

bash
python manage.py spectacular --file openapi.yml
架构
多租户
每个请求都在组织上下文中操作：

组织 (Org): 顶层租户容器

用户: 具有 USER 角色的普通成员

管理员: 具有 ADMIN 角色的组织管理员

超级管理员: 使用 @micropyramid.com 邮箱域名的用户具有平台级访问权限

认证
基于 JWT 的认证：

text
Authorization: Bearer <token>
组织 ID 嵌入在 JWT token 中（不作为头部发送）

访问令牌有效期：1 天

刷新令牌有效期：365 天

中间件
中间件链提供安全保护：

GetProfileAndOrg (common.middleware.get_company):

从 JWT token 声明中提取 org_id（不是头部 - 防止伪造）

验证用户在组织中具有活跃的成员资格

设置 request.profile 和 request.org

RequireOrgContext (common.middleware.rls_context):

为 RLS 设置 PostgreSQL 会话变量 app.current_org

每个请求后重置上下文

行级安全性 (RLS)
PostgreSQL RLS 作为纵深防御的一部分，提供数据库级的租户隔离。

工作原理
中间件设置上下文: SET app.current_org = '<org_id>'

RLS 策略过滤查询: 仅匹配 org_id 的行可见

故障安全设计: 空上下文返回零行（NULLIF 模式）

受保护的表（共 24 个）
类别	表
核心业务	lead, accounts, contacts, opportunity, case, task, invoice
支持功能	comment, attachments, document, teams, activity, tags, address, solution
看板	board, board_column, board_task, board_member
其他	apiSettings, account_email, emailLogs, invoice_history, security_audit_log
配置
RLS 在 common/rls/__init__.py 中配置：

python
from common.rls import RLS_CONFIG, get_enable_policy_sql

# 受保护的表列表
tables = RLS_CONFIG['tables']

# 在表上启用 RLS
cursor.execute(get_enable_policy_sql('my_table'))
管理命令
bash
# 检查所有表的 RLS 状态
python manage.py manage_rls --status

# 验证数据库用户是非超级用户（RLS 必需）
python manage.py manage_rls --verify-user

# 测试组织间的 RLS 隔离
python manage.py manage_rls --test

# 在所有配置的表上启用 RLS
python manage.py manage_rls --enable

# 禁用 RLS（仅用于调试）
python manage.py manage_rls --disable
关键：数据库用户设置
PostgreSQL 超级用户绕过所有 RLS 策略。 必须使用非超级用户：

sql
-- 创建应用用户
CREATE USER crm_app WITH PASSWORD 'your_secure_password';

-- 授予权限
GRANT CONNECT ON DATABASE bottlecrm TO crm_app;
GRANT USAGE ON SCHEMA public TO crm_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO crm_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO crm_app;

-- 未来表继承权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO crm_app;
更新 .env：

env
DBUSER=crm_app
DBPASSWORD=your_secure_password
Celery 任务和 RLS
后台任务不通过中间件，因此需要手动设置 RLS 上下文：

python
from common.tasks import set_rls_context

@app.task
def my_background_task(data_id, org_id):
    set_rls_context(org_id)  # 必需！
    obj = MyModel.objects.get(id=data_id)
    # ... 处理
为新表添加 RLS
将表名添加到 common/rls/__init__.py 中的 ORG_SCOPED_TABLES

使用 get_enable_policy_sql() 创建迁移

确保模型有 org = models.ForeignKey(Org, ...)

BaseModel 模式
所有模型都继承自 BaseModel (common.base.BaseModel)：

UUID 主键（不是整数 ID）

自动时间戳：created_at, updated_at

审计追踪：created_by, updated_by

组织隔离：org = models.ForeignKey(Org)

API 端点模式
text
GET/POST       /api/<模块>/              # 列表/创建
GET/PUT/DELETE /api/<模块>/<pk>/         # 详情/更新/删除
GET/POST       /api/<模块>/comment/<pk>/ # 评论
GET/POST       /api/<模块>/attachment/<pk>/ # 附件
项目结构
text
backend/
├── manage.py
├── requirements.txt
├── crm/                    # Django 项目设置
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
├── common/                 # 核心模型和工具
│   ├── models.py           # 用户、组织、个人资料等
│   ├── base.py             # BaseModel
│   ├── middleware/
│   └── tasks.py            # Celery 任务
├── accounts/
├── leads/
├── contacts/
├── opportunity/
├── cases/
├── tasks/
├── invoices/
├── events/
├── teams/
├── emails/
├── planner/
├── boards/
├── marketing/
├── templates/
└── static/
开发
代码质量
bash
# 格式化代码
black .

# 排序导入
isort .

# 运行测试
pytest
创建新应用
创建应用：

bash
python manage.py startapp myapp
在 crm/settings.py 的 INSTALLED_APPS 中添加

创建继承自 BaseModel 的模型：

python
from common.base import BaseModel
from common.models import Org

class MyModel(BaseModel):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    # ... 其他字段
始终按组织过滤查询：

python
queryset = MyModel.objects.filter(org=request.profile.org)
运行迁移：

bash
python manage.py makemigrations
python manage.py migrate
环境变量参考
变量	描述
SECRET_KEY	Django 密钥
ENV_TYPE	环境类型 (dev 或 prod)
DBNAME	PostgreSQL 数据库名
DBUSER	PostgreSQL 用户名
DBPASSWORD	PostgreSQL 密码
DBHOST	PostgreSQL 主机
DBPORT	PostgreSQL 端口
DEFAULT_FROM_EMAIL	默认发件人邮箱
ADMIN_EMAIL	管理员通知邮箱
CELERY_BROKER_URL	Celery 代理的 Redis URL
CELERY_RESULT_BACKEND	Celery 结果的 Redis URL
DOMAIN_NAME	应用域名
SWAGGER_ROOT_URL	Swagger 文档根 URL
故障排除
数据库连接问题
bash
# 检查 PostgreSQL 是否运行
sudo systemctl status postgresql

# 验证数据库是否存在
sudo -u postgres psql -l
迁移问题
bash
# 显示迁移状态
python manage.py showmigrations

# 重置迁移（仅限开发）
python manage.py migrate --fake <app> zero
Celery 不处理任务
bash
# 检查 Redis 是否运行
redis-cli ping

# 检查 Celery worker 日志
celery -A crm worker --loglevel=DEBUG
许可证
MIT 许可证 - 详见 LICENSE。