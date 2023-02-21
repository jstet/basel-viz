
import { API_URL } from '$env/static/private';

/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {

    

    let country = url.searchParams.get("country")
    let year = url.searchParams.get("year")

    let flows_url = API_URL + "/flows?";
    let points_url = API_URL + "/points?";

    if (country) {

        if (country == "all") {

        }
        else {
            flows_url = flows_url + `c=${country}&`
            points_url = points_url + `c=${country}&`
        }

    }

    if (year) {
        let y = JSON.parse(`[${year}]`)
        flows_url = flows_url + `y=${y[0]}&y=${y[1]}&`
        points_url = points_url + `y=${y[0]}&y=${y[1]}&`
    }

    const flows_response = await fetch(flows_url)
    const flows = flows_response.json()

    const points_response = await fetch(points_url)
    const points = points_response.json()

    return { flows: flows, points: points }
}