import { GraphQLServer } from 'graphql-yoga';
import { typeDefs } from './schema.graphql.js';
import { resolvers } from './resolvers.js';

const server = new GraphQLServer({ typeDefs, resolvers })

server.start(() => console.log(`Server is running on http://localhost:4000`))