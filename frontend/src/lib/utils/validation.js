/**
 * 表单验证提示消息 - 中文版
 */

export const validationMessages = {
  // 通用验证
  required: '此字段为必填项',
  invalid: '请输入有效的值',

  // 邮箱验证
  email: {
    required: '请输入邮箱地址',
    invalid: '请输入有效的邮箱地址'
  },

  // 电话号码验证
  phone: {
    required: '请输入电话号码',
    invalid: '请输入有效的电话号码',
    invalidWithCountry: '请输入有效的电话号码（包含国家代码，如中国+86）'
  },

  // 姓名验证
  name: {
    required: '请输入姓名',
    tooShort: '姓名至少需要2个字符',
    tooLong: '姓名不能超过50个字符'
  },

  // 团队名称验证
  teamName: {
    required: '请输入团队名称',
    tooShort: '团队名称至少需要2个字符',
    tooLong: '团队名称不能超过100个字符'
  },

  // 角色验证
  role: {
    required: '请选择角色'
  },

  // 密码验证
  password: {
    required: '请输入密码',
    tooShort: '密码至少需要8个字符',
    noNumber: '密码必须包含至少一个数字',
    noUppercase: '密码必须包含至少一个大写字母',
    noLowercase: '密码必须包含至少一个小写字母',
    noSpecial: '密码必须包含至少一个特殊字符'
  },

  // 确认密码
  passwordConfirm: {
    required: '请确认密码',
    mismatch: '两次输入的密码不一致'
  }
};

/**
 * 获取验证错误消息
 * @param {string} field - 字段类型
 * @param {string} type - 错误类型
 * @param {Object} params - 额外参数
 * @returns {string} 错误消息
 */
export function getValidationMessage(field, type, params = {}) {
  if (validationMessages[field] && validationMessages[field][type]) {
    let message = validationMessages[field][type];

    // 替换占位符
    if (params.min) {
      message = message.replace('{min}', params.min);
    }
    if (params.max) {
      message = message.replace('{max}', params.max);
    }

    return message;
  }

  return validationMessages[type] || '输入无效';
}