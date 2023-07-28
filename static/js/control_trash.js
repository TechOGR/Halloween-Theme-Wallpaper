setInterval(async () => {
    const basura = document.querySelector(".trashbin");

    await fetch("/obtener_valor", {
        method: "GET"
    }).then(response => response.json())
        .then(data =>{
            if ( data.valor === true) {
                basura.style.cssText = `
                    animation: none;
                `
            } else {
                basura.style.cssText = `
                    animation: animation_trash 1s infinite linear;
                `
            }
        })
        .catch(error => console.log(error))
},1000)