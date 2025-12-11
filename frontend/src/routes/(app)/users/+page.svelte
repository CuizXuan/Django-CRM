<script>
	import { enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import {
		Users,
		UsersRound,
		User,
		Shield,
		Edit,
		Plus,
		Check,
		X,
		Trash2,
		AlertCircle
	} from '@lucide/svelte';
	import PageHeader from '$lib/components/layout/PageHeader.svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import * as Table from '$lib/components/ui/table/index.js';
	import * as Avatar from '$lib/components/ui/avatar/index.js';
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js';
	import * as Tabs from '$lib/components/ui/tabs/index.js';
	import { getInitials, formatDate } from '$lib/utils/formatting.js';
	import { TeamCard, TeamFormDialog } from '$lib/components/users/index.js';

	/** @type {{ data: import('./$types').PageData, form: any }} */
	let { data, form } = $props();

	// Get logged-in user id from data
	let loggedInUserId = $derived(data.user?.id);

	// Transform users data for table display
	let users = $derived(
		Array.isArray(data.users)
			? data.users.map((u) => ({
					id: u.user.id,
					odId: u.profile?.id || u.odId,
					name: u.user.name || u.user.email,
					email: u.user.email,
					role: u.role,
					joined: u.profile?.created_at
						? typeof u.profile.created_at === 'string'
							? u.profile.created_at.slice(0, 10)
							: new Date(u.profile.created_at).toISOString().slice(0, 10)
						: '',
					avatar: u.profile?.profile_photo || '',
					isSelf: loggedInUserId === u.user.id,
					isActive: u.isActive
				}))
			: []
	);

	// Teams data
	let teams = $derived(data.teams || []);

	// Users list for team assignment (active users only, transformed for multi-select)
	let availableUsers = $derived(
		users
			.filter((u) => u.isActive)
			.map((u) => ({
				id: u.odId,
				name: u.name,
				email: u.email
			}))
	);

	// State for editing roles
	/** @type {string | null} */
	let editingRoleId = $state(null);

	// State for team dialog
	let teamDialogOpen = $state(false);
	/** @type {any} */
	let editingTeam = $state(null);
	let isTeamLoading = $state(false);

	// Handle form results
	$effect(() => {
		if (form?.success) {
			if (form.action === 'create_team') {
				toast.success('团队创建成功');
				teamDialogOpen = false;
				editingTeam = null;
			} else if (form.action === 'update_team') {
				toast.success('团队更新成功');
				teamDialogOpen = false;
				editingTeam = null;
			} else if (form.action === 'delete_team') {
				toast.success('团队删除成功');
			}
			invalidateAll();
		} else if (form?.error) {
			toast.error(form.error);
		}
		isTeamLoading = false;
	});

	/**
	 * Open dialog to create a new team
	 */
	function openCreateTeamDialog() {
		editingTeam = null;
		teamDialogOpen = true;
	}

	/**
	 * Open dialog to edit a team
	 * @param {any} team
	 */
	function openEditTeamDialog(team) {
		editingTeam = team;
		teamDialogOpen = true;
	}

	/**
	 * Handle team form submission
	 * @param {{ name: string, description: string, users: string[], teamId?: string }} formData
	 */
	function handleTeamSubmit(formData) {
		isTeamLoading = true;

		// Create a hidden form and submit it
		const form = document.createElement('form');
		form.method = 'POST';
		form.action = formData.teamId ? '?/update_team' : '?/create_team';
		form.style.display = 'none';

		// Add form fields
		const addField = (/** @type {string} */ name, /** @type {string} */ value) => {
			const input = document.createElement('input');
			input.type = 'hidden';
			input.name = name;
			input.value = value;
			form.appendChild(input);
		};

		addField('name', formData.name);
		addField('description', formData.description);
		if (formData.teamId) {
			addField('team_id', formData.teamId);
		}
		formData.users.forEach((userId) => {
			addField('users', userId);
		});

		document.body.appendChild(form);
		form.submit();
	}

	/**
	 * Handle team deletion
	 * @param {string} teamId
	 */
	function handleTeamDelete(teamId) {
		const form = document.createElement('form');
		form.method = 'POST';
		form.action = '?/delete_team';
		form.style.display = 'none';

		const input = document.createElement('input');
		input.type = 'hidden';
		input.name = 'team_id';
		input.value = teamId;
		form.appendChild(input);

		document.body.appendChild(form);
		form.submit();
	}
</script>

<svelte:head>
	<title>用户与团队 - BottleCRM</title>
</svelte:head>

<PageHeader title="用户与团队" subtitle="管理组织中的用户和团队" />

<div class="flex-1 space-y-6 p-4 md:p-6">
	<!-- Error Message -->
	{#if data.error}
		<Card.Root class="border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20">
			<Card.Content class="flex items-center gap-3 p-4">
				<div
					class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-red-100 dark:bg-red-800"
				>
					<AlertCircle class="h-4 w-4 text-red-600 dark:text-red-300" />
				</div>
				<p class="text-sm font-medium text-red-800 dark:text-red-200">
					{data.error.name}
				</p>
			</Card.Content>
		</Card.Root>
	{:else}
		<div class="mx-auto max-w-5xl">
			<Tabs.Root value="users" class="w-full">
				<Tabs.List class="mb-6 grid w-full grid-cols-2 lg:w-[400px]">
					<Tabs.Trigger value="users" class="gap-2">
						<Users class="h-4 w-4" />
						用户
					</Tabs.Trigger>
					<Tabs.Trigger value="teams" class="gap-2">
						<UsersRound class="h-4 w-4" />
						团队
					</Tabs.Trigger>
				</Tabs.List>

				<!-- Users Tab -->
				<Tabs.Content value="users" class="space-y-6">
					<!-- Add User Form -->
					<Card.Root>
						<Card.Header class="pb-4">
							<div class="flex items-center gap-3">
								<div
									class="flex h-10 w-10 items-center justify-center rounded-lg bg-green-100 dark:bg-green-900/30"
								>
									<Plus class="h-5 w-5 text-green-600 dark:text-green-400" />
								</div>
								<div>
									<Card.Title class="">添加新成员</Card.Title>
									<Card.Description class="">邀请新用户加入您的组织</Card.Description>
								</div>
							</div>
						</Card.Header>
						<Card.Content>
							<form
								method="POST"
								action="?/add_user"
								class="flex flex-col gap-4 sm:flex-row sm:items-end"
							>
								<div class="flex-1">
									<Label class="" for="add-user-email">邮箱地址 *</Label>
									<Input
										id="add-user-email"
										name="email"
										type="email"
										required
										placeholder="请输入邮箱地址"
										class="mt-1.5"
									/>
								</div>
								<div class="sm:w-40">
									<Label class="" for="add-user-role">角色</Label>
									<select
										id="add-user-role"
										name="role"
										class="border-input bg-background ring-offset-background focus-visible:ring-ring mt-1.5 flex h-10 w-full rounded-md border px-3 py-2 text-sm focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none"
									>
										<option value="USER">用户</option>
										<option value="ADMIN">管理员</option>
									</select>
								</div>
								<Button type="submit">
									<Plus class="mr-2 h-4 w-4" />
									添加成员
								</Button>
							</form>
						</Card.Content>
					</Card.Root>

					<!-- Users Table -->
					<Card.Root>
						<Card.Header class="pb-4">
							<div class="flex items-center gap-3">
								<div
									class="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900/30"
								>
									<Users class="h-5 w-5 text-blue-600 dark:text-blue-400" />
								</div>
								<div>
									<Card.Title class="">团队成员</Card.Title>
									<Card.Description class=""
										>您的组织中有 {users.length} 名成员</Card.Description
									>
								</div>
							</div>
						</Card.Header>
						<Card.Content>
							<div class="rounded-lg border">
								<Table.Root>
									<Table.Header>
										<Table.Row>
											<Table.Head class="w-[300px]">成员</Table.Head>
											<Table.Head>角色</Table.Head>
											<Table.Head>加入时间</Table.Head>
											<Table.Head class="w-[80px]">操作</Table.Head>
										</Table.Row>
									</Table.Header>
									<Table.Body>
										{#each users as user (user.id)}
											<Table.Row>
												<Table.Cell>
													<div class="flex items-center gap-3">
														<Avatar.Root class="h-9 w-9">
															{#if user.avatar}
																<Avatar.Image class="" src={user.avatar} alt={user.name} />
															{/if}
															<Avatar.Fallback
																class="bg-gradient-to-br from-blue-500 to-purple-600 text-sm text-white"
															>
																{getInitials(user.name)}
															</Avatar.Fallback>
														</Avatar.Root>
														<div>
															<div class="flex items-center gap-2">
																<span class="text-foreground font-medium">{user.name}</span>
																{#if user.isSelf}
																	<Badge variant="secondary" class="text-xs">您</Badge>
																{/if}
																{#if !user.isActive}
																	<Badge variant="outline" class="text-muted-foreground text-xs"
																		>未激活</Badge
																	>
																{/if}
															</div>
															<span class="text-muted-foreground text-sm">{user.email}</span>
														</div>
													</div>
												</Table.Cell>
												<Table.Cell>
													{#if user.isSelf || editingRoleId !== user.id}
														<Badge
															variant={user.role === 'ADMIN' ? 'default' : 'secondary'}
															class="cursor-default"
														>
															{#if user.role === 'ADMIN'}
																<Shield class="mr-1 h-3 w-3" />
															{:else}
																<User class="mr-1 h-3 w-3" />
															{/if}
															{user.role === 'ADMIN' ? '管理员' : '用户'}
														</Badge>
														{#if !user.isSelf}
															<Button
																variant="ghost"
																size="sm"
																class="ml-2 h-6 px-2 text-xs"
																onclick={() => (editingRoleId = user.id)}
															>
																<Edit class="h-3 w-3" />
															</Button>
														{/if}
													{:else}
														<form method="POST" action="?/edit_role" class="flex items-center gap-2">
															<input type="hidden" name="user_id" value={user.id} />
															<select
																name="role"
																class="border-input bg-background h-8 rounded-md border px-2 text-sm"
															>
																<option value="USER" selected={user.role === 'USER'}>用户</option>
																<option value="ADMIN" selected={user.role === 'ADMIN'}>管理员</option>
															</select>
															<Button type="submit" size="icon" class="h-7 w-7" variant="default">
																<Check class="h-3.5 w-3.5" />
															</Button>
															<Button
																type="button"
																size="icon"
																class="h-7 w-7"
																variant="outline"
																onclick={() => (editingRoleId = null)}
															>
																<X class="h-3.5 w-3.5" />
															</Button>
														</form>
													{/if}
												</Table.Cell>
												<Table.Cell>
													<span class="text-muted-foreground text-sm"
														>{formatDate(user.joined)}</span
													>
												</Table.Cell>
												<Table.Cell>
													{#if user.isSelf}
														<span class="text-muted-foreground">-</span>
													{:else}
														<AlertDialog.Root>
															<AlertDialog.Trigger>
																<Button
																	variant="ghost"
																	size="icon"
																	class="text-destructive hover:bg-destructive/10 h-8 w-8"
																>
																	<Trash2 class="h-4 w-4" />
																</Button>
															</AlertDialog.Trigger>
															<AlertDialog.Content>
																<AlertDialog.Header>
																	<AlertDialog.Title>移除团队成员</AlertDialog.Title>
																	<AlertDialog.Description>
																		确定要将 <strong>{user.name}</strong> 从组织中移除吗？此操作无法撤销。
																	</AlertDialog.Description>
																</AlertDialog.Header>
																<AlertDialog.Footer>
																	<AlertDialog.Cancel>取消</AlertDialog.Cancel>
																	<form method="POST" action="?/remove_user" class="inline">
																		<input type="hidden" name="user_id" value={user.id} />
																		<Button type="submit" variant="destructive">移除</Button>
																	</form>
																</AlertDialog.Footer>
															</AlertDialog.Content>
														</AlertDialog.Root>
													{/if}
												</Table.Cell>
											</Table.Row>
										{/each}

										{#if users.length === 0}
											<Table.Row>
												<Table.Cell colspan={4} class="py-8 text-center">
													<Users class="text-muted-foreground/50 mx-auto h-8 w-8" />
													<p class="text-muted-foreground mt-2 text-sm">未找到团队成员</p>
												</Table.Cell>
											</Table.Row>
										{/if}
									</Table.Body>
								</Table.Root>
							</div>
						</Card.Content>
					</Card.Root>
				</Tabs.Content>

				<!-- Teams Tab -->
				<Tabs.Content value="teams" class="space-y-6">
					<!-- Header with Create Button -->
					<div class="flex items-center justify-between">
						<div>
							<h2 class="text-lg font-semibold">团队</h2>
							<p class="text-muted-foreground text-sm">
								创建团队来分组用户，用于分配任务和访问控制。
							</p>
						</div>
						<Button onclick={openCreateTeamDialog}>
							<Plus class="mr-2 h-4 w-4" />
							创建团队
						</Button>
					</div>

					<!-- Teams Grid -->
					{#if teams.length > 0}
						<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
							{#each teams as team (team.id)}
								<TeamCard {team} onEdit={openEditTeamDialog} onDelete={handleTeamDelete} />
							{/each}
						</div>
					{:else}
						<!-- Empty State -->
						<Card.Root class="py-12">
							<Card.Content class="text-center">
								<div
									class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-purple-100 dark:bg-purple-900/30"
								>
									<UsersRound class="h-8 w-8 text-purple-600 dark:text-purple-400" />
								</div>
								<h3 class="mb-2 text-lg font-semibold">暂无团队</h3>
								<p class="text-muted-foreground mx-auto mb-6 max-w-sm text-sm">
									团队可以帮助您组织用户并管理对记录的访问。创建您的第一个团队以开始使用。
								</p>
								<Button onclick={openCreateTeamDialog}>
									<Plus class="mr-2 h-4 w-4" />
									创建您的第一个团队
								</Button>
							</Card.Content>
						</Card.Root>
					{/if}
				</Tabs.Content>
			</Tabs.Root>
		</div>
	{/if}
</div>

<!-- Team Form Dialog -->
<TeamFormDialog
	bind:open={teamDialogOpen}
	team={editingTeam}
	users={availableUsers}
	onClose={() => {
		teamDialogOpen = false;
		editingTeam = null;
	}}
	onSubmit={handleTeamSubmit}
	isLoading={isTeamLoading}
/>
