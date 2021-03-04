export default function () {
  return {
    wantSignUp:false,
    wantSignIn:false,
    wantAuth:false,
    anonymousUserId:-1,
    userId:-1,
    user:{},
    token:localStorage.getItem('token'),
    profile:{},
    calorieNeed:undefined
  }
}
