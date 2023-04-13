const buttons = document.querySelectorAll(".icon-button")
buttons.forEach((button) => {
    button.addEventListener('click', (event) => {
        progressBar = document.getElementById("progressBar")
        progressBar.removeAttribute("hidden")
        const bucket = button.dataset.bucket
        const key = button.dataset.key
        //POST request to download
        fetch('/downloadRequest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ bucket, key })
        }).then(response => {
            return response.json()
        }
        ).then(data => {
            if (data["error"]) {
                errorBanner = document.getElementById("errorMsg")
                errorBanner.innerHTML = "Error: " + data["error"]
                errorBanner.removeAttribute("hidden")
            }
            else {
                //open a url in a new window
                const url = window.location.origin + "/downloadFile?file=" + data.file
                window.open(url)
            }
        })
        progressBar.setAttribute("hidden", true)
    })
})  