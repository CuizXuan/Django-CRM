<script>
	import * as Card from '$lib/components/ui/card/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Progress } from '$lib/components/ui/progress/index.js';
	import { Target, ChevronRight, Calendar } from '@lucide/svelte';
	import { formatCurrency } from '$lib/utils/formatting.js';

	/**
	 * @typedef {Object} Opportunity
	 * @property {string} id
	 * @property {string} name
	 * @property {number | null} amount
	 * @property {string} [currency] - Currency code (e.g., 'USD', 'INR')
	 * @property {string} stage
	 * @property {number | null} probability
	 * @property {string} [createdAt]
	 * @property {{ name: string } | null} [account]
	 * @property {string} [closed_on]
	 */

	/**
	 * @typedef {Object} Props
	 * @property {Opportunity[]} [opportunities] - Opportunities list
	 */

	/** @type {Props} */
	let { opportunities = [] } = $props();

	const stageConfig = /** @type {Record<string, { label: string, color: string }>} */ ({
		PROSPECTING: { label: '初步接触', color: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300' },
		QUALIFICATION: { label: '需求确认', color: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' },
		PROPOSAL: { label: '方案报价', color: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400' },
		NEGOTIATION: { label: '谈判', color: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400' },
		CLOSED_WON: { label: '赢单', color: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' },
		CLOSED_LOST: { label: '丢单', color: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400' }
	});

	/**
	 * Calculate days until close
	 * @param {string | undefined} closeDateStr
	 */
	function getDaysUntilClose(closeDateStr) {
		if (!closeDateStr) return null;
		const closeDate = new Date(closeDateStr);
		const today = new Date();
		today.setHours(0, 0, 0, 0);
		const diffTime = closeDate.getTime() - today.getTime();
		const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
		return diffDays;
	}

	/**
	 * Format days until close
	 * @param {number | null} days
	 */
	function formatDaysUntilClose(days) {
		if (days === null) return '';
		if (days < 0) return `逾期 ${Math.abs(days)} 天`;
		if (days === 0) return '今天';
		if (days === 1) return '明天';
		return `${days} 天`;
	}

	// Only show open opportunities
	const openOpportunities = $derived(
		opportunities.filter((o) => !['CLOSED_WON', 'CLOSED_LOST'].includes(o.stage))
	);
</script>

<Card.Root class="flex h-full flex-col">
	<Card.Header class="flex-row items-center justify-between space-y-0 pb-3">
		<div class="flex items-center gap-2">
			<Target class="h-4 w-4 text-green-500" />
			<Card.Title class="text-foreground text-sm font-medium">我的商机</Card.Title>
		</div>
		<Button variant="ghost" size="sm" href="/opportunities" class="text-xs">
			查看全部
			<ChevronRight class="ml-1 h-3 w-3" />
		</Button>
	</Card.Header>
	<Card.Content class="flex-1 overflow-auto p-0">
		{#if openOpportunities.length === 0}
			<div class="text-muted-foreground flex h-full flex-col items-center justify-center py-8 text-center">
				<Target class="text-muted-foreground/30 mb-2 h-10 w-10" />
				<p class="text-sm">暂无进行中的商机</p>
			</div>
		{:else}
			<div class="divide-border/50 divide-y">
				{#each openOpportunities.slice(0, 5) as opp (opp.id)}
					{@const daysUntilClose = getDaysUntilClose(opp.closed_on)}
					<a
						href="/opportunities/{opp.id}"
						class="hover:bg-muted/50 group block px-4 py-3 transition-colors"
					>
						<div class="mb-2 flex items-start justify-between gap-2">
							<div class="min-w-0 flex-1">
								<p class="text-foreground truncate text-sm font-medium">
									{opp.name}
								</p>
								<p class="text-muted-foreground truncate text-xs">
									{opp.account?.name || '未关联客户'}
								</p>
							</div>
							<span class="text-foreground flex-shrink-0 text-sm font-semibold tabular-nums">
								{formatCurrency(opp.amount, opp.currency || 'USD')}
							</span>
						</div>
						<div class="flex items-center gap-3">
							<Badge class="{stageConfig[opp.stage]?.color} text-[10px]">
								{stageConfig[opp.stage]?.label || opp.stage}
							</Badge>
							<div class="flex flex-1 items-center gap-2">
								<Progress value={opp.probability || 0} class="h-1.5 flex-1" />
								<span class="text-muted-foreground w-8 text-right text-xs tabular-nums">
									{opp.probability || 0}%
								</span>
							</div>
							{#if daysUntilClose !== null}
								<div class="flex items-center gap-1">
									<Calendar class="text-muted-foreground h-3 w-3" />
									<span
										class="text-xs tabular-nums {daysUntilClose < 0
											? 'font-medium text-red-500'
											: daysUntilClose <= 7
												? 'text-orange-500'
												: 'text-muted-foreground'}"
									>
										{formatDaysUntilClose(daysUntilClose)}
									</span>
								</div>
							{/if}
						</div>
					</a>
				{/each}
			</div>
		{/if}
	</Card.Content>
</Card.Root>
