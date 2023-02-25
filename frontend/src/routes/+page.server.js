
import { API_URL } from '$env/static/private';

/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {

    

    let country = url.searchParams.get("country")
    let year = url.searchParams.get("year")

    let flows_url = API_URL + "/flows?";
    let points_url = API_URL + "/points?";
    let coords_url = API_URL + "/coords?";

    let countries_url = API_URL + "/countries?";

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
        console.log(y)
        flows_url = flows_url + `y=${y[0]}&y=${y[1]}&`
        points_url = points_url + `y=${y[0]}&y=${y[1]}&`
    }

    
    let flows_obj = {}
    let points_obj = {}
    let coords_obj = {}
    for (let step = 0; step < 6; step++) {
        flows_url + `l=${step}&`
        points_url + `l=${step}&`
        coords_url + `l=${step}&`
        
        let flows_response = await fetch(flows_url)
        let flows = flows_response.json()
    
        let points_response = await fetch(points_url)
        let points = points_response.json()

        let coords_response = await fetch(coords_url)
        let coords = coords_response.json()

        flows_obj[step] = await flows
        points_obj[step] = await points
        coords_obj[step] = await coords
      }
   

    const countries_response = await fetch(countries_url)
    const countries = countries_response.json()

    
      
    

    return { flows: flows_obj, points: points_obj, coords: coords_obj, countries: countries }
}
