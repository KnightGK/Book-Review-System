const cards = document.querySelectorAll('.card');

let lockBoard = false;
let FlippedCard = false;
let firstCard, secondCard;


function flipCard() {
  if (lockBoard) return;

  this.classList.add('flip');

  if(!FlippedCard)  {
    // First click
    FlippedCard = true;
    firstCard = this;

    return;
  } 
    // second click
    FlippedCard = false;
    secondCard = this;

    checkForMatch();
}

function checkForMatch(){
    // matching 
    if (firstCard.dataset.framework === secondCard.dataset.framework) {
      setTimeout(() => {
      firstCard.removeEventListener('click', flipCard);
      secondCard.removeEventListener('click', flipCard);
    
      firstCard.style ='opacity: 0;' 
      secondCard.style ='opacity: 0;' 
    }, 700);
    } else {
      lockBoard = true;

      setTimeout(() => {
      firstCard.classList.remove('flip');
      secondCard.classList.remove('flip');

      lockBoard = false;
    }, 1000);
    }
}

cards.forEach(card => card.addEventListener('click', flipCard));
