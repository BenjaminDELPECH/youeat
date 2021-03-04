export const sendForm = (component, toDispatch, payload, successMessage, callback, errorCallback) => {
  const store = component.$store
  const quasar  = component.$q
  let notifyColor;
  let notifyMessage;
  store.dispatch(toDispatch, payload)
    .then((data) => {
      if (successMessage.trim() !== "") {
        notifyMessage = successMessage
        notifyColor = 'green-4'
        quasar.notify({
          color: notifyColor,
          textColor: 'white',
          icon: 'cloud_done',
          position: 'right',
          timeout: 900,
          message: notifyMessage
        })
      }
      callback && callback(data)
    })
    .catch(error => {
      error.graphQLErrors.forEach(errGraphql => {
        notifyMessage = errGraphql.message
        if(notifyMessage==="no_social_account_already_exist"){
          notifyMessage = "Adresse e-mail déjà utilisée"
        }
        notifyColor = 'red-5'
        quasar.notify({
          color: notifyColor,
          textColor: 'white',
          icon: 'error',
          position: 'right',
          message: notifyMessage
        })
      })
    })


}
