/**
 * 成功提示消息 - 中文版
 */

export const successMessages = {
  // 用户操作
  USER_ADDED: '用户添加成功',
  USER_REMOVED: '用户移除成功',
  USER_UPDATED: '用户信息更新成功',
  ROLE_CHANGED: '角色更改成功',
  PROFILE_UPDATED: '个人资料更新成功',

  // 团队操作
  TEAM_CREATED: '团队创建成功',
  TEAM_UPDATED: '团队更新成功',
  TEAM_DELETED: '团队删除成功',
  TEAM_MEMBER_ADDED: '成员添加成功',
  TEAM_MEMBER_REMOVED: '成员移除成功',

  // 认证操作
  LOGIN_SUCCESS: '登录成功',
  LOGOUT_SUCCESS: '退出成功',
  REGISTER_SUCCESS: '注册成功',
  PASSWORD_CHANGED: '密码修改成功',
  PASSWORD_RESET: '密码重置邮件已发送',

  // 数据操作
  DATA_SAVED: '数据保存成功',
  DATA_DELETED: '数据删除成功',
  DATA_IMPORTED: '数据导入成功',
  DATA_EXPORTED: '数据导出成功',

  // 文件操作
  FILE_UPLOADED: '文件上传成功',
  FILE_DOWNLOADED: '文件下载成功',
  FILE_DELETED: '文件删除成功',

  // 通用操作
  OPERATION_SUCCESS: '操作成功',
  CHANGES_SAVED: '更改已保存',
  ACTION_COMPLETED: '操作已完成',
  TASK_FINISHED: '任务完成',

  // 组织操作
  ORG_CREATED: '组织创建成功',
  ORG_UPDATED: '组织更新成功',
  ORG_SETTINGS_UPDATED: '组织设置更新成功',
  ORG_SELECTED: '组织选择成功'
};

/**
 * 获取成功消息
 * @param {string} action - 操作类型
 * @param {Object} params - 额外参数
 * @returns {string} 成功消息
 */
export function getSuccessMessage(action, params = {}) {
  let message = successMessages[action] || '操作成功';

  // 替换占位符
  if (params.name) {
    message = message.replace('{name}', params.name);
  }
  if (params.count) {
    message = message.replace('{count}', params.count);
  }

  return message;
}

/**
 * 根据操作类型生成成功消息
 * @param {string} operation - 操作名称
 * @param {string} target - 操作目标
 * @param {string} result - 操作结果
 * @returns {string} 成功消息
 */
export function generateSuccessMessage(operation, target, result = '成功') {
  const operations = {
    create: '创建',
    update: '更新',
    delete: '删除',
    add: '添加',
    remove: '移除',
    edit: '编辑',
    save: '保存'
  };

  const targets = {
    user: '用户',
    team: '团队',
    profile: '个人资料',
    role: '角色',
    member: '成员',
    data: '数据',
    file: '文件',
    record: '记录',
    organization: '组织',
    org: '组织'
  };

  const opText = operations[operation] || operation;
  const targetText = targets[target] || target;

  return `${targetText}${opText}${result}`;
}