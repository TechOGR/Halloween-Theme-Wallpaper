const all_h1 = document.querySelectorAll("h1")

all_h1.forEach((element) => {
    element.addEventListener("click", (event) => {
        const name = element.className;
        const get_value = async function () {
            await fetch("/obtener_valor", {
                method: "GET"
            }).then(response => response.json())
                .then(data => {
                    const estado = data.valor
                    if (estado == false) {
                        fetch("/open", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ name: name })
                        }).then(response => response.text())
                            .then(data => console.log(data))
                            .catch(error => console.log(error))
                    } else {
                        element.style.cssText = "animation: empty_trash 0.3s linear infinite"
                    }
                }).catch(error => console.log(error))
        }
        if (name == "trashbin") {
            get_value()
        } else {
            fetch("/open", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: name })
            })
                .then(response => response.text())
                .then(data => console.log(data))
                .catch(error => console.log(error))
        }
    });
});