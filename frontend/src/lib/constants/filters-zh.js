/**
 * 筛选选项常量（中文版）
 * @module lib/constants/filters-zh
 */

/** @type {{ value: string, label: string }[]} */
export const LEAD_STATUSES = [
	{ value: 'ALL', label: '全部状态' },
	{ value: 'ASSIGNED', label: '已分配' },
	{ value: 'IN_PROCESS', label: '处理中' },
	{ value: 'CONVERTED', label: '已转化' },
	{ value: 'RECYCLED', label: '已回收' },
	{ value: 'CLOSED', label: '已关闭' }
];

/** @type {{ value: string, label: string }[]} */
export const LEAD_SOURCES = [
	{ value: 'ALL', label: '全部来源' },
	{ value: 'call', label: '电话' },
	{ value: 'email', label: '邮件' },
	{ value: 'existing customer', label: '现有客户' },
	{ value: 'partner', label: '合作伙伴' },
	{ value: 'public relations', label: '公共关系' },
	{ value: 'campaign', label: '营销活动' },
	{ value: 'other', label: '其他' }
];

/** @type {{ value: string, label: string }[]} */
export const LEAD_RATINGS = [
	{ value: 'ALL', label: '全部评分' },
	{ value: 'HOT', label: '热门' },
	{ value: 'WARM', label: '温热' },
	{ value: 'COLD', label: '冷门' }
];

/** @type {{ value: string, label: string }[]} */
export const CASE_STATUSES = [
	{ value: 'ALL', label: '全部状态' },
	{ value: 'New', label: '新建' },
	{ value: 'Assigned', label: '已分配' },
	{ value: 'Pending', label: '待处理' },
	{ value: 'Closed', label: '已关闭' },
	{ value: 'Rejected', label: '已拒绝' },
	{ value: 'Duplicate', label: '重复' }
];

/** @type {{ value: string, label: string }[]} */
export const CASE_TYPES = [
	{ value: '', label: '选择类型' },
	{ value: 'Question', label: '问题' },
	{ value: 'Incident', label: '事件' },
	{ value: 'Problem', label: '问题' }
];

/** @type {{ value: string, label: string }[]} */
export const CASE_PRIORITIES = [
	{ value: '', label: '选择优先级' },
	{ value: 'Low', label: '低' },
	{ value: 'Normal', label: '普通' },
	{ value: 'High', label: '高' },
	{ value: 'Urgent', label: '紧急' }
];

/** @type {{ value: string, label: string }[]} */
export const ACCOUNT_STATUSES = [
	{ value: 'ALL', label: '全部状态' },
	{ value: 'ACTIVE', label: '活跃' },
	{ value: 'INACTIVE', label: '非活跃' },
	{ value: 'PENDING', label: '待定' }
];

/** @type {{ value: string, label: string }[]} */
export const OPPORTUNITY_STAGES = [
	{ value: 'ALL', label: '全部阶段' },
	{ value: 'PROSPECTING', label: '开拓中' },
	{ value: 'QUALIFICATION', label: '资格确认' },
	{ value: 'PROPOSAL', label: '提案阶段' },
	{ value: 'NEGOTIATION', label: '谈判中' },
	{ value: 'CLOSED_WON', label: '成功签约' },
	{ value: 'CLOSED_LOST', label: '失败关闭' }
];

/** @type {{ value: string, label: string }[]} */
export const TASK_STATUSES = [
	{ value: 'ALL', label: '全部状态' },
	{ value: 'NOT STARTED', label: '未开始' },
	{ value: 'IN PROGRESS', label: '进行中' },
	{ value: 'PENDING', label: '待处理' },
	{ value: 'COMPLETED', label: '已完成' },
	{ value: 'DEFERRED', label: '已延迟' }
];

/** @type {{ value: string, label: string }[]} */
export const TASK_PRIORITIES = [
	{ value: 'ALL', label: '全部优先级' },
	{ value: 'LOW', label: '低' },
	{ value: 'NORMAL', label: '普通' },
	{ value: 'HIGH', label: '高' },
	{ value: 'URGENT', label: '紧急' }
];

/** @type {{ value: string, label: string }[]} */
export const CURRENCY_CODES = [
	{ value: '', label: '选择币种' },
	{ value: 'USD', label: 'USD - 美元' },
	{ value: 'EUR', label: 'EUR - 欧元' },
	{ value: 'GBP', label: 'GBP - 英镑' },
	{ value: 'JPY', label: 'JPY - 日元' },
	{ value: 'CNY', label: 'CNY - 人民币' },
	{ value: 'HKD', label: 'HKD - 港币' },
	{ value: 'TWD', label: 'TWD - 台币' },
	{ value: 'KRW', label: 'KRW - 韩元' },
	{ value: 'SGD', label: 'SGD - 新加坡元' },
	{ value: 'AUD', label: 'AUD - 澳元' },
	{ value: 'CAD', label: 'CAD - 加元' },
	{ value: 'CHF', label: 'CHF - 瑞士法郎' },
	{ value: 'INR', label: 'INR - 卢比' },
	{ value: 'MYR', label: 'MYR - 马来西亚林吉特' },
	{ value: 'THB', label: 'THB - 泰铢' },
	{ value: 'AED', label: 'AED - 迪拉姆' },
	{ value: 'SAR', label: 'SAR - 沙特里亚尔' },
	{ value: 'BRL', label: 'BRL - 雷亚尔' },
	{ value: 'MXN', label: 'MXN - 墨西哥比索' },
	{ value: 'RUB', label: 'RUB - 卢布' }
];

/** @type {Record<string, string>} */
export const CURRENCY_SYMBOLS = {
	USD: '$',
	EUR: '€',
	GBP: '£',
	JPY: '¥',
	CNY: '¥',
	HKD: 'HK$',
	TWD: 'NT$',
	KRW: '₩',
	SGD: 'S$',
	AUD: 'A$',
	CAD: 'C$',
	CHF: 'Fr',
	INR: '₹',
	MYR: 'RM',
	THB: '฿',
	AED: 'د.إ',
	SAR: '﷼',
	BRL: 'R$',
	MXN: '$',
	RUB: '₽'
};