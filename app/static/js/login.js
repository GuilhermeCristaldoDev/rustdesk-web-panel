const form = document.getElementById("loginForm")
const button = document.getElementById("button")
const errorBox = document.getElementById("error")

function showErrorBox(message) {
    errorBox.textContent = message
    errorBox.hidden = false
}

form.addEventListener("submit", async event => {
    event.preventDefault()
    errorBox.hidden = true
    button.disable = true

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    try {
        const response = await fetch("/auth/login", 
            {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json'
                },
                body: JSON.stringify({username, password})
            }
        )

        if (response.ok){
            window.location.href = "/panel"
            return;
        }

        if (error == "401") {
            showErrorBox("Usuário ou senha inválidos")    
        }
        else {
            showErrorBox("Usuário ou senha inválidos")
        }

    }
    
    catch(error) {
        showErrorBox("Não foi possivel conectar ao servidor")
    } finally {
        button.disable = false
    }
  
});