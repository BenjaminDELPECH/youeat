export const signIn = (component, email, password) => {
  const payload = {
    "email": email,
    "password": password
  }
  let notifyMessage;
  let notifyColor;
  component.$store.dispatch('user/login', payload)
    .then(() => {
      notifyMessage = 'Vous etes connêcté'
      notifyColor = 'green-4'
      component.$q.notify({
        color: notifyColor,
        textColor: 'white',
        icon: 'cloud_done',
        position: 'top',
        message: notifyMessage
      });
      component.$router.push({
        path: '/'
      })
      component.$router.reload()
    })
    .catch((e) => {
      notifyMessage = 'Vos identifiants de connexion ne correspondent a aucun compte sur notre système '
      notifyColor = 'red-5'
      component.$q.notify({
        color: notifyColor,
        textColor: 'white',
        icon: 'error',
        position: 'top',
        message: notifyMessage
      })
    })
}
