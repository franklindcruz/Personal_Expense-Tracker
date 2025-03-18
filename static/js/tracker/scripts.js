document.addEventListener('DOMContentLoaded', function () {
  const deleteButtons = document.querySelectorAll('.delete-btn')

  deleteButtons.forEach(button => {
    button.addEventListener('click', function (event) {
      event.preventDefault() // Prevent direct navigation

      const deleteUrl = this.getAttribute('data-url') // Get the delete URL from data attribute

      Swal.fire({
        title: 'Are you sure to delete?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!',
        reverseButtons: true,
        customClass: {
          confirmButton: 'btn btn-success',
          cancelButton: 'btn btn-danger'
        },
        buttonsStyling: false
      }).then(result => {
        if (result.isConfirmed) {
          // Redirect to the delete URL
          window.location.href = deleteUrl
        } else if (result.dismiss === Swal.DismissReason.cancel) {
          Swal.fire({
            title: 'Cancelled',
            text: 'Your transaction is safe :)',
            icon: 'error',
            timer: 1500
          })
        }
      })
    })
  })
})

// Password Toggle Script

function togglePassword (fieldId, iconId) {
  let passwordField = document.getElementById(fieldId)
  let icon = document.getElementById(iconId)

  if (passwordField.type === 'password') {
    passwordField.type = 'text'
    icon.classList.replace('bi-eye-slash', 'bi-eye')
  } else {
    passwordField.type = 'password'
    icon.classList.replace('bi-eye', 'bi-eye-slash')
  }
}
