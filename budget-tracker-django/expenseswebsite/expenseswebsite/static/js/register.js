const usernameField = document.querySelector('#Username') //#id_name
const emailField = document.querySelector('#Email')
const passwordField = document.querySelector('#Password')

const userfeedbackField = document.querySelector('.invalid-user-feedback') //.class_name
const emailFeedbackField = document.querySelector('.invalid-email-feedback')
const showToggleField = document.querySelector('.showToggle')
const submitButton = document.querySelector('.submit-btn')

// show and hide password
const handleToggle = (e)=> {
  if (showToggleField.textContent === 'show') {
    showToggleField.textContent = 'hide';
    passwordField.setAttribute('type', 'text')
  } else {
    showToggleField.textContent = 'show';
    passwordField.setAttribute('type', 'password')
  }
}
showToggleField.addEventListener('click', handleToggle)

// username check validation and show error message
usernameField.addEventListener('mouseout', (e)=>{
  const usernameValue = e.target.value;

  // reset the feedback message setting, remove the style
  usernameField.classList.remove('is-invalid');
  userfeedbackField.style.display = 'none'

  if (usernameValue) {
    fetch('/authentication/user-validation', {
      body: JSON.stringify({username: usernameValue}),
      method: "POST",
    })
    .then(res => res.json())
    .then(data => {
      console.log(data)
      if (data.username_error) {
        submitButton.setAttribute('disabled', true) // if there's error, disable the submit button
        usernameField.classList.add('is-invalid');
        userfeedbackField.style.display = 'block';
        userfeedbackField.innerHTML = `<p>${data.username_error}</p>`;
      } else {
        submitButton.removeAttribute('disabled');
      }
    })
  }
})

// email check validation and show error message
emailField.addEventListener('mouseout', (e)=>{
  const emailValue = e.target.value;
  emailField.classList.remove('is-invalid');
  emailFeedbackField.style.display = 'none'

  if (emailValue) {
    fetch('/authentication/email-validation', {
      body: JSON.stringify({email: emailValue}),
      method: "POST",
    })
    .then(res => res.json())
    .then(data => {
      console.log(data)
      if (data.email_error) {
        submitButton.setAttribute('disabled', true)
        emailField.classList.add('is-invalid');
        emailFeedbackField.style.display = 'block'
        emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`
      } else {
        submitButton.removeAttribute('disabled')
      }
    })
  }
})