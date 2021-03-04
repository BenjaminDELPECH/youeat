export const callGoApi = (component, url, callback, parameters) => {
  url = url.replace("/", "")
  const additional = getAdditional(parameters, additional);
  component.$axios.get(`${process.env.GO_API_URL}/${url}${additional}`).then(
    response => {
      callback(response.data)
    }
  )
}

export const fetchGoApi = (cpmt, url, propName, parameters, callbackOverride) => {
  let callback = callbackOverride
  if(!callbackOverride) {
    callback = response => {
      cpmt[propName] = response
      console.log(cpmt[propName])
    }
  }
  callGoApi(cpmt, url, callback, parameters)
}


function getAdditional(parameters) {
  let additional = ""
  if (parameters) {
    additional += "?"
    let cpt = 0
    for (const [key, value] of Object.entries(parameters)) {
      if (cpt !== 0) {
        additional += "&"
      }
      additional += key + "=" + value
      cpt++
    }

  }
  return additional
}

export function propsToLowerCase(data) {
  if (data && data.length) {
    data.forEach(elem => {
      for (const prop in elem) {
        const tmp = elem[prop]
        let propName = prop.toLowerCase()
        elem[propName] = tmp
        if (propName !== prop) delete elem[prop]
      }
    })
  }
}
