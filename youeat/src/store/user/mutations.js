/*
export function someMutation (state) {
}
*/
export function exitSignModal (state) {
  state.wantSignIn = false
  state.wantSignUp = false
}
export function showSignUpModal(state, newState){
  state.wantSignUp = newState;
}
export function showSignInModal(state, newState){
  state.wantSignIn = newState;
}
export function setToken(state, token){
  state.token = token
}

export function setAnonymousUserId(state, anonymousUserId){
  state.anonymousUserId = anonymousUserId
}

export function setWantAuth(state, newState){
  state.wantAuth = newState
}
export function setUser(state, newState){
  state.user = newState
}

export function setProfile(state, profile){
  state.profile = profile
}

export function updateCaloriesNeed(state, newVal){
  state.calorieNeed = newVal
}


