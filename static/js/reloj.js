const reloj = document.getElementById("reloj")

const updateClock = async () => {
    setInterval(function () {
        fecha = new Date()

        hora = fecha.getHours()
        minutos = fecha.getMinutes()
        segundos = fecha.getSeconds()

        if (hora < 10) {
            hora = "0" + hora
        }
        if (minutos < 10) {
            minutos = "0" + minutos
        }
        if (segundos < 10) {
            segundos = "0" + segundos
        }

        reloj.innerHTML = `${hora} : ${minutos} : ${segundos}`

    }, 1000)
}
updateClock()