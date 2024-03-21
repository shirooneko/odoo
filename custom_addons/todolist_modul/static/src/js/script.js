odoo.define('todo.task.kanban_checkbox', function (require) {
    "use strict";

    var KanbanRecord = require('web.KanbanRecord');

    KanbanRecord.include({
        events: _.extend({}, KanbanRecord.prototype.events, {
            'change .form-check-input': '_onCheckboxChange',
        }),

        _onCheckboxChange: function (ev) {
            var checkbox = ev.target;
            var checked = checkbox.checked;
            var status = checked ? 'done' : 'in_progress';
            this._rpc({
                model: 'todo.task',
                method: 'write',
                args: [this.record.id, {status: status}],
            });
        },
    });
});