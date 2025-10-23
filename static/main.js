// Main JavaScript for AI Text Platform

// Global state
const state = {
    currentTab: 'detect',
    loading: false
};

// API endpoints
const API = {
    detect: '/api/detect',
    humanize: '/api/humanize',
    process: '/api/process',
    languages: '/api/languages',
    scopes: '/api/scopes',
    audiences: '/api/audiences'
};

// DOM Elements
const elements = {
    // Tabs
    navLinks: document.querySelectorAll('.nav-link'),
    tabContents: document.querySelectorAll('.tab-content'),
    
    // Loading
    loadingOverlay: document.getElementById('loading-overlay'),
    
    // Detect tab
    detectLanguage: document.getElementById('detect-language'),
    detectText: document.getElementById('detect-text'),
    detectCharCount: document.getElementById('detect-char-count'),
    detectBtn: document.getElementById('detect-btn'),
    detectResult: document.getElementById('detect-result'),
    
    // Humanize tab
    humanizeLanguage: document.getElementById('humanize-language'),
    humanizeScope: document.getElementById('humanize-scope'),
    humanizeAudience: document.getElementById('humanize-audience'),
    useWebContext: document.getElementById('use-web-context'),
    humanizeText: document.getElementById('humanize-text'),
    humanizeCharCount: document.getElementById('humanize-char-count'),
    humanizeBtn: document.getElementById('humanize-btn'),
    humanizeResult: document.getElementById('humanize-result'),
    
    // Combined tab
    combinedLanguage: document.getElementById('combined-language'),
    combinedScope: document.getElementById('combined-scope'),
    combinedAudience: document.getElementById('combined-audience'),
    combinedText: document.getElementById('combined-text'),
    combinedCharCount: document.getElementById('combined-char-count'),
    combinedBtn: document.getElementById('combined-btn'),
    combinedDetectResult: document.getElementById('combined-detect-result'),
    combinedHumanizeResult: document.getElementById('combined-humanize-result')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeTextareas();
    initializeButtons();
});

// Tab Navigation
function initializeTabs() {
    elements.navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const tabName = link.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Update nav links
    elements.navLinks.forEach(link => {
        link.classList.toggle('active', link.dataset.tab === tabName);
    });
    
    // Update tab contents
    elements.tabContents.forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });
    
    state.currentTab = tabName;
}

// Textarea character counting
function initializeTextareas() {
    // Detect textarea
    elements.detectText.addEventListener('input', () => {
        elements.detectCharCount.textContent = elements.detectText.value.length;
    });
    
    // Humanize textarea
    elements.humanizeText.addEventListener('input', () => {
        elements.humanizeCharCount.textContent = elements.humanizeText.value.length;
    });
    
    // Combined textarea
    elements.combinedText.addEventListener('input', () => {
        elements.combinedCharCount.textContent = elements.combinedText.value.length;
    });
}

// Button handlers
function initializeButtons() {
    elements.detectBtn.addEventListener('click', handleDetect);
    elements.humanizeBtn.addEventListener('click', handleHumanize);
    elements.combinedBtn.addEventListener('click', handleCombined);
}

// Loading state
function setLoading(isLoading) {
    state.loading = isLoading;
    elements.loadingOverlay.classList.toggle('active', isLoading);
    
    // Disable all buttons when loading
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.disabled = isLoading;
    });
}

// API Handlers
async function handleDetect() {
    const text = elements.detectText.value.trim();
    if (!text) {
        showAlert('Please enter some text to analyze', 'error');
        return;
    }
    
    setLoading(true);
    
    try {
        const response = await fetch(API.detect, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                language: elements.detectLanguage.value || null
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayDetectionResult(data, elements.detectResult);
        } else {
            throw new Error(data.error || 'Detection failed');
        }
    } catch (error) {
        console.error('Detection error:', error);
        showAlert('Error: ' + error.message, 'error');
    } finally {
        setLoading(false);
    }
}

async function handleHumanize() {
    const text = elements.humanizeText.value.trim();
    if (!text) {
        showAlert('Please enter some text to humanize', 'error');
        return;
    }
    
    setLoading(true);
    
    try {
        const response = await fetch(API.humanize, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                scope: elements.humanizeScope.value,
                audience: elements.humanizeAudience.value,
                language: elements.humanizeLanguage.value,
                use_web_context: elements.useWebContext.checked
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayHumanizedResult(data, elements.humanizeResult);
        } else {
            throw new Error(data.error || 'Humanization failed');
        }
    } catch (error) {
        console.error('Humanization error:', error);
        showAlert('Error: ' + error.message, 'error');
    } finally {
        setLoading(false);
    }
}

async function handleCombined() {
    const text = elements.combinedText.value.trim();
    if (!text) {
        showAlert('Please enter some text to process', 'error');
        return;
    }
    
    setLoading(true);
    
    try {
        const response = await fetch(API.process, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                scope: elements.combinedScope.value,
                audience: elements.combinedAudience.value,
                language: elements.combinedLanguage.value,
                use_web_context: true
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayDetectionResult(data.detection, elements.combinedDetectResult);
            displayHumanizedResult(data.humanization, elements.combinedHumanizeResult);
        } else {
            throw new Error(data.error || 'Processing failed');
        }
    } catch (error) {
        console.error('Combined processing error:', error);
        showAlert('Error: ' + error.message, 'error');
    } finally {
        setLoading(false);
    }
}

// Result Display Functions
function displayDetectionResult(data, container) {
    const isAI = data.is_ai_generated;
    const confidence = Math.round(data.confidence * 100);
    const mainLanguage = Object.entries(data.language)[0];
    
    container.innerHTML = `
        <div class="detection-result">
            <div class="ai-score">
                <div class="score-circle ${isAI ? 'ai-detected' : 'human-written'}">
                    <svg width="150" height="150">
                        <circle cx="75" cy="75" r="70" fill="none" stroke="#e5e7eb" stroke-width="10"/>
                        <circle cx="75" cy="75" r="70" fill="none" 
                            stroke="${isAI ? '#ef4444' : '#10b981'}" 
                            stroke-width="10"
                            stroke-dasharray="${confidence * 4.4} 440"
                            stroke-linecap="round"/>
                    </svg>
                    <div class="score-value">${confidence}%</div>
                </div>
                <div class="score-label">
                    ${isAI ? '🤖 AI Generated' : '✍️ Human Written'}
                </div>
                <p>${data.explanation ? data.explanation[0] : ''}</p>
            </div>
            
            <div class="detection-details">
                ${mainLanguage ? `
                <div class="detail-item">
                    <span class="detail-label">Detected Language</span>
                    <span class="detail-value">
                        <span class="language-badge">
                            <i class="fas fa-globe"></i> ${mainLanguage[0]} (${Math.round(mainLanguage[1] * 100)}%)
                        </span>
                    </span>
                </div>
                ` : ''}
                
                ${data.model_scores ? Object.entries(data.model_scores).map(([model, score]) => `
                <div class="detail-item">
                    <span class="detail-label">${formatModelName(model)}</span>
                    <span class="detail-value">${Math.round(score * 100)}%</span>
                </div>
                `).join('') : ''}
            </div>
            
            ${data.explanation && data.explanation.length > 1 ? `
            <div class="modifications-list">
                <h4>Analysis Details</h4>
                <ul>
                    ${data.explanation.slice(1).map(exp => `<li>• ${exp}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
        </div>
    `;
}

function displayHumanizedResult(data, container) {
    const humanizedText = data.humanized_text;
    const copyId = 'copy-' + Date.now();
    
    container.innerHTML = `
        <div class="humanized-result">
            <div class="humanized-text" id="text-${copyId}">${escapeHtml(humanizedText)}</div>
            <button class="copy-button" onclick="copyText('text-${copyId}')">
                <i class="fas fa-copy"></i> Copy Text
            </button>
            
            ${data.modifications && data.modifications.length > 0 ? `
            <div class="modifications-list">
                <h4>Modifications Applied</h4>
                <ul>
                    ${data.modifications.map(mod => `<li>• ${mod}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
            
            ${data.web_contexts && data.web_contexts.length > 0 ? `
            <div class="modifications-list">
                <h4>Web Context Used</h4>
                <ul>
                    ${data.web_contexts.map(ctx => `
                        <li>• <a href="${ctx.url}" target="_blank">${ctx.title || 'Source'}</a></li>
                    `).join('')}
                </ul>
            </div>
            ` : ''}
        </div>
    `;
}

// Utility Functions
function formatModelName(modelName) {
    const nameMap = {
        'heuristic_analysis': 'Linguistic Analysis',
        'Hello-SimpleAI/chatgpt-detector-roberta': 'ChatGPT Detector',
        'umm-maybe/AI-image-detector': 'AI Content Detector'
    };
    return nameMap[modelName] || modelName;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function copyText(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Text copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Copy failed:', err);
        showAlert('Failed to copy text', 'error');
    });
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add to page
    document.querySelector('.main .container').prepend(alert);
    
    // Remove after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        switch (state.currentTab) {
            case 'detect':
                elements.detectBtn.click();
                break;
            case 'humanize':
                elements.humanizeBtn.click();
                break;
            case 'combined':
                elements.combinedBtn.click();
                break;
        }
    }
    
    // Tab navigation with number keys
    if (e.key >= '1' && e.key <= '3' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const tabIndex = parseInt(e.key) - 1;
        const tabs = ['detect', 'humanize', 'combined'];
        if (tabs[tabIndex]) {
            switchTab(tabs[tabIndex]);
        }
    }
});