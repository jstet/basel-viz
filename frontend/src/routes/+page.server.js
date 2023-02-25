
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
        //console.log(y)
        flows_url = flows_url + `y=${y[0]}&y=${y[1]}&`
        points_url = points_url + `y=${y[0]}&y=${y[1]}&`
    }

    //console.log("URL: ", flows_url)
    //console.log("Year: ", url.searchParams.get("year"))
    //console.log("Year2 : ", year)

    


    const flows_response = await fetch(flows_url)
    const flows = flows_response.json()
    const test = await flows
    //console.log("FlowLength: ", test.length)




    const points_response = await fetch(points_url)
    const points = points_response.json()
    const test2 = await points
    //console.log("PointLength: ", test2.length)


    return { flows: flows, points: points }
}