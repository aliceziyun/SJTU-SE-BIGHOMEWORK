import Vue from 'vue'
import VueRouter from 'vue-router';
import App from './App.vue'
import router from './router';
import 'ant-design-vue/dist/antd.css'; 
import "../reset.less"
import { Button} from 'ant-design-vue';
import { Card } from 'ant-design-vue';
import { Col } from 'ant-design-vue';
import { Row } from 'ant-design-vue';
import { Icon } from 'ant-design-vue';
import { Layout } from 'ant-design-vue';
import { Input } from 'ant-design-vue';
import { Tabs } from 'ant-design-vue';
import { Form } from 'ant-design-vue';
import { FormModel } from 'ant-design-vue';
import { Menu } from 'ant-design-vue';
import { Breadcrumb } from 'ant-design-vue';
import { Dropdown } from 'ant-design-vue';
import { Badge } from 'ant-design-vue';
import { Avatar } from 'ant-design-vue';
import { ConfigProvider } from 'ant-design-vue';
import { List } from 'ant-design-vue';
import { Empty } from 'ant-design-vue';
import { Popover } from 'ant-design-vue'
import { Alert } from 'ant-design-vue';
import { Descriptions, Divider} from 'ant-design-vue';
import { Modal} from 'ant-design-vue';
import { Affix } from 'ant-design-vue';
import { Checkbox } from 'ant-design-vue';
import {Comment} from 'ant-design-vue';
import {Tooltip} from 'ant-design-vue';
import { Radio } from 'ant-design-vue';
import {Table} from 'ant-design-vue';
import {Tag} from 'ant-design-vue';
import {Switch} from 'ant-design-vue';
import {Collapse} from 'ant-design-vue';

Vue.use(Button);
Vue.use(Input);
Vue.use(Layout);
Vue.use(Card);
Vue.use(Layout);
Vue.use(Col);
Vue.use(Row);
Vue.use(Icon);
Vue.use(Tabs);
Vue.use(Form);
Vue.use(FormModel);
Vue.use(Menu);
Vue.use(Breadcrumb);
Vue.use(Dropdown);
Vue.use(Badge);
Vue.use(Avatar);
Vue.use(ConfigProvider);
Vue.use(List);
Vue.use(Empty);
Vue.use(Popover);
Vue.use(Alert);
Vue.use(Descriptions);
Vue.use(Divider);
Vue.use(Modal);
Vue.use(Affix);
Vue.use(Checkbox);
Vue.use(Comment);
Vue.use(Tooltip);
Vue.use(Radio);
Vue.use(Table);
Vue.use(Tag);
Vue.use(Switch);
Vue.use(Collapse);

Vue.use(VueRouter);

Vue.config.productionTip = false;

new Vue({
  
  render: h => h(App),
  router: router,
}).$mount('#app')
