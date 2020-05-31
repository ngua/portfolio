function $(x) {
  return document.getElementById(x);
}

const form = $('form');

document.addEventListener('DOMContentLoaded', () => {
  form.addEventListener('submit', (e) => {submitForm(e)});
});

function submitForm(e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const csrf = Cookies.get('csrftoken');
  const errors = document.querySelectorAll('.error');
  errors.forEach(error => error.innerText = '');

  fetch(document.referrer, {
    method: 'POST',
    body: formData,
    headers: new Headers({
      'X-CSRFToken': csrf,
      'X-Requested-With': 'XMLHttpRequest',
      'credentials': 'include'
    })
  }).then(response => response.json())
    .then(data => {
      if (!data.success) {
        const errors = data.errors;
        Object.entries(errors).map(
          ([k, v]) => displayErrors(k, v)
        )
      } else {
        window.location.replace(data.url);
      }
    })
    .catch(error => {console.log(`Error: ${error}`)})
}

function displayErrors(id, errors) {
  const errorContainer = $(`${id}_error`);
  errors.forEach(error => appendError(errorContainer, error));
}

function appendError(errorContainer, error) {
  const errorSpan = document.createElement('span');
  errorSpan.classList.add('uk-animation-fade');
  errorSpan.innerText = error;
  errorContainer.appendChild(errorSpan);
}
