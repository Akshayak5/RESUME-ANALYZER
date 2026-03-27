// ── dashboard.js — ResumeIQ ───────────────────────────────────────────────────
let currentUser     = null;
let currentAnalysis = null;
let selectedFile    = null;
let resumeList      = [];

// ── Soft skills that should NOT appear in the Verify Your Skills test grid ────
const SOFT_SKILLS = new Set([
  'problem solving', 'critical thinking', 'teamwork', 'communication',
  'leadership', 'time management', 'adaptability', 'creativity',
  'emotional intelligence', 'interpersonal skills', 'work ethic',
  'attention to detail', 'decision making', 'conflict resolution',
  'active listening', 'collaboration', 'flexibility', 'self motivation',
  'organization', 'multitasking', 'stress management', 'positive attitude',
  'ux design', 'presentation', 'public speaking', 'negotiation',
  'mentoring', 'coaching', 'analytical thinking', 'strategic thinking',
  'customer service', 'research', 'planning', 'networking',
]);

/**
 * Returns true if the skill is a soft/non-testable skill.
 */
function isSoftSkill(skill) {
  const key = skill.toLowerCase().trim().replace(/[-_]/g, ' ');
  if (SOFT_SKILLS.has(key)) return true;
  for (const soft of SOFT_SKILLS) {
    if (key === soft) return true;
  }
  return false;
}

// ── Skill Test Questions ──────────────────────────────────────────────────────
const TEST_QUESTIONS = {
  python: [
    { q:"What does list(range(3)) return?",               opts:["[0,1,2]","[1,2,3]","[0,1,2,3]","range(3)"],              ans:0 },
    { q:"Which keyword creates an anonymous function?",    opts:["def","fun","lambda","arrow"],                             ans:2 },
    { q:"Output of type({})?",                            opts:["class list","class dict","class set","class tuple"],      ans:1 },
    { q:"Which method removes & returns the last item?",  opts:["remove()","pop()","delete()","clear()"],                  ans:1 },
    { q:"What does len('hello') return?",                 opts:["4","5","6","error"],                                      ans:1 },
  ],
  javascript: [
    { q:"Which method adds to end of array?",             opts:["push()","pop()","shift()","append()"],                    ans:0 },
    { q:"What does === check?",                           opts:["Value only","Type only","Value and Type","Reference"],    ans:2 },
    { q:"typeof null returns?",                           opts:["null","undefined","object","string"],                     ans:2 },
    { q:"Block-scoped variable keyword?",                 opts:["var","let","const","function"],                           ans:1 },
    { q:"Array.isArray([]) returns?",                     opts:["false","true","undefined","error"],                       ans:1 },
  ],
  sql: [
    { q:"Filters rows AFTER grouping?",                   opts:["WHERE","HAVING","FILTER","GROUP BY"],                     ans:1 },
    { q:"INNER JOIN returns?",                            opts:["All rows","Matching rows","Left rows","Right rows"],      ans:1 },
    { q:"Counts all rows including NULLs?",               opts:["COUNT(col)","COUNT(*)","SUM(*)","TOTAL(col)"],            ans:1 },
    { q:"What does DISTINCT do?",                         opts:["Sorts rows","Removes duplicates","Filters nulls","Groups rows"], ans:1 },
    { q:"Permanently removes a table?",                   opts:["DELETE","REMOVE","DROP","TRUNCATE"],                      ans:2 },
  ],
  java: [
    { q:"Prevents method overriding?",                    opts:["static","final","private","abstract"],                    ans:1 },
    { q:"Parent class of all Java classes?",              opts:["Base","Root","Object","Class"],                           ans:2 },
    { q:"Maintains insertion order?",                     opts:["HashSet","TreeSet","LinkedList","HashMap"],               ans:2 },
    { q:"Most restrictive access modifier?",              opts:["public","protected","default","private"],                 ans:3 },
    { q:"Size of int in Java?",                           opts:["16 bit","32 bit","64 bit","8 bit"],                       ans:1 },
  ],
  react: [
    { q:"Hook for component state?",                      opts:["useEffect","useRef","useState","useContext"],             ans:2 },
    { q:"What triggers a re-render?",                     opts:["DOM change","State change","Both","Neither"],             ans:1 },
    { q:"JSX stands for?",                                opts:["JavaScript XML","Java Syntax Extension","JS Extra","None"], ans:0 },
    { q:"Runs after every render?",                       opts:["useState","useEffect","useMemo","useCallback"],           ans:1 },
    { q:"React key prop is used for?",                    opts:["Styling","Unique list identification","State","Routing"], ans:1 },
  ],
  docker: [
    { q:"File that defines a Docker image?",              opts:["docker-compose.yml","Dockerfile","config.yml",".dockerignore"], ans:1 },
    { q:"docker ps shows?",                               opts:["Images","Running containers","Networks","Volumes"],      ans:1 },
    { q:"Command to build an image?",                     opts:["docker run","docker build","docker create","docker start"], ans:1 },
    { q:"EXPOSE in Dockerfile does?",                     opts:["Opens firewall","Documents a port","Binds port","Nothing"], ans:1 },
    { q:"Run container interactively?",                   opts:["docker start -i","docker run -it","docker exec","docker attach"], ans:1 },
  ],
  aws: [
    { q:"S3 stands for?",                                 opts:["Simple Storage Service","Server Storage System","Secure S3","None"], ans:0 },
    { q:"Serverless function service?",                   opts:["EC2","RDS","Lambda","ECS"],                               ans:2 },
    { q:"AMI stands for?",                                opts:["Auto Machine Image","Amazon Machine Image","AWS Memory Instance","None"], ans:1 },
    { q:"Managed relational DB service?",                 opts:["DynamoDB","S3","RDS","Redshift"],                         ans:2 },
    { q:"IAM stands for?",                                opts:["Internet Access Management","Identity and Access Management","Internal Auth","None"], ans:1 },
  ],
  mongodb: [
    { q:"What type of database is MongoDB?",              opts:["Relational","Document-based NoSQL","Graph","Key-value"],  ans:1 },
    { q:"MongoDB equivalent of a SQL table?",             opts:["Document","Collection","Schema","Record"],               ans:1 },
    { q:"What does $match do in aggregation?",            opts:["Joins collections","Filters documents","Groups documents","Sorts documents"], ans:1 },
    { q:"Default unique identifier in MongoDB?",          opts:["uuid","_id (ObjectId)","docId","primaryKey"],            ans:1 },
    { q:"What does $lookup do in aggregation?",           opts:["Filters documents","Joins another collection","Sorts results","Creates indexes"], ans:1 },
  ],
  git: [
    { q:"What does git stash do?",                        opts:["Deletes changes","Temporarily shelves uncommitted changes","Commits all changes","Pushes to remote"], ans:1 },
    { q:"What is a pull request?",                        opts:["Download latest code","Propose and review changes before merging","Create a new branch","Reset to previous commit"], ans:1 },
    { q:"What does git rebase do?",                       opts:["Merges with a merge commit","Replays commits on top of another branch","Deletes a branch","Resets working directory"], ans:1 },
    { q:"Difference between merge and rebase?",           opts:["No difference","Merge preserves history; rebase rewrites it linearly","Rebase is for hotfixes only","Merge only works on main"], ans:1 },
    { q:"What does git cherry-pick do?",                  opts:["Picks best branch to merge","Applies a specific commit to another branch","Reverts last commit","Lists all commits"], ans:1 },
  ],
  typescript: [
    { q:"TypeScript is a superset of?",                   opts:["Python","Java","JavaScript","C#"],                        ans:2 },
    { q:"What does the interface keyword define?",         opts:["A class","The shape/contract of an object","A module","A function"], ans:1 },
    { q:"What does strict: true enable in tsconfig?",     opts:["Faster builds","Strict type-checking rules","Auto formatting","Tree shaking"], ans:1 },
    { q:"What is a union type in TypeScript?",            opts:["Combines two interfaces","A type that can be one of several types","A generic constraint","An intersection type"], ans:1 },
    { q:"What is an enum in TypeScript?",                 opts:["A loop construct","A set of named constant values","A type alias","An error handler"], ans:1 },
  ],
  nodejs: [
    { q:"Node.js is built on which engine?",              opts:["SpiderMonkey","V8","Chakra","Nitro"],                     ans:1 },
    { q:"What is the Node.js event loop?",                opts:["A for loop","Handles async callbacks in a single thread","A built-in HTTP server","A database pool"], ans:1 },
    { q:"What does require() do?",                        opts:["Validates input","Imports a module into the current file","Starts the server","Declares a global variable"], ans:1 },
    { q:"What is npm?",                                   opts:["A Node module pattern","Node Package Manager","A networking protocol module","A process manager"], ans:1 },
    { q:"What is Express.js?",                            opts:["A database driver","A minimal web framework for Node.js","A testing library","A process manager"], ans:1 },
  ],
  css: [
    { q:"What does the CSS box model consist of?",        opts:["margin, border, padding, content","margin, font, color, display","padding, flex, grid, border","content, shadow, outline, margin"], ans:0 },
    { q:"Flexbox vs CSS Grid?",                           opts:["No difference","Flex is 1D layout; Grid is 2D layout","Grid is 1D; Flex is 2D","Flex only works on block elements"], ans:1 },
    { q:"What does CSS specificity determine?",           opts:["Stylesheet load order","Which CSS rule applies when multiple rules match","Animation speed","z-index stacking order"], ans:1 },
    { q:"What is a CSS pseudo-class?",                    opts:["A fake class for testing","Styles an element in a specific state","A browser prefix","A deprecated CSS feature"], ans:1 },
    { q:"What does position: absolute do?",               opts:["Fixes element to viewport","Positions relative to nearest positioned ancestor","Removes element from page","Aligns in flex container"], ans:1 },
  ],
  figma: [
    { q:"Figma is primarily used for?",                   opts:["Backend development","UI/UX design and prototyping","Database management","Video editing"], ans:1 },
    { q:"What are Figma Components?",                     opts:["HTML elements","Reusable design elements that can be instanced","CSS classes","JavaScript modules"], ans:1 },
    { q:"What does Auto Layout do in Figma?",             opts:["Generates front-end code","Auto-resizes frames based on content","Syncs to GitHub","Runs animations"], ans:1 },
    { q:"What is a Figma Prototype?",                     opts:["A coded web app","An interactive simulation linking frames together","A backend mock server","A color theme file"], ans:1 },
    { q:"What are Figma Variants?",                       opts:["Different saved file versions","Multiple states of a component grouped in one set","Color theme overrides","Plugin configuration files"], ans:1 },
  ],
  ".net": [
    { q:"CLR stands for?",                                opts:["Common Language Runtime","Core Library Runtime","Compiled Logic Runtime","Command Line Runtime"],            ans:0 },
    { q:"What is ASP.NET Core?",                          opts:["A database ORM","A cross-platform web framework by Microsoft","A UI component library","A .NET compiler"],   ans:1 },
    { q:"LINQ stands for?",                               opts:["Language Integrated Query","Linked Index Query","List Interface Node Query","Language Input Query"],         ans:0 },
    { q:"What is dependency injection in .NET?",          opts:["A security vulnerability","Providing dependencies from outside a class","An import statement","A data migration tool"], ans:1 },
    { q:"Entity Framework Core is?",                      opts:["A testing framework","An ORM for database access in .NET","A UI component library","A CLI build tool"],     ans:1 },
  ],
  default: [
    { q:"What is the most important skill employers look for?", opts:["Technical knowledge","Communication skills","Luck","Age"], ans:1 },
    { q:"What should you do first when facing a problem at work?", opts:["Ignore it","Blame others","Analyze the problem","Quit"], ans:2 },
    { q:"Which of the following is a strength?", opts:["Procrastination","Time management","Laziness","Avoiding responsibility"], ans:1 },
    { q:"What is the best way to handle criticism?", opts:["Get angry","Ignore it","Learn from it","Argue"], ans:2 },
    { q:"What does teamwork mean?", opts:["Working alone","Competing with others","Collaborating with others","Avoiding responsibility"], ans:2 },
    { q:"What should you do before an interview?", opts:["Sleep","Research the company","Watch movies","Ignore preparation"], ans:1 },
    { q:"What is a good weakness to mention?", opts:["I never make mistakes","I am perfect","I overwork sometimes","I don’t care about work"], ans:2 },
    { q:"What shows leadership?", opts:["Giving orders only","Avoiding responsibility","Helping and guiding others","Working alone"], ans:2 },
    { q:"What is the best way to manage time?", opts:["Do everything at once","Prioritize tasks","Delay work","Ignore deadlines"], ans:1 },
    { q:"Why do employers ask 'Tell me about yourself'?", opts:["To waste time","To know your background","To confuse you","To test memory"], ans:1 },
    { q:"What is professionalism?", opts:["Being rude","Being punctual and respectful","Ignoring work","Being late"], ans:1 },
    { q:"What should you do if you don't know an answer?", opts:["Panic","Lie","Admit and try logically","Stay silent"], ans:2 },
    { q:"What is a positive attitude?", opts:["Complaining always","Staying optimistic","Blaming others","Avoiding work"], ans:1 },
    { q:"What is the purpose of a resume?", opts:["Decoration","Show your skills and experience","Impress friends","Waste paper"], ans:1 },
    { q:"When working under pressure, what is the best approach?", opts:["Rush and finish quickly","Stay calm and prioritize tasks","Avoid responsibility","Blame teammates"], ans:1 },
    { q:"What is the main purpose of teamwork in an organization?", opts:["Divide work randomly","Improve efficiency through collaboration","Reduce responsibility","Compete internally"], ans:1 },
    { q:"Which action shows strong problem-solving skills?", opts:["Ignoring issues","Analyzing root causes","Complaining","Waiting for others"], ans:1 },
    { q:"How should you respond to a difficult coworker?", opts:["Argue with them","Ignore them completely","Communicate professionally","Report immediately"], ans:2 },
    { q:"What is the best way to handle failure?", opts:["Give up","Blame others","Learn and improve","Ignore it"], ans:2 },
    { q:"Why is adaptability important in a job?", opts:["Avoid change","Handle changing situations effectively","Ignore new tasks","Resist learning"], ans:1 },
    { q:"What does accountability mean in a workplace?", opts:["Blaming others","Taking responsibility for actions","Avoiding tasks","Ignoring mistakes"], ans:1 },
    { q:"Which quality is most important for leadership?", opts:["Authority","Communication and guidance","Control","Independence"], ans:1 },
    { q:"What should you do if you disagree with your manager?", opts:["Argue loudly","Stay silent always","Express respectfully with reasons","Ignore instructions"], ans:2 },
    { q:"What is the best way to improve productivity?", opts:["Multitask everything","Prioritize and focus","Delay tasks","Avoid planning"], ans:1 },
    { q:"What is emotional intelligence?", opts:["Ignoring emotions","Understanding and managing emotions","Being emotional","Avoiding people"], ans:1 },
    { q:"Why is time management important?", opts:["To delay work","To complete tasks efficiently","To avoid tasks","To reduce workload"], ans:1 },
    { q:"What is the key to effective communication?", opts:["Talking more","Listening actively","Interrupting","Avoiding discussion"], ans:1 },
    { q:"How should you set goals?", opts:["Randomly","Clearly and realistically","Avoid goals","Set impossible targets"], ans:1 },
    { q:"What is a proactive approach?", opts:["Waiting for instructions","Taking initiative","Avoiding work","Delaying action"], ans:1 },
    { q:"What does conflict resolution require?", opts:["Aggression","Avoidance","Understanding and compromise","Ignoring issues"], ans:2 },
    { q:"What is the purpose of feedback?", opts:["Criticize others","Improve performance","Ignore suggestions","Avoid discussion"], ans:1 },
    { q:"What is the best way to build trust at work?", opts:["Being inconsistent","Being honest and reliable","Avoiding people","Ignoring deadlines"], ans:1 },
    { q:"What is decision-making based on?", opts:["Guessing","Analyzing information","Ignoring data","Following others blindly"], ans:1 },
    { q:"What is adaptability?", opts:["Refusing change","Accepting and adjusting to change","Ignoring new ideas","Being stubborn"], ans:1 }
  ],
};

/**
 * Resolves the best matching question set for any skill string.
 * Handles: exact match, case-insensitive, partial word match.
 */
function resolveTestQuestions(skill) {
  const key = skill.toLowerCase().trim();

  // 1. Exact key match
  if (TEST_QUESTIONS[key]) return TEST_QUESTIONS[key];

  // 2. Case-insensitive / partial key match
  for (const k of Object.keys(TEST_QUESTIONS)) {
    if (k === 'default') continue;
    if (key.includes(k) || k.includes(key)) return TEST_QUESTIONS[k];
  }

  // 3. Word-level match — any meaningful word in the skill matches a key
  const words = key.split(/[\s\-_.\/]+/).filter(w => w.length >= 3);
  for (const word of words) {
    for (const k of Object.keys(TEST_QUESTIONS)) {
      if (k === 'default') continue;
      if (k.includes(word) || word.includes(k)) return TEST_QUESTIONS[k];
    }
  }

  // 4. Fallback to generic tech questions
  return TEST_QUESTIONS.default;
}

let testState = { skill:'', questions:[], answers:[], current:0, resumeId:'' };

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  currentUser = session.require();
  if (!currentUser) return;

  document.getElementById('userName').textContent   = currentUser.name;
  document.getElementById('userAvatar').textContent = currentUser.name[0].toUpperCase();
  if (currentUser.role === 'employer') document.getElementById('empBtn').style.display = 'inline-flex';

  const zone = document.getElementById('uploadZone');
  zone.addEventListener('dragover',  e => { e.preventDefault(); zone.classList.add('drag'); });
  zone.addEventListener('dragleave', ()  => zone.classList.remove('drag'));
  zone.addEventListener('drop', e => {
    e.preventDefault(); zone.classList.remove('drag');
    if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
  });
});

// ── Navigation ────────────────────────────────────────────────────────────────
function showSection(name) {
  document.querySelectorAll('.dash-section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  const section = document.getElementById('sec-' + name);
  if (section) section.classList.add('active');

  const navItem = document.querySelector(`.nav-item[data-section="${name}"]`);
  if (navItem) navItem.classList.add('active');

  if (name === "upload") {
    selectedFile = null;
    const fi  = document.getElementById("fileInput");
    const uz  = document.getElementById("uploadZone");
    const fp  = document.getElementById("filePreview");
    const as_ = document.getElementById("analyzingState");
    const ap  = document.getElementById("analyzeProgress");
    if (fi)  fi.value = "";
    if (uz)  uz.style.display = "block";
    if (fp)  fp.style.display = "none";
    if (as_) as_.style.display = "none";
    if (ap)  ap.style.width = "0%";
    ["step1","step2","step3","step4"].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.classList.remove("active", "done");
    });
  }

  if (name === "history")  loadHistory();
  if (name === "trending") loadTrending();
  if (name === "crud")     loadCRUD();
}

function logout() { session.clear(); window.location.href = '/'; }

// ── File Handling ─────────────────────────────────────────────────────────────
function fileSelected(input) { if (input.files[0]) setFile(input.files[0]); }

function setFile(file) {
  selectedFile = file;
  document.getElementById('uploadZone').style.display  = 'none';
  document.getElementById('filePreview').style.display = 'block';
  document.getElementById('fileName').textContent      = file.name;
  document.getElementById('fileSize').textContent      = (file.size / 1024).toFixed(1) + ' KB';
}

function clearFile() {
  selectedFile = null;
  document.getElementById('fileInput').value           = '';
  document.getElementById('uploadZone').style.display  = 'block';
  document.getElementById('filePreview').style.display = 'none';
}

// ── Analyze ───────────────────────────────────────────────────────────────────
async function analyzeResume() {
  if (!selectedFile) return;
  document.getElementById('filePreview').style.display    = 'none';
  document.getElementById('analyzingState').style.display = 'block';

  const steps    = ['step1','step2','step3','step4'];
  const progress = document.getElementById('analyzeProgress');

  for (let i = 0; i < steps.length; i++) {
    if (i > 0) document.getElementById(steps[i-1]).classList.remove('active');
    document.getElementById(steps[i]).classList.add('active');
    progress.style.width = ((i+1) * 22) + '%';
    await delay(700);
  }

  try {
    const data = await api.analyze(selectedFile, currentUser.user_id);
    progress.style.width = '100%';
    steps.forEach(s => {
      document.getElementById(s).classList.remove('active');
      document.getElementById(s).classList.add('done');
    });
    await delay(400);

    currentAnalysis = data;
    renderAnalysis(data);
    document.getElementById('analyzingState').style.display = 'none';
    document.getElementById('analysisBadge').style.display  = 'inline';
    showSection('analysis');
    showToast('Analysis complete! Score: ' + safeScore(data.analysis.score), 'success');
    updateSideStats(data);
  } catch(err) {
    showToast(err.message || 'Analysis failed', 'error');
    document.getElementById('analyzingState').style.display = 'none';
    document.getElementById('filePreview').style.display    = 'block';
    progress.style.width = '0%';
    steps.forEach(s => document.getElementById(s).classList.remove('active','done'));
  }
}

const delay = ms => new Promise(r => setTimeout(r, ms));

function safeScore(raw) {
  if (typeof raw === 'number') return Math.round(raw);
  if (typeof raw === 'object' && raw !== null)
    return Math.round(Number(raw.total ?? raw.$numberInt ?? raw.$numberDouble ?? Object.values(raw)[0]) || 0);
  return Math.round(Number(raw) || 0);
}

function updateSideStats(data) {
  const score = safeScore(data.analysis.score);
  document.getElementById('sideStats').style.display = 'block';
  document.getElementById('ssSc').textContent = score + '/100';
  document.getElementById('ssSk').textContent = (data.analysis.skills || []).length;
  document.getElementById('ssEx').textContent = (data.analysis.experience_years || 0) + ' yrs';
  document.getElementById('ssSc').style.color = scoreColor(score);
}

// ── Render Analysis ───────────────────────────────────────────────────────────
function renderAnalysis(data) {
  const { candidate, analysis } = data;
  const score = safeScore(analysis.score);
  const exp   = analysis.experience_years || 0;

  document.getElementById('resumeFilename').textContent = candidate.filename || 'Analyzed Resume';
  document.getElementById('cName').textContent  = candidate.name  || '—';
  document.getElementById('cEmail').textContent = candidate.email || '—';
  document.getElementById('cPhone').textContent = candidate.phone || '—';
  document.getElementById('cExp').textContent   = exp > 0 ? `${exp} year${exp !== 1 ? 's' : ''}` : 'Fresher';

  const color = scoreColor(score);
  const arc   = document.getElementById('scoreArc');
  arc.style.stroke = color;
  setTimeout(() => { arc.style.strokeDashoffset = 314 - (314 * score / 100); }, 100);
  document.getElementById('scoreNum').textContent   = score;
  document.getElementById('scoreNum').style.color   = color;
  document.getElementById('scoreLabel').textContent = scoreLabel(score);
  document.getElementById('scoreDesc').textContent  = getScoreDesc(score);
  document.getElementById('expBadge').innerHTML     = exp > 0
    ? `<span class="badge badge-cyan">${exp} yr${exp !== 1?'s':''} experience</span>`
    : `<span class="badge badge-muted">Fresher / No experience</span>`;

  const skillsEl = document.getElementById('skillsFound');
  skillsEl.innerHTML = '';
  (analysis.skills || []).forEach(skill => {
    const v = (analysis.verified_skills || []).includes(skill);
    skillsEl.innerHTML += `<span class="skill-tag ${v?'verified':''}">${v?'✓ ':''}${skill}</span>`;
  });
  document.getElementById('skillCount').textContent = (analysis.skills || []).length;

  const catEl = document.getElementById('categorized');
  catEl.innerHTML = '';
  if (analysis.categorized) {
    Object.entries(analysis.categorized).forEach(([cat, skills]) => {
      if (!skills.length) return;
      catEl.innerHTML += `
        <div class="cat-group">
          <div class="cat-name">${cat}</div>
          <div class="cat-skills">${skills.map(s=>`<span class="skill-tag" style="font-size:11px">${s}</span>`).join('')}</div>
        </div>`;
    });
  }

  const missingEl = document.getElementById('skillsMissing');
  missingEl.innerHTML = '';
  (analysis.missing_skills || []).forEach(s => {
    missingEl.innerHTML += `<span class="skill-tag missing">+ ${s}</span>`;
  });
  document.getElementById('missingCount').textContent = (analysis.missing_skills || []).length;

  const jobsEl = document.getElementById('jobsGrid');
  jobsEl.innerHTML = '';
  (analysis.recommended_jobs || []).forEach(job => {
    const match = job.match_percent || 0;
    const mc    = match >= 80 ? 'var(--green)' : match >= 60 ? 'var(--yellow)' : 'var(--t2)';
    jobsEl.innerHTML += `
      <div class="job-card">
        <div class="job-icon">${job.icon || '💼'}</div>
        <div class="job-title">${job.title}</div>
        <div class="job-match">Match: <span style="color:${mc};font-weight:700">${match}%</span></div>
        <div class="progress" style="margin-top:8px"><div class="progress-fill pf-accent" style="width:${match}%"></div></div>
        ${job.matched_skills ? `<div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:4px">${job.matched_skills.map(s=>`<span class="skill-tag" style="font-size:10px">${s}</span>`).join('')}</div>` : ''}
      </div>`;
  });
  if (!(analysis.recommended_jobs || []).length) {
    jobsEl.innerHTML = `<div style="color:var(--t3);font-size:13px;padding:20px 0">No strong matches yet. Add more skills to unlock job matches.</div>`;
  }

  // ── Verify grid — only show testable (non-soft) skills ──
  const verifyEl      = document.getElementById('verifyGrid');
  verifyEl.innerHTML  = '';
  const allSkills      = analysis.skills || [];
  const verifiedSkills = analysis.verified_skills || [];

  // Filter out soft/interpersonal skills — keep only tech & domain skills
  const testableSkills = allSkills.filter(skill => !isSoftSkill(skill));

  if (!testableSkills.length) {
    verifyEl.innerHTML = `
      <div style="color:var(--t3);font-size:13px;padding:20px 0;text-align:center">
        No testable technical skills found. Add technical skills to your resume to unlock verification.
      </div>`;
  } else {
    testableSkills.forEach(skill => {
      const v         = verifiedSkills.includes(skill);
      const safeSkill = skill.replace(/'/g, "\\'");
      verifyEl.innerHTML += `
        <div class="verify-item ${v?'done':''}">
          <span>${v?'✅':'🎯'}</span>
          <span style="flex:1">${skill}</span>
          ${v
            ? '<span class="badge badge-green">Verified</span>'
            : `<button class="btn btn-outline btn-sm" onclick="startTest('${safeSkill}','${data.resume_id}')">Take Test</button>`}
        </div>`;
    });
  }
}

function getScoreDesc(s) {
  if (s >= 85) return 'Outstanding resume. You are highly competitive!';
  if (s >= 70) return 'Strong resume. A few additions could push you to the top.';
  if (s >= 55) return 'Decent resume. Add more skills and diversify categories.';
  if (s >= 35) return 'Room for improvement. Focus on technical skills.';
  return 'Needs significant work. Add relevant skills to your resume.';
}

// ── CRUD ──────────────────────────────────────────────────────────────────────
async function loadCRUD() {
  const el = document.getElementById('crudContent');
  el.innerHTML = `<div style="display:flex;align-items:center;gap:12px;padding:40px;color:var(--t2)"><div class="spinner"></div>&nbsp;Loading...</div>`;
  try {
    const data = await api.history(currentUser.user_id);
    resumeList  = data.history || [];
    renderCRUDTable();
  } catch(err) {
    el.innerHTML = `<div style="color:var(--red);padding:20px">Error: ${err.message}</div>`;
  }
}

function renderCRUDTable() {
  const el = document.getElementById('crudContent');
  if (!resumeList.length) {
    el.innerHTML = `
      <div class="empty-crud">
        <div style="font-size:48px;margin-bottom:16px">📂</div>
        <h3 style="font-family:var(--display);margin-bottom:8px">No Resumes Found</h3>
        <p style="color:var(--t2);font-size:13px">Upload and analyze a resume to manage it here.</p>
        <button class="btn btn-primary" style="margin-top:20px" onclick="showSection('upload')">
          📄 Upload Resume
        </button>
      </div>`;
    return;
  }

  el.innerHTML = `
    <div class="crud-toolbar">
      <input type="text" class="form-input" id="crudSearch"
        placeholder="Search by name, file, or skill..."
        oninput="filterCRUD(this.value)" style="max-width:340px">
      <div style="display:flex;align-items:center;gap:8px">
        <span class="badge badge-muted">${resumeList.length} resume${resumeList.length!==1?'s':''}</span>
        <button class="btn btn-primary btn-sm" onclick="showSection('upload')">+ New</button>
      </div>
    </div>
    <div class="crud-table-wrap">
      <table class="table">
        <thead>
          <tr><th>File</th><th>Candidate</th><th>Score</th><th>Skills</th><th>Exp</th><th>Date</th><th>Actions</th></tr>
        </thead>
        <tbody id="crudBody">${renderCRUDRows(resumeList)}</tbody>
      </table>
    </div>`;
}

function renderCRUDRows(list) {
  if (!list.length) return `<tr><td colspan="7" style="text-align:center;color:var(--t3);padding:32px">No results</td></tr>`;
  return list.map(item => {
    const score  = safeScore(item.analysis?.score);
    const color  = scoreColor(score);
    const skills = item.analysis?.skills || [];
    const name   = item.candidate?.name || '—';
    const exp    = item.analysis?.experience_years || 0;
    const date   = new Date(item.uploaded_at).toLocaleDateString();
    const id     = item._id;
    return `<tr>
      <td>
        <div style="display:flex;align-items:center;gap:8px">
          <span>📄</span>
          <span style="font-size:12px;max-width:130px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--t2)">${item.filename||'resume'}</span>
        </div>
      </td>
      <td style="font-weight:600">${name}</td>
      <td><span class="crud-score" style="color:${color}">${score}</span></td>
      <td>
        <div style="display:flex;gap:4px;flex-wrap:wrap">
          ${skills.slice(0,3).map(s=>`<span class="skill-tag" style="font-size:10px;padding:3px 8px">${s}</span>`).join('')}
          ${skills.length>3?`<span class="badge badge-muted" style="font-size:10px">+${skills.length-3}</span>`:''}
        </div>
      </td>
      <td style="color:var(--t2)">${exp > 0 ? exp + ' yrs' : 'Fresher'}</td>
      <td style="color:var(--t3);font-size:12px">${date}</td>
      <td>
        <div style="display:flex;gap:6px">
          <button class="btn btn-ghost btn-sm" onclick="crudView('${id}')" title="View">👁</button>
          <button class="btn btn-outline btn-sm" onclick="crudEdit('${id}')" title="Edit">✏️</button>
          <button class="btn btn-red btn-sm" onclick="crudDelete('${id}','${name.replace(/'/g,"\\'")}')">🗑</button>
        </div>
      </td>
    </tr>`;
  }).join('');
}

function filterCRUD(q) {
  const query    = q.toLowerCase();
  const filtered = query
    ? resumeList.filter(r =>
        (r.filename||'').toLowerCase().includes(query) ||
        (r.candidate?.name||'').toLowerCase().includes(query) ||
        (r.analysis?.skills||[]).some(s=>s.toLowerCase().includes(query)))
    : resumeList;
  const body = document.getElementById('crudBody');
  if (body) body.innerHTML = renderCRUDRows(filtered);
}

async function crudView(id) {
  try {
    const data = await api.getResume(id);
    currentAnalysis = data;
    renderAnalysis(data);
    showSection('analysis');
    showToast('Resume loaded', 'info');
  } catch(err) { showToast(err.message, 'error'); }
}

function crudEdit(id) {
  const item = resumeList.find(r => r._id === id);
  if (!item) return;
  openModal(`
    <h3 style="font-family:var(--display);margin-bottom:4px">✏️ Edit Resume</h3>
    <p style="font-size:12px;color:var(--t2);margin-bottom:24px">${item.filename||'Resume'}</p>
    <div class="form-group">
      <label class="form-label">Candidate Name</label>
      <input type="text" class="form-input" id="editName" value="${item.candidate?.name||''}" placeholder="Full name">
    </div>
    <div class="form-group">
      <label class="form-label">Experience Years</label>
      <input type="number" class="form-input" id="editExp" value="${item.analysis?.experience_years||0}" min="0" max="50">
    </div>
    <div class="form-group">
      <label class="form-label">Add Skills <span style="color:var(--t3)">(comma separated)</span></label>
      <input type="text" class="form-input" id="editSkills" placeholder="e.g. React, Docker, AWS">
    </div>
    <div style="display:flex;gap:10px;margin-top:24px">
      <button class="btn btn-primary" onclick="crudSaveEdit('${id}')">💾 Save</button>
      <button class="btn btn-ghost" onclick="closeModal()">Cancel</button>
    </div>`);
}

async function crudSaveEdit(id) {
  const newName   = document.getElementById('editName').value.trim();
  const newExp    = parseInt(document.getElementById('editExp').value) || 0;
  const newSkills = document.getElementById('editSkills').value.split(',').map(s=>s.trim()).filter(Boolean);
  try {
    await fetch(`/api/resume/${id}`, {
      method:'PATCH', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({candidate_name:newName, experience_years:newExp, additional_skills:newSkills}),
    });
  } catch(e) {}
  const item = resumeList.find(r=>r._id===id);
  if (item) {
    if (newName)     item.candidate = {...(item.candidate||{}), name:newName};
    if (newExp >= 0) item.analysis.experience_years = newExp;
    if (newSkills.length) item.analysis.skills = [...new Set([...(item.analysis.skills||[]),...newSkills])];
  }
  closeModal(); renderCRUDTable();
  showToast('Resume updated ✓', 'success');
}

function crudDelete(id, name) {
  openModal(`
    <div style="text-align:center;padding:8px 0">
      <div style="font-size:48px;margin-bottom:16px">🗑️</div>
      <h3 style="font-family:var(--display);margin-bottom:8px">Delete Resume?</h3>
      <p style="color:var(--t2);font-size:13px;margin-bottom:8px">
        Permanently delete <strong style="color:var(--t1)">${name}</strong>'s record.
      </p>
      <p style="color:var(--red);font-size:12px;margin-bottom:24px">This cannot be undone.</p>
      <div style="display:flex;gap:10px;justify-content:center">
        <button class="btn btn-red" onclick="confirmDelete('${id}')">🗑 Yes, Delete</button>
        <button class="btn btn-ghost" onclick="closeModal()">Cancel</button>
      </div>
    </div>`);
}

async function confirmDelete(id) {
  closeModal();
  try {
    const res = await fetch(`/api/resume/${id}`, {method:'DELETE'});
    if (!res.ok) {
      const err = await res.json().catch(()=>({error:'Delete failed'}));
      showToast(err.error || 'Delete failed', 'error');
      return;
    }
    resumeList = resumeList.filter(r => r._id !== id);
    renderCRUDTable();
    showToast('Resume deleted ✓', 'success');
  } catch(err) {
    showToast('Error: ' + err.message, 'error');
  }
}

// ── Modal ─────────────────────────────────────────────────────────────────────
function openModal(html) {
  let overlay = document.getElementById('genericModal');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'genericModal'; overlay.className = 'modal-overlay';
    overlay.onclick = e => { if (e.target===overlay) closeModal(); };
    overlay.innerHTML = `<div class="modal"><button class="modal-close" onclick="closeModal()">✕</button><div id="genericModalBody"></div></div>`;
    document.body.appendChild(overlay);
  }
  document.getElementById('genericModalBody').innerHTML = html;
  overlay.style.display = 'flex';
}

function closeModal() {
  const m = document.getElementById('genericModal');
  if (m) m.style.display = 'none';
}

// ── History ───────────────────────────────────────────────────────────────────
async function loadHistory() {
  const el = document.getElementById('historyContent');
  try {
    const data  = await api.history(currentUser.user_id);
    const items = data.history || [];
    if (!items.length) {
      el.innerHTML = `<div style="text-align:center;padding:60px;color:var(--t3)"><div style="font-size:40px;margin-bottom:16px">📭</div><p>No resumes analyzed yet.</p></div>`;
      return;
    }
    el.innerHTML = `<div class="history-grid">${items.map(item => {
      const score  = safeScore(item.analysis?.score);
      const color  = scoreColor(score);
      const skills = item.analysis?.skills || [];
      const exp    = item.analysis?.experience_years || 0;
      return `
        <div class="history-card" onclick="loadHistoryItem('${item._id}')">
          <span class="hist-icon">📄</span>
          <div class="hist-info">
            <div class="hist-name">${item.filename||'Resume'}</div>
            <div class="hist-meta">${item.candidate?.name||'—'} · ${new Date(item.uploaded_at).toLocaleDateString()} · ${exp > 0 ? exp + ' yrs exp' : 'Fresher'}</div>
            <div class="hist-skills">
              ${skills.slice(0,5).map(s=>`<span class="skill-tag" style="font-size:11px">${s}</span>`).join('')}
              ${skills.length>5?`<span class="badge badge-muted">+${skills.length-5}</span>`:''}
            </div>
          </div>
          <div class="hist-score">
            <div class="hist-score-num" style="color:${color}">${score}</div>
            <div class="hist-score-lbl">${scoreLabel(score)}</div>
          </div>
        </div>`;
    }).join('')}</div>`;
  } catch(err) {
    el.innerHTML = `<div style="color:var(--red);padding:20px">${err.message}</div>`;
  }
}

async function loadHistoryItem(id) {
  try {
    const data = await api.getResume(id);
    currentAnalysis = data;
    renderAnalysis(data);
    showSection('analysis');
  } catch(err) { showToast(err.message, 'error'); }
}

// ── Trending ──────────────────────────────────────────────────────────────────
async function loadTrending() {
  const el = document.getElementById('trendingContent');
  try {
    const data  = await api.trending();
    const items = data.trending || [];
    if (!items.length) {
      el.innerHTML = `<div style="text-align:center;padding:60px;color:var(--t3)"><p>No data yet. Analyze some resumes first.</p></div>`;
      return;
    }
    const max = items[0]?.count || 1;
    el.innerHTML = `<div class="trending-grid">${items.map((item,i)=>`
      <div class="trend-item">
        <div class="trend-rank ${i<3?'top':''}">#${i+1}</div>
        <div class="trend-skill">${item.skill}</div>
        <div class="trend-bar-wrap">
          <div class="progress"><div class="progress-fill pf-accent" style="width:${(item.count/max)*100}%"></div></div>
        </div>
        <div class="trend-count">${item.count} resumes</div>
      </div>`).join('')}</div>`;
  } catch(err) {
    el.innerHTML = `<div style="color:var(--red);padding:20px">${err.message}</div>`;
  }
}

// ── Skill Tests ───────────────────────────────────────────────────────────────
async function startTest(skill, resumeId) {
  document.getElementById('testTitle').textContent    = skill + ' Skill Test';
  document.getElementById('testSubtitle').textContent = 'Generating questions with AI...';
  document.getElementById('testBody').innerHTML = `
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 20px;gap:20px">
      <div class="spinner" style="width:36px;height:36px;border-width:3px"></div>
      <div style="font-size:14px;color:var(--t2)">Groq is crafting <strong style="color:var(--accent)">${skill}</strong> questions for you...</div>
      <div style="font-size:12px;color:var(--t3)">This takes just a second ⚡</div>
    </div>`;
  document.getElementById('testModal').style.display = 'flex';

  try {
    const res = await fetch('/api/resume/generate-questions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify({ skill, count: 5 }),
    });
    
    if (!res.ok) throw new Error('Generation failed');
    const data = await res.json();
    
    // Map Groq format { correct: "A" } → { ans: 0 }
    const letterToIndex = { A: 0, B: 1, C: 2, D: 3 };
    const questions = (data.questions || []).map(q => ({
      q:    q.question,
      opts: q.options.map(o => o.replace(/^[A-D]\.\s*/, '')),
      ans:  letterToIndex[q.correct] ?? 0,
    }));
    const source = 'groq';

    testState = { skill, resumeId, questions, answers: new Array(questions.length).fill(-1), current: 0 };
    document.getElementById('testSubtitle').textContent =
      questions.length + ' questions · ~' + questions.length + ' min' +
      (source === 'groq' ? ' · ✨ AI Generated' : '');
    renderTestQuestion();

  } catch(err) {
    const questions = resolveTestQuestions(skill);
    testState = { skill, resumeId, questions, answers: new Array(questions.length).fill(-1), current: 0 };
    document.getElementById('testSubtitle').textContent = questions.length + ' questions · ~' + questions.length + ' min';
    renderTestQuestion();
  }
}

function authHeaders() {
  const token = localStorage.getItem('token') || sessionStorage.getItem('token') ||
                (typeof session !== 'undefined' && session.getToken && session.getToken()) || '';
  return token ? { 'Authorization': 'Bearer ' + token } : {};
}

function renderTestQuestion() {
  const { questions, current, answers } = testState;
  const q = questions[current];
  document.getElementById('testBody').innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
      <span style="font-size:12px;color:var(--t2)">Question ${current+1} of ${questions.length}</span>
      <div class="progress" style="width:150px">
        <div class="progress-fill pf-accent" style="width:${((current+1)/questions.length)*100}%"></div>
      </div>
    </div>
    <div class="test-q-text">${q.q}</div>
    <div class="test-options" style="margin-top:16px">
      ${q.opts.map((opt,i)=>`
        <button class="test-opt ${answers[current]===i?'selected':''}"
          onclick="selectAnswer(${i})" type="button">
          <span class="opt-letter">${['A','B','C','D'][i]}</span>
          <span class="opt-text">${opt}</span>
        </button>`).join('')}
    </div>
    <div style="display:flex;justify-content:space-between;margin-top:28px">
      <button class="btn btn-ghost btn-sm" onclick="closeTest()" type="button">Cancel</button>
      <button class="btn btn-primary" type="button" id="testNext"
        onclick="${current<questions.length-1?'nextQuestion()':'submitTest()'}"
        ${answers[current]===-1?'disabled':''}>
        ${current<questions.length-1?'Next →':'🎯 Submit'}
      </button>
    </div>`;
}

function selectAnswer(idx) {
  testState.answers[testState.current] = idx;
  document.querySelectorAll('.test-opt').forEach((o,i)=>o.classList.toggle('selected',i===idx));
  const btn = document.getElementById('testNext');
  if (btn) btn.disabled = false;
}

function nextQuestion() { testState.current++; renderTestQuestion(); }

async function submitTest() {
  const { questions, answers, skill, resumeId } = testState;
  let correct = 0;
  answers.forEach((a,i) => { if (a===questions[i].ans) correct++; });
  const passed = correct/questions.length >= 0.6;
  const color  = passed ? 'var(--green)' : 'var(--red)';

  document.getElementById('testBody').innerHTML = `
    <div class="test-result">
      <div class="test-result-score" style="color:${color}">${correct}/${questions.length}</div>
      <div style="font-size:18px;font-weight:700;color:${color};margin-bottom:6px">${passed?'🎉 Passed!':'❌ Not Passed'}</div>
      <div class="test-result-sub">${passed?skill+' verified and added to your profile!':'Score below 60%. Study more and try again.'}</div>
      <div style="margin-top:20px;display:flex;flex-direction:column;gap:8px;text-align:left">
        ${questions.map((q,i)=>`
          <div style="padding:12px;background:var(--bg2);border-radius:var(--r);border:1px solid ${answers[i]===q.ans?'rgba(0,217,163,.3)':'rgba(255,71,87,.3)'}">
            <div style="font-size:12px;color:var(--t2);margin-bottom:4px">${q.q}</div>
            <div style="font-size:13px;color:${answers[i]===q.ans?'var(--green)':'var(--red)'}">
              ${answers[i]===q.ans?'✓':'✗'} ${q.opts[answers[i]]??'No answer'}
            </div>
            ${answers[i]!==q.ans?`<div style="font-size:12px;color:var(--green);margin-top:2px">✓ Correct: ${q.opts[q.ans]}</div>`:''}
          </div>`).join('')}
      </div>
      <button class="btn btn-primary" style="margin-top:20px;width:100%" onclick="closeTest()">Done</button>
    </div>`;

  try {
    await api.verifySkill({ user_id:currentUser.user_id, skill, score:correct, total:questions.length, resume_id:resumeId });
    if (passed) showToast(skill+' verified! ✅', 'success');
  } catch(e) {}
}

function closeTest() {
  document.getElementById('testModal').style.display = 'none';
  if (currentAnalysis) api.getResume(currentAnalysis.resume_id).then(d=>renderAnalysis(d)).catch(()=>{});
}

// ── AI Resume Enhancer ────────────────────────────────────────────────────────
async function enhanceResume() {
  if (!currentAnalysis) {
    showToast('Please analyze a resume first', 'error');
    return;
  }

  const btn    = document.getElementById('enhanceBtn');
  const result = document.getElementById('enhanceResult');

  btn.disabled    = true;
  btn.textContent = '⏳ Enhancing...';
  result.style.display = 'block';

  const messages = [
    'Reading your resume...',
    'Checking spelling & grammar...',
    'Rephrasing weak bullet points...',
    'Generating professional summary...',
    'Finalising enhancements...',
  ];
  let msgIdx = 0;
  result.innerHTML = `
    <div class="enhance-loading">
      <div class="enhance-spinner"></div>
      <div class="enhance-progress-text" id="enhLoadMsg">${messages[0]}</div>
    </div>`;

  const msgTimer = setInterval(() => {
    msgIdx = (msgIdx + 1) % messages.length;
    const el = document.getElementById('enhLoadMsg');
    if (el) el.textContent = messages[msgIdx];
  }, 1400);

  try {
    const resumeId = currentAnalysis.resume_id || currentAnalysis._id;
    if (!resumeId) {
      showToast('Resume ID not found. Please re-analyze.', 'error');
      btn.textContent = '✨ Enhance My Resume';
      btn.disabled = false;
      return;
    }
    const res = await fetch(`/api/resume/enhance/${resumeId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });

    clearInterval(msgTimer);

    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: 'Enhancement failed' }));
      throw new Error(err.error || 'Enhancement failed');
    }

    const data = await res.json();
    renderEnhancements(data.enhancements);
    btn.textContent = '🔄 Re-Enhance';
    btn.disabled    = false;
    showToast('Resume enhanced successfully! ✨', 'success');

  } catch(err) {
    clearInterval(msgTimer);
    result.innerHTML    = `<div style="color:var(--red);font-size:13px;padding:16px">Error: ${err.message}</div>`;
    btn.textContent     = '✨ Enhance My Resume';
    btn.disabled        = false;
    showToast(err.message, 'error');
  }
}

function renderEnhancements(e) {
  const result        = document.getElementById('enhanceResult');
  const spellingCount = (e.spelling_fixes     || []).length;
  const bulletCount   = (e.rephrased_bullets  || []).length;
  const weakCount     = (e.weak_phrases       || []).length;
  const tipCount      = (e.overall_tips       || []).length;

  result.innerHTML = `
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px">
      ${badge('🔤', spellingCount, 'Spelling Fixes',  'var(--red)')}
      ${badge('✏️', bulletCount,  'Bullets Improved', 'var(--accent)')}
      ${badge('💪', weakCount,    'Weak Phrases',      'var(--yellow)')}
      ${badge('💡', tipCount,     'Tips',              'var(--green)')}
    </div>
    <div class="enhance-tabs">
      <button class="etab active" onclick="eTab(this,'ep-enhanced')">📄 Enhanced Resume</button>
      <button class="etab" onclick="eTab(this,'ep-spelling')">🔤 Spelling (${spellingCount})</button>
      <button class="etab" onclick="eTab(this,'ep-bullets')">✏️ Bullets (${bulletCount})</button>
      <button class="etab" onclick="eTab(this,'ep-weak')">💪 Weak Phrases (${weakCount})</button>
      <button class="etab" onclick="eTab(this,'ep-tips')">💡 Tips</button>
    </div>
    <div class="enhance-panel active" id="ep-enhanced">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px">
        <span style="font-size:12px;color:var(--t2)">Full enhanced resume — copy or download as Word file</span>
        <div style="display:flex;gap:8px">
          <button class="copy-btn" onclick="copyEnhanced()">📋 Copy</button>
          <button class="copy-btn" onclick="downloadEnhanced()" style="background:var(--accent-dim);border-color:var(--accent);color:var(--accent)">⬇️ Download DOCX</button>
        </div>
      </div>
      <div id="enhancedStructured">${renderEnhancedSections(e)}</div>
      <div class="enhanced-text-box" id="enhancedTextBox" style="display:none">${escHtml(e.enhanced_text || '')}</div>
    </div>
    <div class="enhance-panel" id="ep-spelling">
      ${(e.spelling_fixes || []).length ? (e.spelling_fixes.map(f => `
        <div class="fix-row">
          <div><div class="fix-original">${escHtml(f.original)}</div><div class="fix-context" style="color:var(--t3)">"${escHtml(f.context||'')}"</div></div>
          <div class="fix-arrow">→</div>
          <div class="fix-improved">${escHtml(f.corrected)}</div>
        </div>`).join('')) : '<div style="color:var(--green);padding:20px;font-size:13px">✅ No spelling errors found!</div>'}
    </div>
    <div class="enhance-panel" id="ep-bullets">
      ${(e.rephrased_bullets || []).length ? (e.rephrased_bullets.map(f => `
        <div class="fix-row" style="grid-template-columns:1fr auto 1fr">
          <div><div style="font-size:11px;color:var(--t3);margin-bottom:4px">ORIGINAL</div><div class="fix-original" style="text-decoration:none;color:var(--t2);font-size:12px">${escHtml(f.original)}</div></div>
          <div class="fix-arrow">→</div>
          <div><div style="font-size:11px;color:var(--t3);margin-bottom:4px">IMPROVED</div><div class="fix-improved" style="font-size:12px">${escHtml(f.improved)}</div></div>
        </div>`).join('')) : '<div style="color:var(--green);padding:20px;font-size:13px">✅ Your bullet points look strong already!</div>'}
    </div>
    <div class="enhance-panel" id="ep-weak">
      ${(e.weak_phrases || []).length ? (e.weak_phrases.map(f => `
        <div class="fix-row">
          <div><div class="fix-original">${escHtml(f.phrase)}</div></div>
          <div class="fix-arrow">→</div>
          <div><div class="fix-improved">${escHtml(f.suggestion)}</div><div class="fix-reason">${escHtml(f.reason||'')}</div></div>
        </div>`).join('')) : '<div style="color:var(--green);padding:20px;font-size:13px">✅ No weak phrases detected!</div>'}
    </div>
    <div class="enhance-panel" id="ep-tips">
      ${(e.overall_tips || []).map(t => `<div class="tip-item">${escHtml(t)}</div>`).join('')}
    </div>`;
}

function badge(icon, count, label, color) {
  return `<div style="display:flex;align-items:center;gap:6px;padding:8px 14px;background:var(--bg3);border-radius:var(--r);border:1px solid var(--border2)">
    <span>${icon}</span>
    <span style="font-weight:700;color:${color};font-family:var(--font)">${count}</span>
    <span style="font-size:12px;color:var(--t2)">${label}</span>
  </div>`;
}

function eTab(el, panelId) {
  document.querySelectorAll('.etab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.enhance-panel').forEach(p => p.classList.remove('active'));
  el.classList.add('active');
  const panel = document.getElementById(panelId);
  if (panel) panel.classList.add('active');
}

function copyEnhanced() {
  const box = document.getElementById('enhancedTextBox');
  if (!box) return;
  navigator.clipboard.writeText(box.textContent).then(() => {
    showToast('Enhanced resume copied to clipboard! 📋', 'success');
  }).catch(() => {
    const range = document.createRange();
    range.selectNode(box);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    document.execCommand('copy');
    showToast('Copied!', 'success');
  });
}

function downloadEnhanced() {
  const resumeId = currentAnalysis?.resume_id || currentAnalysis?._id;
  if (!resumeId) { showToast('No resume found. Please analyze first.', 'error'); return; }
  showToast('Preparing download...', 'info');
  const a = document.createElement('a');
  a.href     = `/api/resume/download-enhanced/${resumeId}`;
  a.download = 'enhanced_resume.docx';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

const SENTENCE_SECTIONS = new Set(["professional summary","summary","objective","profile"]);
const SKILL_SECTIONS    = new Set(["programming languages","tools","tools and technologies","soft skills","skills","technical skills","languages","interests","hobbies","hobby","achievements & awards","awards"]);

function renderEnhancedSections(e) {
  const sections = e.enhanced_sections || [];
  if (sections.length) {
    return sections.map(sec => {
      const heading = sec.heading || '';
      const hl      = heading.toLowerCase();
      const items   = sec.items || [];
      let bodyHtml  = '';
      if (SENTENCE_SECTIONS.has(hl) || hl.includes('summary') || hl.includes('objective') || hl.includes('profile')) {
        bodyHtml = `<div class="enhanced-plain-line" style="line-height:1.7">${escHtml(items.join(' '))}</div>`;
      } else {
        bodyHtml = items.map(i => {
          const clean = i.replace(/\*\*/g, '');
          if (clean.startsWith('>>>')) {
            return `<div style="padding-left:18px;font-size:13px;color:var(--t2);line-height:1.6;margin-bottom:4px">${escHtml(clean.slice(3).trim())}</div>`;
          }
          return `<div class="enhanced-item" style="margin-bottom:2px">
            <span class="enhanced-bullet">▸</span>
            <span>${escHtml(clean)}</span>
          </div>`;
        }).join('');
      }
      return `
      <div class="enhanced-section">
        <div class="enhanced-section-heading">${escHtml(heading)}</div>
        <div class="enhanced-section-body">${bodyHtml}</div>
      </div>`;
    }).join('');
  }
  const text = e.enhanced_text || '';
  if (!text) return '<div style="color:var(--t3);padding:20px">No enhanced content available.</div>';
  return text.split('\n').filter(l => l.trim()).map(line => {
    const isHeading = line.length < 40 && line === line.toUpperCase() && line.trim().length > 2;
    const isBullet  = line.trim().startsWith('-') || line.trim().startsWith('•');
    if (isHeading) {
      return `<div class="enhanced-section-heading">${escHtml(line.trim())}</div>`;
    } else if (isBullet) {
      return `<div class="enhanced-item"><span class="enhanced-bullet">▸</span><span>${escHtml(line.replace(/^[-•]\s*/,'').trim())}</span></div>`;
    } else {
      return `<div class="enhanced-plain-line">${escHtml(line.trim())}</div>`;
    }
  }).join('');
}

function escHtml(str) {
  return String(str || '')
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}

// ── Career Roadmap ────────────────────────────────────────────────────────────
function quickJob(title) {
  document.getElementById('jobInput').value = title;
  generateRoadmap();
}

async function generateRoadmap() {
  const jobInput = document.getElementById('jobInput');
  const jobTitle = (jobInput.value || '').trim();
  if (!jobTitle) { showToast('Enter a job title first', 'error'); jobInput.focus(); return; }

  const btn    = document.getElementById('roadmapBtn');
  const result = document.getElementById('roadmapResult');

  btn.disabled    = true;
  btn.textContent = '⏳ Analysing...';
  result.style.display = 'block';

  const steps = [
    '🔍 Analysing job requirements...',
    '🧠 Mapping your current skills...',
    '📊 Calculating skill gaps...',
    '🗺️ Building your learning path...',
    '🎯 Finalising your roadmap...',
  ];

  result.innerHTML = `
    <div class="roadmap-loading">
      <div class="roadmap-spinner"></div>
      <div class="roadmap-loading-steps">
        ${steps.map((s,i) => `<div class="roadmap-loading-step" id="rlStep${i}">${s}</div>`).join('')}
      </div>
    </div>`;

  let stepIdx = 0;
  const stepTimer = setInterval(() => {
    const el = document.getElementById(`rlStep${stepIdx}`);
    if (el) el.classList.add('visible');
    stepIdx++;
    if (stepIdx >= steps.length) clearInterval(stepTimer);
  }, 900);

  try {
    const payload = { job_title: jobTitle };
    if (currentAnalysis?.resume_id) payload.resume_id = currentAnalysis.resume_id;

    const res = await fetch('/api/resume/roadmap', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    clearInterval(stepTimer);

    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: 'Roadmap generation failed' }));
      throw new Error(err.error || 'Failed');
    }

    const data = await res.json();
    renderRoadmap(data.roadmap);
    btn.textContent = '🔄 Regenerate';
    btn.disabled    = false;
    showToast(`Roadmap for "${jobTitle}" ready! 🗺️`, 'success');

  } catch(err) {
    clearInterval(stepTimer);
    result.innerHTML = `<div style="color:var(--red);padding:24px;font-size:13px">Error: ${err.message}</div>`;
    btn.textContent  = '🗺️ Generate Roadmap';
    btn.disabled     = false;
    showToast(err.message, 'error');
  }
}

// ── Job Board URL mapper ──────────────────────────────────────────────────────
function getJobBoardUrl(boardName, jobTitle) {
  const encoded = encodeURIComponent(jobTitle || '');
  const slug    = (jobTitle || '').toLowerCase().replace(/\s+/g, '-');
  const urls = {
    'linkedin':       `https://www.linkedin.com/jobs/search/?keywords=${encoded}`,
    'indeed':         `https://www.indeed.com/jobs?q=${encoded}`,
    'glassdoor':      `https://www.glassdoor.com/Job/jobs.htm?sc.keyword=${encoded}`,
    'naukri':         `https://www.naukri.com/${slug}-jobs`,
    'internshala':    `https://internshala.com/jobs/${slug}-jobs`,
    'monster':        `https://www.monster.com/jobs/search?q=${encoded}`,
    'wellfound':      `https://wellfound.com/jobs?q=${encoded}`,
    'angel.co':       `https://wellfound.com/jobs?q=${encoded}`,
    'angellist':      `https://wellfound.com/jobs?q=${encoded}`,
    'dice':           `https://www.dice.com/jobs?q=${encoded}`,
    'ziprecruiter':   `https://www.ziprecruiter.com/candidate/search?search=${encoded}`,
    'remoteok':       `https://remoteok.com/remote-${slug}-jobs`,
    'weworkremotely': `https://weworkremotely.com/remote-jobs/search?term=${encoded}`,
  };
  const key   = boardName.toLowerCase().trim();
  const match = Object.entries(urls).find(([k]) => key.includes(k));
  return match
    ? match[1]
    : `https://www.google.com/search?q=${encoded}+jobs+${encodeURIComponent(boardName)}`;
}

function renderRoadmap(r) {
  const result     = document.getElementById('roadmapResult');
  const match      = Math.min(Math.max(r.match_score || 0, 0), 100);
  const matchColor = match >= 70 ? 'var(--green)' : match >= 40 ? 'var(--yellow)' : 'var(--red)';
  const missingSkills = r.skills_missing   || [];
  const haveSkills    = r.skills_have      || [];
  const phases        = r.phases           || [];
  const projects      = r.projects         || [];
  const certs         = r.certifications   || [];
  const interviews    = r.interview_topics || [];
  const jobBoards     = r.job_boards       || [];

  result.innerHTML = `
    <div class="roadmap-summary-bar">
      <div class="rsb-item">
        <div class="rsb-val" style="color:${matchColor}">${match}%</div>
        <div class="rsb-lbl">Current Match</div>
        <div class="match-bar-track" style="margin-top:8px">
          <div class="match-bar-fill" id="matchBarFill" style="width:0%;background:${matchColor}"></div>
        </div>
      </div>
      <div class="rsb-item"><div class="rsb-val" style="color:var(--accent)">${missingSkills.length}</div><div class="rsb-lbl">Skills to Learn</div></div>
      <div class="rsb-item"><div class="rsb-val" style="color:var(--green)">${haveSkills.length}</div><div class="rsb-lbl">Skills You Have</div></div>
      <div class="rsb-item"><div class="rsb-val" style="color:var(--t1)">${escHtml(r.time_to_ready || '—')}</div><div class="rsb-lbl">Est. Time to Ready</div></div>
      <div class="rsb-item"><div class="rsb-val" style="color:var(--t1);font-size:14px">${escHtml(r.salary_range || '—')}</div><div class="rsb-lbl">Salary Range</div></div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div class="roadmap-banner">
        <div style="flex:1">
          <div class="section-title" style="margin-bottom:8px">📋 Your Assessment for <span style="color:var(--accent)">${escHtml(r.job_title)}</span></div>
          <p style="font-size:13px;color:var(--t2);line-height:1.7">${escHtml(r.overview || '')}</p>
        </div>
      </div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div class="section-title" style="margin-bottom:16px">⚡ Skills Gap Analysis</div>
      <div class="gap-grid">
        <div>
          <div class="gap-col-title" style="color:var(--green)">✅ You Already Have (${haveSkills.length})</div>
          <div style="display:flex;flex-wrap:wrap;gap:6px">
            ${haveSkills.length
              ? haveSkills.map(s => `<span class="skill-tag skill-have">${escHtml(s)}</span>`).join('')
              : '<span style="color:var(--t3);font-size:12px">No matching skills yet</span>'}
          </div>
        </div>
        <div>
          <div class="gap-col-title" style="color:var(--red)">🎯 Skills to Learn (${missingSkills.length})</div>
          ${missingSkills.map(s => `
            <div class="skill-missing-tag priority-${s.priority || 'nice'}">
              <div style="flex:1">
                <div style="display:flex;align-items:center;gap:8px">
                  <span style="font-weight:700;font-size:13px">${escHtml(s.skill)}</span>
                  <span class="priority-badge pb-${s.priority || 'nice'}">${s.priority || 'nice'}</span>
                  ${s.time_weeks ? `<span style="font-size:10px;color:var(--t3)">${s.time_weeks}w</span>` : ''}
                </div>
                <div class="missing-detail">${escHtml(s.why || '')}</div>
                ${s.learn_at ? `<div class="missing-resource">📚 ${escHtml(s.learn_at)}</div>` : ''}
              </div>
            </div>`).join('')}
        </div>
      </div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div class="section-title" style="margin-bottom:20px">🗺️ Learning Roadmap — Phase by Phase</div>
      <div class="phase-timeline">
        ${phases.map((p, i) => `
          <div class="phase-item">
            <div class="phase-dot"></div>
            <div class="phase-card">
              <div class="phase-header" onclick="togglePhase(${i})">
                <div class="phase-num">${p.phase || i+1}</div>
                <div class="phase-title-text">${escHtml(p.title || '')}</div>
                <div class="phase-meta">
                  <span class="badge badge-muted">⏱ ${escHtml(p.duration || '')}</span>
                  <span class="badge badge-muted">${(p.tasks||[]).length} tasks</span>
                  <span id="phaseChevron${i}" style="color:var(--t3);transition:transform .2s">▼</span>
                </div>
              </div>
              <div class="phase-body ${i === 0 ? 'open' : ''}" id="phaseBody${i}">
                ${p.goal ? `<div class="phase-goal">🎯 Goal: ${escHtml(p.goal)}</div>` : ''}
                ${(p.tasks || []).map(t => `
                  <div class="task-row">
                    <div class="task-type-icon">${taskIcon(t.type)}</div>
                    <div style="flex:1">
                      <div class="task-text">${escHtml(t.task || '')}</div>
                      ${t.resource ? `<div class="task-resource">📎 ${escHtml(t.resource)}</div>` : ''}
                    </div>
                    ${t.hours ? `<div class="task-hours">~${t.hours}h</div>` : ''}
                  </div>`).join('')}
              </div>
            </div>
          </div>`).join('')}
      </div>
    </div>

    ${projects.length ? `
    <div class="card" style="margin-bottom:16px">
      <div class="section-title" style="margin-bottom:16px">🛠️ Portfolio Projects to Build</div>
      <div class="projects-grid">
        ${projects.map(p => `
          <div class="project-card">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:6px">
              <div class="project-title">${escHtml(p.title || '')}</div>
              <span class="diff-badge diff-${p.difficulty || 'beginner'}">${p.difficulty || 'beginner'}</span>
            </div>
            <div class="project-desc">${escHtml(p.description || '')}</div>
            <div style="display:flex;flex-wrap:wrap;gap:4px">
              ${(p.skills_practiced || []).map(s => `<span class="skill-tag" style="font-size:10px;padding:3px 8px">${escHtml(s)}</span>`).join('')}
            </div>
          </div>`).join('')}
      </div>
    </div>` : ''}

    ${certs.length ? `
    <div class="card" style="margin-bottom:16px">
      <div class="section-title" style="margin-bottom:16px">🏆 Recommended Certifications</div>
      <div class="cert-grid">
        ${certs.map(c => `
          <div class="cert-card">
            <div class="cert-name">${escHtml(c.name || '')}</div>
            <div class="cert-meta">
              <div>🏢 ${escHtml(c.provider || '')}</div>
              <div>📈 Relevance: <span style="color:var(--accent)">${escHtml(c.relevance || '')}</span></div>
              ${c.cost       ? `<div>💰 ${escHtml(c.cost)}</div>`       : ''}
              ${c.time_weeks ? `<div>⏱ ~${c.time_weeks} weeks</div>`    : ''}
            </div>
          </div>`).join('')}
      </div>
    </div>` : ''}

    ${interviews.length ? `
    <div class="card" style="margin-bottom:16px">
      <div class="section-title" style="margin-bottom:12px">🎤 Key Interview Topics to Prepare</div>
      <div class="interview-grid">
        ${interviews.map(t => `<div class="interview-chip">💬 ${escHtml(t)}</div>`).join('')}
      </div>
    </div>` : ''}

    ${jobBoards.length ? `
    <div class="card">
      <div class="section-title" style="margin-bottom:12px">🔍 Where to Apply</div>
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        ${jobBoards.map(j => {
          const href = getJobBoardUrl(j, r.job_title);
          return `<a href="${href}" target="_blank" rel="noopener noreferrer" style="text-decoration:none">
            <span class="badge badge-muted"
              style="font-size:13px;padding:8px 16px;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px"
              onmouseover="this.style.background='var(--bg3)';this.style.borderColor='var(--accent)'"
              onmouseout="this.style.background='';this.style.borderColor=''">
              🌐 ${escHtml(j)} ↗
            </span>
          </a>`;
        }).join('')}
      </div>
    </div>` : ''}
  `;

  setTimeout(() => {
    const bar = document.getElementById('matchBarFill');
    if (bar) bar.style.width = match + '%';
  }, 200);

  updateChevrons();
}

function togglePhase(i) {
  const body    = document.getElementById(`phaseBody${i}`);
  const chevron = document.getElementById(`phaseChevron${i}`);
  if (!body) return;
  const isOpen = body.classList.toggle('open');
  if (chevron) chevron.style.transform = isOpen ? 'rotate(180deg)' : '';
}

function updateChevrons() {
  document.querySelectorAll('[id^="phaseChevron"]').forEach((el, i) => {
    const body = document.getElementById(`phaseBody${i}`);
    el.style.transform = body?.classList.contains('open') ? 'rotate(180deg)' : '';
  });
}

function taskIcon(type) {
  const icons = { course:'📚', project:'🛠️', reading:'📖', practice:'💻' };
  return icons[type] || '📌';
}