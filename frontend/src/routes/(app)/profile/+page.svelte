<script>
	import { enhance } from '$app/forms';
	import { User, Mail, Phone, Building2, Calendar, Edit, Save, X, Check } from '@lucide/svelte';
	import { validatePhoneNumber, formatPhoneNumber } from '$lib/utils/phone.js';
	import { formatDate, getInitials } from '$lib/utils/formatting.js';
	import PageHeader from '$lib/components/layout/PageHeader.svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Avatar from '$lib/components/ui/avatar/index.js';

	/** @type {{ data: import('./$types').PageData, form: import('./$types').ActionData }} */
	let { data, form } = $props();

	let isEditing = $state(false);
	let isSubmitting = $state(false);
	let phoneError = $state('');

	// Form data state - initialized by $effect below
	let formData = $state({
		name: '',
		phone: ''
	});

	// Reset form data when not editing or when data changes
	$effect(() => {
		if (!isEditing) {
			formData = {
				name: data.user.name || '',
				phone: data.user.phone || ''
			};
			phoneError = '';
		}
	});

	// Validate phone number on input
	function validatePhone() {
		if (!formData.phone.trim()) {
			phoneError = '';
			return;
		}

		const validation = validatePhoneNumber(formData.phone);
		if (!validation.isValid) {
			phoneError = validation.error || 'Invalid phone number';
		} else {
			phoneError = '';
		}
	}

	function toggleEdit() {
		isEditing = !isEditing;
		if (!isEditing) {
			// Reset form data when canceling edit
			formData = {
				name: data.user.name || '',
				phone: data.user.phone || ''
			};
			phoneError = '';
		}
	}

	// Handle form submission
	function handleSubmit() {
		isSubmitting = true;
		return async (
			/** @type {{ result: any, update: () => Promise<void> }} */ { result, update }
		) => {
			isSubmitting = false;
			if (result.type === 'success') {
				isEditing = false;
			}
			await update();
		};
	}
</script>

<svelte:head>
	<title>个人资料 - BottleCRM</title>
</svelte:head>

<PageHeader title="个人资料" subtitle="管理您的个人信息">
	{#snippet actions()}
		<Button
			variant={isEditing ? 'outline' : 'default'}
			onclick={toggleEdit}
			disabled={isSubmitting}
		>
			{#if isEditing}
				<X class="mr-2 h-4 w-4" />
				取消
			{:else}
				<Edit class="mr-2 h-4 w-4" />
				编辑资料
			{/if}
		</Button>
	{/snippet}
</PageHeader>

<div class="flex-1 space-y-6 p-4 md:p-6">
	<!-- Success/Error Messages -->
	{#if form?.success}
		<Card.Root class="border-green-200 bg-green-50 dark:border-green-800 dark:bg-green-900/20">
			<Card.Content class="flex items-center gap-3 p-4">
				<div
					class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-green-100 dark:bg-green-800"
				>
					<Check class="h-4 w-4 text-green-600 dark:text-green-300" />
				</div>
				<p class="text-sm font-medium text-green-800 dark:text-green-200">
					{form.message}
				</p>
			</Card.Content>
		</Card.Root>
	{/if}

	{#if form?.error}
		<Card.Root class="border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20">
			<Card.Content class="flex items-center gap-3 p-4">
				<div
					class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-red-100 dark:bg-red-800"
				>
					<X class="h-4 w-4 text-red-600 dark:text-red-300" />
				</div>
				<p class="text-sm font-medium text-red-800 dark:text-red-200">
					{form.error}
				</p>
			</Card.Content>
		</Card.Root>
	{/if}

	<div class="mx-auto max-w-3xl space-y-6">
		<!-- Profile Header Card -->
		<Card.Root>
			<Card.Content class="p-6">
				<div class="flex flex-col items-center gap-6 sm:flex-row sm:items-start">
					<!-- Avatar -->
					<Avatar.Root class="h-20 w-20 text-xl">
						{#if data.user.profilePhoto}
							<Avatar.Image
								src={data.user.profilePhoto}
								alt={data.user.name || '个人资料'}
								class=""
							/>
						{/if}
						<Avatar.Fallback class="bg-gradient-to-br from-blue-500 to-purple-600 text-white">
							{getInitials(data.user.name)}
						</Avatar.Fallback>
					</Avatar.Root>

					<!-- User Info -->
					<div class="flex-1 text-center sm:text-left">
						<h2 class="text-foreground text-xl font-semibold">
							{data.user.name || '未命名用户'}
						</h2>
						<p class="text-muted-foreground">{data.user.email}</p>
						<div class="mt-3">
							<Badge variant={data.user.isActive ? 'default' : 'destructive'}>
								{data.user.isActive ? '活跃' : '未激活'}
							</Badge>
						</div>
					</div>
				</div>
			</Card.Content>
		</Card.Root>

		<!-- Profile Information Card -->
		<Card.Root>
			<Card.Header class="">
				<Card.Title class="">个人资料信息</Card.Title>
				<Card.Description class="">
					{isEditing
						? '在下方更新您的个人信息'
						: '您的个人信息和账户资料'}
				</Card.Description>
			</Card.Header>
			<Card.Content>
				{#if isEditing}
					<!-- Edit Form -->
					<form method="POST" action="?/updateProfile" use:enhance={handleSubmit} class="space-y-6">
						<div class="grid gap-6 sm:grid-cols-2">
							<!-- Name -->
							<div class="sm:col-span-2">
								<Label for="name" class="">全名 *</Label>
								<Input
									type="text"
									id="name"
									name="name"
									bind:value={formData.name}
									required
									placeholder="请输入您的全名"
									class="mt-1.5"
								/>
							</div>

							<!-- Email (read-only) -->
							<div>
								<Label for="email" class="">邮箱地址</Label>
								<Input
									type="email"
									id="email"
									value={data.user.email}
									disabled
									class="bg-muted mt-1.5"
								/>
								<p class="text-muted-foreground mt-1 text-xs">邮箱无法更改</p>
							</div>

							<!-- Phone -->
							<div>
								<Label for="phone" class="">电话号码</Label>
								<Input
									type="tel"
									id="phone"
									name="phone"
									bind:value={formData.phone}
									oninput={validatePhone}
									placeholder="请输入您的电话号码"
									class="mt-1.5"
								/>
								{#if phoneError}
									<p class="text-destructive mt-1 text-sm">{phoneError}</p>
								{/if}
							</div>
						</div>

						<Separator />

						<div class="flex justify-end gap-3">
							<Button type="button" variant="outline" onclick={toggleEdit} disabled={isSubmitting}>
								取消
							</Button>
							<Button type="submit" disabled={isSubmitting || !!phoneError}>
								{#if isSubmitting}
									<svg class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
										<circle
											class="opacity-25"
											cx="12"
											cy="12"
											r="10"
											stroke="currentColor"
											stroke-width="4"
										></circle>
										<path
											class="opacity-75"
											fill="currentColor"
											d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
										></path>
									</svg>
									保存中...
								{:else}
									<Save class="mr-2 h-4 w-4" />
									保存更改
								{/if}
							</Button>
						</div>
					</form>
				{:else}
					<!-- View Mode -->
					<div class="grid gap-6 sm:grid-cols-2">
						<!-- Email -->
						<div class="space-y-1">
							<div class="text-muted-foreground flex items-center gap-2 text-sm font-medium">
								<Mail class="h-4 w-4" />
								邮箱地址
							</div>
							<p class="text-foreground">{data.user.email}</p>
						</div>

						<!-- Phone -->
						<div class="space-y-1">
							<div class="text-muted-foreground flex items-center gap-2 text-sm font-medium">
								<Phone class="h-4 w-4" />
								电话号码
							</div>
							<p class="text-foreground">
								{data.user.phone ? formatPhoneNumber(data.user.phone) : '未提供'}
							</p>
						</div>

						<!-- Last Login -->
						<div class="space-y-1">
							<div class="text-muted-foreground flex items-center gap-2 text-sm font-medium">
								<Calendar class="h-4 w-4" />
								最后登录
							</div>
							<p class="text-foreground">{formatDate(data.user.lastLogin)}</p>
						</div>

						<!-- Member Since -->
						<div class="space-y-1">
							<div class="text-muted-foreground flex items-center gap-2 text-sm font-medium">
								<Calendar class="h-4 w-4" />
								注册时间
							</div>
							<p class="text-foreground">{formatDate(data.user.createdAt)}</p>
						</div>
					</div>
				{/if}
			</Card.Content>
		</Card.Root>

		<!-- Organizations Card -->
		{#if data.user.organizations && data.user.organizations.length > 0}
			<Card.Root>
				<Card.Header class="">
					<Card.Title class="">所属组织</Card.Title>
					<Card.Description class="">您所属的组织</Card.Description>
				</Card.Header>
				<Card.Content class="space-y-4">
					{#each data.user.organizations as userOrg}
						<div class="bg-muted/30 flex items-center justify-between rounded-lg border p-4">
							<div class="flex items-center gap-3">
								<div
									class="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600"
								>
									<Building2 class="h-5 w-5 text-white" />
								</div>
								<div>
									<h4 class="text-foreground font-medium">
										{userOrg.organization.name}
									</h4>
									<p class="text-muted-foreground text-sm">
										加入于 {formatDate(userOrg.joinedAt)}
									</p>
								</div>
							</div>
							<Badge variant={userOrg.role === 'ADMIN' ? 'default' : 'secondary'}>
								{userOrg.role === 'ADMIN' ? '管理员' : userOrg.role}
							</Badge>
						</div>
					{/each}
				</Card.Content>
			</Card.Root>
		{/if}
	</div>
</div>
