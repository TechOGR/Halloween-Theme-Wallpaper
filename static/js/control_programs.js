setInterval(async () => {
    await fetch("/check_program", {
        method: "GET"
    }).then(response => response.json())
        .then(data => {
            nombre = data.programa
            let elemento = document.querySelector(`.${nombre}`);
            elemento.style.cssText = "animation: none;";
        })
        .catch(error => console.log(error))
}, 5000)