let collectedClues = [];
let suspectStressMap = {};
let isUVMode = false;

// ==========================================
// 🎵 RETRO SYNTH AUDIO ENGINE
// ==========================================
const AudioContext = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function getAudioContext() {
    if (!audioCtx) audioCtx = new AudioContext();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    return audioCtx;
}

function playClueSound() {
    try {
        const ctx = getAudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.25);
    } catch (e) {}
}

function playClickSound() {
    try {
        const ctx = getAudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(140, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(40, ctx.currentTime + 0.04);
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.04);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.04);
    } catch (e) {}
}

function playCardSelectSound() {
    try {
        const ctx = getAudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(660, ctx.currentTime + 0.08);
        gain.gain.setValueAtTime(0.1, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.08);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.08);
    } catch (e) {}
}

function playTensionSound() {
    try {
        const ctx = getAudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'square';
        osc.frequency.setValueAtTime(160, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(80, ctx.currentTime + 0.12);
        gain.gain.setValueAtTime(0.18, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.12);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.12);
    } catch (e) {}
}

function playVictorySound() {
    try {
        const ctx = getAudioContext();
        const notes = [440, 554.37, 659.25, 880];
        notes.forEach((freq, idx) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'square';
            osc.frequency.value = freq;
            const startTime = ctx.currentTime + (idx * 0.12);
            gain.gain.setValueAtTime(0.08, startTime);
            gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.35);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(startTime);
            osc.stop(startTime + 0.35);
        });
    } catch (e) {}
}

function playBuzzerSound() {
    try {
        const ctx = getAudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(130, ctx.currentTime);
        osc.frequency.linearRampToValueAtTime(100, ctx.currentTime + 0.4);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.4);
    } catch (e) {}
}

// ==========================================
// 🔦 UV FLASHLIGHT INTERACTIVE LOGIC
// ==========================================
function toggleUVMode() {
    const box = document.getElementById('uv-canvas-container');
    const light = document.getElementById('uv-light');
    const btn = document.getElementById('uv-toggle-btn');
    
    isUVMode = !isUVMode;
    if (isUVMode) {
        box.classList.add('uv-mode-active');
        light.style.display = 'block';
        btn.innerText = "🔦 Exit UV Mode";
        btn.style.background = "#bc8cff";
        btn.style.color = "#000";
    } else {
        box.classList.remove('uv-mode-active');
        light.style.display = 'none';
        btn.innerText = "🔦 Toggle UV Mode";
        btn.style.background = "#21262d";
        btn.style.color = "#d2a8ff";
        document.querySelectorAll('.hidden-clue-item').forEach(el => el.classList.remove('revealed'));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const box = document.getElementById('uv-canvas-container');
    const light = document.getElementById('uv-light');

    if (box && light) {
        box.addEventListener('mousemove', (e) => {
            if (!isUVMode) return;
            const rect = box.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            light.style.left = `${x}px`;
            light.style.top = `${y}px`;

            document.querySelectorAll('.hidden-clue-item').forEach(clueEl => {
                const clueRect = clueEl.getBoundingClientRect();
                const clueX = (clueRect.left + clueRect.width / 2) - rect.left;
                const clueY = (clueRect.top + clueRect.height / 2) - rect.top;

                const dist = Math.hypot(x - clueX, y - clueY);
                if (dist < 75) {
                    clueEl.classList.add('revealed');
                } else {
                    clueEl.classList.remove('revealed');
                }
            });
        });
    }
    
    initPolygraph();
});

// ==========================================
// 📈 POLYGRAPH OSCILLOSCOPE (CANVAS WAVE)
// ==========================================
let polygraphCurrentStress = 15;
let polygraphOffset = 0;

function initPolygraph() {
    const canvas = document.getElementById('polygraphCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function drawWave() {
        ctx.fillStyle = '#020406';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.lineWidth = 2;
        let color = '#7ee787';
        let amplitude = 6;
        let freqMultiplier = 0.04;

        if (polygraphCurrentStress > 65) {
            color = '#da3633';
            amplitude = 22;
            freqMultiplier = 0.12;
        } else if (polygraphCurrentStress > 35) {
            color = '#f0883e';
            amplitude = 12;
            freqMultiplier = 0.07;
        }

        ctx.strokeStyle = color;
        ctx.shadowBlur = 8;
        ctx.shadowColor = color;

        ctx.beginPath();
        const midY = canvas.height / 2;

        for (let x = 0; x < canvas.width; x++) {
            let y = midY + Math.sin((x + polygraphOffset) * freqMultiplier) * amplitude;
            
            if ((x + polygraphOffset) % 90 < 10) {
                y += (Math.random() - 0.5) * (amplitude * 2);
            }

            if (x === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }

        ctx.stroke();
        ctx.shadowBlur = 0;
        polygraphOffset += (polygraphCurrentStress > 65 ? 6 : 2);
        requestAnimationFrame(drawWave);
    }
    drawWave();
}

function updatePolygraph(stress) {
    polygraphCurrentStress = stress;
    const statusTxt = document.getElementById('polygraph-status');
    if (!statusTxt) return;

    if (stress > 65) {
        statusTxt.innerText = `🚨 CRITICAL DECEPTION: ${110 + Math.floor(stress/3)} BPM`;
        statusTxt.style.color = '#da3633';
    } else if (stress > 35) {
        statusTxt.innerText = `⚠️ ELEVATED STRESS: ${85 + Math.floor(stress/4)} BPM`;
        statusTxt.style.color = '#f0883e';
    } else {
        statusTxt.innerText = `STABLE: 68 BPM`;
        statusTxt.style.color = '#7ee787';
    }
}

// ==========================================
// ⌨️ TYPEWRITER ANIMATION
// ==========================================
function typeWriterEffect(element, text, speed = 25) {
    element.innerHTML = '';
    element.classList.add('typing-cursor');
    let i = 0;
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            if (i % 2 === 0) playClickSound();
            i++;
            setTimeout(type, speed);
        } else {
            element.classList.remove('typing-cursor');
        }
    }
    type();
}

// ==========================================
// 🌡️ STRESS METER & SUSPECT PANIC JITTER
// ==========================================
function updateStressUI(suspectId, stressVal) {
    suspectStressMap[suspectId] = stressVal;
    
    const activeSuspect = document.getElementById('suspect-select').value;
    if (activeSuspect === suspectId) {
        const mainBar = document.getElementById('main-stress-bar');
        const percentTxt = document.getElementById('stress-percent');
        const statusTxt = document.getElementById('stress-status');
        const badge = document.getElementById('stress-badge');

        mainBar.style.width = `${stressVal}%`;
        percentTxt.innerText = `${stressVal}%`;

        if (stressVal < 35) {
            statusTxt.innerText = "Calm";
            badge.style.color = "#7ee787";
        } else if (stressVal < 65) {
            statusTxt.innerText = "Uneasy / Anxious";
            badge.style.color = "#f0883e";
        } else {
            statusTxt.innerText = "Nervous Breakdown";
            badge.style.color = "#da3633";
            playTensionSound();
        }

        updatePolygraph(stressVal);
    }

    // Mini stress bar on Case Board
    const cardBar = document.getElementById(`card-stress-${suspectId}`);
    if (cardBar) cardBar.style.width = `${stressVal}%`;

    // 😰 ANIMATION 1: Suspect Panic Jitter Shake on Card
    const card = document.getElementById(`card-${suspectId}`);
    if (card) {
        if (stressVal > 65) {
            card.classList.add('suspect-panic');
        } else {
            card.classList.remove('suspect-panic');
        }
    }
}

function onSuspectChange() {
    const suspectId = document.getElementById('suspect-select').value;
    const currentStress = suspectStressMap[suspectId] || 15;
    updateStressUI(suspectId, currentStress);
}

// ==========================================
// 🕹️ GAMEPLAY LOGIC & ANIMATIONS
// ==========================================

// ✨ ANIMATION 2: Clue Discovery Bounce Pulse
async function collectClue(clueId) {
    playClueSound();

    const clueEl = document.getElementById(`clue-box-${clueId}`);
    if (clueEl) {
        clueEl.classList.add('clue-collected-anim');
        setTimeout(() => clueEl.classList.remove('clue-collected-anim'), 500);
    }

    try {
        const res = await fetch('/api/collect-clue', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ clue_id: clueId })
        });
        const data = await res.json();
        collectedClues = data.inventory;
        renderInventory();
    } catch (err) {
        console.error("Error collecting clue:", err);
    }
}

function renderInventory() {
    const list = document.getElementById('inventory-list');
    const count = document.getElementById('clue-count');
    if (!list || !count) return;

    list.innerHTML = '';
    count.textContent = collectedClues.length;

    collectedClues.forEach(clue => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${clue.name}:</strong> ${clue.desc}`;
        list.appendChild(li);
    });
}

function selectSuspectFromBoard(suspectId) {
    playCardSelectSound();
    const dropdown = document.getElementById('suspect-select');
    if (!dropdown) return;
    
    dropdown.value = suspectId;
    onSuspectChange();
    const selectedName = dropdown.options[dropdown.selectedIndex].text;
    appendMessage(`Selected ${selectedName} for interrogation.`, 'system');
}

async function askQuestion() {
    const input = document.getElementById('player-question');
    const question = input.value.trim();
    const suspectSelect = document.getElementById('suspect-select');
    const suspectId = suspectSelect.value;

    if (!question) return;

    playClickSound();

    appendMessage(question, 'player');
    input.value = '';

    const thinkingId = appendMessage("Interrogating...", 'system');

    try {
        const res = await fetch('/api/interrogate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ suspect_id: suspectId, question: question })
        });
        const data = await res.json();

        const tempMsg = document.getElementById(thinkingId);
        if (tempMsg) tempMsg.remove();

        const chatBox = document.getElementById('chat-box');
        const suspectMsg = document.createElement('div');
        suspectMsg.className = 'message suspect';
        chatBox.appendChild(suspectMsg);
        
        typeWriterEffect(suspectMsg, data.reply);
        chatBox.scrollTop = chatBox.scrollHeight;

        if (data.stress) {
            updateStressUI(suspectId, data.stress);
        }
    } catch (e) {
        const tempMsg = document.getElementById(thinkingId);
        if (tempMsg) tempMsg.remove();
        appendMessage("Interrogation connection error. Please try again.", 'system');
    }
}

function appendMessage(text, type) {
    const chatBox = document.getElementById('chat-box');
    const div = document.createElement('div');
    const msgId = 'msg-' + Date.now();
    div.id = msgId;
    div.className = `message ${type}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgId;
}

function handleKeyPress(e) {
    if (e.key === 'Enter') askQuestion();
}

// 💥 ANIMATION 3: Screen Shake & 🏆 ANIMATION 4: Victory Glow Pulse
async function accuseSuspect() {
    const suspectId = document.getElementById('suspect-select').value;
    try {
        const res = await fetch('/api/accuse', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ suspect_id: suspectId })
        });
        const data = await res.json();

        const modal = document.getElementById('result-modal');
        const modalContent = modal.querySelector('.modal-content');
        const modalTitle = document.getElementById('modal-title');
        const modalMessage = document.getElementById('modal-message');
        const modalBtn = modal.querySelector('button');

        modalMessage.innerHTML = data.message.replace(/\n/g, '<br>');

        if (data.result === 'correct') {
            playVictorySound();
            modalContent.classList.add('modal-victory');
            modalTitle.style.color = '#7ee787';
            modalTitle.innerText = "🎉 CASE SOLVED!";
            
            if (data.has_next) {
                modalBtn.innerText = "Proceed to Next Level ➡️";
                modalBtn.onclick = async () => {
                    await fetch('/api/next-level', { method: 'POST' });
                    location.reload();
                };
            } else {
                modalBtn.innerText = "Play Again from Level 1";
                modalBtn.onclick = async () => {
                    await fetch('/api/restart', { method: 'POST' });
                    location.reload();
                };
            }
        } else {
            playBuzzerSound();
            modalContent.classList.remove('modal-victory');

            // 💥 Trigger Screen Shake
            document.body.classList.add('screen-shake');
            setTimeout(() => document.body.classList.remove('screen-shake'), 450);

            modalTitle.style.color = '#da3633';
            modalTitle.innerText = "❌ CASE FAILED!";
            modalBtn.innerText = "Retry Level";
            modalBtn.onclick = () => location.reload();
        }

        modal.style.display = 'flex';
    } catch (err) {
        console.error("Error accusing suspect:", err);
    }
}