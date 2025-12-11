/**
 * 登录页 - 邮箱/密码登录
 *
 * Django endpoint: POST /api/auth/login/
 */

import axios from 'axios';
import { fail, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import { env as publicEnv } from '$env/dynamic/public';

// Cookie configuration
const COOKIE_OPTIONS = {
	path: '/',
	httpOnly: true,
	sameSite: 'lax'
};

/**
 * Get secure cookie options based on environment
 * @param {number} maxAge - Cookie max age in seconds
 * @returns {object} Cookie options with secure flag for production
 */
function getCookieOptions(maxAge) {
	return {
		...COOKIE_OPTIONS,
		secure: env.NODE_ENV === 'production',
		maxAge
	};
}

/** @type {import('@sveltejs/kit').ServerLoad} */
export async function load({ url, cookies }) {
	// 已登录直接跳转
	const jwtAccess = cookies.get('jwt_access');
	if (jwtAccess) {
		throw redirect(307, '/org');
	}

	const error = url.searchParams.get('error');
	return { error };
}

/** @type {import('./$types').Actions} */
export const actions = {
	login: async ({ request, cookies }) => {
		const formData = await request.formData();
		const email = formData.get('email')?.toString().trim();
		const password = formData.get('password')?.toString();

		if (!email || !password) {
			return fail(400, { error: '请输入邮箱和密码', action: 'login' });
		}

		// 后端基地址，默认指向本地 8000
		const apiUrl = publicEnv.PUBLIC_DJANGO_API_URL || 'http://localhost:8000';

		try {
			const response = await axios.post(
				`${apiUrl}/api/auth/login/`,
				{ email, password },
				{
					headers: { 'Content-Type': 'application/json' },
					timeout: 30000
				}
			);

			const { access_token, refresh_token, current_org } = response.data;

			// 记录 JWT
			cookies.set('jwt_access', access_token, getCookieOptions(60 * 60 * 24)); // 1 day
			cookies.set('jwt_refresh', refresh_token, getCookieOptions(60 * 60 * 24 * 365)); // 1 year

			// 若后端返回当前组织，则同步 org cookie
			if (current_org?.id) {
				cookies.set('org', current_org.id, {
					path: '/',
					sameSite: 'strict',
					maxAge: 60 * 60 * 24 * 365
				});
			} else {
				// 没有组织则清理旧 org cookie，跳转去创建组织
				cookies.delete('org', { path: '/' });
			}
		} catch (error) {
			console.error('登录失败:', error.response?.data || error.message);
			const message =
				error.response?.data?.error ||
				error.response?.data?.detail ||
				(Array.isArray(error.response?.data?.non_field_errors)
					? error.response.data.non_field_errors.join(', ')
					: error.response?.data?.non_field_errors) ||
				'邮箱或密码错误';

			return fail(error.response?.status || 400, { error: message, action: 'login' });
		}

		// 有组织走选择/切换页，没有组织直接去创建页
		if (cookies.get('org')) {
			throw redirect(303, '/org');
		}
		throw redirect(303, '/org/new');
	},
	register: async ({ request }) => {
		const formData = await request.formData();
		const email = formData.get('email')?.toString().trim();
		const password = formData.get('password')?.toString();
		const confirmPassword = formData.get('confirm_password')?.toString();

		if (!email || !password || !confirmPassword) {
			return fail(400, { error: '请填写完整信息', action: 'register' });
		}

		// 后端基地址，默认指向本地 8000
		const apiUrl = publicEnv.PUBLIC_DJANGO_API_URL || 'http://localhost:8000';

		try {
			await axios.post(
				`${apiUrl}/api/auth/register/`,
				{ email, password, confirm_password: confirmPassword },
				{
					headers: { 'Content-Type': 'application/json' },
					timeout: 30000
				}
			);
		} catch (error) {
			console.error('注册失败:', error.response?.data || error.message);
			const message =
				error.response?.data?.error ||
				error.response?.data?.detail ||
				(Array.isArray(error.response?.data?.non_field_errors)
					? error.response.data.non_field_errors.join(', ')
					: error.response?.data?.non_field_errors) ||
				error.response?.data?.password ||
				'注册失败，请检查邮箱或密码';

			return fail(error.response?.status || 400, { error: message, action: 'register' });
		}

		return { success: '注册成功，请查收邮箱激活账号后再登录', action: 'register' };
	}
};
