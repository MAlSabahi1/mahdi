/**
 * فلترة ديناميكية للهيكل التنظيمي في Django Admin
 * ─────────────────────────────────────────────────
 * عند تغيير "إدارة أمن المحافظة" →
 *   تُحدّث الإدارات المركزية / الفروع / شرطة المديريات تلقائياً
 */
(function () {
    'use strict';

    var API_BASE = '/api/v1/dictionaries/';
    var DEPENDENT_FIELDS = {
        'central_department': 'central-departments',
        'branch': 'branches',
        'district_police': 'district-police'
    };

    function getCookie(name) {
        var value = '; ' + document.cookie;
        var parts = value.split('; ' + name + '=');
        if (parts.length === 2) return parts.pop().split(';').shift();
        return '';
    }

    function fetchFiltered(endpoint, saId, callback) {
        var url = API_BASE + endpoint + '/?security_admin=' + saId + '&page_size=200';
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var data = JSON.parse(xhr.responseText);
                callback(data.results || data.data || []);
            }
        };
        xhr.send();
    }

    function rebuildSelect(selectEl, items, currentValue) {
        // حفظ أول خيار (------)
        var emptyOption = selectEl.options[0];

        // إفراغ
        selectEl.innerHTML = '';
        if (emptyOption) {
            selectEl.appendChild(emptyOption);
        } else {
            var opt = document.createElement('option');
            opt.value = '';
            opt.textContent = '---------';
            selectEl.appendChild(opt);
        }

        // إضافة خيارات جديدة
        for (var i = 0; i < items.length; i++) {
            var option = document.createElement('option');
            option.value = items[i].id;
            option.textContent = items[i].name;
            if (String(items[i].id) === String(currentValue)) {
                option.selected = true;
            }
            selectEl.appendChild(option);
        }

        console.log('[org_filter] ' + selectEl.name + ': ' + items.length + ' items loaded');
    }

    function filterDependents(saId) {
        console.log('[org_filter] security_admin changed to: ' + saId);

        var fieldNames = Object.keys(DEPENDENT_FIELDS);
        for (var i = 0; i < fieldNames.length; i++) {
            var fieldName = fieldNames[i];
            var endpoint = DEPENDENT_FIELDS[fieldName];
            var depSelect = document.getElementById('id_' + fieldName);

            if (!depSelect) {
                console.log('[org_filter] field not found: id_' + fieldName);
                continue;
            }

            if (!saId) {
                rebuildSelect(depSelect, [], '');
                continue;
            }

            // IIFE to capture fieldName and depSelect in closure
            (function (sel, val) {
                fetchFiltered(endpoint, saId, function (items) {
                    rebuildSelect(sel, items, val);
                });
            })(depSelect, depSelect.value);
        }
    }

    function init() {
        var saSelect = document.getElementById('id_security_admin');
        if (!saSelect) {
            console.log('[org_filter] id_security_admin not found!');
            return;
        }

        console.log('[org_filter] initialized. security_admin type: ' + saSelect.tagName);

        // ربط الحدث الرئيسي لإدارة الأمن
        saSelect.addEventListener('change', function () {
            filterDependents(this.value);
        });

        // ربط أحداث التفرد (Mutual Exclusivity) للإدارات الفرعية
        var level2Fields = ['id_central_department', 'id_branch', 'id_district_police'];
        level2Fields.forEach(function (fieldId) {
            var el = document.getElementById(fieldId);
            if (el) {
                el.addEventListener('change', function () {
                    if (this.value) { // إذا تم اختيار قيمة
                        level2Fields.forEach(function (otherId) {
                            if (otherId !== fieldId) {
                                var otherEl = document.getElementById(otherId);
                                if (otherEl && otherEl.value) {
                                    otherEl.value = ''; // تصفير الحقل الآخر
                                    console.log('[org_filter] cleared ' + otherId + ' because ' + fieldId + ' was selected.');
                                }
                            }
                        });
                    }
                });
            }
        });

        // عند فتح نموذج تعديل — فلترة أولية
        if (saSelect.value) {
            console.log('[org_filter] initial load with value: ' + saSelect.value);
            filterDependents(saSelect.value);
        }
    }

    // انتظار تحميل DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        setTimeout(init, 200);
    }
})();
