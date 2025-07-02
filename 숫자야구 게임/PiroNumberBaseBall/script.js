let answer = [];
let attempts = 9;
let isGameOver = false;


const inputFields = [
  document.getElementById('number1'),
  document.getElementById('number2'),
  document.getElementById('number3')
];
const submitButton = document.querySelector('.submit-button');
const resultsDiv = document.getElementById('results');
const attemptsSpan = document.getElementById('attempts');
const resultImg = document.getElementById('game-result-img');

// 랜덤 숫자 3개 생성 (1~9, 중복X)
function generateAnswer() {
  const nums = [];
  while (nums.length < 3) {
    const n = Math.floor(Math.random() * 9) + 1;
    if (!nums.includes(n)) nums.push(n);
  }
  return nums;
}

// 입력값 유효성 검사
function validateInput() {
  const values = inputFields.map(f => f.value.trim());
  if (values.some(v => v === '')) return false;
  if (values.some(v => isNaN(v) || v < 1 || v > 9)) return false;
  if (new Set(values).size !== 3) return false;
  return true;
}

// 스트라이크/볼/아웃 판정
function getResult(userInput) {
  let strike = 0, ball = 0;
  for (let i = 0; i < 3; i++) {
    if (userInput[i] === answer[i]) strike++;
    else if (answer.includes(userInput[i])) ball++;
  }
  if (strike === 0 && ball === 0) return {strike, ball, out: true};
  return {strike, ball, out: false};
}

// 결과 출력 
function printResult(userInput, resultObj) {
  const row = document.createElement('div');
  row.style.display = 'flex';
  row.style.alignItems = 'center';
  row.style.justifyContent = 'flex-start';
  row.style.marginBottom = '6px';

  // 입력 숫자
  const numSpan = document.createElement('span');
  numSpan.textContent = userInput.join(' ');
  numSpan.style.width = '60px';
  numSpan.style.display = 'inline-block';
  numSpan.style.textAlign = 'right';
  row.appendChild(numSpan);

  
  const colon = document.createElement('span');
  colon.textContent = ' : ';
  colon.style.margin = '0 180px 0 10px';
  row.appendChild(colon);

  // 결과 
  if (resultObj.out) {
    const outSpan = document.createElement('span');
    outSpan.textContent = 'O';
    outSpan.className = 'num-result out';
    row.appendChild(outSpan);
  } else {
    // 스트라이크
    const sNum = document.createElement('span');
    sNum.textContent = resultObj.strike;
    sNum.style.marginRight = '2px';
    row.appendChild(sNum);
    const sSpan = document.createElement('span');
    sSpan.textContent = 'S';
    sSpan.className = 'num-result strike';
    sSpan.style.marginRight = '8px';
    row.appendChild(sSpan);
    // 볼
    const bNum = document.createElement('span');
    bNum.textContent = resultObj.ball;
    bNum.style.marginRight = '2px';
    row.appendChild(bNum);
    const bSpan = document.createElement('span');
    bSpan.textContent = 'B';
    bSpan.className = 'num-result ball';
    row.appendChild(bSpan);
  }
  resultsDiv.appendChild(row);
}

// 게임 종료 처리
function endGame(isWin) {
  isGameOver = true;
  submitButton.disabled = true;
  submitButton.style.backgroundColor = '#ccc';
  resultImg.src = isWin ? 'success.png' : 'fail.png';
  resultImg.alt = isWin ? '성공' : '실패';
}

// 입력창, 결과, 상태 초기화
function resetGame() {
  answer = generateAnswer();
  attempts = 9;
  isGameOver = false;
  attemptsSpan.textContent = attempts;
  resultsDiv.innerHTML = '';
  resultImg.src = '';
  submitButton.disabled = false;
  submitButton.style.backgroundColor = '';
  inputFields.forEach(f => { f.value = ''; f.disabled = false; });
  inputFields[0].focus();
  const banner = document.getElementById('game-result-banner');
  if (banner) banner.style.display = 'none';
}

// 숫자 확인 버튼 이벤트 (index.html에서 onclick으로 연결)
function check_numbers() {
  if (isGameOver) return;
  if (!validateInput()) {
    alert('1~9 사이의 중복 없는 숫자를 모두 입력하세요!');
    inputFields.forEach(f => f.value = '');
    inputFields[0].focus();
    return;
  }
  const userInput = inputFields.map(f => Number(f.value));
  const resultObj = getResult(userInput);
  printResult(userInput, resultObj);
  attempts--;
  attemptsSpan.textContent = attempts;

  if (resultObj.strike === 3) {
    endGame(true);
    alert('정답입니다! 다시 시작하려면 초기화 하세요');
  } else if (attempts === 0) {
    endGame(false);
    alert(`실패! 정답은 ${answer.join(' ')} 입니다.`);
  }
  inputFields.forEach(f => f.value = '');
  inputFields[0].focus();
}

// 결과 초기화
window.onload = resetGame;
