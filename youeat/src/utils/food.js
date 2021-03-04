import {sendForm} from "src/utils/sendForm";

export const addFood = (component, food, mealId, conversionFactorId, quantityId) => {
  let payload = {
    "foodId": parseInt(food.id),
    "mealId": parseInt(mealId),
  }
  const callback = () => {
  }
  sendForm(component, "meals/createLinkMealFood", payload,  "Aliment bien ajouté au repas !", callback)
  payload = {
    "id": parseInt(food.id)
  }
  component.$store.dispatch('meals/clickOnFood', payload)
}
