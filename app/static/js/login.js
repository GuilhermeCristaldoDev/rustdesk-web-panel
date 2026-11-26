import { api } from './api.js'

const form = document.getElementById("loginForm")
const button = document.getElementById("button")
const errorBox = document.getElementById("error")
const buttonShowPassword = document.getElementsByClassName("mostrar")[0]
const inputPassword = document.getElementById("password")


buttonShowPassword.addEventListener("click", async () => {  
     if (inputPassword.getAttribute("type") == "password") {
        inputPassword.setAttribute("type", "text")
        buttonShowPassword.textContent = "Esconder"
     } else {
        inputPassword.setAttribute("type", "password")
        buttonShowPassword.textContent = "Ocultar"
     }
})

function showErrorBox(message) {
    errorBox.textContent = message
    errorBox.hidden = false
}

form.addEventListener("submit", async event => {
    event.preventDefault()
    errorBox.hidden = true
    button.disabled = true

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    try {
        const response = await api("/auth/login", "POST", true, JSON.stringify({username, password}))

        if (response.ok){
            window.location.href = "/panel"
            return;
        }else {
            showErrorBox("Usuário ou senha incorretos.Verifique os dados e tente novamente")
        }

    }
    
    catch(error) {
        showErrorBox("Não foi possivel conectar ao servidor")
    } finally {
        button.disabled = false
    }
  
});