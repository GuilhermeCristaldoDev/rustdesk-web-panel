const table = document.getElementById('linhas')
const modelo = document.getElementById('modelo-linha')
const noClientsText = document.getElementById('estado')
const dlgClient = document.getElementById('dlg-cliente')
const form = document.getElementById('form-cliente')
const newClientButton = document.getElementById('novo')
const cancelButton = document.getElementById('cancelar')


async function getClients(){
    const response = await fetch("/clients/")
    const clients = await response.json()

    if (clients.length == 0) {
        noClientsText.hidden = false
        return
    }

    noClientsText.hidden = true
    table.textContent = ""

    const clone = modelo.content.cloneNode(true)

    clients.forEach(client => {
        clone.querySelector('.chip-id').textContent = client.id
        clone.querySelector('.col-nome').textContent = client.name
        clone.querySelector('.col-device').textContent = client.device || "-"
        clone.querySelector('.col-criado').textContent = new Date(client.created_at).toLocaleDateString("pt-BR")
        clone.querySelector('.col-acesso').textContent = client.last_session || "-"

        table.appendChild(clone)
    });
    
}

newClientButton.addEventListener("click", () => {
    dlgClient.showModal()
})

cancelButton.addEventListener("click", event => {
    dlgClient.close()
})

dlgClient.addEventListener("close", () => {
    form.reset()
})

form.addEventListener("submit", async (event) => {
    event.preventDefault()

    const dados = Object.fromEntries(new FormData(form))

    const response = await fetch("/clients/", {
        method: "POST",
        headers: {
            'Content-type': 'application/json',
        },
        body: JSON.stringify(dados)
    })

    if (response == 422) {
        const erro = await response.json()
        console.error(erro)
    }

    if(response.ok)
        dlgClient.close()
        getClients()
})

getClients()


