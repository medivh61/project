//Изменение параметров карточки при клике мышки

const elem = document.querySelectorAll('.cards_2');
for (let i = 0; i < elem.length; i++) {
    elem[i].classList.add("card--hide");
}

const cards = document.querySelectorAll('.cards');
cards.forEach(card => {
    card.addEventListener('click', ({ target }) => {
        const card1 = card.querySelector('.cards_1');
        const card2 = card.querySelector('.cards_2');
        if (target.classList.contains('btn_1')) {
            card1.classList.add('card--hide');
            card2.classList.remove('card--hide');
        }
        else if (target.classList.contains('btn_2')) {
            card1.classList.remove('card--hide');
            card2.classList.add('card--hide');
        }
    });
});