function handleFileSelect() {
    const fileInput = document.getElementById('formFile');
    const fileName = fileInput.files[0].name;
    document.getElementById("formRoute").value = fileName;
  }