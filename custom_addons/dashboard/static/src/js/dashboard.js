/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class EcoethnoDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.loadSequence = 0;
        this.state = useState({
            loading: true,
            error: false,
            period: "year",
            dateStart: "",
            dateEnd: "",
            data: this.emptyData(),
        });

        onWillStart(() => this.loadData());
    }

    emptyData() {
        return {
            cards: [],
            reservation_trend: [],
            visit_distribution: [],
            recent_reservations: [],
            inventory_rows: [],
        };
    }

    async loadData() {
        const sequence = ++this.loadSequence;
        this.state.loading = true;
        this.state.error = false;
        try {
            const data = await this.orm.call(
                "dashboard.ecoethno",
                "get_dashboard_data",
                [this.state.period, this.state.dateStart || false, this.state.dateEnd || false]
            );
            if (sequence !== this.loadSequence) {
                return;
            }
            this.state.data = data;
        } catch (error) {
            if (sequence !== this.loadSequence) {
                return;
            }
            this.state.error = this.getErrorMessage(error);
            this.state.data = this.emptyData();
        } finally {
            if (sequence === this.loadSequence) {
                this.state.loading = false;
            }
        }
    }

    async onPeriodClick(ev) {
        this.state.period = ev.currentTarget.dataset.period;
        if (this.state.period !== "custom") {
            this.state.dateStart = "";
            this.state.dateEnd = "";
        }
        await this.loadData();
    }

    async onDateStartChange(ev) {
        this.state.dateStart = ev.target.value;
        this.state.period = "custom";
        this.state.error = false;
    }

    async onDateEndChange(ev) {
        this.state.dateEnd = ev.target.value;
        this.state.period = "custom";
        this.state.error = false;
    }

    async applyCustomDate() {
        this.state.period = "custom";
        if (!this.state.dateStart || !this.state.dateEnd) {
            this.state.error = "Tanggal mulai dan tanggal akhir wajib diisi.";
            return;
        }
        if (this.state.dateStart > this.state.dateEnd) {
            this.state.error = "Tanggal mulai tidak boleh lebih besar dari tanggal akhir.";
            return;
        }
        await this.loadData();
    }

    async resetFilters() {
        this.state.period = "year";
        this.state.dateStart = "";
        this.state.dateEnd = "";
        await this.loadData();
    }

    getErrorMessage(error) {
        return error?.data?.message || error?.message || "Dashboard gagal dimuat.";
    }

    openRecordFromDataset(ev) {
        const model = ev.currentTarget.dataset.model;
        const id = Number(ev.currentTarget.dataset.id);
        if (!model || !id) {
            return;
        }
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: model,
            res_id: id,
            views: [[false, "form"]],
            target: "current",
        });
    }

    periodButtonClass(period) {
        return `o_eco_dashboard_filter${this.state.period === period ? " is-active" : ""}`;
    }

    get customApplyDisabled() {
        return this.state.loading || !this.state.dateStart || !this.state.dateEnd;
    }

    formatCardValue(card) {
        if (card.type === "currency") {
            return this.formatCurrency(card.value);
        }
        return this.formatNumber(card.value);
    }

    formatCardDaily(card) {
        if (card.type === "currency") {
            return this.formatCurrency(card.daily_value);
        }
        return this.formatNumber(card.daily_value);
    }

    formatCurrency(value) {
        return new Intl.NumberFormat("id-ID", {
            style: "currency",
            currency: "IDR",
            maximumFractionDigits: 0,
        }).format(value || 0);
    }

    formatNumber(value) {
        return new Intl.NumberFormat("id-ID", { maximumFractionDigits: 0 }).format(value || 0);
    }

    formatQuantity(value) {
        return new Intl.NumberFormat("id-ID", { maximumFractionDigits: 2 }).format(value || 0);
    }

    formatDate(value) {
        if (!value) {
            return "-";
        }
        return new Intl.DateTimeFormat("id-ID", {
            day: "2-digit",
            month: "short",
            year: "numeric",
        }).format(new Date(`${value}T00:00:00`));
    }

    formatReservationCode(row) {
        return `R-${String(row.id).padStart(3, "0")}`;
    }

    get trendMax() {
        const values = this.state.data.reservation_trend.map((item) => item.count || 0);
        return Math.max(1, ...values);
    }

    barStyle(point) {
        if (!point.count) {
            return "height: 0%;";
        }
        const height = Math.max(6, Math.round((point.count / this.trendMax) * 100));
        return `height: ${height}%;`;
    }

    get distributionTotal() {
        return this.state.data.visit_distribution.reduce((total, item) => total + (item.value || 0), 0);
    }

    get hasDistribution() {
        return this.distributionTotal > 0;
    }

    donutStyle() {
        if (!this.hasDistribution) {
            return "background: #f0f2f5;";
        }
        const colors = ["#1890ff", "#13c2c2", "#52c41a", "#faad14", "#eb2f96", "#722ed1"];
        let cursor = 0;
        const segments = this.state.data.visit_distribution.map((item, index) => {
            const start = cursor;
            cursor += ((item.value || 0) / this.distributionTotal) * 100;
            return `${colors[index % colors.length]} ${start}% ${cursor}%`;
        });
        return `background: conic-gradient(${segments.join(", ")});`;
    }

    statusLabelClass(status) {
        return `o_eco_status o_eco_status_${status || "unknown"}`;
    }

    inventoryStatusLabel(status) {
        const labels = {
            available: "Aktif",
            low: "Menipis",
            out: "Habis",
        };
        return labels[status] || "-";
    }

    inventoryStatusClass(status) {
        return `o_eco_status o_eco_inventory_${status || "unknown"}`;
    }
}

EcoethnoDashboard.template = "dashboard.EcoethnoDashboard";

registry.category("actions").add("dashboard.ecoethno_client_action", EcoethnoDashboard);
