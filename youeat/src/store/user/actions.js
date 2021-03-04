/*
export function someAction (context) {
}
*/
import {djangoClient} from '../../plugins/apollo'

import {setCookie} from "src/utils/cookieUtils";
import {
  activateUserMutation, changePasswordMutation,
  createUserMutation,
  deleteUserMutation,
  getProfile,
  getUserQuery,
  loginMutation, sendVerification, update_profile, verifyCodeMutation
} from "src/store/user/query";
import {getCalory} from "src/utils/calories";


export async function createUser(context, payload) {
  const {data, error} = await djangoClient.mutate({
    mutation: createUserMutation,
    variables: payload
  });
  if (data) {
    return data;
  } else if (error) {
    return error;
  }
}

export async function login(context, payload) {
  const {email, password} = payload;
  const {data, error} = await djangoClient.mutate({
    mutation: loginMutation,
    variables: {
      username: email,
      password: password
    }
  });
  if (data) {
    const {token, userId} = data["tokenAuth"];
    localStorage.setItem('token', token)
    localStorage.setItem('userId', userId)
    return data;
  } else if (error) {
    return error;
  }
}

export async function loadProfile(context) {
  const {data} = await djangoClient.query({
    query: getProfile
  });
  const {profile} = data;
  context.commit("updateCaloriesNeed", getCalory(profile))
  context.commit("updateProfile", profile)
}

export async function activateUser(context, payload) {
  const {data} = await djangoClient.mutate({
    mutation: activateUserMutation,
    variables: payload
  })
  if (data) return data
  else if (error) return error
}


export async function sendVerificationCodeMail(context, payload) {
  const {data} = await djangoClient.mutate({
    mutation: sendVerification,
    variables: payload
  })
  if (data) return data
  else if (error) return error
}

export async function deleteAccount(context, payload) {
  const {data} = await djangoClient.mutate({
    mutation: deleteUserMutation,
    variables: payload
  })
  if (data) return data
  else if (error) return error;
}

export async function getUser(context, payload) {
  const {data} = await djangoClient.query({
    query: getUserQuery,

  })
  const {user} = data
  context.commit('setUser', user)
}

export async function updateProfile(context, payload) {
  const {data} = await djangoClient.mutate({
    mutation: update_profile,
    variables: payload
  });
  const {updateProfile: objResult} = data["updateProfile"];
  const calory = getCalory(objResult)
  context.commit("updateCaloriesNeed", calory)
  context.commit("setProfile", objResult)
}

export async function verifyCode(context, payload) {
  const {data} = await djangoClient.mutate({
    mutation: verifyCodeMutation,
    variables: payload
  })
  if (data) return data
  else if (error) return erro
}

export async function changePassword(context, payload){

  const {data} = await djangoClient.mutate({
    mutation : changePasswordMutation,
    variables: payload
  })
  if(data) return data
  else if(error) return erro
}


