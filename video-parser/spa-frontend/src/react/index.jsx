// -*- coding: utf-8 -*-
/**
 * React版本的前端应用主入口
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './components/react/App.jsx';

// 导入Bootstrap CSS和JS
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';

// 创建根节点
const root = ReactDOM.createRoot(document.getElementById('app'));

// 渲染应用
root.render(<App />);
