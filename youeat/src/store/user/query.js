import gql from "graphql-tag";


export const createUserMutation = gql`
  mutation($email:String!, $password:String!, $isSocialAccount:Boolean, $anonymousUserId:Int){
    createUser(email:$email, password:$password, isSocialAccount:$isSocialAccount, anonymousUserId: $anonymousUserId){
      user{
        email
        password
      }
    }
  }
`;

export const loginMutation = gql`
  mutation($username:String!, $password:String!){
    tokenAuth(username:$username, password:$password){
      token
      userId
    }
  }
`;

export const getProfile = gql`
  {
    profile{
      id
      sexe
      age
      taille
      poid
      activity
      carbohydrateProportion
      fatProportion
      proteinProportion
    }
  }
`;

export const getUserQuery = gql`
{
  user{
    id
    username
    email
  }
}

`;


export const deleteUserMutation = gql`
mutation($userId:Int!){
  deleteUser(userId:$userId){
    success
  }
}
`;


// export const update_profile = gql`
//   mutation($activity:Float!, $taille:Int!, $age:Int!, $poid: Int!, $sexe:Int!, $carbohydrateProportion: Float!, $fatProportion: Float!, $proteinProportion: Float!, $fiberNeed: Float!){
//     updateProfile(activity:$activity, taille:$taille, age:$age, poid:$poid, sexe:$sexe, carbohydrateProportion:$carbohydrateProportion, fatProportion: $fatProportion, proteinProportion: $proteinProportion, fiberNeed:$fiberNeed){
//       updateProfile{
//         id
//         sexe
//         age
//         taille
//         poid
//         activity
//         carbohydrateProportion
//         fatProportion
//         proteinProportion
//
//
//       }
//     }
//   }
// `;


export const update_profile = gql`
  mutation($activity:Float!, $taille:Int!, $age:Int!, $poid: Int!, $sexe:Int!){
    updateProfile(activity:$activity, taille:$taille, age:$age, poid:$poid, sexe:$sexe){
      updateProfile{
        id
        sexe
        age
        taille
        poid
        activity



      }
    }
  }
`;

export const sendVerification = gql`
mutation($email: String!){
  sendVerificationCodeMail(email:$email){
    mailSended
  }
}
`;


export const verifyCodeMutation = gql`
mutation($code:Int!, $email:String!){
  verifyCode(code:$code, email:$email){
    success
  }
}
`;


export const changePasswordMutation= gql`
mutation($email: String!, $newPassword: String!){
  changePassword(email:$email, newPassword: $newPassword){
    token
    userId

  }
}
`;
