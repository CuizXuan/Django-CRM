<script>
	import { enhance } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import { page } from '$app/stores';
	import { tick, onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import {
		Plus,
		Eye,
		User,
		Mail,
		Phone,
		Building2,
		Briefcase,
		MapPin,
		FileText,
		Linkedin,
		PhoneOff,
		Calendar,
		Tag,
		Filter
	} from '@lucide/svelte';
	import { PageHeader } from '$lib/components/layout';
	import { CrmDrawer } from '$lib/components/ui/crm-drawer';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import { CrmTable } from '$lib/components/ui/crm-table';
	import { FilterBar, SearchInput, DateRangeFilter } from '$lib/components/ui/filter';
	import { Pagination } from '$lib/components/ui/pagination';
	import { formatRelativeDate, formatPhone, getNameInitials } from '$lib/utils/formatting.js';
	import { goto } from '$app/navigation';
	import { COUNTRIES, getCountryName } from '$lib/constants/countries.js';
	import { apiRequest } from '$lib/api.js';

	// Column visibility configuration
	const STORAGE_KEY = 'contacts-column-config';

	/**
	 * @typedef {'text' | 'email' | 'number' | 'date' | 'select' | 'checkbox' | 'relation'} ColumnType
	 * @typedef {{ key: string, label: string, type?: ColumnType, width?: string, editable?: boolean, canHide?: boolean, getValue?: (row: any) => any, emptyText?: string, relationIcon?: string }} ColumnDef
	 */

	/** @type {ColumnDef[]} */
	const columns = [
		{
			key: 'name',
			label: '联系人',
			type: 'text',
			width: 'w-48',
			editable: false,
			canHide: false,
			getValue: (row) => `${row.firstName || ''} ${row.lastName || ''}`.trim(),
			emptyText: '未命名'
		},
		{
			key: 'organization',
			label: '公司',
			type: 'text',
			width: 'w-40',
			emptyText: ''
		},
		{ key: 'title', label: '职位', type: 'text', width: 'w-36', emptyText: '' },
		{ key: 'email', label: '邮箱', type: 'email', width: 'w-52', emptyText: '' },
		{ key: 'phone', label: '电话', type: 'text', width: 'w-36', emptyText: '' },
		{
			key: 'createdAt',
			label: '创建时间',
			type: 'date',
			width: 'w-32',
			editable: false
		},
		// Hidden by default
		{
			key: 'owner',
			label: '负责人',
			type: 'relation',
			width: 'w-36',
			relationIcon: 'user',
			canHide: true,
			getValue: (row) => row.owner?.name || row.owner?.email,
			emptyText: ''
		}
	];

	// Default visible columns (excludes owner)
	const DEFAULT_VISIBLE_COLUMNS = ['name', 'organization', 'title', 'email', 'phone', 'createdAt'];

	// Country options for drawer
	const countryOptions = COUNTRIES.map((c) => ({ value: c.code, label: c.name }));

	/** @type {{ data: import('./$types').PageData }} */
	let { data } = $props();

	// Lazy-loaded dropdown options (fetched when drawer opens)
	let loadedOwners = $state(/** @type {any[]} */ ([]));
	let loadedTags = $state(/** @type {any[]} */ ([]));
	let dropdownOptionsLoaded = $state(false);
	let dropdownOptionsLoading = $state(false);

	// Use lazy-loaded data
	const allTags = $derived(loadedTags);

	/**
	 * Fetch dropdown options for the drawer (lazy load)
	 */
	async function loadDropdownOptions() {
		if (dropdownOptionsLoaded || dropdownOptionsLoading) return;

		dropdownOptionsLoading = true;
		try {
			const [ownersResponse, tagsResponse] = await Promise.all([
				apiRequest('/users/'),
				apiRequest('/tags/').catch(() => ({ tags: [] }))
			]);

			// Transform owners
			const activeUsers = ownersResponse.active_users?.active_users || [];
			loadedOwners = activeUsers.map((/** @type {any} */ user) => ({
				id: user.id,
				name: user.user_details?.email || user.email,
				email: user.user_details?.email || user.email
			}));

			// Transform tags
			loadedTags = (tagsResponse.tags || tagsResponse || []).map((/** @type {any} */ tag) => ({
				id: tag.id,
				name: tag.name
			}));

			dropdownOptionsLoaded = true;
		} catch (err) {
			console.error('Failed to load dropdown options:', err);
		} finally {
			dropdownOptionsLoading = false;
		}
	}

	// Drawer column definitions for CrmDrawer (derived to include allTags)
	const drawerColumns = $derived([
		{ key: 'firstName', label: '名', type: 'text', icon: User, placeholder: '请输入名' },
		{ key: 'lastName', label: '姓', type: 'text', placeholder: '请输入姓' },
		{ key: 'email', label: '邮箱', type: 'email', icon: Mail, placeholder: '请输入邮箱' },
		{ key: 'phone', label: '电话', type: 'text', icon: Phone, placeholder: '请输入电话' },
		{
			key: 'organization',
			label: '公司',
			type: 'text',
			icon: Building2,
			placeholder: '请输入公司名称'
		},
		{ key: 'title', label: '职位', type: 'text', icon: Briefcase, placeholder: '请输入职位' },
		{ key: 'department', label: '部门', type: 'text', placeholder: '请输入部门' },
		{
			key: 'doNotCall',
			label: '禁止致电',
			type: 'checkbox',
			icon: PhoneOff
		},
		{
			key: 'linkedInUrl',
			label: 'LinkedIn',
			type: 'text',
			icon: Linkedin,
			placeholder: 'https://linkedin.com/in/...'
		},
		{
			key: 'addressLine',
			label: '地址',
			type: 'text',
			icon: MapPin,
			placeholder: '街道地址'
		},
		{ key: 'city', label: '城市', type: 'text', placeholder: '城市' },
		{ key: 'state', label: '省/州', type: 'text', placeholder: '省/州' },
		{ key: 'postcode', label: '邮编', type: 'text', placeholder: '邮政编码' },
		{
			key: 'country',
			label: '国家',
			type: 'select',
			options: countryOptions,
			placeholder: '选择国家'
		},
		{
			key: 'tags',
			label: '标签',
			type: 'multiselect',
			icon: Tag,
			options: allTags.map((/** @type {any} */ t) => ({ id: t.id, name: t.name })),
			emptyText: '无标签'
		},
		{
			key: 'description',
			label: '备注',
			type: 'textarea',
			icon: FileText,
			placeholder: '添加关于此联系人的备注...'
		}
	]);

	// Column visibility state - use defaults (excludes owner)
	let visibleColumns = $state([...DEFAULT_VISIBLE_COLUMNS]);

	// Load column visibility from localStorage
	onMount(() => {
		const saved = localStorage.getItem(STORAGE_KEY);
		if (saved) {
			try {
				visibleColumns = JSON.parse(saved);
			} catch (e) {
				console.error('Failed to parse saved columns:', e);
			}
		}
	});

	// Save column visibility when changed
	$effect(() => {
		localStorage.setItem(STORAGE_KEY, JSON.stringify(visibleColumns));
	});

	/**
	 * @param {string} key
	 */
	function toggleColumn(key) {
		const col = columns.find((c) => c.key === key);
		if (col?.canHide === false) return;

		if (visibleColumns.includes(key)) {
			visibleColumns = visibleColumns.filter((k) => k !== key);
		} else {
			visibleColumns = [...visibleColumns, key];
		}
	}

	// Computed values from data (contacts and owners)
	const contacts = $derived(data.contacts || []);
	const pagination = $derived(data.pagination || { page: 1, limit: 10, total: 0, totalPages: 0 });
	const owners = $derived(loadedOwners);

	// Drawer state (simplified - single drawer)
	let drawerOpen = $state(false);

	// Load dropdown options when drawer opens (lazy load)
	$effect(() => {
		if (drawerOpen && !dropdownOptionsLoaded) {
			loadDropdownOptions();
		}
	});
	/** @type {'view' | 'create'} */
	let drawerMode = $state('view');
	/** @type {any} */
	let selectedContact = $state(null);
	let drawerLoading = $state(false);
	let isSubmitting = $state(false);

	// Empty contact template for create mode
	const emptyContact = {
		firstName: '',
		lastName: '',
		email: '',
		phone: '',
		organization: '',
		title: '',
		department: '',
		doNotCall: false,
		linkedInUrl: '',
		addressLine: '',
		city: '',
		state: '',
		postcode: '',
		country: '',
		description: '',
		tags: /** @type {string[]} */ ([])
	};

	// Drawer form data - mutable copy for editing
	let drawerFormData = $state({ ...emptyContact });

	// Reset form data when contact changes or drawer opens
	$effect(() => {
		if (drawerOpen) {
			if (drawerMode === 'create') {
				drawerFormData = { ...emptyContact };
			} else if (selectedContact) {
				drawerFormData = {
					...selectedContact,
					// Extract tag IDs from tag objects
					tags: (selectedContact.tags || []).map((/** @type {any} */ t) => t.id)
				};
			}
		}
	});

	// Computed display name for drawer title
	const drawerTitle = $derived(
		`${drawerFormData.firstName || ''} ${drawerFormData.lastName || ''}`.trim() || ''
	);

	// URL sync
	$effect(() => {
		const viewId = $page.url.searchParams.get('view');
		const action = $page.url.searchParams.get('action');

		if (action === 'create') {
			selectedContact = null;
			drawerMode = 'create';
			drawerOpen = true;
		} else if (viewId && contacts.length > 0) {
			const contact = contacts.find((c) => c.id === viewId);
			if (contact) {
				selectedContact = contact;
				drawerMode = 'view';
				drawerOpen = true;
			}
		}
	});

	/**
	 * Update URL
	 * @param {string | null} viewId
	 * @param {string | null} action
	 * @returns {Promise<void>}
	 */
	async function updateUrl(viewId, action) {
		const url = new URL($page.url);
		if (viewId) {
			url.searchParams.set('view', viewId);
			url.searchParams.delete('action');
		} else if (action) {
			url.searchParams.set('action', action);
			url.searchParams.delete('view');
		} else {
			url.searchParams.delete('view');
			url.searchParams.delete('action');
		}
		await goto(url.toString(), { replaceState: true, noScroll: true });
	}

	/**
	 * Open drawer for viewing/editing a contact
	 * @param {any} contact
	 */
	function openContact(contact) {
		selectedContact = contact;
		drawerMode = 'view';
		drawerOpen = true;
		updateUrl(contact.id, null);
	}

	/**
	 * Open drawer for creating a new contact
	 */
	function openCreate() {
		selectedContact = null;
		drawerMode = 'create';
		drawerOpen = true;
		updateUrl(null, 'create');
	}

	/**
	 * Close drawer
	 * @returns {Promise<void>}
	 */
	async function closeDrawer() {
		drawerOpen = false;
		await updateUrl(null, null);
	}

	/**
	 * Handle drawer open change
	 * @param {boolean} open
	 */
	function handleDrawerChange(open) {
		drawerOpen = open;
		if (!open) updateUrl(null, null);
	}

	// URL-based filter state from server
	const filters = $derived(data.filters);

	// Count active filters
	const activeFiltersCount = $derived.by(() => {
		let count = 0;
		if (filters.search) count++;
		if (filters.assigned_to?.length > 0) count++;
		if (filters.tags?.length > 0) count++;
		if (filters.created_at_gte || filters.created_at_lte) count++;
		return count;
	});

	/**
	 * Update URL with new filters
	 * @param {Record<string, any>} newFilters
	 */
	async function updateFilters(newFilters) {
		const url = new URL($page.url);
		// Clear existing filter params (preserve view/action)
		['search', 'assigned_to', 'tags', 'created_at_gte', 'created_at_lte'].forEach((key) =>
			url.searchParams.delete(key)
		);
		// Set new params
		Object.entries(newFilters).forEach(([key, value]) => {
			if (Array.isArray(value)) {
				value.forEach((v) => url.searchParams.append(key, v));
			} else if (value) {
				url.searchParams.set(key, value);
			}
		});
		await goto(url.toString(), { replaceState: true, noScroll: true, invalidateAll: true });
	}

	/**
	 * Clear all filters
	 */
	function clearFilters() {
		updateFilters({});
	}

	/**
	 * Handle page change
	 * @param {number} newPage
	 */
	async function handlePageChange(newPage) {
		const url = new URL($page.url);
		url.searchParams.set('page', newPage.toString());
		await goto(url.toString(), { replaceState: true, noScroll: true, invalidateAll: true });
	}

	/**
	 * Handle limit change
	 * @param {number} newLimit
	 */
	async function handleLimitChange(newLimit) {
		const url = new URL($page.url);
		url.searchParams.set('limit', newLimit.toString());
		url.searchParams.set('page', '1'); // Reset to first page
		await goto(url.toString(), { replaceState: true, noScroll: true, invalidateAll: true });
	}

	// Contacts are already filtered server-side
	const filteredContacts = $derived(contacts);

	// Filter panel expansion state
	let filtersExpanded = $state(false);

	// Form references for server actions
	/** @type {HTMLFormElement} */
	let createForm;
	/** @type {HTMLFormElement} */
	let updateForm;
	/** @type {HTMLFormElement} */
	let deleteForm;

	// Form data state
	let formState = $state({
		contactId: '',
		firstName: '',
		lastName: '',
		email: '',
		phone: '',
		organization: '',
		title: '',
		department: '',
		doNotCall: false,
		linkedInUrl: '',
		addressLine: '',
		city: '',
		state: '',
		postcode: '',
		country: '',
		description: '',
		tags: /** @type {string[]} */ ([])
	});

	/**
	 * Get full name
	 * @param {any} contact
	 */
	function getFullName(contact) {
		return `${contact.firstName} ${contact.lastName}`.trim();
	}

	/**
	 * Get initials for contact
	 * @param {any} contact
	 */
	function getContactInitials(contact) {
		return getNameInitials(contact.firstName, contact.lastName);
	}

	/**
	 * Convert contact to form state for quick edit
	 * @param {any} contact
	 */
	function contactToFormState(contact) {
		return {
			contactId: contact.id,
			firstName: contact.firstName || '',
			lastName: contact.lastName || '',
			email: contact.email || '',
			phone: contact.phone || '',
			organization: contact.organization || '',
			title: contact.title || '',
			department: contact.department || '',
			doNotCall: contact.doNotCall || false,
			linkedInUrl: contact.linkedInUrl || '',
			addressLine: contact.addressLine || '',
			city: contact.city || '',
			state: contact.state || '',
			postcode: contact.postcode || '',
			country: contact.country || '',
			description: contact.description || '',
			tags: (contact.tags || []).map((/** @type {any} */ t) => t.id || t)
		};
	}

	/**
	 * Handle quick edit from cell (inline editing)
	 * @param {any} contact
	 * @param {string} field
	 * @param {any} value
	 */
	async function handleQuickEdit(contact, field, value) {
		// Populate form state with current contact data
		const currentState = contactToFormState(contact);

		// Update the specific field
		currentState[field] = value;

		// Copy to form state
		Object.assign(formState, currentState);

		await tick();
		updateForm.requestSubmit();
	}

	/**
	 * Handle row change from CrmTable (inline editing)
	 * @param {any} row
	 * @param {string} field
	 * @param {any} value
	 */
	async function handleRowChange(row, field, value) {
		await handleQuickEdit(row, field, value);
	}

	/**
	 * Handle field change from CrmDrawer - just updates local state
	 * @param {string} field
	 * @param {any} value
	 */
	function handleDrawerFieldChange(field, value) {
		// Update local form data only - no auto-save
		drawerFormData = { ...drawerFormData, [field]: value };
	}

	/**
	 * Handle save for view/edit mode
	 */
	async function handleDrawerUpdate() {
		if (drawerMode !== 'view' || !selectedContact) return;

		isSubmitting = true;
		formState.contactId = selectedContact.id;
		formState.firstName = drawerFormData.firstName || '';
		formState.lastName = drawerFormData.lastName || '';
		formState.email = drawerFormData.email || '';
		formState.phone = drawerFormData.phone || '';
		formState.organization = drawerFormData.organization || '';
		formState.title = drawerFormData.title || '';
		formState.department = drawerFormData.department || '';
		formState.doNotCall = drawerFormData.doNotCall || false;
		formState.linkedInUrl = drawerFormData.linkedInUrl || '';
		formState.addressLine = drawerFormData.addressLine || '';
		formState.city = drawerFormData.city || '';
		formState.state = drawerFormData.state || '';
		formState.postcode = drawerFormData.postcode || '';
		formState.country = drawerFormData.country || '';
		formState.description = drawerFormData.description || '';
		formState.tags = drawerFormData.tags || [];

		await tick();
		updateForm.requestSubmit();
	}

	/**
	 * Handle save for create mode
	 */
	async function handleDrawerSave() {
		if (drawerMode !== 'create') return;

		isSubmitting = true;
		formState.firstName = drawerFormData.firstName || '';
		formState.lastName = drawerFormData.lastName || '';
		formState.email = drawerFormData.email || '';
		formState.phone = drawerFormData.phone || '';
		formState.organization = drawerFormData.organization || '';
		formState.title = drawerFormData.title || '';
		formState.department = drawerFormData.department || '';
		formState.doNotCall = drawerFormData.doNotCall || false;
		formState.linkedInUrl = drawerFormData.linkedInUrl || '';
		formState.addressLine = drawerFormData.addressLine || '';
		formState.city = drawerFormData.city || '';
		formState.state = drawerFormData.state || '';
		formState.postcode = drawerFormData.postcode || '';
		formState.country = drawerFormData.country || '';
		formState.description = drawerFormData.description || '';
		formState.tags = drawerFormData.tags || [];

		await tick();
		createForm.requestSubmit();
	}

	/**
	 * Handle contact delete
	 */
	async function handleDelete() {
		if (!selectedContact) return;
		if (!confirm(`Are you sure you want to delete ${getFullName(selectedContact)}?`)) return;

		formState.contactId = selectedContact.id;
		await tick();
		deleteForm.requestSubmit();
	}

	/**
	 * Create enhance handler for form actions
	 * @param {string} successMessage
	 * @param {boolean} closeOnSuccess
	 */
	function createEnhanceHandler(successMessage, closeOnSuccess = true) {
		return () => {
			return async ({ result }) => {
				isSubmitting = false;
				if (result.type === 'success') {
					toast.success(successMessage);
					if (closeOnSuccess) {
						await closeDrawer();
					}
					await invalidateAll();
				} else if (result.type === 'failure') {
					toast.error(result.data?.error || 'Operation failed');
				} else if (result.type === 'error') {
					toast.error('An unexpected error occurred');
				}
			};
		};
	}
</script>

<svelte:head>
	<title>联系人 - BottleCRM</title>
</svelte:head>

<PageHeader title="联系人" subtitle="{filteredContacts.length} / {contacts.length} 个联系人">
	{#snippet actions()}
		<div class="flex items-center gap-2">
			<!-- Filter Toggle Button -->
			<Button
				variant={filtersExpanded ? 'secondary' : 'outline'}
				size="sm"
				class="gap-2"
				onclick={() => (filtersExpanded = !filtersExpanded)}
			>
				<Filter class="h-4 w-4" />
				筛选
				{#if activeFiltersCount > 0}
					<span
						class="rounded-full bg-blue-100 px-1.5 py-0.5 text-xs font-medium text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
					>
						{activeFiltersCount}
					</span>
				{/if}
			</Button>

			<!-- Column Visibility Dropdown -->
			<DropdownMenu.Root>
				<DropdownMenu.Trigger>
					{#snippet child({ props })}
						<Button {...props} variant="outline" size="sm" class="gap-2">
							<Eye class="h-4 w-4" />
							Columns
							{#if visibleColumns.length < columns.length}
								<span
									class="rounded-full bg-blue-100 px-1.5 py-0.5 text-xs font-medium text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
								>
									{visibleColumns.length}/{columns.length}
								</span>
							{/if}
						</Button>
					{/snippet}
				</DropdownMenu.Trigger>
				<DropdownMenu.Content align="end" class="w-48">
					<DropdownMenu.Label>切换列</DropdownMenu.Label>
					<DropdownMenu.Separator />
					{#each columns as column (column.key)}
						<DropdownMenu.CheckboxItem
							class=""
							checked={visibleColumns.includes(column.key)}
							onCheckedChange={() => toggleColumn(column.key)}
							disabled={column.canHide === false}
						>
							{column.label}
						</DropdownMenu.CheckboxItem>
					{/each}
				</DropdownMenu.Content>
			</DropdownMenu.Root>

			<Button onclick={openCreate}>
				<Plus class="mr-2 h-4 w-4" />
				新建联系人
			</Button>
		</div>
	{/snippet}
</PageHeader>

<div class="flex-1">
	<!-- Collapsible Filter Bar -->
	<FilterBar
		minimal={true}
		expanded={filtersExpanded}
		activeCount={activeFiltersCount}
		onClear={clearFilters}
		class="pb-4"
	>
		<SearchInput
			value={filters.search}
			placeholder="搜索联系人..."
			onchange={(value) => updateFilters({ ...filters, search: value })}
			class="w-64"
		/>
		<DateRangeFilter
			label="创建时间"
			startDate={filters.created_at_gte}
			endDate={filters.created_at_lte}
			onchange={(start, end) =>
				updateFilters({ ...filters, created_at_gte: start, created_at_lte: end })}
			class="w-56"
		/>
	</FilterBar>

	<!-- Table -->
	{#if filteredContacts.length === 0}
		<div class="flex flex-col items-center justify-center py-16 text-center">
			<User class="text-muted-foreground/50 mb-4 h-12 w-12" />
			<h3 class="text-foreground text-lg font-medium">未找到联系人</h3>
		</div>
	{:else}
		<CrmTable
			data={filteredContacts}
			{columns}
			bind:visibleColumns
			onRowChange={handleRowChange}
			onRowClick={(row) => openContact(row)}
		>
			{#snippet emptyState()}
				<div class="flex flex-col items-center justify-center py-16 text-center">
					<User class="text-muted-foreground/50 mb-4 h-12 w-12" />
					<h3 class="text-foreground text-lg font-medium">未找到联系人</h3>
				</div>
			{/snippet}
		</CrmTable>
	{/if}

	<!-- Pagination -->
	<Pagination
		page={pagination.page}
		limit={pagination.limit}
		total={pagination.total}
		onPageChange={handlePageChange}
		onLimitChange={handleLimitChange}
	/>
</div>

<!-- Contact Drawer -->
<CrmDrawer
	bind:open={drawerOpen}
	onOpenChange={handleDrawerChange}
	data={{ ...drawerFormData, displayName: drawerTitle }}
	columns={drawerColumns}
	titleKey="displayName"
	titlePlaceholder="新建联系人"
	titleEditable={false}
	headerLabel="Contact"
	mode={drawerMode}
	loading={drawerLoading || isSubmitting}
	onFieldChange={handleDrawerFieldChange}
	onDelete={handleDelete}
	onClose={closeDrawer}
>
	{#snippet activitySection()}
		<!-- Metadata (view mode only) -->
		{#if drawerMode !== 'create' && selectedContact}
			<div>
				<p
					class="mb-2 text-xs font-medium tracking-wider text-gray-500 uppercase dark:text-gray-400"
				>
					Details
				</p>
				<div class="grid grid-cols-2 gap-3 text-sm">
					<div>
						<p class="text-xs text-gray-400 dark:text-gray-500">Owner</p>
						<p class="font-medium text-gray-900 dark:text-gray-100">
							{selectedContact.owner?.name || 'Unassigned'}
						</p>
					</div>
					<div>
						<p class="text-xs text-gray-400 dark:text-gray-500">Created</p>
						<p class="font-medium text-gray-900 dark:text-gray-100">
							{formatRelativeDate(selectedContact.createdAt)}
						</p>
					</div>
				</div>
			</div>
		{/if}
	{/snippet}

	{#snippet footerActions()}
		{#if drawerMode === 'create'}
			<Button variant="outline" onclick={closeDrawer} disabled={isSubmitting}>取消</Button>
			<Button
				onclick={handleDrawerSave}
				disabled={isSubmitting || !drawerFormData.firstName?.trim()}
			>
				{isSubmitting ? '创建中...' : '创建联系人'}
			</Button>
		{:else}
			<Button variant="outline" onclick={closeDrawer} disabled={isSubmitting}>取消</Button>
			<Button
				onclick={handleDrawerUpdate}
				disabled={isSubmitting || !drawerFormData.firstName?.trim()}
			>
				{isSubmitting ? '保存中...' : '保存'}
			</Button>
		{/if}
	{/snippet}
</CrmDrawer>

<!-- Hidden forms for server actions -->
<form
	method="POST"
	action="?/create"
	bind:this={createForm}
	use:enhance={createEnhanceHandler('Contact created successfully')}
	class="hidden"
>
	<input type="hidden" name="firstName" value={formState.firstName} />
	<input type="hidden" name="lastName" value={formState.lastName} />
	<input type="hidden" name="email" value={formState.email} />
	<input type="hidden" name="phone" value={formState.phone} />
	<input type="hidden" name="organization" value={formState.organization} />
	<input type="hidden" name="title" value={formState.title} />
	<input type="hidden" name="department" value={formState.department} />
	<input type="hidden" name="doNotCall" value={formState.doNotCall} />
	<input type="hidden" name="linkedInUrl" value={formState.linkedInUrl} />
	<input type="hidden" name="addressLine" value={formState.addressLine} />
	<input type="hidden" name="city" value={formState.city} />
	<input type="hidden" name="state" value={formState.state} />
	<input type="hidden" name="postcode" value={formState.postcode} />
	<input type="hidden" name="country" value={formState.country} />
	<input type="hidden" name="description" value={formState.description} />
	<input type="hidden" name="tags" value={JSON.stringify(formState.tags)} />
</form>

<form
	method="POST"
	action="?/update"
	bind:this={updateForm}
	use:enhance={createEnhanceHandler('Contact updated successfully', true)}
	class="hidden"
>
	<input type="hidden" name="contactId" value={formState.contactId} />
	<input type="hidden" name="firstName" value={formState.firstName} />
	<input type="hidden" name="lastName" value={formState.lastName} />
	<input type="hidden" name="email" value={formState.email} />
	<input type="hidden" name="phone" value={formState.phone} />
	<input type="hidden" name="organization" value={formState.organization} />
	<input type="hidden" name="title" value={formState.title} />
	<input type="hidden" name="department" value={formState.department} />
	<input type="hidden" name="doNotCall" value={formState.doNotCall} />
	<input type="hidden" name="linkedInUrl" value={formState.linkedInUrl} />
	<input type="hidden" name="addressLine" value={formState.addressLine} />
	<input type="hidden" name="city" value={formState.city} />
	<input type="hidden" name="state" value={formState.state} />
	<input type="hidden" name="postcode" value={formState.postcode} />
	<input type="hidden" name="country" value={formState.country} />
	<input type="hidden" name="description" value={formState.description} />
	<input type="hidden" name="tags" value={JSON.stringify(formState.tags)} />
</form>

<form
	method="POST"
	action="?/delete"
	bind:this={deleteForm}
	use:enhance={createEnhanceHandler('Contact deleted successfully')}
	class="hidden"
>
	<input type="hidden" name="contactId" value={formState.contactId} />
</form>
