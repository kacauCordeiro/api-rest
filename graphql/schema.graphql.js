const typeDefs = `
    type Query {
        times: [Time!]!
    }

    type Time {
        ID_TIME_TM: ID!
        DS_TIME_TM: String!
        DS_LOCALIDADE_TM: String!
        CLASSIFICACAO_TIME_TM: String!
        DT_CADASTRO: String!
    }
`;

export { typeDefs };