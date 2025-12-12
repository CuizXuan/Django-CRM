<script>
	import { DollarSign, TrendingUp, Target, Percent, AlertCircle } from '@lucide/svelte';
	import {
		KPICard,
		FocusBar,
		MiniPipeline,
		MiniPipelineWithCurrency,
		PipelineChart,
		PipelineChartWithCurrency,
		TaskList,
		HotLeadsPanel,
		OpportunitiesTable,
		ActivityFeed
	} from '$lib/components/dashboard';
	import { formatCurrency } from '$lib/utils/formatting.js';
	import { getCurrencySymbol } from '$lib/utils/currencySymbols.js';
	import { orgSettings } from '$lib/stores/org.js';
	import { onMount } from 'svelte';

	/** @type {{ data: any }} */
	let { data } = $props();

	const metrics = $derived(data.metrics || {});
	const recentData = $derived(data.recentData || {});
	const urgentCounts = $derived(data.urgentCounts || {});
	const pipelineByStage = $derived(data.pipelineByStage || {});
	const revenueMetrics = $derived(data.revenueMetrics || {});
	const hotLeads = $derived(data.hotLeads || []);

	// Initialize org settings from server data
	let serverOrgSettings = $state({
		default_currency: 'CNY',
		default_country: 'CN'
	});

	// Initialize settings on page load
	$effect(() => {
		if (data.orgSettings) {
			console.log('Dashboard: Org settings received:', data.orgSettings);
			serverOrgSettings = data.orgSettings;
			orgSettings.set(data.orgSettings);
		}
	});

	// Also run on mount to ensure store is initialized
	onMount(() => {
		if (data.orgSettings) {
			orgSettings.set(data.orgSettings);
			serverOrgSettings = data.orgSettings;
		}
	});

	// Get org's default currency for KPI display
	const orgCurrency = $derived(serverOrgSettings.default_currency || 'CNY');
	const orgCurrencySymbol = $derived(getCurrencySymbol(orgCurrency));
	const otherCurrencyCount = $derived(revenueMetrics.other_currency_count || 0);
	const currencyNote = $derived(
		otherCurrencyCount > 0
			? `${orgCurrency} 结算（另有 ${otherCurrencyCount} 个其他币种）`
			: `${orgCurrency} 结算`
	);

	// Format currency with symbol in the desired format (e.g., ¥2.32)
	function formatCurrencyWithSymbol(amount, currency = orgCurrency) {
		if (amount === null || amount === undefined) return '-';
		const formattedNumber = formatCurrency(amount, currency, false, false); // 不显示符号，不使用紧凑格式
		const symbol = getCurrencySymbol(currency);
		return `${symbol}${formattedNumber}`;
	}
</script>

<svelte:head>
	<title>仪表盘 - CRM系统</title>
</svelte:head>

<div class="space-y-6 p-6" style="animation: fadeIn 0.5s ease-in-out;">
	<!-- Header -->
	<div class="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center" style="animation: slideInDown 0.5s ease-out;">
		<div>
			<h1 class="text-foreground text-3xl font-bold bg-gradient-to-r from-primary to-primary/70 bg-clip-text text-transparent">
				仪表盘
			</h1>
			<p class="text-muted-foreground text-sm mt-2">
				欢迎回来，以下是当前业务概览。
			</p>
		</div>
	</div>

	{#if data.error}
		<div
			class="flex items-center gap-3 rounded-lg border border-red-200 bg-red-50 p-4 dark:border-red-800 dark:bg-red-900/20"
			style="animation: slideInUp 0.5s ease-out;"
		>
			<AlertCircle class="h-5 w-5 text-red-500 dark:text-red-400" />
			<span class="text-sm text-red-700 dark:text-red-300">{data.error}</span>
		</div>
	{:else}
		<!-- Focus Bar - Urgent Items -->
		<div style="animation: slideInUp 0.5s ease-out 0.1s both;">
			<FocusBar
				overdueCount={urgentCounts.overdue_tasks || 0}
				todayCount={urgentCounts.tasks_due_today || 0}
				followupsCount={urgentCounts.followups_today || 0}
				hotLeadsCount={urgentCounts.hot_leads || 0}
			/>
		</div>

		<!-- Pipeline Overview - Full Width -->
		<div class="rounded-xl border bg-card p-6 shadow-sm hover:shadow-md transition-all duration-300" style="animation: slideInUp 0.5s ease-out 0.2s both;">
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-foreground text-lg font-semibold flex items-center gap-2">
					<span class="w-1 h-6 bg-primary rounded-full"></span>
					销售管道
				</h2>
				<span class="text-muted-foreground text-sm">{currencyNote}</span>
			</div>
			<MiniPipelineWithCurrency pipelineData={pipelineByStage} currency={orgCurrency} />
		</div>

		<!-- Revenue Metrics + Pipeline Chart -->
		<div class="grid grid-cols-1 gap-6 lg:grid-cols-2" style="animation: fadeIn 0.5s ease-out 0.3s both;">
			<!-- Revenue Metrics - 2x2 Grid -->
			<div class="grid grid-cols-2 gap-4">
				<KPICard
					label="管道金额"
					value={formatCurrencyWithSymbol(revenueMetrics.pipeline_value || 0, orgCurrency)}
					subtitle={currencyNote}
					borderColor="border-t-blue-500"
					class="hover:shadow-lg transition-all duration-300"
					style="animation: slideInUp 0.5s ease-out 0.4s both;"
				>
					{#snippet icon()}
						<DollarSign class="h-5 w-5" />
					{/snippet}
				</KPICard>
				<KPICard
					label="加权管道"
					value={formatCurrencyWithSymbol(revenueMetrics.weighted_pipeline || 0, orgCurrency)}
					subtitle={currencyNote}
					borderColor="border-t-purple-500"
					iconBgClass="bg-purple-100 dark:bg-purple-900/30"
					iconClass="text-purple-600 dark:text-purple-400"
					class="hover:shadow-lg transition-all duration-300"
					style="animation: slideInUp 0.5s ease-out 0.5s both;"
				>
					{#snippet icon()}
						<TrendingUp class="h-5 w-5" />
					{/snippet}
				</KPICard>
				<KPICard
					label="本月赢单"
					value={formatCurrencyWithSymbol(revenueMetrics.won_this_month || 0, orgCurrency)}
					subtitle={currencyNote}
					borderColor="border-t-green-500"
					iconBgClass="bg-green-100 dark:bg-green-900/30"
					iconClass="text-green-600 dark:text-green-400"
					class="hover:shadow-lg transition-all duration-300"
					style="animation: slideInUp 0.5s ease-out 0.6s both;"
				>
					{#snippet icon()}
						<Target class="h-5 w-5" />
					{/snippet}
				</KPICard>
				<KPICard
					label="转化率"
					value="{revenueMetrics.conversion_rate || 0}%"
					borderColor="border-t-orange-500"
					iconBgClass="bg-orange-100 dark:bg-orange-900/30"
					iconClass="text-orange-600 dark:text-orange-400"
					class="hover:shadow-lg transition-all duration-300"
					style="animation: slideInUp 0.5s ease-out 0.7s both;"
				>
					{#snippet icon()}
						<Percent class="h-5 w-5" />
					{/snippet}
				</KPICard>
			</div>

			<!-- Pipeline Chart -->
			<div class="animate-scale-in" style="animation: scaleIn 0.5s ease-out 0.8s both;">
				<PipelineChartWithCurrency pipelineData={pipelineByStage} currency={orgCurrency} />
			</div>
		</div>

		<!-- Tasks + Hot Leads -->
		<div class="grid grid-cols-1 gap-6 lg:grid-cols-2" style="animation: fadeIn 0.5s ease-out 0.9s both;">
			<div style="animation: slideInLeft 0.5s ease-out 1s both;">
				<TaskList tasks={recentData.tasks || []} />
			</div>
			<div style="animation: slideInRight 0.5s ease-out 1.1s both;">
				<HotLeadsPanel leads={hotLeads} />
			</div>
		</div>

		<!-- Opportunities + Activity Feed -->
		<div class="grid grid-cols-1 gap-6 lg:grid-cols-2" style="animation: fadeIn 0.5s ease-out 1.2s both;">
			<div style="animation: slideInLeft 0.5s ease-out 1.3s both;">
				<OpportunitiesTable opportunities={recentData.opportunities || []} />
			</div>
			<div style="animation: slideInRight 0.5s ease-out 1.4s both;">
				<ActivityFeed activities={recentData.activities || []} />
			</div>
		</div>
	{/if}
</div>

<style>
	:global {
		/* 页面进入动画 */
		@keyframes fadeIn {
			from {
				opacity: 0;
			}
			to {
				opacity: 1;
			}
		}

		@keyframes slideInDown {
			from {
				opacity: 0;
				transform: translateY(-20px);
			}
			to {
				opacity: 1;
				transform: translateY(0);
			}
		}

		@keyframes slideInUp {
			from {
				opacity: 0;
				transform: translateY(20px);
			}
			to {
				opacity: 1;
				transform: translateY(0);
			}
		}

		@keyframes slideInLeft {
			from {
				opacity: 0;
				transform: translateX(-20px);
			}
			to {
				opacity: 1;
				transform: translateX(0);
			}
		}

		@keyframes slideInRight {
			from {
				opacity: 0;
				transform: translateX(20px);
			}
			to {
				opacity: 1;
				transform: translateX(0);
			}
		}

		@keyframes scaleIn {
			from {
				opacity: 0;
				transform: scale(0.95);
			}
			to {
				opacity: 1;
				transform: scale(1);
			}
		}
	}
</style>