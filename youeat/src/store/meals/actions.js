import {djangoClient, goLangClient} from '../../plugins/apollo'
import {
  createLinkMealFoodQuery,
  createMealMutation, deleteLinkMealFoodMutation,
  deleteMealMutation,
  mealsQuery, updateLinkMealFoodMutation, updateMealMutation
} from "src/store/meals/query";
import gql from "graphql-tag";



export async function createMeal(context, payload) {
  const {data} = await djangoClient.mutate({
    mutation: createMealMutation,
    variables: payload
  });
}


export async function deleteMeal(context, payload) {
  const {data} = await djangoClient.mutate({
    mutation: deleteMealMutation,
    variables: payload
  });


}


export async function createLinkMealFood(context, payload) {
  const {data, error } = await djangoClient.mutate({
    mutation: createLinkMealFoodQuery,
    variables: payload
  })
  if(data) return data
  else if (error) return error
}

export async function deleteLinkMealFoodFunc(context, payload) {
  djangoClient.mutate({
    mutation: deleteLinkMealFoodMutation,
    variables: payload
  })
}

export async function updateLinkMealFood(context, payload) {
  djangoClient.mutate({
    mutation: updateLinkMealFoodMutation,
    variables: payload
  })

}





export async function updateMeal(context, payload){
  const {data} = await djangoClient.mutate({
    mutation :updateMealMutation,
    variables : payload
  })
  const {meal} = data
  context.commit('meals/updateMeal', meal)
}

