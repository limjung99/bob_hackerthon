
async function sendJSON() {
    event.preventDefault();
    const name = document.getElementById("namefield").value;
    const thoughtImage = document.getElementById("textfield").value;
    const button = document.getElementById("button");
    button.disabled = true;

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
    /* http get으로 이미지 렌더링*/
    for(var i=0;i<2;i++){
        const imageURL = jsonData[i];
        const div = document.createElement("div");
       
        if(i===0){
            const title = document.createElement("li");
            title.innerText= "나의 BOB위키를 바탕으로 생성한 미지";
        }
        else{
            const title = document.createElement("li");
            title.innerText = "내가 생각한 나의 이미지를 바탕으로 생성한 이미지"
        }
        div.appendChild(title);
        const imageElement = document.createElement("img");
        imageElement.src = imageURL;
        imageElement.width=400;
        imageElement.height=400;
        const container = document.getElementById("container");
        container.appendChild(imageElement);
        div.appendChild(container);
        
    }
    button.disabled=false;
}



  