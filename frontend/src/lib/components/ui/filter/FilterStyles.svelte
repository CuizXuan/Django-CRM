<script>
	// This component provides additional styles for filter components
</script>

<style>
	/* 全局样式 - 确保下拉箭头正确对齐 */
	:global(.filter-select-wrapper) {
		position: relative;
	}

	:global(.filter-select) {
		appearance: none;
		-webkit-appearance: none;
		-moz-appearance: none;
		padding-right: 2.5rem !important;
		background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
		background-position: right 0.5rem center;
		background-repeat: no-repeat;
		background-size: 1.5em 1.5em;
	}

	:global(.filter-select-wrapper::after) {
		content: '';
		position: absolute;
		right: 0.75rem;
		top: 50%;
		transform: translateY(-50%);
		pointer-events: none;
	}

	/* 搜索框样式优化 */
	:global(.search-input) {
		font-size: 0.875rem;
		line-height: 1.25rem;
	}

	:global(.search-input::placeholder) {
		color: rgb(156 163 175);
	}

	/* 暗色模式下的样式 */
	:global(.dark .filter-select) {
		background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%239ca3af' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
	}

	:global(.dark .search-input::placeholder) {
		color: rgb(156 163 175);
	}

	/* 确保图标对齐 */
	:global(.filter-icon) {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	/* 下拉菜单样式 */
	:global(.filter-dropdown-content) {
		max-height: 240px;
		overflow-y: auto;
		scrollbar-width: thin;
		scrollbar-color: rgb(203 213 225) transparent;
	}

	:global(.filter-dropdown-content::-webkit-scrollbar) {
		width: 6px;
	}

	:global(.filter-dropdown-content::-webkit-scrollbar-track) {
		background: transparent;
	}

	:global(.filter-dropdown-content::-webkit-scrollbar-thumb) {
		background-color: rgb(203 213 225);
		border-radius: 3px;
	}

	:global(.filter-dropdown-content::-webkit-scrollbar-thumb:hover) {
		background-color: rgb(156 163 175);
	}

	/* 按钮hover效果 */
	:global(.filter-button) {
		transition: all 0.2s ease-in-out;
	}

	:global(.filter-button:hover) {
		transform: translateY(-1px);
		box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -1px rgb(0 0 0 / 0.06);
	}

	/* 标签样式 */
	:global(.filter-label) {
		font-size: 0.75rem;
		font-weight: 500;
		color: rgb(107 114 128);
		margin-bottom: 0.25rem;
		display: block;
	}

	:global(.dark .filter-label) {
		color: rgb(156 163 175);
	}

	/* 输入框组样式 */
	:global(.filter-input-group) {
		position: relative;
		display: flex;
		align-items: center;
	}

	:global(.filter-input-group .search-icon) {
		position: absolute;
		left: 0.75rem;
		z-index: 10;
		pointer-events: none;
	}

	:global(.filter-input-group .clear-icon) {
		position: absolute;
		right: 0.75rem;
		z-index: 10;
		opacity: 0;
		transition: opacity 0.2s;
	}

	:global(.filter-input-group.has-value .clear-icon) {
		opacity: 1;
	}

	:global(.filter-input) {
		padding-left: 2.5rem !important;
		padding-right: 2.5rem !important;
	}

	/* 调整字体大小和行高 */
	:global(.filter-text) {
		font-size: 0.875rem;
		line-height: 1.25rem;
		font-weight: 400;
	}

	/* 日期选择器样式 */
	:global(.filter-date-input) {
		font-size: 0.875rem;
		line-height: 1.25rem;
	}

	/* 批量操作按钮组 */
	:global(.filter-action-group) {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	/* 激活状态样式 */
	:global(.filter-active) {
		border-color: rgb(59 130 246) !important;
		box-shadow: 0 0 0 1px rgb(59 130 246) !important;
	}

	:global(.dark .filter-active) {
		border-color: rgb(96 165 250) !important;
		box-shadow: 0 0 0 1px rgb(96 165 250) !important;
	}
</style>