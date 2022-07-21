import fetch from 'node-fetch';

const baseURL = `http://localhost:8000/v1`

const resolvers = {
    Query: {
        times: async () => {
            const res = await fetch(`${baseURL}/times`)
            return await res.json()
        },
        time: async (parent, args) => {
            const { id } = args;
            const res = await fetch(`${baseURL}/times/?id=${id}`)
            const response = await res.json();
            return response;
        }
    }
}

export { resolvers, baseURL };