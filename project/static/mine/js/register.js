$(document).ready(function () {
    var accunt = document.getElementById("accunt")
    var accunterr = document.getElementById("accunterr")
    var checkerr = document.getElementById("checkerr")

    var pass = document.getElementById("pass")
    var passwd = document.getElementById("passwd")

    var passwderr = document.getElementById("passwderr")
    var passerr = document.getElementById("passerr")

    accunt.addEventListener("focus", function () {
        accunterr.style.display = "none"
        checkerr.style.display = "none"
    }, false)
    accunt.addEventListener("blur", function () {
        reguser = this.value
        if (reguser.length < 6 || reguser.length > 12) {
            accunterr.style.display = "block"
        }
        $.post("/checkuserid/", {"userid": reguser}, function (data) {
            if (data["status"] == "error") {
                checkerr.style.display = "block"
            }
        })
    }, false)

    pass.addEventListener("focus", function () {
        passerr.style.display = "none"
    }, false)
    pass.addEventListener("blur", function () {
        regpass = this.value
        if (regpass.length < 6 || regpass.length > 12) {
            passerr.style.display = "block"
        }
    }, false)

    passwd.addEventListener("focus", function () {
        passwderr.style.display = "none"
    }, false)
    passwd.addEventListener("blur", function () {
        compass = this.value
        if (compass != regpass) {
            passwderr.style.display = "block"
        }
    }, false)
})