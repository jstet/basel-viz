/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {

console.log(url.searchParams)
console.log(url.searchParams.get("country"))
console.log(url.searchParams.get("normalize"))
}