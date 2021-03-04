import {ApolloClient} from 'apollo-client'
import {createHttpLink} from 'apollo-link-http'
import {InMemoryCache} from 'apollo-cache-inmemory'
import VueApollo from 'vue-apollo'
import {ApolloLink} from "apollo-link";

console.log(process.env)

// HTTP connection to the API
let httpLink = new createHttpLink({
  // You should use an absolute URL here
  uri: "https://youeat.fr/django/graphql/"
  // uri: "http://127.0.0.1:8888/graphql/"
})

const authMiddleware = new ApolloLink((operation, forward) => {
  const token = localStorage.getItem("token")
  operation.setContext({
    headers: {
      authorization: token ? `JWT ${token}` : null,
    }
  })
  return forward(operation)
})

const cache = new InMemoryCache()

export const djangoClient = new ApolloClient({
  link: authMiddleware.concat(httpLink),
  cache: cache,
  defaultOptions: {
    query: {
      fetchPolicy: 'network-only'
    },
  },

  connectToDevTools: true,
})

export const apolloProvider = new VueApollo({
  defaultClient: djangoClient,
  clients: {djangoClient: djangoClient},
  errorHandler({graphQLErrors, networkError}) {
    // if (graphQLErrors) {
    //   graphQLErrors.map(({message, locations, path}) =>
    //     console.log(
    //       `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
    //     )
    //   )
    // }
    // if (networkError) {
    //   console.log(`[Network error]: ${networkError}`)
    // }
  }
})
export default ({app, Vue}) => {
  Vue.use(VueApollo)
  app.apolloProvider = apolloProvider
}
