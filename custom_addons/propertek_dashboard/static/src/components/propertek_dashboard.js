/** @odoo-module **/

import { registry } from '@web/core/registry';
const { Component, useState, onWillStart, useRef } = owl;
import { useService } from "@web/core/utils/hooks";

export class OwlPropertekDashboard extends Component {
    setup(){
        this.state = useState({value:1})
    }
}

OwlPropertekDashboard.template = 'owl.PropertekDashboard'
registry.category('actions').add('owl.action_propertek_dashboard_js', OwlPropertekDashboard);