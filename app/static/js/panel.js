import { api } from './api.js'

const table = document.getElementById('linhas')
const modelo = document.getElementById('modelo-linha')
const noClientsText = document.getElementById('estado')
const dlgClient = document.getElementById('dlg-cliente')
const form = document.getElementById('form-cliente')
const newClientButton = document.getElementById('novo')
const cancelButton = document.getElementById('cancelar')
const erroForm = document.getElementById('erro-form')
const inputId = document.getElementById('f-id')
const buttonSave = document.getElementById('salvar')
const clientsCount = document.getElementById('contagem')
const dlgExclude = document.getElementById('dlg-excluir')
const buttonLogout = document.getElementById('sair')


async function getClients(){
    try {
    const response = await api("/clients", "GET")
   
    
    if (!response.ok) { 
        table.textContent = "Erro ao buscar clientes"
        return
    }

    const clients = await response.json()
    table.textContent = ""

    clientsCount.textContent = `${clients.length} clientes`

    if (clients.length == 0) {
        noClientsText.hidden = false
        return
    }

    noClientsText.hidden = true
    
    clients.forEach(client => {
        const clone = modelo.content.cloneNode(true)

        clone.querySelector('tr').dataset.id = client.id

        clone.querySelector('.chip-id').textContent = client.id
        clone.querySelector('.col-nome').textContent = client.name
        clone.querySelector('.col-device').textContent = client.device || "-"
        clone.querySelector('.col-criado').textContent = new Date(client.created_at).toLocaleDateString("pt-BR")
        clone.querySelector('.col-acesso').textContent = client.last_session? new Date(client.last_session).toLocaleDateString("pt-BR") : "-"
        table.appendChild(clone)
    });
    } catch(error) {
        console.log(error)
    }
}

table.addEventListener("click", async event => {
    const button = event.target.closest('.btn-excluir')

    if (!button) return

    const line = button.closest('tr')
    dlgClient.dataset.id = line.dataset.id

    dlgExclude.showModal()
})

dlgExclude.addEventListener("click", async event => {
    const buttonDlg = event.target.closest('button')

    if (!buttonDlg) return 

    if (buttonDlg.textContent.trim() === "Excluir") {
        const id = dlgClient.dataset.id

        try{
            const response = await api(`/clients/${id}`, "DELETE")

            if (response.ok) {
                await getClients()
            }

            if (response.status == 404) {
                const data = await response.json()

                console.log(data.detail)
            }

        } catch(error) {
            console.log(error)
        }
        
    } 
    delete dlgExclude.dataset.id
    dlgExclude.close()
    
})

newClientButton.addEventListener("click", () => {
    dlgClient.showModal()
})

cancelButton.addEventListener("click", () => {
    buttonSave.disabled = false
    dlgClient.close()
})

dlgClient.addEventListener("close", () => {
    form.reset()
    erroForm.hidden = true
})

form.addEventListener("submit", async (event) => {
    event.preventDefault()
    buttonSave.disabled = true

    const dados = Object.fromEntries(new FormData(form))

    const response = await api("/clients/", "POST", true, JSON.stringify(dados))
    
    if (response.status === 422) {
        showErrorForm(response)
    }

    if (response.status === 409) {
        showErrorForm(response, inputId)
    }

    if(response.ok)
        dlgClient.close()
        getClients()

    buttonSave.disabled = false   
})

buttonLogout.addEventListener("click", async () => {
    const response = await fetch("/auth/logout", {
        method: "POST",
        headers: {
            'Content-type': 'application/json'      
        }
    })

    if (response.ok) {
        window.location.href = "/"
    }
})

async function showErrorForm(res, inputToFocus) {
    const data = await res.json()

    erroForm.textContent = data.detail
    erroForm.hidden = false
    if (inputToFocus)
        inputToFocus.focus
}

getClients()


