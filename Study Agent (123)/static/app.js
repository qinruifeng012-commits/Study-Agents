const API_BASE_URL = 'http://127.0.0.1:8000';

let currentProfileId = null;
let currentPlanId = null;

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function showResult(elementId, html) {
    const element = document.getElementById(elementId);
    element.innerHTML = html;
    element.classList.remove('hidden');
}

function showError(elementId, message) {
    showResult(elementId, `<p class="error">❌ 错误：${message}</p>`);
}

function showSuccess(elementId, message) {
    showResult(elementId, `<p class="success">✅ ${message}</p>`);
}

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
        
        const html = `
            <h3>🎉 用户画像创建成功！</h3>
            <p><strong>画像ID：</strong>${result.id}</p>
            <p><strong>总结：</strong>${result.summary}</p>
            <p><strong>优势：</strong></p>
            <ul>
                ${result.strengths.map(s => `<li>${s}</li>`).join('')}
            </ul>
            <p><strong>薄弱点：</strong></p>
            <ul>
                ${result.weaknesses.map(w => `<li>${w}</li>`).join('')}
            </ul>
            <p><strong>学习偏好：</strong></p>
            <ul>
                ${result.preferences.map(p => `<li>${p}</li>`).join('')}
            </ul>
            <p><strong>风险点：</strong></p>
            <ul>
                ${result.risk_points.map(r => `<li>${r}</li>`).join('')}
            </ul>
            <p class="info">💡 请记住你的画像ID：${result.id}，后续步骤会用到</p>
        `;
        
        showResult('profile-result', html);
        event.target.reset();
        
    } catch (error) {
        showError('profile-result', error.message);
    } finally {
        hideLoading();
    }
}

async function createPlan(event) {
    event.preventDefault();
    showLoading();
    
    const formData = new FormData(event.target);
    const topic = formData.get('topic');
    
    try {
        const response = await fetch(`${API_BASE_URL}/plan?topic=${encodeURIComponent(topic)}${currentProfileId ? `&profile_id=${currentProfileId}` : ''}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        currentPlanId = result.id;
        
        const html = `
            <h3>📚 学习计划生成成功！</h3>
            <p><strong>计划ID：</strong>${result.id}</p>
            <p><strong>主题：</strong>${result.topic}</p>
            <p><strong>总结：</strong>${result.summary}</p>
            <h4>学习章节：</h4>
            <ul>
                ${result.units.map(unit => `
                    <li>
                        <strong>${unit.title}</strong> (ID: ${unit.id})
                        <br>
                        <small>预计时间：${unit.estimated_time_minutes}分钟</small>
                    </li>
                `).join('')}
            </ul>
            <p class="info">💡 请记住计划ID：${result.id}，学习课程时会用到</p>
        `;
        
        showResult('plan-result', html);
        event.target.reset();
        
    } catch (error) {
        showError('plan-result', error.message);
    } finally {
        hideLoading();
    }
}

async function getLesson(event) {
    event.preventDefault();
    showLoading();
    
    const formData = new FormData(event.target);
    const topic = formData.get('lesson-topic');
    const unitId = formData.get('unit-id');
    
    try {
        const response = await fetch(`${API_BASE_URL}/lesson`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                plan_id: currentPlanId || 1,
                unit_id: unitId
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        const html = `
            <h3>📖 课程内容</h3>
            <p><strong>章节ID：</strong>${result.unit_id}</p>
            <h4>🤔 问题引入</h4>
            <p>${result.introduction}</p>
            <h4>📚 核心讲解</h4>
            <p>${result.explanation}</p>
            ${result.examples.length > 0 ? `
                <h4>💡 示例</h4>
                <ul>
                    ${result.examples.map(ex => `<li>${ex}</li>`).join('')}
                </ul>
            ` : ''}
            ${result.exercises.length > 0 ? `
                <h4>✏️ 练习题</h4>
                <ul>
                    ${result.exercises.map(ex => `<li>${ex}</li>`).join('')}
                </ul>
            ` : ''}
        `;
        
        showResult('lesson-result', html);
        
    } catch (error) {
        showError('lesson-result', error.message);
    } finally {
        hideLoading();
    }
}

async function getReview(event) {
    event.preventDefault();
    showLoading();
    
    const formData = new FormData(event.target);
    const topic = formData.get('review-topic');
    const unitId = formData.get('review-unit-id');
    
    try {
        const response = await fetch(`${API_BASE_URL}/review`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                plan_id: currentPlanId || 1,
                unit_id: unitId
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        const html = `
            <h3>🔄 复习计划</h3>
            <h4>需要复习的内容：</h4>
            <ul>
                ${result.items.map(item => `
                    <li>
                        <strong>${item.reference_unit_id || item.knowledge_point_id}</strong>
                        <br>
                        <small>${item.reason}</small>
                    </li>
                `).join('')}
            </ul>
            ${result.combined_exercises.length > 0 ? `
                <h4>📝 综合练习题</h4>
                <ul>
                    ${result.combined_exercises.map(ex => `<li>${ex}</li>`).join('')}
                </ul>
            ` : ''}
        `;
        
        showResult('review-result', html);
        
    } catch (error) {
        showError('review-result', error.message);
    } finally {
        hideLoading();
    }
}

async function submitFeedback(event) {
    event.preventDefault();
    showLoading();
    
    const formData = new FormData(event.target);
    const data = {
        profile_id: parseInt(formData.get('feedback-profile-id')),
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
        
        const html = `
            <h3>💬 反馈提交成功！</h3>
            <p class="success">感谢你的反馈！我们会根据你的建议不断改进。</p>
            ${result.profile_updates ? '<p class="info">用户画像已更新</p>' : ''}
            ${result.plan_adjustment_summary ? `<p><strong>调整建议：</strong>${result.plan_adjustment_summary}</p>` : ''}
        `;
        
        showResult('feedback-result', html);
        event.target.reset();
        
    } catch (error) {
        showError('feedback-result', error.message);
    } finally {
        hideLoading();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('profile-form').addEventListener('submit', createProfile);
    document.getElementById('plan-form').addEventListener('submit', createPlan);
    document.getElementById('lesson-form').addEventListener('submit', getLesson);
    document.getElementById('review-form').addEventListener('submit', getReview);
    document.getElementById('feedback-form').addEventListener('submit', submitFeedback);
});