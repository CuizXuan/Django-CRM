/**
 * Comment Admin - 级联选择功能
 * 当选择content_type时，自动刷新页面以加载相应的对象列表
 */

(function($) {
    'use strict';

    $(document).ready(function() {
        // 监听content_type字段的变更
        $('#id_content_type').on('change', function() {
            var contentTypeValue = $(this).val();

            if (contentTypeValue) {
                // 检查是否需要刷新
                var urlParams = new URLSearchParams(window.location.search);
                var currentContentType = urlParams.get('content_type');

                // 如果URL中的content_type已经匹配，不需要刷新
                if (currentContentType === contentTypeValue) {
                    return;
                }

                // 构建新URL
                var currentUrl = window.location.pathname;
                var newParams = new URLSearchParams();
                newParams.set('content_type', contentTypeValue);

                // 保留其他有用的参数
                if (urlParams.has('org')) {
                    newParams.set('org', urlParams.get('org'));
                }

                // 延迟执行，避免快速连续点击
                setTimeout(function() {
                    window.location.href = currentUrl + '?' + newParams.toString();
                }, 100);
            } else {
                // 如果没有选择content_type，跳转到基础页面
                window.location.href = window.location.pathname;
            }
        });

        // 添加提示文本
        var objectIdSelect = $('#id_object_id');
        if (objectIdSelect.length > 0) {
            if (objectIdSelect.find('option').length <= 1) {
                objectIdSelect.attr('title', '请先选择内容类型');
            }
        }

        // 防止表单提交时意外刷新
        $('form').on('submit', function() {
            // 移除change事件监听，避免提交时触发刷新
            $('#id_content_type').off('change');
        });
    });

})(django.jQuery || jQuery);