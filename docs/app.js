// Airstreams Training Flashcards
// Multi-Module Support
// Airstreams Renewables - Tehachapi, CA

let currentModule = null;
let currentIndex = 0;
let studiedCount = 0;
let isFlipped = false;
let autoFlipMode = false;
let flashcards = [];
let cards = [];

// Load modules on page load
document.addEventListener('DOMContentLoaded', async function() {
    await loadModules();
    setupEventListeners();
});

// Load available modules from modules.json
async function loadModules() {
    try {
        const response = await fetch('modules.json');
        const data = await response.json();

        const moduleList = document.getElementById('moduleList');
        moduleList.innerHTML = '';

        // Group modules by source
        data.sources.forEach(source => {
            const sourceSection = createSourceSection(source);
            moduleList.appendChild(sourceSection);
        });

        const totalModules = data.sources.reduce((sum, s) => sum + s.moduleCount, 0);
        console.log(`✅ Loaded ${data.sources.length} training sources with ${totalModules} modules`);
    } catch (error) {
        console.error('Error loading modules:', error);
        document.getElementById('moduleList').innerHTML =
            '<p class="loading" style="color: red;">Error loading modules. Check console for details.</p>';
    }
}

// Create a source section with its modules
function createSourceSection(source) {
    const section = document.createElement('div');
    section.className = 'source-section';

    const header = document.createElement('div');
    header.className = 'source-header';
    header.innerHTML = `
        <div class="source-info">
            <h2>${source.title}</h2>
            <p>${source.description}</p>
            <div class="source-meta">
                <span class="source-stats">${source.moduleCount} modules • ${source.totalCards} flashcards</span>
                <a href="${source.slidesDownload}" class="slides-download-main" download>📥 Download All Slides</a>
            </div>
        </div>
    `;

    const modulesContainer = document.createElement('div');
    modulesContainer.className = 'module-grid';

    source.modules.forEach(module => {
        const card = createModuleCard(module);
        modulesContainer.appendChild(card);
    });

    section.appendChild(header);
    section.appendChild(modulesContainer);

    return section;
}

// Create a module selection card
function createModuleCard(module) {
    const card = document.createElement('div');
    card.className = 'module-card' + (module.enabled ? '' : ' disabled');

    card.innerHTML = `
        <h3>${module.title}</h3>
        <p>${module.description}</p>
        <div class="module-meta">
            <span class="module-card-count">${module.cardCount} cards</span>
            ${module.status ? `<span class="module-status">${module.status}</span>` : ''}
        </div>
    `;

    if (module.enabled) {
        card.onclick = () => selectModule(module);
    } else {
        card.onclick = () => alert('This module is not ready yet. Add your training video and flashcards!');
    }

    return card;
}

// Select a module and load its flashcards
async function selectModule(module) {
    currentModule = module;

    // Show loading
    document.getElementById('moduleTitle').textContent = 'Loading...';
    document.getElementById('moduleDescription').textContent = module.title;

    // Hide module selection, show study screen
    document.getElementById('moduleSelect').style.display = 'none';
    document.getElementById('studyScreen').style.display = 'block';

    try {
        // Dynamically load the module's flashcards
        await loadFlashcards(module.flashcardsFile);

        // Update UI
        document.getElementById('moduleTitle').textContent = module.title;
        document.getElementById('moduleDescription').textContent = module.description;
        document.getElementById('total').textContent = flashcards.length;

        console.log(`✅ Loaded module: ${module.title} (${flashcards.length} cards)`);
    } catch (error) {
        console.error('Error loading flashcards:', error);
        alert('Error loading flashcards for this module. Check console for details.');
        backToModules();
    }
}

// Dynamically load flashcards from a module file
async function loadFlashcards(filename) {
    // Create a script element to load the flashcards file
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = filename;
        script.onload = () => {
            // flashcards variable should now be defined by the loaded script
            if (typeof flashcards !== 'undefined' && flashcards.length > 0) {
                cards = [...flashcards]; // Copy to working array
                resolve();
            } else {
                reject(new Error('Flashcards not loaded or empty'));
            }
        };
        script.onerror = () => reject(new Error(`Failed to load ${filename}`));
        document.body.appendChild(script);
    });
}

// Back to module selection
function backToModules() {
    document.getElementById('studyScreen').style.display = 'none';
    document.getElementById('moduleSelect').style.display = 'block';

    // Reset study state
    currentIndex = 0;
    studiedCount = 0;
    isFlipped = false;
    document.getElementById('startBtn').style.display = 'block';
    document.getElementById('flipBtn').style.display = 'none';
    document.getElementById('navButtons').style.display = 'none';

    // Remove previously loaded flashcards script
    const scripts = document.querySelectorAll('script[src*="flashcards-"]');
    scripts.forEach(script => script.remove());
}

// Update UI elements
function updateStats() {
    document.getElementById('current').textContent = currentIndex + 1;
    document.getElementById('total').textContent = cards.length;
    document.getElementById('studied').textContent = studiedCount;
}

function loadCard() {
    if (cards.length === 0) {
        document.getElementById('question').textContent = "No flashcards available!";
        document.getElementById('answer').textContent = "Please check the module configuration.";
        return;
    }

    const card = cards[currentIndex];
    document.getElementById('question').textContent = card.question;
    document.getElementById('answer').textContent = card.answer;

    // Reset flip state
    const flashcard = document.getElementById('flashcard');
    flashcard.classList.remove('flipped');
    isFlipped = false;

    // Update button text
    document.getElementById('flipBtn').textContent = 'Show Answer';

    updateStats();
}

function startStudying() {
    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('flipBtn').style.display = 'block';
    document.getElementById('navButtons').style.display = 'flex';

    currentIndex = 0;
    studiedCount = 0;
    loadCard();
}

function flipCard() {
    const flashcard = document.getElementById('flashcard');
    isFlipped = !isFlipped;

    if (isFlipped) {
        flashcard.classList.add('flipped');
        document.getElementById('flipBtn').textContent = 'Show Question';
        if (studiedCount < currentIndex + 1) {
            studiedCount = currentIndex + 1;
        }
    } else {
        flashcard.classList.remove('flipped');
        document.getElementById('flipBtn').textContent = 'Show Answer';
    }

    updateStats();
}

function nextCard() {
    if (currentIndex < cards.length - 1) {
        currentIndex++;
        loadCard();

        // Auto-flip if enabled
        if (autoFlipMode) {
            setTimeout(() => {
                if (!isFlipped) flipCard();
            }, 2000);
        }
    } else {
        alert('🎉 You\'ve completed this module! Great job!\n\nClick "Back to Modules" to study another topic or "Shuffle" to review again.');
    }
}

function previousCard() {
    if (currentIndex > 0) {
        currentIndex--;
        loadCard();

        // Auto-flip if enabled
        if (autoFlipMode) {
            setTimeout(() => {
                if (!isFlipped) flipCard();
            }, 2000);
        }
    }
}

function shuffleCards() {
    // Fisher-Yates shuffle algorithm
    for (let i = cards.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [cards[i], cards[j]] = [cards[j], cards[i]];
    }

    // Reset to beginning
    currentIndex = 0;
    studiedCount = 0;
    loadCard();

    alert('🔀 Cards shuffled! Starting from the beginning.');
}

function toggleAutoFlip() {
    autoFlipMode = document.getElementById('autoFlip').checked;

    if (autoFlipMode) {
        alert('✅ Auto-flip enabled!\n\nCards will automatically show the answer after 2 seconds when you navigate.');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Allow clicking on the card to flip
    const flashcard = document.getElementById('flashcard');
    flashcard.addEventListener('click', function() {
        if (document.getElementById('flipBtn').style.display !== 'none') {
            flipCard();
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (document.getElementById('studyScreen').style.display === 'none') return;
        if (document.getElementById('flipBtn').style.display === 'none') return;

        switch(e.key) {
            case ' ':
            case 'Enter':
                e.preventDefault();
                flipCard();
                break;
            case 'ArrowRight':
            case 'n':
                e.preventDefault();
                nextCard();
                break;
            case 'ArrowLeft':
            case 'p':
                e.preventDefault();
                previousCard();
                break;
            case 's':
                e.preventDefault();
                shuffleCards();
                break;
            case 'Escape':
                e.preventDefault();
                backToModules();
                break;
        }
    });

    console.log('Keyboard shortcuts:');
    console.log('  Space/Enter: Flip card');
    console.log('  Arrow Right / N: Next card');
    console.log('  Arrow Left / P: Previous card');
    console.log('  S: Shuffle');
    console.log('  Escape: Back to modules');
}
