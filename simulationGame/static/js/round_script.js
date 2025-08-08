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