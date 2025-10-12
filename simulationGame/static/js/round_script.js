const eintritt = document.getElementsByName('eintritt')[0];
const standmiete = document.getElementsByName('standmiete')[0];
const submitButton = document.getElementsByName('submitButton')[0];

//Verhindere zu submitten, wenn ein der beiden Felder mindestens leer ist
function validateInputs(e) {
  if (eintritt.value === '' || standmiete.value === '') {
    e.preventDefault();
    alert('Bitte beide Felder ausfüllen!');
  }
}

submitButton.addEventListener('click', validateInputs);

//Animation
const { animate, text, stagger,svg } = anime;
const { chars } = text.split('.round_header', {
  chars: { wrap: true },
});

animate(chars, {
  y: ['80%', '0'],
  duration: 750,
  ease: 'out(3)',
  delay: stagger(50),
  loop: false,
  alternate: true,
  delay: 200
});
