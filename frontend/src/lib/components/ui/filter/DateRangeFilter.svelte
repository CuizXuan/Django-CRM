<script>
	import { CalendarDays, ChevronDown, X } from '@lucide/svelte';
	import { cn } from '$lib/utils.js';
	import * as Popover from '$lib/components/ui/popover/index.js';
	import Calendar from '$lib/components/ui/calendar/Calendar.svelte';
	import { Button } from '$lib/components/ui/button/index.js';
	import { today, getLocalTimeZone, parseDate } from '@internationalized/date';

	/**
	 * @type {{
	 *   startDate?: string,
	 *   endDate?: string,
	 *   label?: string,
	 *   placeholder?: string,
	 *   class?: string,
	 *   onchange?: (startDate: string, endDate: string) => void,
	 * }}
	 */
	let {
		startDate = $bindable(''),
		endDate = $bindable(''),
		label = '',
		placeholder = '选择日期范围',
		class: className,
		onchange
	} = $props();

	let open = $state(false);
	let selectingEnd = $state(false);

	const todayDate = today(getLocalTimeZone());

	// Convert string dates to DateValue for calendar
	const startDateValue = $derived(startDate ? parseDate(startDate) : undefined);
	const endDateValue = $derived(endDate ? parseDate(endDate) : undefined);

	/** @type {{ label: string, getRange: () => { start: string, end: string } }[]} */
	const presets = [
		{
			label: '今天',
			getRange: () => {
				const d = toDateString(todayDate);
				return { start: d, end: d };
			}
		},
		{
			label: '最近7天',
			getRange: () => ({
				start: toDateString(todayDate.subtract({ days: 7 })),
				end: toDateString(todayDate)
			})
		},
		{
			label: '最近30天',
			getRange: () => ({
				start: toDateString(todayDate.subtract({ days: 30 })),
				end: toDateString(todayDate)
			})
		},
		{
			label: '本月',
			getRange: () => ({
				start: toDateString(todayDate.set({ day: 1 })),
				end: toDateString(todayDate)
			})
		},
		{
			label: '上月',
			getRange: () => {
				const lastMonth = todayDate.subtract({ months: 1 });
				const lastDayOfLastMonth = lastMonth.set({ day: 1 }).add({ months: 1 }).subtract({ days: 1 });
				return {
					start: toDateString(lastMonth.set({ day: 1 })),
					end: toDateString(lastDayOfLastMonth)
				};
			}
		}
	];

	const displayText = $derived.by(() => {
		if (!startDate && !endDate) return placeholder;
		if (startDate && endDate) {
			if (startDate === endDate) return formatDate(startDate);
			return `${formatDate(startDate)} ~ ${formatDate(endDate)}`;
		}
		if (startDate) return `${formatDate(startDate)} ~ `;
		return `~ ${formatDate(endDate)}`;
	});

	/**
	 * 将日期值转换为 YYYY-MM-DD 格式字符串
	 * @param {import('@internationalized/date').DateValue | string} dateValue
	 */
	function toDateString(dateValue) {
		if (!dateValue) return '';
		if (typeof dateValue === 'string') {
			return dateValue;
		}
		return dateValue.toString();
	}

	/**
	 * @param {string} dateStr
	 */
	function formatDate(dateStr) {
		if (!dateStr) return '';
		// 日期格式已经是 YYYY-MM-DD，直接返回
		return dateStr;
	}

	/**
	 * @param {{ label: string, getRange: () => { start: string, end: string } }} preset
	 */
	function handlePreset(preset) {
		const { start, end } = preset.getRange();
		startDate = start;
		endDate = end;
		onchange?.(start, end);
		open = false;
	}

	/**
	 * @param {import('@internationalized/date').DateValue | undefined} dateValue
	 */
	function handleDateSelect(dateValue) {
		if (!dateValue) return;
		const dateStr = toDateString(dateValue);

		if (!selectingEnd) {
			startDate = dateStr;
			endDate = '';
			selectingEnd = true;
		} else {
			// Ensure end is after start
			if (dateStr < startDate) {
				endDate = startDate;
				startDate = dateStr;
			} else {
				endDate = dateStr;
			}
			selectingEnd = false;
			onchange?.(startDate, endDate);
			open = false;
		}
	}

	function handleClear() {
		startDate = '';
		endDate = '';
		selectingEnd = false;
		onchange?.('', '');
	}

	const hasValue = $derived(!!startDate || !!endDate);
</script>

<div class={cn('filter-item', className)}>
	{#if label}
		<span class="filter-label">{label}</span>
	{/if}
	<div class="filter-input-wrapper">
		<Popover.Root bind:open onOpenChange={(o) => { if (!o) selectingEnd = false; }}>
		<Popover.Trigger asChild class="">
			{#snippet child({ props })}
				<button
					type="button"
					class={cn(
						'relative flex h-9 w-full items-center rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm transition-colors hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 overflow-hidden',
						hasValue && 'border-blue-500'
					)}
					style="height: 36px; border: 1px solid #d9d9d9 !important; background: #ffffff !important;"
					{...props}
				>
					<div class="flex items-center gap-2 flex-1 min-w-0 overflow-hidden pr-8">
						<CalendarDays class="h-4 w-4 text-muted-foreground flex-shrink-0" />
						<span class={cn('truncate', !hasValue && 'text-muted-foreground')} style="min-width: 0;">
							{displayText}
						</span>
					</div>
					{#if hasValue}
						<!-- svelte-ignore node_invalid_placement_ssr -->
						<span
							role="button"
							tabindex="0"
							onclick={(e) => {
								e.stopPropagation();
								e.preventDefault();
								handleClear();
							}}
							onkeydown={(e) => {
								if (e.key === 'Enter' || e.key === ' ') {
									e.stopPropagation();
									e.preventDefault();
									handleClear();
								}
							}}
							class="absolute right-8 top-1/2 -translate-y-1/2 rounded-sm p-0.5 hover:bg-muted cursor-pointer flex-shrink-0 z-10"
						>
							<X class="h-3 w-3" />
						</span>
					{/if}
					<ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 opacity-50 flex-shrink-0 z-10" />
				</button>
			{/snippet}
		</Popover.Trigger>
		<Popover.Content align="start" class="w-auto p-0">
			<div class="flex">
				<!-- Presets sidebar -->
				<div class="flex flex-col gap-1 border-r p-2">
					{#each presets as preset}
						<Button
							variant="ghost"
							size="sm"
							class="justify-start"
							onclick={() => handlePreset(preset)}
						>
							{preset.label}
						</Button>
					{/each}
				</div>
				<!-- Calendar -->
				<div class="p-2">
					<div class="mb-2 text-center text-sm text-muted-foreground">
						{#if selectingEnd}
							选择结束日期
						{:else}
							选择开始日期
						{/if}
					</div>
					<Calendar
						value={selectingEnd ? endDateValue : startDateValue}
						onValueChange={handleDateSelect}
					/>
					{#if startDate && !endDate}
						<div class="mt-2 text-center text-xs text-muted-foreground">
							开始：{formatDate(startDate)}
						</div>
					{/if}
				</div>
			</div>
		</Popover.Content>
	</Popover.Root>
	</div>
</div>
