import {link_meal_food_attrs, meal_attrs} from "src/store/meals/attrs";
import gql from "graphql-tag";

export const mealsQuery = gql`
  {
    meals{
      ...meal_attrs
    }
  }
  ${meal_attrs}
`;

export const createMealMutation = gql`
  mutation($name:String!, $objectTypeId:Int){
    createMeal(name:$name, objectTypeId:$objectTypeId){
      meal{
        ...meal_attrs
      }
    }
  }
  ${meal_attrs}
`;

export const deleteMealMutation = gql`
  mutation($idList:[Int]!){
    deleteMealList(idList:$idList){
      idList
    }
  }
`;


export const createLinkMealFoodQuery = gql`
    mutation($foodId:Int!, $mealId:Int!){
      createLinkMealFood(foodId:$foodId, mealId:$mealId){
        linkMealFood{
          id
        }
        linkNutrientsFood{
          id
        }
      }
    }

  `
;

export const deleteLinkMealFoodMutation = gql`
  mutation($linkMealFoodIdList:[Int]!){
    deleteLinkMealFood(linkMealFoodIdList:$linkMealFoodIdList){
      idList
    }
  }
`;

export const updateLinkMealFoodMutation = gql`
  mutation($id:Int!, $conversionFactorId:Int!, $quantity: Int!){
    updateLinkMealFood(id:$id, conversionFactorId:$conversionFactorId, quantity:$quantity){
      linkMealFood{
        id
      }
    }
  }
`;


export const updateMealMutation = gql`
mutation($id:Int!, $name:String){
  updateMeal(id:$id, name:$name){
    meal{
      ...meal_attrs
    }
  }
}
${meal_attrs}
`;



