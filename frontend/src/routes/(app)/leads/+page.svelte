<script>
	import { enhance } from '$app/forms';
	import { invalidateAll, goto } from '$app/navigation';
	import { tick, onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import {
		Plus,
		Phone,
		Mail,
		Building2,
		User,
		Calendar,
		Eye,
		Star,
		Globe,
		Briefcase,
		Linkedin,
		Target,
		DollarSign,
		Percent,
		MapPin,
		FileText,
		Users,
		UserPlus,
		Tag,
		MessageSquare,
		Loader2,
		ArrowRightCircle,
		Banknote,
		Filter
	} from '@lucide/svelte';
	import { page } from '$app/stores';
	import { FilterBar, SearchInput, SelectFilter, DateRangeFilter } from '$lib/components/ui/filter';
	import { Pagination } from '$lib/components/ui/pagination';
	import { Button } from '$lib/components/ui/button/index.js';
	import { PageHeader } from '$lib/components/layout';
	import { INDUSTRIES, COUNTRIES } from '$lib/constants/lead-choices.js';
	import { CURRENCY_CODES } from '$lib/constants/filters-zh.js';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu/index.js';
	import { formatRelativeDate, formatDate, getNameInitials } from '$lib/utils/formatting.js';
	import {
		leadStatusOptions,
		leadRatingOptions,
		getOptionStyle,
		getOptionLabel,
		getOptionBgColor
	} from '$lib/utils/table-helpers.js';
	import CrmTable from '$lib/components/ui/crm-table/CrmTable.svelte';
	import CrmDrawer from '$lib/components/ui/crm-drawer/CrmDrawer.svelte';
	import { apiRequest } from '$lib/api.js';
	import { orgSettings } from '$lib/stores/org.js';

	// Column visibility configuration
	const STORAGE_KEY = 'leads-column-config';

	/**
	 * @typedef {'text' | 'email' | 'number' | 'date' | 'select' | 'checkbox' | 'relation'} ColumnType
	 * @typedef {{ key: string, label: string, type?: ColumnType, width?: string, editable?: boolean, canHide?: boolean, getValue?: (row: any) => any, emptyText?: string, relationIcon?: string, options?: any[] }} ColumnDef
	 */

	/** @type {ColumnDef[]} */
	const columns = [
		{
			key: 'title',
			label: '标题',
			type: 'text',
			width: 'w-[200px]',
			canHide: false,
			emptyText: '未命名'
		},
		{
			key: 'name',
			label: '姓名',
			type: 'text',
			width: 'w-[180px]',
			editable: false,
			canHide: true,
			getValue: (row) => `${row.firstName || ''} ${row.lastName || ''}`.trim(),
			emptyText: ''
		},
		{
			key: 'company',
			label: '公司',
			type: 'relation',
			width: 'w-40',
			relationIcon: 'building',
			getValue: (row) => (typeof row.company === 'object' ? row.company?.name : row.company),
			emptyText: ''
		},
		{
			key: 'email',
			label: '邮箱',
			type: 'email',
			width: 'w-52',
			emptyText: ''
		},
		{
			key: 'status',
			label: '状态',
			type: 'select',
			width: 'w-36',
			options: leadStatusOptions
		},
		{
			key: 'rating',
			label: '评分',
			type: 'select',
			width: 'w-28',
			options: leadRatingOptions
		},
		{
			key: 'createdAt',
			label: '创建时间',
			type: 'date',
			width: 'w-36',
			editable: false
		},
		// Hidden by default
		{
			key: 'phone',
			label: '电话',
			type: 'text',
			width: 'w-36',
			canHide: true,
			emptyText: ''
		},
		{
			key: 'jobTitle',
			label: '职位',
			type: 'text',
			width: 'w-36',
			canHide: true,
			emptyText: ''
		},
		{
			key: 'leadSource',
			label: '来源',
			type: 'select',
			width: 'w-28',
			canHide: true
		},
		{
			key: 'industry',
			label: '行业',
			type: 'select',
			width: 'w-32',
			canHide: true,
			options: INDUSTRIES.map((i) => ({
				...i,
				color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
			}))
		},
		{
			key: 'owner',
			label: '负责人',
			type: 'relation',
			width: 'w-36',
			canHide: true,
			relationIcon: 'user',
			getValue: (row) => row.owner?.name || '',
			emptyText: ''
		}
	];

	// Default visible columns (7 columns: Title, Name, Company, Email, Status, Rating, Created)
	const DEFAULT_VISIBLE_COLUMNS = [
		'title',
		'name',
		'company',
		'email',
		'status',
		'rating',
		'createdAt'
	];
	let visibleColumns = $state([...DEFAULT_VISIBLE_COLUMNS]);

	// Source options for leads
	const sourceOptions = [
		{
			value: 'call',
			label: '电话',
			color: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
		},
		{
			value: 'email',
			label: '邮件',
			color: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400'
		},
		{
			value: 'existing customer',
			label: '现有客户',
			color: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
		},
		{
			value: 'partner',
			label: '合作伙伴',
			color: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'
		},
		{
			value: 'public relations',
			label: '公共关系',
			color: 'bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-400'
		},
		{
			value: 'campaign',
			label: '营销活动',
			color: 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-400'
		},
		{
			value: 'other',
			label: '其他',
			color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
		}
	];

	// Salutation options
	const salutationOptions = [
		{
			value: 'Mr',
			label: 'Mr',
			color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
		},
		{
			value: 'Mrs',
			label: 'Mrs',
			color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
		},
		{
			value: 'Ms',
			label: 'Ms',
			color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
		},
		{
			value: 'Dr',
			label: 'Dr',
			color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
		},
		{
			value: 'Prof',
			label: 'Prof',
			color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
		}
	];

	// Currency options for select
	const currencyOptions = CURRENCY_CODES.filter((c) => c.value).map((c) => ({
		value: c.value,
		label: c.label,
		color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
	}));

	// Full drawer columns for NotionDrawer (all lead fields)
	// Using $derived so currency symbol updates with org settings
	const drawerColumns = $derived([
		// Contact Information
		{
			key: 'salutation',
			label: '称谓',
			type: 'select',
			icon: User,
			options: salutationOptions
		},
		{
			key: 'firstName',
			label: '名',
			type: 'text',
			icon: User,
			placeholder: '请输入名',
			essential: true
		},
		{
			key: 'lastName',
			label: '姓',
			type: 'text',
			icon: User,
			placeholder: '请输入姓',
			essential: true
		},
		{
			key: 'email',
			label: '邮箱',
			type: 'email',
			icon: Mail,
			placeholder: '请输入邮箱',
			essential: true
		},
		{
			key: 'phone',
			label: '电话',
			type: 'text',
			icon: Phone,
			placeholder: '请输入电话',
			essential: true
		},
		{
			key: 'jobTitle',
			label: '职位',
			type: 'text',
			icon: Briefcase,
			placeholder: '请输入职位'
		},
		{
			key: 'company',
			label: '公司',
			type: 'text',
			icon: Building2,
			getValue: (/** @type {any} */ row) =>
				typeof row.company === 'object' ? row.company?.name : row.company,
			placeholder: '请输入公司名称',
			essential: true
		},
		{
			key: 'website',
			label: '网站',
			type: 'text',
			icon: Globe,
			placeholder: '请输入网站地址'
		},
		{
			key: 'linkedinUrl',
			label: 'LinkedIn',
			type: 'text',
			icon: Linkedin,
			placeholder: '请输入LinkedIn链接'
		},
		// Lead Details
		{
			key: 'status',
			label: '状态',
			type: 'select',
			icon: Briefcase,
			options: leadStatusOptions,
			essential: true
		},
		{
			key: 'rating',
			label: '评分',
			type: 'select',
			icon: Star,
			options: leadRatingOptions
		},
		// Metadata
		{
			key: 'createdAt',
			label: '创建时间',
			type: 'date',
			icon: Calendar,
			editable: false,
			hideOnCreate: true
		},
		{
			key: 'leadSource',
			label: '来源',
			type: 'select',
			icon: Target,
			options: sourceOptions
		},
		{
			key: 'industry',
			label: '行业',
			type: 'select',
			icon: Building2,
			options: INDUSTRIES.map((i) => ({
				...i,
				color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
			}))
		},
		// Deal Information
		{
			key: 'opportunityAmount',
			label: '交易金额',
			type: 'number',
			icon: DollarSign,
			placeholder: '0',
			essential: true
		},
		{
			key: 'currency',
			label: '币种',
			type: 'select',
			icon: Banknote,
			options: currencyOptions,
			placeholder: '选择币种',
			essential: true
		},
		{
			key: 'probability',
			label: '成交概率',
			type: 'number',
			icon: Percent,
			placeholder: '0-100'
		},
		{
			key: 'closeDate',
			label: '预计成交日期',
			type: 'date',
			icon: Calendar,
			placeholder: '选择日期',
			hideOnCreate: true
		},
		// 活动记录
		{
			key: 'lastContacted',
			label: '最后联系',
			type: 'date',
			icon: Calendar,
			placeholder: '选择日期',
			hideOnCreate: true
		},
		{
			key: 'nextFollowUp',
			label: '下次跟进',
			type: 'date',
			icon: Calendar,
			placeholder: '选择日期'
		},
		// Address
		{
			key: 'addressLine',
			label: '地址',
			type: 'text',
			icon: MapPin,
			placeholder: '街道地址'
		},
		{
			key: 'city',
			label: '城市',
			type: 'text',
			icon: MapPin,
			placeholder: '城市'
		},
		{
			key: 'state',
			label: '省/州',
			type: 'text',
			icon: MapPin,
			placeholder: '省/州'
		},
		{
			key: 'postcode',
			label: '邮编',
			type: 'text',
			icon: MapPin,
			placeholder: '邮政编码'
		},
		{
			key: 'country',
			label: '国家',
			type: 'select',
			icon: Globe,
			options: COUNTRIES.map((c) => ({
				...c,
				color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
			})),
			essential: true
		},
		// Notes
		{
			key: 'description',
			label: '备注',
			type: 'textarea',
			icon: FileText,
			placeholder: '添加备注...'
		},
		// Assignment (multi-select fields - options populated dynamically)
		{
			key: 'assignedTo',
			label: '分配给',
			type: 'multiselect',
			icon: Users,
			options: []
		},
		{
			key: 'teams',
			label: '团队',
			type: 'multiselect',
			icon: Users,
			options: []
		},
		{
			key: 'contacts',
			label: '联系人',
			type: 'multiselect',
			icon: UserPlus,
			options: []
		},
		{
			key: 'tags',
			label: '标签',
			type: 'multiselect',
			icon: Tag,
			options: []
		}
	]);

	/**
	 * Load column visibility from localStorage
	 */
	function loadColumnVisibility() {
		if (typeof window === 'undefined') return;
		try {
			const saved = localStorage.getItem(STORAGE_KEY);
			if (saved) {
				const parsed = JSON.parse(saved);
				// Filter to only include valid column keys
				visibleColumns = parsed.filter((key) => columns.some((c) => c.key === key));
			}
		} catch (e) {
			console.error('Failed to load column visibility:', e);
		}
	}

	onMount(() => {
		loadColumnVisibility();
	});

	// Save to localStorage when column visibility changes
	$effect(() => {
		if (typeof window !== 'undefined') {
			localStorage.setItem(STORAGE_KEY, JSON.stringify(visibleColumns));
		}
	});

	/**
	 * Toggle column visibility
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

	/** @type {{ data: any }} */
	let { data } = $props();

	// Computed values
	const leads = $derived(data.leads || []);
	const pagination = $derived(data.pagination || { page: 1, limit: 10, total: 0, totalPages: 0 });

	// Lazy-loaded form options (only fetched when drawer opens)
	let formOptions = $state(
		/** @type {{ users: any[], teamsList: any[], contactsList: any[], tagsList: any[] }} */ ({
			users: [],
			teamsList: [],
			contactsList: [],
			tagsList: []
		})
	);
	let formOptionsLoaded = $state(false);
	let formOptionsLoading = $state(false);

	/**
	 * Load form options for drawer (lazy-loaded on first drawer open)
	 */
	async function loadFormOptions() {
		if (formOptionsLoaded || formOptionsLoading) return;

		formOptionsLoading = true;
		try {
			const [usersResponse, teamsResponse, contactsResponse, tagsResponse] = await Promise.all([
				apiRequest('/users/').catch(() => ({ active_users: { active_users: [] } })),
				apiRequest('/teams/').catch(() => ({ teams: [] })),
				apiRequest('/contacts/').catch(() => ({ contact_obj_list: [] })),
				apiRequest('/tags/').catch(() => [])
			]);

			// Transform responses
			const activeUsers = usersResponse?.active_users?.active_users || [];
			const users = activeUsers.map((/** @type {any} */ u) => ({
				value: u.id,
				label: u.user_details?.email || u.user?.email || u.email || '未知'
			}));

			const teamsList = (teamsResponse.teams || teamsResponse || []).map(
				(/** @type {any} */ t) => ({
					value: t.id,
					label: t.name || '未知'
				})
			);

			const contactsList = (
				contactsResponse.contact_obj_list ||
				contactsResponse.results ||
				contactsResponse ||
				[]
			).map((/** @type {any} */ c) => ({
				value: c.id,
				label: `${c.first_name || ''} ${c.last_name || ''}`.trim() || c.email || '未知'
			}));

			const tagsList = (
				Array.isArray(tagsResponse) ? tagsResponse : tagsResponse.results || []
			).map((/** @type {any} */ t) => ({
				value: t.id,
				label: t.name || '未知'
			}));

			formOptions = { users, teamsList, contactsList, tagsList };
			formOptionsLoaded = true;
		} catch (err) {
			console.error('Failed to load form options:', err);
		} finally {
			formOptionsLoading = false;
		}
	}

	// Drawer state (NotionDrawer for view/create)
	let drawerOpen = $state(false);
	/** @type {'view' | 'create'} */
	let drawerMode = $state(/** @type {'view' | 'create'} */ ('view'));
	/** @type {any} */
	let drawerData = $state(null);
	let drawerLoading = $state(false);
	let isSaving = $state(false);

	// For create mode - temporary form data
	let createFormData = $state(
		/** @type {Record<string, any>} */ ({
			title: '',
			salutation: '',
			firstName: '',
			lastName: '',
			email: '',
			phone: '',
			jobTitle: '',
			company: '',
			website: '',
			linkedinUrl: '',
			status: 'ASSIGNED',
			rating: '',
			leadSource: '',
			industry: '',
			opportunityAmount: '',
			probability: '',
			closeDate: '',
			lastContacted: '',
			nextFollowUp: '',
			addressLine: '',
			city: '',
			state: '',
			postcode: '',
			country: '',
			description: '',
			assignedTo: [],
			teams: [],
			contacts: [],
			tags: []
		})
	);

	// Current drawer data (either selected lead or create form data)
	const currentDrawerData = $derived(drawerMode === 'create' ? createFormData : drawerData);

	// Drawer columns with dynamic options for multi-selects
	const drawerColumnsWithOptions = $derived(
		drawerColumns.map((col) => {
			if (col.key === 'assignedTo') return { ...col, options: formOptions.users || [] };
			if (col.key === 'teams') return { ...col, options: formOptions.teamsList || [] };
			if (col.key === 'contacts') return { ...col, options: formOptions.contactsList || [] };
			if (col.key === 'tags') return { ...col, options: formOptions.tagsList || [] };
			return col;
		})
	);

	// URL sync
	$effect(() => {
		const viewId = $page.url.searchParams.get('view');
		const action = $page.url.searchParams.get('action');

		if (action === 'create') {
			drawerData = null;
			drawerMode = 'create';
			drawerOpen = true;
			// Lazy load form options when drawer opens via URL
			loadFormOptions();
		} else if (viewId && leads.length > 0) {
			const lead = leads.find((l) => l.id === viewId);
			if (lead) {
				drawerData = lead;
				drawerMode = 'view';
				drawerOpen = true;
				// Lazy load form options when drawer opens via URL
				loadFormOptions();
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
	 * Open drawer for viewing/editing a lead
	 * @param {any} lead
	 */
	function openLead(lead) {
		drawerData = lead;
		drawerMode = 'view';
		drawerOpen = true;
		updateUrl(lead.id, null);
		// Lazy load form options when drawer opens
		loadFormOptions();
	}

	/**
	 * Open drawer for creating a new lead
	 */
	function openCreate() {
		// Reset create form data
		createFormData = {
			title: '',
			salutation: '',
			firstName: '',
			lastName: '',
			email: '',
			phone: '',
			jobTitle: '',
			company: '',
			website: '',
			linkedinUrl: '',
			status: 'ASSIGNED',
			rating: '',
			leadSource: '',
			industry: '',
			opportunityAmount: '',
			probability: '',
			closeDate: '',
			lastContacted: '',
			nextFollowUp: '',
			addressLine: '',
			city: '',
			state: '',
			postcode: '',
			country: '',
			description: '',
			assignedTo: [],
			teams: [],
			contacts: [],
			tags: []
		};
		drawerData = null;
		drawerMode = 'create';
		drawerOpen = true;
		updateUrl(null, 'create');
		// Lazy load form options when drawer opens
		loadFormOptions();
	}

	/**
	 * Close drawer
	 * @returns {Promise<void>}
	 */
	async function closeDrawer() {
		drawerOpen = false;
		drawerData = null;
		await updateUrl(null, null);
	}

	/**
	 * Handle drawer open change
	 * @param {boolean} open
	 */
	function handleDrawerChange(open) {
		drawerOpen = open;
		if (!open) {
			drawerData = null;
			updateUrl(null, null);
		}
	}

	/**
	 * Handle row change from NotionTable (inline editing)
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
		if (drawerMode === 'create') {
			// For create mode, just update the form data
			createFormData = { ...createFormData, [field]: value };
		} else if (drawerData) {
			// For edit mode, just update local data - no auto-save
			drawerData = { ...drawerData, [field]: value };
		}
	}

	/**
	 * Handle save for view/edit mode
	 */
	async function handleDrawerUpdate() {
		if (drawerMode !== 'view' || !drawerData) return;

		isSaving = true;
		// Populate form state with current drawer data
		const currentState = leadToFormState(drawerData);
		Object.assign(formState, currentState);

		await tick();
		updateForm.requestSubmit();
	}

	/**
	 * Handle title change from NotionDrawer
	 * @param {string} value
	 */
	async function handleTitleChange(value) {
		if (drawerMode === 'create') {
			// Parse the name into firstName and lastName
			const parts = value.trim().split(' ');
			createFormData = {
				...createFormData,
				title: value,
				firstName: parts[0] || '',
				lastName: parts.slice(1).join(' ') || ''
			};
		} else if (drawerData) {
			// For existing leads, update title
			await handleQuickEdit(drawerData, 'title', value);
		}
	}

	/**
	 * Handle delete from NotionDrawer
	 */
	async function handleDrawerDelete() {
		if (!drawerData) return;
		const lead = drawerData;
		closeDrawer();
		await handleRowDelete(lead);
	}

	/**
	 * Handle convert from NotionDrawer
	 */
	async function handleDrawerConvert() {
		if (!drawerData) return;
		formState.leadId = drawerData.id;
		await tick();
		convertForm.requestSubmit();
	}

	/**
	 * Handle create new lead
	 */
	async function handleCreateLead() {
		if (!createFormData.title?.trim()) {
			toast.error('线索标题是必填项');
			return;
		}

		isSaving = true;
		try {
			// Populate form state
			formState.salutation = createFormData.salutation || '';
			formState.title = createFormData.title || '';
			formState.firstName = createFormData.firstName || '';
			formState.lastName = createFormData.lastName || '';
			formState.email = createFormData.email || '';
			formState.phone = createFormData.phone || '';
			formState.jobTitle = createFormData.jobTitle || '';
			formState.company = createFormData.company || '';
			formState.website = createFormData.website || '';
			formState.linkedinUrl = createFormData.linkedinUrl || '';
			formState.status = createFormData.status || 'ASSIGNED';
			formState.source = createFormData.leadSource || '';
			formState.rating = createFormData.rating || '';
			formState.industry = createFormData.industry || '';
			formState.opportunityAmount = createFormData.opportunityAmount || '';
			formState.currency = createFormData.currency || $orgSettings.default_currency || 'USD';
			formState.probability = createFormData.probability || '';
			formState.closeDate = createFormData.closeDate || '';
			formState.lastContacted = createFormData.lastContacted || '';
			formState.nextFollowUp = createFormData.nextFollowUp || '';
			formState.addressLine = createFormData.addressLine || '';
			formState.city = createFormData.city || '';
			formState.state = createFormData.state || '';
			formState.postcode = createFormData.postcode || '';
			formState.country = createFormData.country || '';
			formState.description = createFormData.description || '';
			formState.assignedTo = createFormData.assignedTo || [];
			formState.teams = createFormData.teams || [];
			formState.contacts = createFormData.contacts || [];
			formState.tags = createFormData.tags || [];

			await tick();
			createForm.requestSubmit();
		} finally {
			isSaving = false;
		}
	}

	// URL-based filter state from server
	const filters = $derived(data.filters);
	const filterOptions = $derived(data.filterOptions);

	// Count active filters (excluding status since it's handled via chips in header)
	const active筛选Count = $derived.by(() => {
		let count = 0;
		if (filters.search) count++;
		if (filters.source) count++;
		if (filters.rating) count++;
		if (filters.assigned_to?.length > 0) count++;
		if (filters.tags?.length > 0) count++;
		if (filters.created_at_gte || filters.created_at_lte) count++;
		return count;
	});

	/**
	 * Update URL with new filters
	 * @param {Record<string, any>} new筛选
	 */
	async function update筛选(new筛选) {
		const url = new URL($page.url);
		// Clear existing filter params (preserve view/action)
		[
			'search',
			'status',
			'source',
			'rating',
			'assigned_to',
			'tags',
			'created_at_gte',
			'created_at_lte'
		].forEach((key) => url.searchParams.delete(key));
		// Set new params
		Object.entries(new筛选).forEach(([key, value]) => {
			if (Array.isArray(value)) {
				value.forEach((v) => url.searchParams.append(key, v));
			} else if (value && value !== 'ALL') {
				url.searchParams.set(key, value);
			}
		});
		await goto(url.toString(), { replaceState: true, noScroll: true, invalidateAll: true });
	}

	/**
	 * Clear all filters
	 */
	function clear筛选() {
		update筛选({});
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

	// Status counts for filter chips
	const openStatuses = ['ASSIGNED', 'IN_PROCESS'];
	const lostStatuses = ['CLOSED', 'RECYCLED'];
	const openCount = $derived(
		leads.filter((/** @type {any} */ l) => openStatuses.includes(l.status)).length
	);
	const lostCount = $derived(
		leads.filter((/** @type {any} */ l) => lostStatuses.includes(l.status)).length
	);

	// Status chip filter state (quick filter from UI)
	let statusChipFilter = $state('ALL');

	// Filter panel expansion state
	let filtersExpanded = $state(false);

	// Leads are already filtered server-side, just apply chip filter if active
	const filteredLeads = $derived.by(() => {
		let filtered = leads;
		if (statusChipFilter === 'open') {
			filtered = filtered.filter((/** @type {any} */ l) => openStatuses.includes(l.status));
		} else if (statusChipFilter === 'lost') {
			filtered = filtered.filter((/** @type {any} */ l) => lostStatuses.includes(l.status));
		}
		return filtered;
	});

	// Form references for server actions
	/** @type {HTMLFormElement} */
	let createForm;
	/** @type {HTMLFormElement} */
	let updateForm;
	/** @type {HTMLFormElement} */
	let deleteForm;
	/** @type {HTMLFormElement} */
	let convertForm;
	// Form data state
	let formState = $state({
		leadId: '',
		// Core Information
		salutation: '',
		firstName: '',
		lastName: '',
		email: '',
		phone: '',
		company: '',
		title: '',
		jobTitle: '',
		website: '',
		linkedinUrl: '',
		// Sales Pipeline
		status: '',
		source: '',
		industry: '',
		rating: '',
		opportunityAmount: '',
		currency: '',
		probability: '',
		closeDate: '',
		// Address
		addressLine: '',
		city: '',
		state: '',
		postcode: '',
		country: '',
		// 活动记录
		lastContacted: '',
		nextFollowUp: '',
		description: '',
		// Assignment
		ownerId: '',
		assignedTo: /** @type {string[]} */ ([]),
		teams: /** @type {string[]} */ ([]),
		contacts: /** @type {string[]} */ ([]),
		tags: /** @type {string[]} */ ([])
	});

	/**
	 * Get full name
	 * @param {any} lead
	 */
	function getFullName(lead) {
		return `${lead.firstName} ${lead.lastName}`.trim();
	}

	/**
	 * Get initials for lead
	 * @param {any} lead
	 */
	function getLeadInitials(lead) {
		return getNameInitials(lead.firstName, lead.lastName);
	}

	/**
	 * Handle form submit from drawer
	 * @param {any} formData
	 */
	async function handleFormSubmit(formData) {
		// Populate form state
		// Core Information
		formState.firstName = formData.first_name || '';
		formState.lastName = formData.last_name || '';
		formState.email = formData.email || '';
		formState.phone = formData.phone || '';
		formState.company = formData.company_name || '';
		formState.title = formData.title || '';
		formState.jobTitle = formData.job_title || '';
		formState.website = formData.website || '';
		formState.linkedinUrl = formData.linkedin_url || '';
		// Sales Pipeline
		formState.status = formData.status || '';
		formState.source = formData.source || '';
		formState.industry = formData.industry || '';
		formState.rating = formData.rating || '';
		formState.opportunityAmount = formData.opportunity_amount || '';
		formState.currency = formData.currency || $orgSettings.default_currency || 'USD';
		formState.probability = formData.probability || '';
		formState.closeDate = formData.close_date || '';
		// Address
		formState.addressLine = formData.address_line || '';
		formState.city = formData.city || '';
		formState.state = formData.state || '';
		formState.postcode = formData.postcode || '';
		formState.country = formData.country || '';
		// 活动记录
		formState.lastContacted = formData.last_contacted || '';
		formState.nextFollowUp = formData.next_follow_up || '';
		formState.description = formData.description || '';

		await tick();

		if (drawerMode === 'view' && drawerData) {
			// Edit mode
			formState.leadId = drawerData.id;
			// Use existing owner when editing (form doesn't have owner selection)
			formState.ownerId = drawerData.owner?.id || '';
			await tick();
			updateForm.requestSubmit();
		} else {
			// Create mode
			formState.ownerId = '';
			createForm.requestSubmit();
		}
	}

	/**
	 * Handle lead delete
	 */
	async function handleDelete() {
		if (!drawerData) return;
		if (!confirm(`确定要删除 ${getFullName(drawerData)}?`)) return;

		formState.leadId = drawerData.id;
		await tick();
		deleteForm.requestSubmit();
	}

	/**
	 * Handle lead convert
	 */
	async function handleConvert() {
		if (!drawerData) return;

		formState.leadId = drawerData.id;
		await tick();
		convertForm.requestSubmit();
	}

	/**
	 * Handle lead delete from row action
	 * @param {any} lead
	 */
	async function handleRowDelete(lead) {
		if (!confirm(`确定要删除 ${getFullName(lead)}?`)) return;

		formState.leadId = lead.id;
		await tick();
		deleteForm.requestSubmit();
	}

	/**
	 * Convert lead to form state for quick edit
	 * @param {any} lead
	 */
	function leadToFormState(lead) {
		return {
			leadId: lead.id,
			salutation: lead.salutation || '',
			firstName: lead.firstName || '',
			lastName: lead.lastName || '',
			email: lead.email || '',
			phone: lead.phone || '',
			company: typeof lead.company === 'object' ? lead.company?.name || '' : lead.company || '',
			title: lead.title || '',
			jobTitle: lead.jobTitle || '',
			website: lead.website || '',
			linkedinUrl: lead.linkedinUrl || '',
			status: lead.status || '',
			source: lead.leadSource || '',
			industry: lead.industry || '',
			rating: lead.rating || '',
			opportunityAmount: lead.opportunityAmount || '',
			probability: lead.probability || '',
			closeDate: lead.closeDate || '',
			addressLine: lead.addressLine || '',
			city: lead.city || '',
			state: lead.state || '',
			postcode: lead.postcode || '',
			country: lead.country || '',
			lastContacted: lead.lastContacted || '',
			nextFollowUp: lead.nextFollowUp || '',
			description: lead.description || '',
			ownerId: lead.owner?.id || '',
			assignedTo: lead.assignedTo || [],
			teams: lead.teams || [],
			contacts: lead.contacts || [],
			tags: lead.tags || []
		};
	}

	/**
	 * Handle quick edit from cell
	 * @param {any} lead
	 * @param {string} field
	 * @param {string} value
	 */
	async function handleQuickEdit(lead, field, value) {
		// Populate form state with current lead data
		const currentState = leadToFormState(lead);

		// Update the specific field
		currentState[field] = value;

		// Copy to form state
		Object.assign(formState, currentState);

		await tick();
		updateForm.requestSubmit();
	}

	/**
	 * Create enhance handler for form actions
	 * @param {string} successMessage
	 * @param {boolean} shouldCloseDrawer
	 */
	function createEnhanceHandler(successMessage, shouldCloseDrawer = true) {
		return () => {
			return async ({ result }) => {
				isSaving = false;
				if (result.type === 'success') {
					toast.success(successMessage);
					if (shouldCloseDrawer) {
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
	<title>线索 - BottleCRM</title>
</svelte:head>

<PageHeader title="线索" subtitle="{filteredLeads.length} / {leads.length} 条线索">
	{#snippet actions()}
		<div class="flex items-center gap-2">
			<!-- Status Filter Chips -->
			<div class="flex gap-1">
				<button
					type="button"
					onclick={() => (statusChipFilter = 'ALL')}
					class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium transition-colors {statusChipFilter ===
					'ALL'
						? 'bg-gray-900 text-white dark:bg-white dark:text-gray-900'
						: 'bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700'}"
				>
					全部
					<span
						class="rounded-full px-1.5 py-0.5 text-xs {statusChipFilter === 'ALL'
							? 'bg-gray-700 text-gray-200 dark:bg-gray-200 dark:text-gray-700'
							: 'bg-gray-200 text-gray-500 dark:bg-gray-700 dark:text-gray-500'}"
					>
						{leads.length}
					</span>
				</button>
				<button
					type="button"
					onclick={() => (statusChipFilter = 'open')}
					class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium transition-colors {statusChipFilter ===
					'open'
						? 'bg-blue-600 text-white dark:bg-blue-500'
						: 'bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700'}"
				>
					进行中
					<span
						class="rounded-full px-1.5 py-0.5 text-xs {statusChipFilter === 'open'
							? 'bg-blue-700 text-blue-100 dark:bg-blue-600'
							: 'bg-gray-200 text-gray-500 dark:bg-gray-700 dark:text-gray-500'}"
					>
						{openCount}
					</span>
				</button>
				<button
					type="button"
					onclick={() => (statusChipFilter = 'lost')}
					class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium transition-colors {statusChipFilter ===
					'lost'
						? 'bg-red-600 text-white dark:bg-red-500'
						: 'bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700'}"
				>
					已关闭
					<span
						class="rounded-full px-1.5 py-0.5 text-xs {statusChipFilter === 'lost'
							? 'bg-red-700 text-red-100 dark:bg-red-600'
							: 'bg-gray-200 text-gray-500 dark:bg-gray-700 dark:text-gray-500'}"
					>
						{lostCount}
					</span>
				</button>
			</div>

			<div class="bg-border mx-1 h-6 w-px"></div>

			<!-- Filter Toggle Button -->
			<Button
				variant={filtersExpanded ? 'secondary' : 'outline'}
				size="sm"
				class="gap-2"
				onclick={() => (filtersExpanded = !filtersExpanded)}
			>
				<Filter class="h-4 w-4" />
				筛选
				{#if active筛选Count > 0}
					<span
						class="rounded-full bg-blue-100 px-1.5 py-0.5 text-xs font-medium text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
					>
						{active筛选Count}
					</span>
				{/if}
			</Button>

			<!-- Column Visibility -->
			<DropdownMenu.Root>
				<DropdownMenu.Trigger asChild>
					{#snippet child({ props })}
						<Button {...props} variant="outline" size="sm" class="gap-2">
							<Eye class="h-4 w-4" />
							列
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
							disabled={column.canHide === false}
							onCheckedChange={() => toggleColumn(column.key)}
						>
							{column.label}
						</DropdownMenu.CheckboxItem>
					{/each}
				</DropdownMenu.Content>
			</DropdownMenu.Root>

			<Button onclick={openCreate}>
				<Plus class="mr-2 h-4 w-4" />
				新建线索
			</Button>
		</div>
	{/snippet}
</PageHeader>

<div class="flex-1">
	<!-- Collapsible Filter Bar -->
	<FilterBar
		minimal={true}
		expanded={filtersExpanded}
		activeCount={active筛选Count}
		onClear={clear筛选}
		class="pb-4"
	>
		<SearchInput
			value={filters.search}
			placeholder="搜索线索..."
			onchange={(value) => update筛选({ ...filters, search: value })}
			class="w-64"
		/>
		<SelectFilter
			label="来源"
			options={filterOptions.sources}
			value={filters.source || 'ALL'}
			onchange={(value) => update筛选({ ...filters, source: value })}
			class="w-40"
		/>
		<SelectFilter
			label="评分"
			options={filterOptions.ratings}
			value={filters.rating || 'ALL'}
			onchange={(value) => update筛选({ ...filters, rating: value })}
			class="w-32"
		/>
		<DateRangeFilter
			label="创建时间"
			startDate={filters.created_at_gte}
			endDate={filters.created_at_lte}
			onchange={(start, end) =>
				update筛选({ ...filters, created_at_gte: start, created_at_lte: end })}
			class="w-56"
		/>
	</FilterBar>

	<!-- Table -->
	{#if filteredLeads.length === 0}
		<div class="flex flex-col items-center justify-center py-16 text-center">
			<User class="mb-4 h-12 w-12 text-gray-300 dark:text-gray-600" />
			<h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">未找到线索</h3>
		</div>
	{:else}
		<!-- Desktop Table using CrmTable -->
		<div class="hidden md:block">
			<CrmTable
				data={filteredLeads}
				{columns}
				bind:visibleColumns
				onRowChange={handleRowChange}
				onRowClick={(row) => openLead(row)}
			>
				{#snippet emptyState()}
					<div class="flex flex-col items-center justify-center py-16 text-center">
						<User class="mb-4 h-12 w-12 text-gray-300 dark:text-gray-600" />
						<h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">未找到线索</h3>
					</div>
				{/snippet}
			</CrmTable>
		</div>

		<!-- Mobile Card View -->
		<div class="divide-y md:hidden dark:divide-gray-800">
			{#each filteredLeads as lead (lead.id)}
				<button
					type="button"
					class="flex w-full items-start gap-3 px-4 py-3 text-left transition-colors hover:bg-gray-50/30 dark:hover:bg-gray-800/30"
					onclick={() => openLead(lead)}
				>
					<div class="min-w-0 flex-1">
						<div class="flex items-start justify-between gap-2">
							<div>
								<p class="text-sm font-medium text-gray-900 dark:text-gray-100">
									{getFullName(lead)}
								</p>
								{#if lead.company}
									<p class="text-sm text-gray-500 dark:text-gray-400">
										{typeof lead.company === 'object' ? lead.company.name : lead.company}
									</p>
								{/if}
							</div>
							<span
								class="shrink-0 rounded-full px-2 py-0.5 text-xs font-medium {getOptionStyle(
									lead.status,
									leadStatusOptions
								)}"
							>
								{getOptionLabel(lead.status, leadStatusOptions)}
							</span>
						</div>
						<div
							class="mt-2 flex flex-wrap items-center gap-3 text-xs text-gray-500 dark:text-gray-400"
						>
							{#if lead.rating}
								<span
									class="rounded-full px-2 py-0.5 {getOptionStyle(lead.rating, leadRatingOptions)}"
								>
									{getOptionLabel(lead.rating, leadRatingOptions)}
								</span>
							{/if}
							<span>{formatRelativeDate(lead.createdAt)}</span>
						</div>
					</div>
				</button>
			{/each}

			<!-- Mobile new row button -->
			<button
				type="button"
				onclick={openCreate}
				class="flex w-full items-center gap-2 px-4 py-3 text-sm text-gray-500 transition-colors hover:bg-gray-50 hover:text-gray-700 dark:hover:bg-gray-800 dark:hover:text-gray-300"
			>
				<Plus class="h-4 w-4" />
				新建
			</button>
		</div>
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

<!-- Lead Drawer -->
<CrmDrawer
	bind:open={drawerOpen}
	onOpenChange={handleDrawerChange}
	data={currentDrawerData}
	columns={drawerColumnsWithOptions}
	titleKey="title"
	titlePlaceholder={drawerMode === 'create' ? '线索标题' : '未命名线索'}
	headerLabel={drawerMode === 'create' ? '新建线索' : '线索'}
	mode={drawerMode}
	loading={drawerLoading}
	onFieldChange={handleDrawerFieldChange}
	onDelete={drawerMode !== 'create' ? handleDrawerDelete : undefined}
	onClose={closeDrawer}
>
	{#snippet activitySection()}
		{#if drawerMode !== 'create' && drawerData?.comments?.length > 0}
			<div class="space-y-3">
				<div class="flex items-center gap-2 text-sm font-medium text-gray-500 dark:text-gray-400">
					<MessageSquare class="h-4 w-4" />
					活动记录
				</div>
				{#each drawerData.comments.slice(0, 3) as comment (comment.id)}
					<div class="flex gap-3">
						<div
							class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800"
						>
							<MessageSquare class="h-4 w-4 text-gray-400 dark:text-gray-500" />
						</div>
						<div class="min-w-0 flex-1">
							<p class="text-sm text-gray-900 dark:text-gray-100">
								<span class="font-medium">{comment.author?.name || '未知'}</span>
								{' '}添加了备注
							</p>
							<p class="mt-0.5 text-xs text-gray-500 dark:text-gray-400">
								{formatRelativeDate(comment.createdAt)}
							</p>
							<p class="mt-1 line-clamp-2 text-sm text-gray-600 dark:text-gray-400">
								{comment.body}
							</p>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	{/snippet}

	{#snippet footerActions()}
		{#if drawerMode === 'create'}
			<Button variant="outline" onclick={closeDrawer}>取消</Button>
			<Button onclick={handleCreateLead} disabled={isSaving}>
				{#if isSaving}
					<Loader2 class="mr-2 h-4 w-4 animate-spin" />
					创建中...
				{:else}
					创建线索
				{/if}
			</Button>
		{:else}
			<Button variant="outline" onclick={closeDrawer} disabled={isSaving}>取消</Button>
			{#if drawerData?.status !== 'converted'}
				<Button variant="outline" onclick={handleDrawerConvert} disabled={isSaving}>
					<ArrowRightCircle class="mr-2 h-4 w-4" />
					转化
				</Button>
			{/if}
			<Button onclick={handleDrawerUpdate} disabled={isSaving}>
				{#if isSaving}
					<Loader2 class="mr-2 h-4 w-4 animate-spin" />
					保存中...
				{:else}
					保存
				{/if}
			</Button>
		{/if}
	{/snippet}
</CrmDrawer>

<!-- Hidden forms for server actions -->
<form
	method="POST"
	action="?/create"
	bind:this={createForm}
	use:enhance={createEnhanceHandler('Lead created successfully')}
	class="hidden"
>
	<!-- Core Information -->
	<input type="hidden" name="salutation" value={formState.salutation} />
	<input type="hidden" name="firstName" value={formState.firstName} />
	<input type="hidden" name="lastName" value={formState.lastName} />
	<input type="hidden" name="email" value={formState.email} />
	<input type="hidden" name="phone" value={formState.phone} />
	<input type="hidden" name="company" value={formState.company} />
	<input type="hidden" name="title" value={formState.title} />
	<input type="hidden" name="jobTitle" value={formState.jobTitle} />
	<input type="hidden" name="website" value={formState.website} />
	<input type="hidden" name="linkedinUrl" value={formState.linkedinUrl} />
	<!-- Sales Pipeline -->
	<input type="hidden" name="status" value={formState.status} />
	<input type="hidden" name="source" value={formState.source} />
	<input type="hidden" name="industry" value={formState.industry} />
	<input type="hidden" name="rating" value={formState.rating} />
	<input type="hidden" name="opportunityAmount" value={formState.opportunityAmount} />
	<input type="hidden" name="currency" value={formState.currency} />
	<input type="hidden" name="probability" value={formState.probability} />
	<input type="hidden" name="closeDate" value={formState.closeDate} />
	<!-- Address -->
	<input type="hidden" name="addressLine" value={formState.addressLine} />
	<input type="hidden" name="city" value={formState.city} />
	<input type="hidden" name="state" value={formState.state} />
	<input type="hidden" name="postcode" value={formState.postcode} />
	<input type="hidden" name="country" value={formState.country} />
	<!-- 活动记录 -->
	<input type="hidden" name="lastContacted" value={formState.lastContacted} />
	<input type="hidden" name="nextFollowUp" value={formState.nextFollowUp} />
	<input type="hidden" name="description" value={formState.description} />
	<!-- Assignment -->
	<input type="hidden" name="ownerId" value={formState.ownerId} />
	<input type="hidden" name="assignedTo" value={JSON.stringify(formState.assignedTo)} />
	<input type="hidden" name="teams" value={JSON.stringify(formState.teams)} />
	<input type="hidden" name="contacts" value={JSON.stringify(formState.contacts)} />
	<input type="hidden" name="tags" value={JSON.stringify(formState.tags)} />
</form>

<form
	method="POST"
	action="?/update"
	bind:this={updateForm}
	use:enhance={createEnhanceHandler('Lead updated successfully')}
	class="hidden"
>
	<input type="hidden" name="leadId" value={formState.leadId} />
	<!-- Core Information -->
	<input type="hidden" name="salutation" value={formState.salutation} />
	<input type="hidden" name="firstName" value={formState.firstName} />
	<input type="hidden" name="lastName" value={formState.lastName} />
	<input type="hidden" name="email" value={formState.email} />
	<input type="hidden" name="phone" value={formState.phone} />
	<input type="hidden" name="company" value={formState.company} />
	<input type="hidden" name="title" value={formState.title} />
	<input type="hidden" name="jobTitle" value={formState.jobTitle} />
	<input type="hidden" name="website" value={formState.website} />
	<input type="hidden" name="linkedinUrl" value={formState.linkedinUrl} />
	<!-- Sales Pipeline -->
	<input type="hidden" name="status" value={formState.status} />
	<input type="hidden" name="source" value={formState.source} />
	<input type="hidden" name="industry" value={formState.industry} />
	<input type="hidden" name="rating" value={formState.rating} />
	<input type="hidden" name="opportunityAmount" value={formState.opportunityAmount} />
	<input type="hidden" name="currency" value={formState.currency} />
	<input type="hidden" name="probability" value={formState.probability} />
	<input type="hidden" name="closeDate" value={formState.closeDate} />
	<!-- Address -->
	<input type="hidden" name="addressLine" value={formState.addressLine} />
	<input type="hidden" name="city" value={formState.city} />
	<input type="hidden" name="state" value={formState.state} />
	<input type="hidden" name="postcode" value={formState.postcode} />
	<input type="hidden" name="country" value={formState.country} />
	<!-- 活动记录 -->
	<input type="hidden" name="lastContacted" value={formState.lastContacted} />
	<input type="hidden" name="nextFollowUp" value={formState.nextFollowUp} />
	<input type="hidden" name="description" value={formState.description} />
	<!-- Assignment -->
	<input type="hidden" name="ownerId" value={formState.ownerId} />
	<input type="hidden" name="assignedTo" value={JSON.stringify(formState.assignedTo)} />
	<input type="hidden" name="teams" value={JSON.stringify(formState.teams)} />
	<input type="hidden" name="contacts" value={JSON.stringify(formState.contacts)} />
	<input type="hidden" name="tags" value={JSON.stringify(formState.tags)} />
</form>

<form
	method="POST"
	action="?/delete"
	bind:this={deleteForm}
	use:enhance={createEnhanceHandler('Lead deleted successfully')}
	class="hidden"
>
	<input type="hidden" name="leadId" value={formState.leadId} />
</form>

<form
	method="POST"
	action="?/convert"
	bind:this={convertForm}
	use:enhance={createEnhanceHandler('Lead converted successfully')}
	class="hidden"
>
	<input type="hidden" name="leadId" value={formState.leadId} />
</form>
