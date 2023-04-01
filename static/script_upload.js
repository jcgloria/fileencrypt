function handleFileSelect() {
  const fileInput = document.getElementById('formFile');
  const fileName = fileInput.files[0].name;
  document.getElementById("formRoute").value = fileName;
}
const form = document.querySelector('form');

form.addEventListener('submit', (event) => {
  if (form.checkValidity()) {
    progressBar = document.getElementById("progressBar")
    progressBar.removeAttribute("hidden")
  }
})