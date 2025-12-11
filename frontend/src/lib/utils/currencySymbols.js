/**
 * 货币符号映射表
 */

export const CURRENCY_SYMBOLS = {
	// 人民币
	CNY: '¥',
	CNH: '¥',
	YUAN: '¥',

	// 美元
	USD: '$',

	// 欧元
	EUR: '€',

	// 英镑
	GBP: '£',

	// 日元
	JPY: '¥',

	// 韩元
	KRW: '₩',

	// 港币
	HKD: 'HK$',

	// 新台币
	TWD: 'NT$',

	// 新加坡元
	SGD: 'S$',

	// 加拿大元
	CAD: 'C$',

	// 澳元
	AUD: 'A$',

	// 其他常用货币
	INR: '₹',
	CHF: 'CHF',
	SEK: 'kr',
	NOK: 'kr',
	DKK: 'kr',
	PLN: 'zł',
	RUB: '₽',
	BRL: 'R$',
	MXN: '$',
	ZAR: 'R',
	THB: '฿',
	VND: '₫',
	IDR: 'Rp',
	MYR: 'RM',
	PHP: '₱',
};

/**
 * 获取货币符号
 * @param {string} currencyCode - 货币代码（如 CNY, USD）
 * @returns {string} 货币符号
 */
export function getCurrencySymbol(currencyCode) {
	return CURRENCY_SYMBOLS[currencyCode] || currencyCode || '';
}