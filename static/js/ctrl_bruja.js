const cuadro = document.getElementById("cuadro")

let conteo = 0

const esto = async function () {
    await fetch("/sonar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ valor: "suena" })
    })
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.log(error))

}

cuadro.addEventListener("click", (event) => {

    if (conteo == 0) {

        esto()

        let nuevo_item = document.createElement("div")
        nuevo_item.className = "cuadro_dos";

        cuadro.parentNode.insertBefore(nuevo_item, cuadro.nextSibling)

        conteo = 1
    } else {
        conteo = 0
    }

})