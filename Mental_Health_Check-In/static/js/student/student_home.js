const buttons = document.querySelectorAll('.mood-btn');

function clearSelection(btn) {
btn.dataset.selected = '';
btn.style.backgroundColor = '';
btn.querySelector('.mood-icon').style.backgroundColor = '';
btn.querySelector('.mood-label').style.color = '';
}

buttons.forEach(btn => {
btn.addEventListener('click', () => {
    const wasSelected = btn.dataset.selected === 'true';

    buttons.forEach(clearSelection);

    if (wasSelected) return;

    const color = btn.style.getPropertyValue('--c').trim();
    btn.dataset.selected = 'true';
    btn.style.backgroundColor = color + '22'; 
    btn.querySelector('.mood-icon').style.backgroundColor = color;
    btn.querySelector('.mood-label').style.color = color;
});
});