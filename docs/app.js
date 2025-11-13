// OSHA Flashcards Web App
// Airstreams Renewables Training - Tehachapi, CA

let currentIndex = 0;
let studiedCount = 0;
let isFlipped = false;
let autoFlipMode = false;
let cards = [...flashcards]; // Copy of flashcards array

// Update UI elements
function updateStats() {
    document.getElementById('current').textContent = currentIndex + 1;
    document.getElementById('total').textContent = cards.length;
    document.getElementById('studied').textContent = studiedCount;
}

function loadCard() {
    if (cards.length === 0) {
        document.getElementById('question').textContent = "No flashcards available!";
        document.getElementById('answer').textContent = "Please check the flashcards.js file.";
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
        alert('🎉 You\'ve reached the end! Great job studying!\n\nClick "Shuffle" to review again or go back to review specific cards.');
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

// Allow clicking on the card to flip
document.addEventListener('DOMContentLoaded', function() {
    const flashcard = document.getElementById('flashcard');
    flashcard.addEventListener('click', function() {
        if (document.getElementById('flipBtn').style.display !== 'none') {
            flipCard();
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
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
        }
    });

    console.log(`✅ OSHA Flashcards loaded: ${flashcards.length} cards`);
    console.log('Keyboard shortcuts:');
    console.log('  Space/Enter: Flip card');
    console.log('  Arrow Right / N: Next card');
    console.log('  Arrow Left / P: Previous card');
    console.log('  S: Shuffle');
});
