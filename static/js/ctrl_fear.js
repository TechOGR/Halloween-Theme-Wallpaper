const los_div = document.querySelectorAll("div")
const los_h1 = document.querySelectorAll("h1")

setInterval(async () => {
    await fetch("/get_fear", {
        method: "GET"
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.value)
            if (data.value == "Activar") {
                const sonar = async () => {
                    await fetch("/sonar", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ valor: "grito" })
                    })
                        .then(response => response.text())
                        .then(data => console.log(data))
                        .then(error => console.log(error))
                }
                sonar()
                setTimeout(() => {
                    los_div.forEach((elemento) => {
                        elemento.style.display = "none";
                    })
                    los_h1.forEach((elemento) => {
                        elemento.style.display = "none";
                    })
                    document.body.style.backgroundImage = "url('../img/Susto.png')"
                    document.body.style.backgroundSize = "cover"
                    document.body.style.backgroundPosition = "fixed"
                    document.body.style.backgroundRepeat = "no-repeat"
                }, 500)

            } else {
                los_div.forEach((elemento) => {
                    elemento.style.display = "flex";
                })
                los_h1.forEach((elemento) => {
                    elemento.style.display = "inline";
                })
                document.body.style.backgroundImage = "url('../img/fondo.png')"
                document.body.style.backgroundSize = "cover"
                document.body.style.backgroundPosition = "fixed"
                document.body.style.backgroundRepeat = "no-repeat"
            }
        })
        .catch(error => console.log(Error))
}, 4000)