
export async function api(route, method, headers, body) {
    const response = await fetch(route, {
        method: method, 
        headers: headers ? {'Content-type': 'application/json'} : undefined,
        body: body ? body : undefined
    })
    

    if (response.status == 401 && route != "/auth/login") {
        window.location.href = "/"
    }

    return response
}