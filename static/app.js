const table = document.getElementById('clientsTableBody')


async function getClients(){
    const response = await fetch("/clients/")
    const clients = await response.json()

    table.innerHTML = ""

    clients.forEach(client => {
        const row = `
                <tr>
                    <td><strong>${client.name}</strong></td>
                    <td><span class="badge-id">${client.id}</span></td>
                    <td>${client.device || "-"}</td>
                    <td><code>${client.passwd || "-"}</code></td>
                    <td>${client.created_at}</td>
                    <td class="actions">
                        <button class="btn-icon" title="Editar">✏️</button>
                        <button class="btn-icon btn-danger" title="Excluir">🗑️</button>
                    </td>
                </tr>
        `
        table.innerHTML += row
    });
}

getClients()

