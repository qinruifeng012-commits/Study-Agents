# Study Agent - 建站学习指南

> 本指南专为正在学习编程的学生设计，详细记录从零开始搭建 Study Agent 网站的每一步。

---

## 📁 项目结构

```
study-agent/
├── apps/
│   ├── web/              # 主网站 (Next.js)
│   └── docs/             # 文档站点 (Next.js)
├── packages/
│   ├── ui/               # 共享 UI 组件
│   ├── eslint-config/    # ESLint 配置
│   └── typescript-config/# TypeScript 配置
├── package.json          # 根目录配置
└── turbo.json            # Turborepo 配置
```

---

## 🚀 第一阶段：环境准备

### 1.1 安装必要工具

| 工具 | 下载地址 | 用途 |
|------|----------|------|
| Node.js | https://nodejs.org/ | JavaScript 运行时 (已安装 v24.12.0) |
| VS Code | https://code.visualstudio.com/ | 代码编辑器 |
| Git | https://git-scm.com/ | 版本控制 |

### 1.2 验证安装

打开终端，输入以下命令验证：

```bash
node --version    # 应显示版本号
npm --version     # 应显示版本号
git --version     # 应显示版本号
```

---

## 🏗️ 第二阶段：项目初始化

### 2.1 创建 Turborepo 项目

```bash
# 进入项目目录
cd "c:\Users\Qin\Desktop\study agent(claude)\project"

# 使用 create-turbo 创建项目
npx create-turbo@latest study-agent --package-manager npm --no-git
```

**什么是 Turborepo？**
- Turborepo 是一个用于 JavaScript/TypeScript 项目的构建系统
- 它可以帮助你管理多个包（monorepo）
- 优点：共享代码、统一配置、高效构建

### 2.2 启动开发服务器

```bash
# 进入项目目录
cd study-agent

# 启动所有应用的开发服务器
npm run dev
```

启动后，访问：
- Web 应用：http://localhost:3000
- Docs 应用：http://localhost:3001

---

## 📦 第三阶段：安装依赖

### 3.1 为 Web 应用安装依赖

```bash
# 进入 apps/web 目录
cd apps/web

# 安装 Next.js 依赖 (已默认安装，以下为额外依赖)
npm install lucide-react        # 图标库
npm install class-variance-authority  # 样式工具
npm install clsx                # 类名工具
npm install tailwind-merge      # Tailwind 工具
```

### 3.2 安装后端相关依赖

```bash
# 返回根目录
cd ../..

# 安装后端框架
npm install fastify @fastify/cors --workspace=apps/web

# 安装 Agent 框架
npm install langchain @langchain/core @langchain/anthropic --workspace=apps/web

# 安装数据库工具
npm install drizzle-orm postgres --workspace=apps/web
npm install -D drizzle-kit --workspace=apps/web
```

---

## 🎨 第四阶段：UI 改造

### 4.1 安装 shadcn/ui

shadcn/ui 是一个现代化的 UI 组件库，代码完全开源可定制。

```bash
# 进入 web 应用目录
cd apps/web

# 初始化 shadcn/ui
npx shadcn@latest init

# 添加常用组件
npx shadcn@latest add button
npx shadcn@latest add input
npx shadcn@latest add card
npx shadcn@latest add dialog
npx shadcn@latest add tabs
```

### 4.2 安装 React Flow（知识网可视化）

```bash
npm install @xyflow/react
```

---

## 🔧 第五阶段：项目配置

### 5.1 创建环境变量文件

在 `apps/web` 目录下创建 `.env.local` 文件：

```env
# Claude API (用于 AI 功能)
ANTHROPIC_API_KEY=your_api_key_here

# 数据库连接
DATABASE_URL=postgresql://user:password@localhost:5432/study_agent

# Redis 缓存
REDIS_URL=redis://localhost:6379
```

### 5.2 修改 Next.js 配置

编辑 `apps/web/next.config.js`：

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // 允许 API 路由
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
};

module.exports = nextConfig;
```

---

## 📝 第六阶段：开发计划

### Phase 1 MVP - 用户画像 + 基础教学生成 (2-3 周)

#### 第 1 周：项目设置
- [ ] 完成环境搭建
- [ ] 安装所有依赖
- [ ] 配置 TypeScript
- [ ] 设置 ESLint 规则

#### 第 2 周：用户画像系统
- [ ] 创建用户输入表单（学习阶段、方向、目标等）
- [ ] 实现表单验证
- [ ] 连接 Claude API 生成用户画像
- [ ] 保存画像到数据库

#### 第 3 周：基础教学生成
- [ ] 实现简单的教学文本生成
- [ ] 创建教学页面布局
- [ ] 添加加载状态

### Phase 2 - 知识网 + 逻辑校验 + 学习规划 (3-4 周)

### Phase 3 - 复盘系统 + 反馈循环 (2-3 周)

---

## 💻 常用命令速查

### 开发相关

```bash
# 启动开发服务器
npm run dev

# 启动特定应用
npm run dev --filter=web
npm run dev --filter=docs

# 构建项目
npm run build

# 检查类型
npm run check-types

# 格式化代码
npm run format
```

### Git 相关

```bash
# 初始化 Git
git init

# 添加文件
git add .

# 提交更改
git commit -m "描述你的更改"

# 查看状态
git status
```

---

## 📚 学习资源

### Next.js 学习
- [Next.js 官方文档](https://nextjs.org/docs)
- [Next.js 中文文档](https://nextjs.org/docs)

### TypeScript 学习
- [TypeScript 官方手册](https://www.typescriptlang.org/zh/docs/)
- [TypeScript 入门教程](https://ts.xcatliu.com/)

### React 学习
- [React 官方文档](https://react.dev/)
- [React 中文文档](https://zh-hans.react.dev/)

### Tailwind CSS
- [Tailwind CSS 官方文档](https://tailwindcss.com/docs)
- [Tailwind CSS 中文文档](https://tailwindcss.bootcss.com/)

---

## 🐛 常见问题

### 问题 1：端口被占用

**现象：** 启动开发服务器时报错 `Port 3000 is in use`

**解决：**
```bash
# Windows - 查找占用端口的进程
netstat -ano | findstr :3000

# 杀死进程（替换 PID）
taskkill /PID <PID> /F
```

### 问题 2：依赖安装失败

**现象：** `npm install` 报错

**解决：**
```bash
# 清理缓存
npm cache clean --force

# 删除 node_modules 和 lock 文件
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

### 问题 3：TypeScript 类型错误

**现象：** 红色波浪线，类型不匹配

**解决：**
1. 检查 import 路径是否正确
2. 检查类型定义是否完整
3. 运行 `npm run check-types` 查看所有错误

---

## 📞 获取帮助

- 项目问题：查看 `PRD.md` 和 `TECH_STACK.md`
- 代码问题：使用 `npm run lint` 检查
- 类型问题：使用 `npm run check-types` 检查

---

## 🎯 下一步行动

1. **完成环境验证**
   ```bash
   cd "c:\Users\Qin\Desktop\study agent(cursor)\project\study-agent"
   npm run dev
   ```

2. **访问 http://localhost:3000 确认网站运行**

3. **开始阅读 Next.js 文档，学习基础概念**

4. **尝试修改 `apps/web/app/page.tsx`，看到你的第一个更改生效**

---

*最后更新：2026-03-02*

---

## 📖 附录：知识链与学习路径

> 本部分为零基础学习者设计，按照"学中做，做中学"的理念，边学边练。

### 知识链总览

```
JavaScript 基础 → TypeScript 入门 → React 基础 → Next.js 框架 → 全栈开发
                                            ↓
                                    Study Agent 项目实践
```

---

### 第一阶段：编程基础（1-2 周）

#### 1.1 JavaScript 基础

**学习目标：** 理解编程基本概念

| 知识点 | 学习内容 | 实践练习 | 资源链接 |
|--------|----------|----------|----------|
| 变量与数据类型 | let/const、字符串、数字、布尔 | 创建个人简介变量 | [MDN JavaScript](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript) |
| 函数 | 箭头函数、参数、返回值 | 写一个打招呼函数 | 同上 |
| 数组与对象 | 创建、访问、遍历 | 创建书单数组 | 同上 |
| DOM 操作 | 选择元素、事件监听 | 制作点击按钮变色 | 同上 |

**每日练习示例：**
```javascript
// 第 1 天：变量练习
const name = "你的名字";
const age = 18;
console.log(`你好，我是${name}，今年${age}岁`);

// 第 2 天：函数练习
function greet(name) {
  return `欢迎，${name}!`;
}
console.log(greet("小明"));

// 第 3 天：数组练习
const books = ["书 1", "书 2", "书 3"];
books.forEach(book => console.log(book));
```

---

#### 1.2 TypeScript 入门（3-5 天）

**学习目标：** 理解类型系统

| 知识点 | 学习内容 | 为什么需要 |
|--------|----------|------------|
| 类型注解 | `let age: number = 18` | 防止类型错误 |
| 接口 | `interface User { name: string }` | 定义数据结构 |
| 泛型 | `function identity<T>(arg: T): T` | 代码复用 |

**实践练习：**
```typescript
// 定义用户类型
interface User {
  id: number;
  name: string;
  email: string;
}

// 创建用户
const user: User = {
  id: 1,
  name: "小明",
  email: "xiaoming@example.com"
};

// TypeScript 会报错如果属性不对
// const badUser: User = { name: "缺少 id 和 email" }; // 错误！
```

---

### 第二阶段：前端基础（2-3 周）

#### 2.1 React 基础

**学习目标：** 理解组件化思想

| 知识点 | 学习内容 | 项目中的应用 |
|--------|----------|--------------|
| JSX 语法 | HTML + JavaScript 混合 | 写页面结构 |
| 组件 | Function Component | 页面各部分 |
| Props | 组件间传值 | 传递用户数据 |
| State | useState 钩子 | 表单状态管理 |
| 效果 | useEffect 钩子 | 数据获取 |

**组件示例（可复用）：**
```jsx
// 一个简单的卡片组件
function Card({ title, children }) {
  return (
    <div className="border rounded-lg p-4">
      <h3 className="text-lg font-bold">{title}</h3>
      <div>{children}</div>
    </div>
  );
}

// 使用组件
<Card title="用户信息">
  <p>姓名：小明</p>
  <p>学习目标：学会编程</p>
</Card>
```

**学习资源：**
- [React 官方教程](https://zh-hans.react.dev/learn)
- [React 基础中文教程](https://www.ruanyifeng.com/blog/2015/03/react.html)

---

#### 2.2 Tailwind CSS

**学习目标：** 快速样式开发

| 类别 | 常用类名 | 效果 |
|------|----------|------|
| 间距 | `p-4`, `m-2`, `px-4` | 内边距/外边距 |
| 颜色 | `bg-blue-500`, `text-white` | 背景色/文字色 |
| 布局 | `flex`, `justify-center` | Flex 布局 |
| 尺寸 | `w-full`, `h-10` | 宽高 |

**练习：** 用 Tailwind 写一个按钮
```jsx
<button className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
  点击我
</button>
```

---

### 第三阶段：Next.js 全栈（2-3 周）

#### 3.1 Next.js 基础

**学习目标：** 理解服务端渲染和路由

| 知识点 | 说明 | 项目应用 |
|--------|------|----------|
| 文件路由 | `app/page.tsx` = 首页 | 创建页面 |
| 布局 | `layout.tsx` | 统一导航栏 |
| API 路由 | `app/api/xxx/route.ts` | 后端接口 |
| 服务端组件 | 默认 | 数据获取 |
| 客户端组件 | `"use client"` | 交互功能 |

**第一个 Next.js 页面修改：**
```jsx
// 打开 apps/web/app/page.tsx
// 修改为：
export default function Home() {
  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold">我的学习助手</h1>
      <p className="mt-4">开始你的学习之旅</p>
    </main>
  );
}
```

---

#### 3.2 创建 API 接口

**学习目标：** 理解前后端交互

```typescript
// apps/web/app/api/hello/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({ message: 'Hello, World!' });
}

// 访问 http://localhost:3000/api/hello 测试
```

---

### 第四阶段：项目实战（持续）

#### 4.1 用户画像表单

**用到的知识：**
- React 表单
- TypeScript 类型定义
- API 调用

```jsx
// 简化的表单示例
"use client";
import { useState } from 'react';

export default function ProfileForm() {
  const [formData, setFormData] = useState({
    stage: '',
    direction: '',
    goal: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    // 发送到 API
    const response = await fetch('/api/profile', {
      method: 'POST',
      body: JSON.stringify(formData)
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        placeholder="学习阶段"
        value={formData.stage}
        onChange={e => setFormData({...formData, stage: e.target.value})}
      />
      <button type="submit">提交</button>
    </form>
  );
}
```

---

### 学习检查清单

#### JavaScript 基础检查
- [ ] 理解变量声明（let/const）
- [ ] 会写箭头函数
- [ ] 理解数组的 map/filter/forEach
- [ ] 理解对象的解构赋值

#### React 检查
- [ ] 理解 JSX 是什么
- [ ] 会创建 Function Component
- [ ] 理解 props 和 state 的区别
- [ ] 会用 useState 和 useEffect

#### Next.js 检查
- [ ] 理解文件路由
- [ ] 会创建 API 路由
- [ ] 理解服务端组件和客户端组件
- [ ] 会部署到 Vercel

---

### 推荐学习节奏

| 时间 | 内容 | 目标 |
|------|------|------|
| 第 1 周 | JavaScript 基础 | 完成 MDN 入门教程 |
| 第 2 周 | TypeScript + React | 理解类型和组件 |
| 第 3 周 | Next.js 基础 | 创建简单博客 |
| 第 4 周 | 项目实战 | 开始 Study Agent 开发 |

---

### 遇到问题时的解决步骤

1. **理解错误信息** - 仔细阅读报错，通常会告诉你问题在哪
2. **搜索错误** - 复制错误信息到 Google/Stack Overflow
3. **简化代码** - 创建一个最小可复现的例子
4. **询问 AI** - 向 Claude 或其他 AI 助手提问
5. **检查文档** - 官方文档通常有答案

---

### 学习心态建议

1. **不要追求完美** - 先做出能用的东西，再优化
2. **接受不懂** - 有些概念需要时间消化，先记住怎么用
3. **多动手** - 看教程不如自己动手写
4. **记录问题** - 建立一个"错误本"，记录遇到的问题和解决方案
5. **休息很重要** - 遇到 bug 先休息，回来可能就有思路了
