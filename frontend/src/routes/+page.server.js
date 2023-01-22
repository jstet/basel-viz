
import { API_URL } from '$env/static/private';

/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {

    let api_url = API_URL + "/all";
    let country = url.searchParams.get("country")

    console.log(url.searchParams.get("country"))

    if (country) {
        api_url = API_URL + `/country?c=${country}`
        if (country == "all") {
            api_url = API_URL + "/all";
        }
    }


    const response = await fetch(api_url)

    const data = response.json()

    console.log(url.searchParams.get("normalize"))

    return data
}