
import { PUBLIC_API_URL } from "$env/static/public";

/** @type {import('./$types').PageServerLoad} */
export async function load({ url }) {

    let selected = url.searchParams.get("selection")
    let level = url.searchParams.get("level")
    let years = url.searchParams.get("years")
    let per_capita = url.searchParams.get("per_capita")
    let categories = url.searchParams.get("categories")

    let flows_url = PUBLIC_API_URL + "/flows?";
    let points_url = PUBLIC_API_URL + "/points?";
    let coords_url = PUBLIC_API_URL + "/coords?";
    let no_exports_url = PUBLIC_API_URL + "/no_exports?";
   
    if (selected) {
        if (selected == "all") {
        }
        else {
            flows_url = flows_url + `s=${selected}&`
            points_url = points_url + `s=${selected}&`
            no_exports_url = no_exports_url + `s=${selected}&`

        }
    }
    if (years) {
        let y = JSON.parse(`[${years}]`)
        flows_url = flows_url + `y=${y[0]}&y=${y[1]}&`
        points_url = points_url + `y=${y[0]}&y=${y[1]}&`
        no_exports_url = no_exports_url + `y=${y[0]}&y=${y[1]}&`
    }
    if (level) {
        flows_url = flows_url + `l=${level}&`
        points_url = points_url + `l=${level}&`
        coords_url = coords_url + `l=${level}&`
        no_exports_url = no_exports_url + `l=${level}&`
    }
    if (per_capita) {
        flows_url = flows_url + `n=${per_capita}&`
        points_url = points_url + `n=${per_capita}&`
        coords_url = coords_url + `n=${per_capita}&`
        no_exports_url = no_exports_url + `n=${per_capita}&`
    }
    if (categories) {
        if (categories == "all") {
        }
        else{
        let c = categories.split(",")
        let cs = "";
        for (let i = 0; i < c.length; i++) {
            cs += "u=" + c[i] + "&";
          } 
        flows_url = flows_url + cs
        points_url = points_url + cs
        coords_url = coords_url + cs
        no_exports_url = no_exports_url + cs
        }
    }
    console.log("Flow:", flows_url, selected)
    const flows_response = await fetch(flows_url)
    const flows = flows_response.json()

    const points_response = await fetch(points_url)
    const points = points_response.json()

    const coords_response = await fetch(coords_url)
    const coords = coords_response.json()

    const no_exports_response = await fetch(no_exports_url)
    const no_exports = no_exports_response.json()

    let select_options_obj = []
    const levels = ["country", "sub_region", "region"];
    for (let i = 0; i < levels.length; i++) {
        
        let select_options_url = PUBLIC_API_URL + "/coords?d=True&l=" + levels[i]
        let select_options_response = await fetch(select_options_url)
        let select_options = select_options_response.json()
        select_options_obj[i] = await select_options
        
      } 
      
    // const countries_response = await fetch(countries_url)
    // const countries = countries_response.json()
    //   console.log(select_options_obj[0])
    return { flows: flows, points: points, coords: coords, no_exports: no_exports, select_options: select_options_obj}
}
