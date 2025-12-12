<script>
	import { enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import { Settings, Building2, Globe, Banknote } from '@lucide/svelte';
	import { PageHeader } from '$lib/components/layout';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { CURRENCY_CODES } from '$lib/constants/filters-zh.js';

	/** @type {{ data: any, form: any }} */
	let { data, form } = $props();

	const settings = $derived(data.settings || {});
	let isLoading = $state(false);

	// Currency options for select
	const currencyOptions = CURRENCY_CODES.filter((c) => c.value);

	// Country options (simplified list of common countries)
	const countryOptions = [
		{ value: '', label: '选择国家' },
		{ value: 'CN', label: '中国' },
		{ value: 'US', label: '美国' },
		{ value: 'GB', label: '英国' },
		{ value: 'CA', label: '加拿大' },
		{ value: 'AU', label: '澳大利亚' },
		{ value: 'DE', label: '德国' },
		{ value: 'FR', label: '法国' },
		{ value: 'IN', label: '印度' },
		{ value: 'JP', label: '日本' },
		{ value: 'SG', label: '新加坡' },
		{ value: 'AE', label: '阿联酋' },
		{ value: 'BR', label: '巴西' },
		{ value: 'MX', label: '墨西哥' },
		{ value: 'CH', label: '瑞士' },
		{ value: 'NL', label: '荷兰' },
		{ value: 'ES', label: '西班牙' },
		{ value: 'IT', label: '意大利' },
		{ value: 'KR', label: '韩国' },
		{ value: 'HK', label: '香港' },
		{ value: 'TW', label: '台湾' }
	];

	// Form state - initialized from settings via $effect
	let formName = $state('');
	let formDomain = $state('');
	let formDescription = $state('');
	let formCurrency = $state('CNY');
	let formCountry = $state('');

	// Update form state when settings change
	$effect(() => {
		formName = settings.name || '';
		formDomain = settings.domain || '';
		formDescription = settings.description || '';
		formCurrency = settings.default_currency || 'CNY';
		formCountry = settings.default_country || 'CN';
	});

	// Handle form result
	$effect(() => {
		if (form?.success) {
			toast.success('组织设置更新成功');
			invalidateAll();
		} else if (form?.error) {
			toast.error(form.error);
		}
	});
</script>

<svelte:head>
	<title>组织设置 - BottleCRM</title>
</svelte:head>

<PageHeader title="组织设置" subtitle="管理您的组织偏好">
	{#snippet actions()}
		<div class="flex items-center gap-2">
			<Settings class="text-muted-foreground h-5 w-5" />
		</div>
	{/snippet}
</PageHeader>

<div class="flex-1 space-y-6 p-4 md:p-6">
	<form
		method="POST"
		action="?/update"
		use:enhance={() => {
			isLoading = true;
			return async ({ update }) => {
				await update();
				isLoading = false;
			};
		}}
	>
		<!-- Organization Details -->
		<Card.Root class="mb-6">
			<Card.Header class="pb-4">
				<Card.Title class="flex items-center gap-2 text-lg">
					<Building2 class="h-5 w-5" />
					组织详细信息
				</Card.Title>
				<Card.Description class="">关于您组织的基本信息</Card.Description>
			</Card.Header>
			<Card.Content class="space-y-4">
				<div class="grid gap-4 md:grid-cols-2">
					<div class="grid gap-2">
						<Label class="" for="name">组织名称</Label>
						<Input
							id="name"
							name="name"
							type="text"
							bind:value={formName}
							placeholder="请输入组织名称"
						/>
					</div>
					<div class="grid gap-2">
						<Label class="" for="domain">域名</Label>
						<div class="relative">
							<Globe class="text-muted-foreground absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2" />
							<Input
								id="domain"
								name="domain"
								type="text"
								bind:value={formDomain}
								placeholder="yourcompany.com"
								class="pl-10"
							/>
						</div>
					</div>
				</div>
				<div class="grid gap-2">
					<Label class="" for="description">描述</Label>
					<textarea
						id="description"
						name="description"
						rows="3"
						bind:value={formDescription}
						placeholder="描述您的组织..."
						class="border-input bg-background ring-offset-background placeholder:text-muted-foreground focus-visible:ring-ring flex min-h-[80px] w-full rounded-md border px-3 py-2 text-sm focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50"
					></textarea>
				</div>
			</Card.Content>
		</Card.Root>

		<!-- Locale Settings -->
		<Card.Root class="mb-6">
			<Card.Header class="pb-4">
				<Card.Title class="flex items-center gap-2 text-lg">
					<Globe class="h-5 w-5" />
					本地化设置
				</Card.Title>
				<Card.Description class="">
					为您的组织配置默认货币和国家
				</Card.Description>
			</Card.Header>
			<Card.Content class="space-y-4">
				<div class="grid gap-4 md:grid-cols-2">
					<div class="grid gap-2">
						<Label class="" for="default_currency">默认货币</Label>
						<div class="relative">
							<Banknote class="text-muted-foreground absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2" />
							<select
								id="default_currency"
								name="default_currency"
								bind:value={formCurrency}
								class="border-input bg-background w-full rounded-md border py-2 pl-10 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
							>
								{#each currencyOptions as currency}
									<option value={currency.value}>{currency.label}</option>
								{/each}
							</select>
						</div>
						<p class="text-muted-foreground text-xs">
							这将是新商机、线索和发票的默认货币。
						</p>
					</div>

					<div class="grid gap-2">
						<Label class="" for="default_country">默认国家</Label>
						<div class="relative">
							<Globe class="text-muted-foreground absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2" />
							<select
								id="default_country"
								name="default_country"
								bind:value={formCountry}
								class="border-input bg-background w-full rounded-md border py-2 pl-10 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
							>
								{#each countryOptions as country}
									<option value={country.value}>{country.label}</option>
								{/each}
							</select>
						</div>
						<p class="text-muted-foreground text-xs">
							地址和本地化格式的默认国家。
						</p>
					</div>
				</div>

				<!-- Preview -->
				{#if formCurrency}
					<div class="bg-muted/50 rounded-lg p-4">
						<p class="text-muted-foreground mb-2 text-sm font-medium">预览</p>
						<p class="text-foreground text-lg font-semibold">
							{new Intl.NumberFormat('zh-CN', {
								style: 'currency',
								currency: formCurrency
							}).format(12345.67)}
						</p>
					</div>
				{/if}
			</Card.Content>
		</Card.Root>

		<!-- Save Button -->
		<div class="flex justify-end">
			<Button type="submit" disabled={isLoading}>
				{isLoading ? '保存中...' : '保存更改'}
			</Button>
		</div>
	</form>
</div>
