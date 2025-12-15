// -*- coding: utf-8 -*-
/**
 * 前端应用主入口
 */

import { createApp } from 'vue';
import App from './App.vue';

// 导入Bootstrap CSS和JS
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';

// 创建Vue应用
const app = createApp(App);

// 挂载应用
app.mount('#app');
