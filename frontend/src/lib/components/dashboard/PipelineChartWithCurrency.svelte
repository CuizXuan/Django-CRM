<script>
	import * as Card from '$lib/components/ui/card/index.js';
	import { formatCurrency } from '$lib/utils/formatting.js';
	import { getCurrencySymbol } from '$lib/utils/currencySymbols.js';

	/**
	 * @typedef {Object} StageData
	 * @property {number} count - Number of opportunities in this stage
	 * @property {number} value - Total value of opportunities in this stage
	 * @property {string} label - Display label for the stage
	 */

	/**
	 * @typedef {Object} Props
	 * @property {Record<string, StageData>} [pipelineData] - Pipeline data by stage
	 * @property {string} [currency] - Currency code for formatting (default: CNY)
	 */

	/** @type {Props} */
	let { pipelineData = {}, currency = 'CNY' } = $props();

	// Only show open stages in the chart (not closed)
	const stages = [
		{ id: 'PROSPECTING', color: 'bg-gray-400 dark:bg-gray-500' },
		{ id: 'QUALIFICATION', color: 'bg-blue-500' },
		{ id: 'PROPOSAL', color: 'bg-purple-500' },
		{ id: 'NEGOTIATION', color: 'bg-orange-500' }
	];

	const stageNameMap = {
		PROSPECTING: '初步接触',
		QUALIFICATION: '需求确认',
		PROPOSAL: '方案报价',
		NEGOTIATION: '谈判'
	};

	const maxValue = $derived(Math.max(...stages.map((s) => pipelineData[s.id]?.value || 0), 1));

	// Get currency symbol
	const currencySymbol = getCurrencySymbol(currency);

	// Format currency with symbol in the desired format (e.g., ¥2.32)
	function formatCurrencyWithSymbol(amount) {
		if (amount === null || amount === undefined) return '-';
		const formattedNumber = formatCurrency(amount, currency, false, false); // 不显示符号，不使用紧凑格式
		return `${currencySymbol}${formattedNumber}`;
	}
</script>

<Card.Root class="p-5">
	<Card.Header class="p-0 pb-4">
		<Card.Title class="text-foreground text-sm font-medium">按阶段的管道</Card.Title>
	</Card.Header>
	<Card.Content class="p-0">
		<div class="space-y-3">
			{#each stages as stage}
				{@const data = pipelineData[stage.id] || { count: 0, value: 0, label: stage.id }}
				{@const percentage = maxValue > 0 ? (data.value / maxValue) * 100 : 0}
				<div class="space-y-1.5">
					<div class="flex items-center justify-between text-xs">
						<span class="text-muted-foreground">{stageNameMap[stage.id] || data.label || stage.id}</span>
						<span class="text-foreground font-medium tabular-nums">{formatCurrencyWithSymbol(data.value)}</span>
					</div>
					<div class="bg-muted h-2 w-full overflow-hidden rounded-full">
						<div
							class="h-full rounded-full transition-all duration-500 ease-out {stage.color}"
							style="width: {percentage}%"
						></div>
					</div>
				</div>
			{/each}
		</div>
		<!-- Summary row -->
		<div class="border-border/50 mt-4 flex justify-between border-t pt-3 text-xs">
			<span class="text-muted-foreground">开放管道总额</span>
			<span class="text-foreground font-semibold tabular-nums">
				{formatCurrencyWithSymbol(
					stages.reduce((sum, s) => sum + (pipelineData[s.id]?.value || 0), 0)
				)}
			</span>
		</div>
	</Card.Content>
</Card.Root>