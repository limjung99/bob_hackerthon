

async function sendJSON() {
    event.preventDefault();
    const name = document.getElementById("namefield").value;
    const thoughtImage = document.getElementById("textfield").value;

    const data = {
        "name" : name,
        "describe" : thoughtImage
    }

    console.log(data)

    const response = await fetch("http://localhost:8000/api/generate",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const jsonData = await response.json();
    console.log(jsonData);
}



  