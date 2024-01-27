let button = document.querySelector('.buttons-right li');
let boombox = document.querySelector('.boombox');

button.addEventListener('click', (e) => {
  boombox.classList.toggle('on');
});