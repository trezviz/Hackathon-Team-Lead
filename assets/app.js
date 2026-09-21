const $ = (selector) => document.querySelector(selector);
const taskInput = $('#taskInput');
const constraintsInput = $('#constraintsInput');
const fileSearch = $('#fileSearch');
const checkboxes = [...document.querySelectorAll('input[name="check"]')];
const steps = document.querySelectorAll('.step');

let allFiles = [];
let state = { phase: 'draft', planId: null, plan: null, task: '', constraints: '' };

function list(items) {
  return items.map((item) => `<li>${item}</li>`).join('');
}

function setState(phase) {
  state.phase = phase;
  const labels = { draft: 'Черновик', planned: 'План готов', approved: 'Согласовано', completed: 'Завершено' };
  $('#stateLabel').textContent = labels[phase];
  $('#stateLabel').className = `status-pill ${phase === 'approved' ? 'approved' : phase === 'completed' ? 'completed' : ''}`;
  const order = ['draft', 'planned', 'approved', 'completed'];
  const activeIndex = order.indexOf(phase);
  steps.forEach((step, index) => {
    step.classList.toggle('is-active', index === activeIndex);
    step.classList.toggle('is-complete', index < activeIndex);
  });
}

function show(section) {
  $('#emptyState').classList.toggle('hidden', section !== 'empty');
  $('#planContent').classList.toggle('hidden', section !== 'plan');
  $('#approvedContent').classList.toggle('hidden', section !== 'approved');
  $('#reportContent').classList.toggle('hidden', section !== 'report');
}

function showError(message) {
  const banner = $('#errorBanner');
  banner.textContent = message;
  banner.classList.toggle('hidden', !message);
}

function renderProjectMap() {
  $('#projectMap').innerHTML = allFiles
    .map((file) => `<li data-file="${file}">${file}</li>`)
    .join('');
  $('#fileCount').textContent = `${allFiles.length} файлов`;
}

function highlightProjectMap(files) {
  document.querySelectorAll('#projectMap li').forEach((item) => {
    item.classList.toggle('is-relevant', files.includes(item.dataset.file));
  });
}

async function loadFiles() {
  try {
    const res = await fetch('/api/files');
    const data = await res.json();
    allFiles = data.files || [];
    renderProjectMap();
  } catch (err) {
    showError('Не удалось получить список файлов репозитория с сервера. Убедитесь, что запущен server.py.');
  }
}

async function loadHealth() {
  const banner = $('#aiStatusBanner');
  try {
    const res = await fetch('/api/health');
    const data = await res.json();
    if (data.aiConfigured) {
      const providerLabel = data.provider === 'gemini' ? 'Google Gemini' : 'Anthropic Claude';
      banner.textContent = `Подключено к ${providerLabel} (${data.model}) — планы и правки формирует реальная модель.`;
      banner.classList.remove('warning-note');
      banner.classList.add('ok-note');
    } else {
      banner.textContent = 'Ключ ИИ не настроен на сервере. Скопируйте .env.example в .env и задайте ANTHROPIC_API_KEY или GEMINI_API_KEY, чтобы включить реальные ответы ИИ.';
      banner.classList.add('warning-note');
    }
  } catch (err) {
    banner.textContent = 'Сервер недоступен. Запустите: python server.py';
    banner.classList.add('warning-note');
  }
}

async function api(path, body) {
  const res = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body || {}),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || `Ошибка запроса (${res.status})`);
  }
  return data;
}

function setBusy(button, busy, busyLabel) {
  if (busy) {
    button.dataset.originalLabel = button.innerHTML;
    button.innerHTML = busyLabel;
    button.disabled = true;
  } else {
    button.innerHTML = button.dataset.originalLabel || button.innerHTML;
    button.disabled = false;
  }
}

async function generatePlan() {
  const task = taskInput.value.trim();
  const constraints = constraintsInput.value.trim();
  if (!task) {
    $('#validation').textContent = 'Сначала укажите конкретную цель задачи.';
    taskInput.focus();
    return;
  }
  $('#validation').textContent = '';
  showError('');
  const button = $('#planButton');
  setBusy(button, true, 'Claude формирует план…');
  try {
    const { planId, plan } = await api('/api/plan', { task, constraints });
    state.planId = planId;
    state.plan = plan;
    state.task = task;
    state.constraints = constraints || 'Ограничения не указаны — требуется уточнение.';

    $('#goalOutput').textContent = task;
    $('#constraintsOutput').textContent = state.constraints;
    $('#filesOutput').innerHTML = list(plan.relevantFiles || []);
    $('#verificationOutput').textContent = plan.verification || '—';
    $('#changesOutput').innerHTML = (plan.steps || []).map((item) => `<li>${item}</li>`).join('');
    const safety = $('#safetyMessage');
    safety.hidden = !plan.secretsFlag;
    safety.textContent = plan.secretsFlag
      ? 'Ограничение безопасности: агент не должен раскрывать или выводить секреты, токены, пароли и значения .env.'
      : '';
    $('#outputTitle').textContent = 'Короткий план (Claude)';
    highlightProjectMap(plan.relevantFiles || []);
    setState('planned');
    show('plan');
  } catch (err) {
    showError(err.message);
  } finally {
    setBusy(button, false);
  }
}

function approvePlanUI() {
  $('#outputTitle').textContent = 'Согласование и проверки';
  $('#checkValidation').textContent = '';
  const editable = state.plan.editableFiles || [];
  const select = $('#targetFileSelect');
  select.innerHTML = editable.map((f) => `<option value="${f}">${f}</option>`).join('');
  $('#targetFileWrap').hidden = editable.length === 0;
  $('#noEditableHint').hidden = editable.length !== 0;
  setState('approved');
  show('approved');
}

async function approvePlan() {
  showError('');
  const button = $('#approveButton');
  setBusy(button, true, 'Согласование…');
  try {
    await api('/api/approve', { planId: state.planId });
    approvePlanUI();
  } catch (err) {
    showError(err.message);
  } finally {
    setBusy(button, false);
  }
}

async function completeTask() {
  const selectedChecks = checkboxes.filter((check) => check.checked).map((check) => check.value);
  if (!selectedChecks.length) {
    $('#checkValidation').textContent = 'Выберите хотя бы одну подходящую проверку.';
    return;
  }
  $('#checkValidation').textContent = '';
  showError('');
  const button = $('#completeButton');
  setBusy(button, true, 'Применение и проверка…');
  try {
    const editable = state.plan.editableFiles || [];
    const targetFile = editable.length ? $('#targetFileSelect').value : null;

    if (targetFile) {
      await api('/api/apply', { planId: state.planId, targetFile });
    }
    const { results } = await api('/api/checks', { planId: state.planId, checks: selectedChecks });
    const report = await api('/api/report', { planId: state.planId });

    $('#reportFiles').innerHTML = report.changedFiles.length ? list(report.changedFiles) : '<li>Файлы не изменялись</li>';
    $('#checkResults').innerHTML = results
      .map((r) => `<li><span class="pass-dot ${r.passed ? '' : 'fail-dot'}"></span>${r.name}: ${r.detail}</li>`)
      .join('');
    $('#resultOutput').textContent = report.summary;
    $('#riskOutput').textContent = report.risks || 'Существенных рисков не выявлено.';
    $('#reportMark').textContent = report.allChecksPassed ? '✓' : '!';
    $('#reportMark').classList.toggle('mark-warning', !report.allChecksPassed);
    if (report.diff) {
      $('#diffSection').hidden = false;
      $('#diffOutput').textContent = report.diff;
    } else {
      $('#diffSection').hidden = true;
    }
    $('#outputTitle').textContent = 'Итоговый отчёт';
    setState('completed');
    show('report');
  } catch (err) {
    showError(err.message);
  } finally {
    setBusy(button, false);
  }
}

function resetWorkflow() {
  state = { phase: 'draft', planId: null, plan: null, task: '', constraints: '' };
  taskInput.value = '';
  constraintsInput.value = '';
  fileSearch.value = '';
  document.querySelectorAll('#projectMap li').forEach((item) => { item.hidden = false; item.classList.remove('is-relevant'); });
  $('#fileCount').textContent = `${allFiles.length} файлов`;
  $('#validation').textContent = '';
  $('#checkValidation').textContent = '';
  $('#outputTitle').textContent = 'Ожидание задачи';
  showError('');
  setState('draft');
  show('empty');
  taskInput.focus();
}

function searchFiles() {
  const query = fileSearch.value.trim().toLowerCase();
  let visible = 0;
  document.querySelectorAll('#projectMap li').forEach((item) => {
    const match = !query || item.textContent.toLowerCase().includes(query);
    item.hidden = !match;
    if (match) visible += 1;
  });
  $('#fileCount').textContent = `${visible} из ${allFiles.length} файлов`;
}

$('#planButton').addEventListener('click', generatePlan);
$('#approveButton').addEventListener('click', approvePlan);
$('#completeButton').addEventListener('click', completeTask);
$('#newTaskButton').addEventListener('click', resetWorkflow);
$('#resetButton').addEventListener('click', resetWorkflow);
$('#backToPlanButton').addEventListener('click', () => { $('#outputTitle').textContent = 'Короткий план (Claude)'; setState('planned'); show('plan'); });
taskInput.addEventListener('input', () => { $('#validation').textContent = ''; });
fileSearch.addEventListener('input', searchFiles);

loadHealth();
loadFiles();
