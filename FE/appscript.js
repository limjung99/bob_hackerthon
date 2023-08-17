
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
        const jsons = jsonData[i];
        const imageURL = jsons["image_url"];
        const text = jsons["text"];
        console.log(text);
        const imageElement = document.createElement("img");
        imageElement.src = imageURL;
        imageElement.width=400;
        imageElement.height=400;
        const container = document.getElementById("container");
        const liElement = document.createElement("li");
        const childLiElement = document.createElement("li");
        childLiElement.innerText = text;
        i==0? liElement.innerText="나의 생각을 바탕으로 생성한 이미지. 반영키워드:"+text : liElement.innerText="BOB위키로 생성한 이미지. 반영키워드:"+text;
        container.appendChild(liElement);
        container.appendChild(imageElement);

    }
    button.disabled=false;
}



  