import SearchResult from "pages/SearchResult";

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      // {path: '', component: () => import('pages/SearchResult.vue')},
      {path: '', component: () => import('pages/MyMeals.vue')},
      {path: '/myMeals', component: () => import('pages/MyMeals.vue')},
      {path: '/meal/:id', component: () => import('pages/MealView.vue')},
      {path: '/food/:id', component: () => import('pages/FoodView.vue')},
      {path: '/signIn', component: () => import('pages/Auth.vue')},
      {path: '/signUp', component: () => import('pages/Auth.vue')},
      {path: '/activate', component: () => import('pages/Activate.vue')},
      {path: '/signOut', component: () => import('pages/SignOut.vue')},
      {path: '/newMeal', component: () => import('pages/NewMeal.vue')},
      {path: '/profil', component: () => import('pages/Profil.vue')},
      {path: '/forgotPassword', component: () => import('pages/ForgotPassword.vue')},
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
