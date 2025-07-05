let timer;
let running = false;
let startTime;
let elapsedTime = 0;
let recordCount = 0;
let isTimerMode = false;
let targetTime = 0;

// DOM 요소들
const recordList = document.getElementById('recordList');
const displaySeconds = document.getElementById('seconds');
const displayMilliseconds = document.getElementById('milliseconds');
const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const resetBtn = document.getElementById('resetBtn');
const deleteButton = document.getElementById('deleteButton');
const selectAllCheckbox = document.getElementById('selectAllCheckbox');
const stopwatchMode = document.getElementById('stopwatchMode');
const timerMode = document.getElementById('timerMode');
const timerSettings = document.getElementById('timerSettings');
const minutesInput = document.getElementById('minutesInput');
const secondsInput = document.getElementById('secondsInput');

function formatTime(ms) {
    if (isTimerMode) {
        // 타이머 모드: 카운트다운
        const remainingMs = Math.max(0, targetTime - ms);
        const minutes = Math.floor((remainingMs / 1000) / 60);
        const seconds = Math.floor((remainingMs / 1000) % 60);
        const milliseconds = Math.floor((remainingMs % 1000) / 10);
        return {
            minutes: String(minutes).padStart(2, '0'),
            seconds: String(seconds).padStart(2, '0'),
            milliseconds: String(milliseconds).padStart(2, '0')
        };
    } else {
        // 스톱워치 모드: 카운트업
        const minutes = Math.floor((ms / 1000) / 60);
        const seconds = Math.floor((ms / 1000) % 60);
        const milliseconds = Math.floor((ms % 1000) / 10);
        return {
            minutes: String(minutes).padStart(2, '0'),
            seconds: String(seconds).padStart(2, '0'),
            milliseconds: String(milliseconds).padStart(2, '0')
        };
    }
}

function updateDisplay() {
    const time = formatTime(elapsedTime);
    displaySeconds.textContent = time.minutes !== '00' ? `${time.minutes}:${time.seconds}` : time.seconds;
    displayMilliseconds.textContent = time.milliseconds;
    if (isTimerMode && elapsedTime >= targetTime && targetTime > 0) {
        clearInterval(timer);
        running = false;
        startBtn.disabled = false;
        pauseBtn.disabled = true;
        minutesInput.disabled = false;
        secondsInput.disabled = false;
        alert('타이머가 완료되었습니다!');
    }
}

function startTimer() {
    if (!running) {
        if (isTimerMode) {
            if (!running) {
                const minutes = parseInt(minutesInput.value) || 0;
                const seconds = parseInt(secondsInput.value) || 0;
                targetTime = (minutes * 60 + seconds) * 1000;
                if (targetTime === 0) {
                    alert('타이머 시간을 설정해주세요!');
                    return;
                }
                minutesInput.disabled = true;
                secondsInput.disabled = true;
            }
        }
        running = true;
        startTime = Date.now() - elapsedTime;
        timer = setInterval(() => {
            elapsedTime = Date.now() - startTime;
            updateDisplay();
            if (isTimerMode && elapsedTime >= targetTime && targetTime > 0) {
                clearInterval(timer);
                running = false;
                startBtn.disabled = false;
                pauseBtn.disabled = true;
                minutesInput.disabled = false;
                secondsInput.disabled = false;
                alert('타이머가 완료되었습니다!');
            }
        }, 10);
        startBtn.disabled = true;
        pauseBtn.disabled = false;
    }
}

function pauseTimer() {
    if (running) {
        running = false;
        clearInterval(timer);
        startBtn.disabled = false;
        pauseBtn.disabled = true;
        if (isTimerMode) {
            minutesInput.disabled = false;
            secondsInput.disabled = false;
        }
        if (!isTimerMode) {
            addRecord();
        }
    }
}

function resetTimer() {
    running = false;
    clearInterval(timer);
    elapsedTime = 0;
    targetTime = 0;
    updateDisplay();
    startBtn.disabled = false;
    pauseBtn.disabled = true;
    if (isTimerMode) {
        minutesInput.value = 0;
        secondsInput.value = 0;
        minutesInput.disabled = false;
        secondsInput.disabled = false;
    }
}

function addRecord() {
    recordCount++;
    const time = formatTime(elapsedTime);
    const recordText = (time.minutes !== '00' ? `${time.minutes}:` : '') + `${time.seconds}:${time.milliseconds}`;
    const listItem = document.createElement('li');
    listItem.className = 'lap-item';
    listItem.innerHTML = `
        <input type="checkbox" class="lap-checkbox">
        <span class="checkbox-icon">
            <i class="fas fa-circle"></i>
            <i class="fas fa-check-circle"></i>
        </span>
        <span class="lap-time">${recordText}</span>
    `;
    recordList.prepend(listItem);
    selectAllCheckbox.checked = false;
}

function deleteSelectedRecords() {
    const checkboxes = document.querySelectorAll('.lap-checkbox:checked');
    if (checkboxes.length === 0) {
        alert('삭제할 기록을 선택해주세요!');
        return; 
    }
    checkboxes.forEach(checkbox => {
        checkbox.closest('li').remove();
    });
    reorderRecords();
    updateSelectAllCheckbox();
}

function toggleSelectAllRecords() {
    const checkboxes = document.querySelectorAll('.lap-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
}

function updateSelectAllCheckbox() {
    const checkboxes = document.querySelectorAll('.lap-checkbox');
    const checked = document.querySelectorAll('.lap-checkbox:checked');
    selectAllCheckbox.checked = checkboxes.length > 0 && checkboxes.length === checked.length;
}

function reorderRecords() {
    const listItems = recordList.querySelectorAll('li');
    recordCount = listItems.length;
}

function switchToStopwatch() {
    isTimerMode = false;
    stopwatchMode.classList.add('active');
    timerMode.classList.remove('active');
    timerSettings.style.display = 'none';
    resetTimer();
}

function switchToTimer() {
    isTimerMode = true;
    timerMode.classList.add('active');
    stopwatchMode.classList.remove('active');
    timerSettings.style.display = 'flex';
    resetTimer();
}

// 커스텀 체크박스 클릭 시 실제 체크박스 토글
recordList.addEventListener('click', function(e) {
    if (e.target.closest('.checkbox-icon')) {
        const li = e.target.closest('li');
        const checkbox = li.querySelector('.lap-checkbox');
        checkbox.checked = !checkbox.checked;
        updateSelectAllCheckbox();
    }
});

// lap-checkbox 개별 클릭 시 전체선택 체크박스 상태 동기화
recordList.addEventListener('change', function(e) {
    if (e.target.classList.contains('lap-checkbox')) {
        updateSelectAllCheckbox();
    }
});

// 전체선택 체크박스 이벤트
selectAllCheckbox.addEventListener('change', toggleSelectAllRecords);

// 이벤트 리스너들
startBtn.addEventListener('click', startTimer);
pauseBtn.addEventListener('click', pauseTimer);
resetBtn.addEventListener('click', resetTimer);
deleteButton.addEventListener('click', deleteSelectedRecords);
stopwatchMode.addEventListener('click', switchToStopwatch);
timerMode.addEventListener('click', switchToTimer);

// 초기화
resetTimer();