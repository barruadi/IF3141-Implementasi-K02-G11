/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";

patch(ListController.prototype, {
    async createRecord() {
        if (this.props.resModel === "inventory.item") {
            this.env.services.action.doAction(
                {
                    type: "ir.actions.act_window",
                    res_model: "inventory.item",
                    view_mode: "form",
                    target: "new",
                    views: [[false, "form"]],
                },
                {
                    onClose: () => this.model.root.load(),
                }
            );
            return;
        }
        return super.createRecord(...arguments);
    },
});
