import fetch from 'node-fetch';

const baseURL = `http://localhost:8000/v1`

const resolvers = {
    Query: {
        times: async () => {
            const res = await fetch(`${baseURL}/times`)
            return await res.json()
        }
    }
}

export { resolvers, baseURL };