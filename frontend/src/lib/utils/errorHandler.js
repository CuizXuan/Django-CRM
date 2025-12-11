/**
 * 友好的错误消息处理器 - 中文版
 */

export const errorTypes = {
  // 网络错误
  NETWORK_ERROR: '网络错误',
  TIMEOUT: '请求超时',
  OFFLINE: '网络连接已断开',

  // 权限错误
  PERMISSION_DENIED: '权限不足',
  UNAUTHORIZED: '未授权，请重新登录',
  FORBIDDEN: '访问被禁止',

  // 服务器错误
  SERVER_ERROR: '服务器错误',
  BAD_REQUEST: '请求参数错误',
  NOT_FOUND: '请求的资源不存在',
  CONFLICT: '数据冲突',

  // 业务逻辑错误
  VALIDATION_ERROR: '数据验证失败',
  DUPLICATE_ERROR: '数据已存在',
  RESOURCE_LIMIT: '资源数量已达上限',
  OPERATION_NOT_ALLOWED: '操作不被允许',

  // 通用错误
  UNKNOWN_ERROR: '未知错误'
};

export const friendlyMessages = {
  // 用户相关错误
  'user already in organization': '该用户已在组织中',
  'no user found with that email': '未找到使用该邮箱的用户',
  'you cannot change your own role': '您不能更改自己的角色',
  'you cannot remove yourself': '您不能移除自己',
  'organization must have at least one admin': '组织必须至少有一名管理员',

  // 团队相关错误
  'a team with this name already exists': '该名称的团队已存在',
  'team name is required': '团队名称为必填项',
  'team id is required': '团队ID为必填项',

  // 通用业务错误
  'email and role are required': '邮箱和角色为必填项',
  'user and role are required': '用户和角色为必填项',
  'user is required': '用户为必填项',
  'name is required': '姓名为必填项',
  'organization name is required': '组织名称为必填项',
  'team name is required': '团队名称为必填项',

  // 服务器响应错误
  'failed to load users': '加载用户失败',
  'failed to add user': '添加用户失败',
  'failed to edit role': '编辑角色失败',
  'failed to remove user': '移除用户失败',
  'failed to create team': '创建团队失败',
  'failed to update team': '更新团队失败',
  'failed to delete team': '删除团队失败',
  'failed to update profile': '更新个人资料失败',
  'failed to load organization settings': '加载组织设置失败',
  'failed to update settings': '更新设置失败',
  'failed to update org settings': '更新组织设置失败',
  'failed to create organization': '创建组织失败',

  // 网络相关
  'network error': '网络连接异常，请检查网络后重试',
  'timeout': '请求超时，请稍后重试',
  'failed to fetch': '网络请求失败'
};

/**
 * 获取友好的错误消息
 * @param {string|Error} error - 原始错误
 * @returns {string} 友好的错误消息
 */
export function getFriendlyErrorMessage(error) {
  const errorMessage = error instanceof Error ? error.message : String(error);
  const lowerMessage = errorMessage.toLowerCase();

  // 查找匹配的错误消息
  for (const [key, value] of Object.entries(friendlyMessages)) {
    if (lowerMessage.includes(key.toLowerCase())) {
      return value;
    }
  }

  // 根据错误类型返回友好消息
  if (lowerMessage.includes('network') || lowerMessage.includes('fetch')) {
    return '网络连接异常，请检查网络后重试';
  }

  if (lowerMessage.includes('timeout')) {
    return '请求超时，请稍后重试';
  }

  if (lowerMessage.includes('unauthorized') || lowerMessage.includes('401')) {
    return '登录已过期，请重新登录';
  }

  if (lowerMessage.includes('forbidden') || lowerMessage.includes('403')) {
    return '权限不足，请联系管理员';
  }

  if (lowerMessage.includes('not found') || lowerMessage.includes('404')) {
    return '请求的资源不存在';
  }

  if (lowerMessage.includes('server error') || lowerMessage.includes('500')) {
    return '服务器内部错误，请稍后重试';
  }

  // 返回原始错误或默认消息
  return errorMessage || '操作失败，请稍后重试';
}

/**
 * 根据HTTP状态码获取错误消息
 * @param {number} status - HTTP状态码
 * @returns {string} 错误消息
 */
export function getErrorMessageByStatus(status) {
  switch (status) {
    case 400:
      return '请求参数错误，请检查输入信息';
    case 401:
      return '未授权，请重新登录';
    case 403:
      return '权限不足，无法执行此操作';
    case 404:
      return '请求的资源不存在';
    case 409:
      return '数据冲突，请刷新后重试';
    case 422:
      return '数据验证失败，请检查输入';
    case 429:
      return '请求过于频繁，请稍后重试';
    case 500:
      return '服务器内部错误，请稍后重试';
    case 502:
      return '服务器网关错误，请稍后重试';
    case 503:
      return '服务暂时不可用，请稍后重试';
    default:
      return '请求失败，请稍后重试';
  }
}