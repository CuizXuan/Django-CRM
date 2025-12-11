<svelte:options runes={true} />

<script>
	import '../../../app.css';

	import imgLogo from '$lib/assets/images/logo.png';
	import {
		Users,
		BarChart3,
		CheckCircle2,
		TrendingUp,
		Shield,
		Lock,
		ArrowRight,
		Sparkles,
		Building2,
		Target,
		PieChart
	} from '@lucide/svelte';

	let { data, form } = $props();
	let isLoading = $state(false);
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let mode = $state('login'); // 'login' | 'register'

	const features = [
		{
			icon: Users,
			title: '客户管理',
			description: '集中管理客户信息，随时掌握联系记录'
		},
		{
			icon: Target,
			title: '销售管道',
			description: '清晰展示商机阶段，实时追踪进度'
		},
		{
			icon: BarChart3,
			title: '数据洞察',
			description: '可视化报表与仪表盘，助力决策'
		},
		{
			icon: Building2,
			title: '多组织协同',
			description: '一个账号管理多家公司与团队'
		}
	];

	const stats = [
		{ value: '10K+', label: '活跃用户' },
		{ value: '500K+', label: '客户记录' },
		{ value: '99.9%', label: '系统可用性' }
	];

	const actionName = $derived(form?.action);
	const loginError = $derived(actionName === 'login' ? form?.error || data?.error : null);
	const registerError = $derived(actionName === 'register' ? form?.error : null);
	const registerSuccess = $derived(actionName === 'register' ? form?.success : null);

	$effect(() => {
		// 根据上次提交的表单切换模式
		if (actionName === 'register') {
			mode = 'register';
		} else if (actionName === 'login') {
			mode = 'login';
		}
	});

	$effect(() => {
		// 动作完成后停止 loading
		if (form && !form?.pending) {
			isLoading = false;
		}
	});

	function handleSubmit() {
		isLoading = true;
	}
</script>

<svelte:head>
	<title>登录 | BottleCRM</title>
	<meta
		name="description"
		content="使用邮箱和密码登录 BottleCRM，管理客户、商机与团队协作。"
	/>
</svelte:head>

<div class="flex min-h-screen">
	<!-- Left Panel - Branding & Features -->
	<div class="relative hidden w-1/2 overflow-hidden bg-slate-900 lg:flex lg:flex-col">
		<!-- Subtle gradient overlay -->
		<div class="absolute inset-0 bg-gradient-to-br from-blue-600/20 via-transparent to-purple-600/20"></div>

		<!-- Grid pattern background -->
		<div class="absolute inset-0 opacity-[0.03]" style="background-image: url(&quot;data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E&quot;);"></div>

		<!-- Content -->
		<div class="relative z-10 flex flex-1 flex-col justify-between p-12">
			<!-- Top - Logo -->
			<div>
				<div class="flex items-center gap-3">
					<img src={imgLogo} alt="BottleCRM" class="h-10 w-auto" />
					<span class="text-xl font-semibold text-white">BottleCRM</span>
				</div>
			</div>

			<!-- Middle - Features -->
			<div class="space-y-8">
				<div>
					<h1 class="text-4xl font-bold leading-tight text-white">
						专为成长团队打造的
						<span class="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
							现代化 CRM
						</span>
					</h1>
					<p class="mt-4 text-lg text-slate-400">
						开源、直观、安全，帮助团队高效管理客户关系，持续增长。
					</p>
				</div>

				<div class="grid gap-4">
					{#each features as feature}
						<div class="group flex items-start gap-4 rounded-xl border border-slate-800 bg-slate-800/50 p-4 transition-all hover:border-slate-700 hover:bg-slate-800">
							<div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400">
								{#snippet featureIcon(/** @type {any} */ icon)}
									{@const Icon = icon}
									<Icon class="h-5 w-5" />
								{/snippet}
								{@render featureIcon(feature.icon)}
							</div>
							<div>
								<h3 class="font-semibold text-white">{feature.title}</h3>
								<p class="mt-1 text-sm text-slate-400">{feature.description}</p>
							</div>
						</div>
					{/each}
				</div>
			</div>

			<!-- Bottom - Stats -->
			<div class="border-t border-slate-800 pt-8">
				<div class="grid grid-cols-3 gap-8">
					{#each stats as stat}
						<div>
							<div class="text-2xl font-bold text-white">{stat.value}</div>
							<div class="text-sm text-slate-500">{stat.label}</div>
						</div>
					{/each}
				</div>
			</div>
		</div>
	</div>

	<!-- Right Panel - Login Form -->
	<div class="flex w-full flex-col bg-white lg:w-1/2">
		<!-- Mobile Header -->
		<div class="flex items-center justify-between border-b border-slate-100 p-4 lg:hidden">
			<div class="flex items-center gap-2">
				<img src={imgLogo} alt="BottleCRM" class="h-8 w-auto" />
				<span class="font-semibold text-slate-900">BottleCRM</span>
			</div>
		</div>

		<!-- Login Form Container -->
		<div class="flex flex-1 items-center justify-center p-8">
			<div class="w-full max-w-sm">
				<!-- Header -->
				<div class="mb-8 text-center">
					<div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-blue-50">
						<Sparkles class="h-6 w-6 text-blue-600" />
					</div>
					<h2 class="text-2xl font-bold text-slate-900">欢迎回来</h2>
					<p class="mt-2 text-slate-600">使用邮箱和密码登录，继续你的工作</p>
				</div>

				<!-- Mode Switch -->
				<div class="mb-6 grid grid-cols-2 rounded-lg bg-slate-50 p-1 text-sm font-semibold text-slate-600">
					<button
						type="button"
						class={`rounded-md px-3 py-2 transition ${mode === 'login' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
						onclick={() => (mode = 'login')}
					>
						登录
					</button>
					<button
						type="button"
						class={`rounded-md px-3 py-2 transition ${mode === 'register' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
						onclick={() => (mode = 'register')}
					>
						注册
					</button>
				</div>

				{#if mode === 'login'}
					<form method="POST" action="?/login" class="space-y-6" onsubmit={handleSubmit}>

						{#if loginError}
							<div class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
								{loginError}
							</div>
						{/if}

						<div class="space-y-2">
							<label for="email" class="block text-sm font-medium text-slate-700">邮箱</label>
							<input
								id="email"
								name="email"
								type="email"
								class="block w-full rounded-lg border border-slate-200 px-3.5 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
								placeholder="请输入邮箱"
								bind:value={email}
								required
							/>
						</div>

						<div class="space-y-2">
							<label for="password" class="block text-sm font-medium text-slate-700">密码</label>
							<input
								id="password"
								name="password"
								type="password"
								class="block w-full rounded-lg border border-slate-200 px-3.5 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
								placeholder="请输入密码"
								bind:value={password}
								required
							/>
						</div>

						<button
							type="submit"
							class="group relative flex w-full items-center justify-center gap-3 rounded-lg bg-blue-600 px-4 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-70"
							disabled={isLoading}
						>
							{#if isLoading}
								<div class="h-5 w-5 animate-spin rounded-full border-2 border-white/60 border-t-white"></div>
								<span>正在登录...</span>
							{:else}
								<span>登录</span>
								<ArrowRight class="ml-auto h-4 w-4 text-white/80 transition-transform group-hover:translate-x-0.5" />
							{/if}
						</button>
					</form>
				{:else}
					<form method="POST" action="?/register" class="space-y-6" onsubmit={handleSubmit}>
						{#if registerError}
							<div class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
								{registerError}
							</div>
						{/if}

						{#if registerSuccess}
							<div class="rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
								{registerSuccess}
							</div>
						{/if}

						<div class="space-y-2">
							<label for="register-email" class="block text-sm font-medium text-slate-700">邮箱</label>
							<input
								id="register-email"
								name="email"
								type="email"
								class="block w-full rounded-lg border border-slate-200 px-3.5 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
								placeholder="请输入邮箱"
								required
							/>
						</div>

						<div class="space-y-2">
							<label for="register-password" class="block text-sm font-medium text-slate-700">密码（至少 8 位）</label>
							<input
								id="register-password"
								name="password"
								type="password"
								minlength="8"
								class="block w-full rounded-lg border border-slate-200 px-3.5 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
								placeholder="请输入密码"
								bind:value={password}
								required
							/>
						</div>

						<div class="space-y-2">
							<label for="register-confirm" class="block text-sm font-medium text-slate-700">确认密码</label>
							<input
								id="register-confirm"
								name="confirm_password"
								type="password"
								minlength="8"
								class="block w-full rounded-lg border border-slate-200 px-3.5 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
								placeholder="再次输入密码"
								bind:value={confirmPassword}
								required
							/>
						</div>

						<button
							type="submit"
							class="group relative flex w-full items-center justify-center gap-3 rounded-lg bg-slate-900 px-4 py-3.5 text-sm font-semibold text-white shadow-sm transition hover:bg-black focus:outline-none focus:ring-2 focus:ring-slate-800 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-70"
							disabled={isLoading}
						>
							{#if isLoading}
								<div class="h-5 w-5 animate-spin rounded-full border-2 border-white/60 border-t-white"></div>
								<span>正在注册...</span>
							{:else}
								<span>注册并激活</span>
								<ArrowRight class="ml-auto h-4 w-4 text-white/80 transition-transform group-hover:translate-x-0.5" />
							{/if}
						</button>

						<p class="text-xs text-slate-500">
							注册后我们会发送一封激活邮件，请前往邮箱完成激活，再使用上方登录方式进入系统。
						</p>
					</form>
				{/if}

				<!-- Divider -->
				<div class="my-8 flex items-center gap-4">
					<div class="h-px flex-1 bg-slate-200"></div>
					<span class="text-xs font-medium uppercase tracking-wider text-slate-400">安全登录</span>
					<div class="h-px flex-1 bg-slate-200"></div>
				</div>

				<!-- Trust Signals -->
				<div class="space-y-4">
					<div class="flex items-center gap-3 rounded-lg bg-slate-50 p-3">
						<div class="flex h-8 w-8 items-center justify-center rounded-full bg-green-100">
							<Shield class="h-4 w-4 text-green-600" />
						</div>
						<div class="flex-1">
							<p class="text-sm font-medium text-slate-700">企业级安全</p>
							<p class="text-xs text-slate-500">数据全程加密传输与存储</p>
						</div>
					</div>

					<div class="flex items-center gap-3 rounded-lg bg-slate-50 p-3">
						<div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100">
							<Lock class="h-4 w-4 text-blue-600" />
						</div>
						<div class="flex-1">
							<p class="text-sm font-medium text-slate-700">隐私优先</p>
							<p class="text-xs text-slate-500">自部署可控，数据完全归你所有</p>
						</div>
					</div>
				</div>

				<!-- Features for Mobile -->
				<div class="mt-8 lg:hidden">
					<p class="mb-3 text-xs font-medium uppercase tracking-wider text-slate-400">你将获得</p>
					<div class="grid grid-cols-2 gap-2">
						{#each ['不限客户数量', '销售阶段看板', '任务提醒', '团队协作'] as item}
							<div class="flex items-center gap-2 text-sm text-slate-600">
								<CheckCircle2 class="h-4 w-4 text-green-500" />
								<span>{item}</span>
							</div>
						{/each}
					</div>
				</div>
			</div>
		</div>

		<!-- Footer -->
		<div class="border-t border-slate-100 p-6">
			<div class="flex flex-col items-center justify-between gap-4 text-sm sm:flex-row">
				<p class="text-slate-500">
					还没有账号？
					<span class="text-slate-700">联系管理员创建或邀请加入团队</span>
				</p>
				<div class="flex items-center gap-4 text-slate-400">
					<a href="https://github.com/MicroPyramid/Django-CRM" target="_blank" rel="noopener noreferrer" class="hover:text-slate-600">
						GitHub
					</a>
					<span>·</span>
					<a href="/docs" class="hover:text-slate-600">文档</a>
					<span>·</span>
					<a href="/privacy" class="hover:text-slate-600">隐私政策</a>
				</div>
			</div>
		</div>
	</div>
</div>
