const buttons = document.querySelectorAll(".icon-button")
buttons.forEach((button) => {
    button.addEventListener('click',(event) =>{
        const bucket = button.dataset.bucket
        const key = button.dataset.key
        //POST request to download
        fetch('/downloadRequest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({bucket, key})
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            throw new Error('Request failed!')
        }, networkError => console.log(networkError.message)
        ).then(data => {
            //open a url in a new window
            const url = window.location.origin + "/downloadFile?file=" + data.file
            window.open(url)  
        })     
    })
})  