const taskInput = document.querySelector('#taskInput');
const planButton = document.querySelector('#planButton');
const approveButton = document.querySelector('#approveButton');
const completeButton = document.querySelector('#completeButton');
const newTaskButton = document.querySelector('#newTaskButton');
const resetButton = document.querySelector('#resetButton');
const backToPlanButton = document.querySelector('#backToPlanButton');
const validation = document.querySelector('#validation');
const stateLabel = document.querySelector('#stateLabel');
const outputTitle = document.querySelector('#outputTitle');
const emptyState = document.querySelector('#emptyState');
const planContent = document.querySelector('#planContent');
const approvedContent = document.querySelector('#approvedContent');
const reportContent = document.querySelector('#reportContent');
const steps = document.querySelectorAll('.step');

let workflow = { state: 'draft', task: '' };

function filesFor(task) {
  const lower = task.toLowerCase();
  if (lower.includes('readme')) return ['README.md', 'AGENTS.md'];
  if (lower.includes('test')) return ['relevant source file', 'relevant test file'];
  return ['relevant project file', 'AGENTS.md'];
}

function setState(state) {
  workflow.state = state;
  const titles = { draft: 'Draft', planned: 'Plan ready', approved: 'Approved', completed: 'Completed' };
  stateLabel.textContent = titles[state];
  stateLabel.className = `status-pill ${state === 'approved' ? 'approved' : state === 'completed' ? 'completed' : ''}`;
  const order = ['draft', 'planned', 'approved', 'completed'];
  const activeIndex = order.indexOf(state);
  steps.forEach((step, index) => {
    step.classList.toggle('is-active', index === activeIndex);
    step.classList.toggle('is-complete', index < activeIndex);
  });
}

function show(section) {
  emptyState.classList.toggle('hidden', section !== 'empty');
  planContent.classList.toggle('hidden', section !== 'plan');
  approvedContent.classList.toggle('hidden', section !== 'approved');
  reportContent.classList.toggle('hidden', section !== 'report');
}

function generatePlan() {
  const task = taskInput.value.trim();
  if (!task) {
    validation.textContent = 'Describe a small technical task before generating a plan.';
    taskInput.focus();
    return;
  }
  validation.textContent = '';
  workflow.task = task;
  const files = filesFor(task);
  document.querySelector('#goalOutput').textContent = task;
  document.querySelector('#filesOutput').innerHTML = files.map(file => `<li>${file}</li>`).join('');
  document.querySelector('#verificationOutput').textContent = 'Review the changed-file scope and run the narrowest applicable check.';
  document.querySelector('#changesOutput').textContent = `Inspect the relevant context, then make the smallest approved change needed to: ${task}`;
  document.querySelector('#reportFiles').innerHTML = files.slice(0, 1).map(file => `<li>${file}</li>`).join('');
  document.querySelector('#resultOutput').textContent = `The approved change for “${task}” is shown as completed within this local demo.`;
  const sensitive = /\.env|secret|password|token|credential|api key/i.test(task);
  const safety = document.querySelector('#safetyMessage');
  safety.hidden = !sensitive;
  safety.textContent = sensitive ? 'Safety notice: real agent work must never reveal credentials, secrets, or .env values.' : '';
  outputTitle.textContent = 'Proposed plan';
  setState('planned');
  show('plan');
}

function approvePlan() {
  outputTitle.textContent = 'Approval recorded';
  setState('approved');
  show('approved');
}

function completeTask() {
  outputTitle.textContent = 'Final report';
  setState('completed');
  show('report');
}

function resetWorkflow() {
  workflow = { state: 'draft', task: '' };
  validation.textContent = '';
  taskInput.value = '';
  outputTitle.textContent = 'Waiting for task';
  setState('draft');
  show('empty');
  taskInput.focus();
}

planButton.addEventListener('click', generatePlan);
approveButton.addEventListener('click', approvePlan);
completeButton.addEventListener('click', completeTask);
newTaskButton.addEventListener('click', resetWorkflow);
resetButton.addEventListener('click', resetWorkflow);
backToPlanButton.addEventListener('click', () => { outputTitle.textContent = 'Proposed plan'; setState('planned'); show('plan'); });
taskInput.addEventListener('input', () => { validation.textContent = ''; });
