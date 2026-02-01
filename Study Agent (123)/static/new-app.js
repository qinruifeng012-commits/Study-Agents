const API_BASE_URL = 'http://127.0.0.1:8000';

let currentProfileId = null;
let currentPlanId = null;
let currentTopic = '';
let currentLessonIndex = 0;
let courseUnits = [];

// 本地存储键名
const STORAGE_KEYS = {
    PROFILE: 'study_agent_profile',
    PLAN: 'study_agent_plan',
    PROGRESS: 'study_agent_progress',
    COMPLETED_LESSONS: 'study_agent_completed_lessons'
};

// 页面导航
function navigateTo(pageId) {
    // 隐藏所有页面
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // 显示目标页面
    document.getElementById(pageId).classList.add('active');
}

// 加载动画
function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

// Markdown解析
function parseMarkdown(text) {
    if (!text) return '';
    
    // 替换标题
    text = text.replace(/### (.*?)(?=###|$)/g, '<h3>$1</h3>');
    
    // 替换加粗
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // 替换问题引导
    text = text.replace(/### 问题引导(.*?)(?=###|$)/gs, '<div class="question-guide"><h3>🤔 问题引入</h3><p>$1</p></div>');
    
    // 替换核心概念讲解
    text = text.replace(/### 核心概念讲解(.*?)(?=###|$)/gs, '<div class="key-concept"><h3>📚 核心讲解</h3><p>$1</p></div>');
    
    // 替换示例
    text = text.replace(/### 简短短示例(.*?)(?=###|$)/gs, '<div class="example-box"><h4>💡 示例</h4><p>$1</p></div>');
    
    // 替换练习题
    text = text.replace(/### 练习题(.*?)(?=###|$)/gs, '<div class="exercise-box"><h4>✏️ 练习题</h4><p>$1</p></div>');
    
    // 替换换行
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

// 显示结果
function showResult(elementId, html) {
    const element = document.getElementById(elementId);
    element.innerHTML = html;
    element.classList.remove('hidden');
}

// 显示错误
function showError(elementId, message) {
    showResult(elementId, `<p class="error">❌ 错误：${message}</p>`);
}

// 本地存储操作
function saveToStorage(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
}

function getFromStorage(key) {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

function clearStorage() {
    localStorage.removeItem(STORAGE_KEYS.PROFILE);
    localStorage.removeItem(STORAGE_KEYS.PLAN);
    localStorage.removeItem(STORAGE_KEYS.PROGRESS);
    localStorage.removeItem(STORAGE_KEYS.COMPLETED_LESSONS);
}

// 加载保存的进度
function loadSavedProgress() {
    const profile = getFromStorage(STORAGE_KEYS.PROFILE);
    const plan = getFromStorage(STORAGE_KEYS.PLAN);
    
    if (profile) {
        currentProfileId = profile.id;
    }
    
    if (plan) {
        currentPlanId = plan.id;
        currentTopic = plan.topic;
        courseUnits = plan.units;
    }
    
    return !!profile && !!plan;
}

// 创建用户画像
async function createProfile(event) {
    event.preventDefault();
    showLoading();
    
    const formData = new FormData(event.target);
    const data = {
        stage: formData.get('stage'),
        direction: formData.get('direction'),
        plan: formData.get('plan'),
        goal: formData.get('goal'),
        pace: formData.get('pace')
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/profile`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        currentProfileId = result.id;
        
        // 保存到本地存储（包含用户输入的direction字段）
        const profileToSave = {
            ...result,
            direction: formData.get('direction')
        };
        saveToStorage(STORAGE_KEYS.PROFILE, profileToSave);
        
        const html = `
            <h3>🎉 用户画像创建成功！</h3>
            <p><strong>画像ID：</strong>${result.id}</p>
            <p><strong>总结：</strong>${parseMarkdown(result.summary)}</p>
            <p><strong>优势：</strong></p>
            <ul>
                ${result.strengths.map(s => `<li>${parseMarkdown(s)}</li>`).join('')}
            </ul>
            <p><strong>薄弱点：</strong></p>
            <ul>
                ${result.weaknesses.map(w => `<li>${parseMarkdown(w)}</li>`).join('')}
            </ul>
            <p><strong>学习偏好：</strong></p>
            <ul>
                ${result.preferences.map(p => `<li>${parseMarkdown(p)}</li>`).join('')}
            </ul>
            <p><strong>风险点：</strong></p>
            <ul>
                ${result.risk_points.map(r => `<li>${parseMarkdown(r)}</li>`).join('')}
            </ul>
            <div class="profile-actions">
                <button onclick="editProfile()" class="btn btn-secondary">修改画像</button>
                <button onclick="navigateToPlanPage()" class="btn btn-primary">下一步：生成学习计划</button>
            </div>
        `;
        
        showResult('profile-result', html);
        
        // 隐藏表单
        document.getElementById('profile-form-container').style.display = 'none';
        event.target.reset();
        
    } catch (error) {
        showError('profile-result', error.message);
    } finally {
        hideLoading();
    }
}

// 生成学习计划
async function createPlan(event) {
    event.preventDefault();
    showLoading();
    
    const formData = new FormData(event.target);
    const topic = formData.get('topic');
    currentTopic = topic;
    
    try {
        const response = await fetch(`${API_BASE_URL}/plan?topic=${encodeURIComponent(topic)}${currentProfileId ? `&profile_id=${currentProfileId}` : ''}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        currentPlanId = result.id;
        courseUnits = result.units;
        
        // 保存到本地存储
        saveToStorage(STORAGE_KEYS.PLAN, result);
        saveToStorage(STORAGE_KEYS.PROGRESS, { currentLessonIndex: 0 });
        saveToStorage(STORAGE_KEYS.COMPLETED_LESSONS, []);
        
        // 隐藏表单
        document.getElementById('plan-form-container').style.display = 'none';
        
        // 显示课程列表
        displayCourseList(result);
        navigateTo('course-list-page');
        
    } catch (error) {
        showError('plan-result', error.message);
    } finally {
        hideLoading();
    }
}

// 显示课程列表
function displayCourseList(plan) {
    document.getElementById('course-list-topic').textContent = plan.topic;
    
    const completedLessons = getFromStorage(STORAGE_KEYS.COMPLETED_LESSONS) || [];
    const progress = getFromStorage(STORAGE_KEYS.PROGRESS) || { currentLessonIndex: 0 };
    
    const courseListHTML = courseUnits.map((unit, index) => {
        let statusClass = '';
        let statusIcon = '';
        let statusText = '';
        
        if (completedLessons.includes(unit.id)) {
            statusClass = 'completed';
            statusIcon = '✅';
            statusText = '已完成';
        } else if (index === progress.currentLessonIndex) {
            statusClass = 'current';
            statusIcon = '▶️';
            statusText = '进行中';
        } else if (index > progress.currentLessonIndex) {
            statusClass = 'locked';
            statusIcon = '🔒';
            statusText = '未解锁';
        } else {
            statusClass = '';
            statusIcon = '📄';
            statusText = '可复习';
        }
        
        const isLocked = index > progress.currentLessonIndex;
        
        return `
            <div class="course-item ${statusClass}" onclick="${isLocked ? '' : `loadLesson(${index})`}">
                <h3>${unit.title}</h3>
                <p>预计时间：${unit.estimated_time_minutes}分钟</p>
                <div class="course-item-status">
                    <span class="status-icon">${statusIcon}</span>
                    <span class="status-text ${statusClass}">${statusText}</span>
                </div>
            </div>
        `;
    }).join('');
    
    document.getElementById('course-list').innerHTML = courseListHTML;
}

// 加载课程内容
async function loadLesson(index) {
    if (index >= courseUnits.length) return;
    
    const unit = courseUnits[index];
    currentLessonIndex = index;
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE_URL}/lesson`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                plan_id: currentPlanId || 1,
                unit_id: unit.id
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // 更新页面标题
        document.getElementById('lesson-title').textContent = unit.title;
        
        // 显示课程内容
        const lessonHTML = `
            <h2>${unit.title}</h2>
            <div class="lesson-section">
                <h3>🤔 问题引入</h3>
                <div class="markdown-content">${parseMarkdown(result.introduction)}</div>
            </div>
            <div class="lesson-section">
                <h3>📚 核心讲解</h3>
                <div class="markdown-content">${parseMarkdown(result.explanation)}</div>
            </div>
            ${result.examples.length > 0 ? `
                <div class="lesson-section">
                    <h3>💡 示例</h3>
                    <ul>
                        ${result.examples.map(ex => `<li>${parseMarkdown(ex)}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            ${result.exercises.length > 0 ? `
                <div class="lesson-section">
                    <h3>✏️ 练习题</h3>
                    <ul>
                        ${result.exercises.map(ex => `<li>${parseMarkdown(ex)}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        `;
        
        document.getElementById('lesson-content').innerHTML = lessonHTML;
        
        // 更新按钮状态
        document.getElementById('next-lesson-btn').style.display = index < courseUnits.length - 1 ? 'block' : 'none';
        
        navigateTo('lesson-page');
        
    } catch (error) {
        alert('加载课程失败：' + error.message);
    } finally {
        hideLoading();
    }
}

// 完成课程
function completeLesson() {
    const currentUnit = courseUnits[currentLessonIndex];
    if (!currentUnit) return;
    
    // 更新已完成课程
    let completedLessons = getFromStorage(STORAGE_KEYS.COMPLETED_LESSONS) || [];
    if (!completedLessons.includes(currentUnit.id)) {
        completedLessons.push(currentUnit.id);
        saveToStorage(STORAGE_KEYS.COMPLETED_LESSONS, completedLessons);
    }
    
    // 更新当前进度
    if (currentLessonIndex < courseUnits.length - 1) {
        const newIndex = currentLessonIndex + 1;
        saveToStorage(STORAGE_KEYS.PROGRESS, { currentLessonIndex: newIndex });
    }
    
    alert('🎉 课程学习完成！');
    navigateTo('course-list-page');
    
    // 重新加载课程列表
    const plan = getFromStorage(STORAGE_KEYS.PLAN);
    if (plan) {
        displayCourseList(plan);
    }
}

// 下一课
function nextLesson() {
    if (currentLessonIndex < courseUnits.length - 1) {
        loadLesson(currentLessonIndex + 1);
    }
}

// 修改用户画像
function editProfile() {
    // 显示表单
    document.getElementById('profile-form-container').style.display = 'block';
    
    // 隐藏结果
    document.getElementById('profile-result').classList.add('hidden');
}

// 跳转到计划页面
function navigateToPlanPage() {
    // 获取用户画像数据
    const profile = getFromStorage(STORAGE_KEYS.PROFILE);
    
    // 跳转到计划页面
    navigateTo('plan-page');
    
    // 如果有用户画像，尝试从学习方向中提取学习主题
    if (profile && profile.direction) {
        const topicInput = document.getElementById('topic');
        if (topicInput) {
            topicInput.value = profile.direction;
        }
    }
}

// 提交反馈
async function submitFeedback(event) {
    event.preventDefault();
    showLoading();
    
    const formData = new FormData(event.target);
    const data = {
        profile_id: currentProfileId || 1,
        satisfaction: parseInt(formData.get('satisfaction')),
        difficulty: parseInt(formData.get('difficulty')),
        comment: formData.get('comment'),
        preferred_changes: []
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        alert('💬 反馈提交成功！感谢你的建议！');
        navigateTo('course-list-page');
        event.target.reset();
        
    } catch (error) {
        alert('提交反馈失败：' + error.message);
    } finally {
        hideLoading();
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 绑定事件
    document.getElementById('start-learning-btn').addEventListener('click', function() {
        navigateTo('profile-page');
    });
    
    document.getElementById('continue-learning-btn').addEventListener('click', function() {
        const hasSavedProgress = loadSavedProgress();
        if (hasSavedProgress) {
            const plan = getFromStorage(STORAGE_KEYS.PLAN);
            if (plan) {
                displayCourseList(plan);
                navigateTo('course-list-page');
            } else {
                navigateTo('plan-page');
            }
        } else {
            navigateTo('profile-page');
        }
    });
    
    document.getElementById('profile-form').addEventListener('submit', createProfile);
    document.getElementById('plan-form').addEventListener('submit', createPlan);
    document.getElementById('feedback-form').addEventListener('submit', submitFeedback);
    
    document.getElementById('complete-lesson-btn').addEventListener('click', completeLesson);
    document.getElementById('next-lesson-btn').addEventListener('click', nextLesson);
    
    // 检查是否有保存的进度
    const hasSavedProgress = loadSavedProgress();
    if (hasSavedProgress) {
        document.getElementById('continue-learning-btn').style.display = 'block';
        
        // 显示最近的学习计划
        displayRecentPlan();
    }
});

// 显示最近的学习计划
function displayRecentPlan() {
    const plan = getFromStorage(STORAGE_KEYS.PLAN);
    if (plan) {
        const recentPlanContent = document.getElementById('recent-plan-content');
        const recentPlanSection = document.getElementById('recent-plan');
        
        const progress = getFromStorage(STORAGE_KEYS.PROGRESS) || { currentLessonIndex: 0 };
        const completedLessons = getFromStorage(STORAGE_KEYS.COMPLETED_LESSONS) || [];
        
        const planHTML = `
            <div class="recent-plan-item">
                <h4>${plan.topic}</h4>
                <p>总课程数：${plan.units.length}</p>
                <p>已完成：${completedLessons.length}</p>
                <p>当前进度：第${progress.currentLessonIndex + 1}课</p>
                <button onclick="navigateTo('course-list-page')" class="btn btn-sm btn-primary">查看详情</button>
            </div>
        `;
        
        recentPlanContent.innerHTML = planHTML;
        recentPlanSection.classList.remove('hidden');
    }
}