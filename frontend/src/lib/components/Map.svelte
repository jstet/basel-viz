<script>
    import {
        control,
        divIcon,
        DomUtil,
        layerGroup,
        map,
        polyline,
        tileLayer,
        LatLng,
        svg
    } from "leaflet";

    export let flows;
    export let points;

    $: console.log(points)
    $: console.log(flows)

    import { geoTransform, select, geoPath, arc, pie, scaleOrdinal } from "d3";

    import countries from "$lib/geojson/countries_small.json"

    const initialView = [20, 0];

    function createMap(container) {
        // Setting initial position and zoom of map and restricting zoom posibilites
        let m = map(container, {
            preferCanvas: false,
            maxZoom: 8,
            minZoom: 2,
            maxBounds: [
                //south west
                [-90, -200],
                //north east
                [90, 200],
            ],
        }).setView(initialView, 3);
        // available basemaps: https://leaflet-extras.github.io/leaflet-providers/preview/
        tileLayer(
            "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
            {
                attribution:
                    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                subdomains: "abcd",
                maxZoom: 20,
            }
        ).addTo(m);
        return m;
    }

    function createCountryDonuts(map1) {
        const dummyData = [
            {"country_code":"ad",
                "un_classes": [
                    { label: "UN1", value: 20 },
                    { label: "UN2", value: 5 },
                    { label: "UN3", value: 12 },
                    { label: "UN4", value: 0 }
                ]},
            {"country_code":"fr",
                "un_classes": [
                    { label: "UN1", value: 20 },
                    { label: "UN2", value: 30 },
                    { label: "UN1", value: 20 },
                    { label: "UN4", value: 30 }
                ]},
            {"country_code":"br",
                "un_classes": [
                    { label: "UN1", value: 20 },
                    { label: "UN2", value: 16 },
                    { label: "UN3", value: 20 },
                    { label: "UN4", value: 70 },
                    { label: "UN5", value: 12 },
                    { label: "UN6", value: 4 }
                ]},
            {"country_code":"de",
                "un_classes": [
                    { label: "UN1", value: 120 },
                    { label: "UN2", value: 4 },
                    { label: "UN3", value: 20 },
                    { label: "UN4", value: 70 },
                    { label: "UN5", value: 12 },
                    { label: "UN6", value: 4 }
                ]}
        ]
        //Adds a svg to the map which always contains all the things we add into it
        svg({clickable:true}).addTo(map1)
        var d3Svg = select(map1.getPanes().overlayPane).select("svg")
        d3Svg.append("g").attr("id", "donutGroup")
        var donutGroups = d3Svg.select("#donutGroup").selectAll("g").data(dummyData).enter().append("g")

        var colorScale = scaleOrdinal()
            .range(["#7F3C8D","#11A579","#3969AC","#F2B701","#E73F74","#80BA5A","#E68310",
                    "#008695","#CF1C90","#f97b72","#4b4b8f","#A5AA99"]) // bold from carto.com

        // pie generator
        var pie1 = pie()
            .sort(null)
            .value(function(d) {return d.value});

        //slices
        var slice1 = donutGroups.selectAll("path")
            //.data(d => pie1(d.properties.un_classes))
            .data(d => pie1(d.un_classes))
            .enter()
            .append("path")
            .attr("fill", function(d) {return colorScale(d.data.label); });

        function update(e) {
            var radius = 20;
                ///0.5 * Math.pow(2,e.zoom);

            //arc generator
            var arc1 = arc()
                .innerRadius(radius*0.5)
                .outerRadius(radius);

            donutGroups.selectAll("path")
                .attr("d", arc1)

            donutGroups.attr("style", function (d){
                var coord = map1._latLngToNewLayerPoint(countries[d.country_code].coordinates, e.zoom, e.center);
                return 'transform: translate('+coord.x+'px,'+coord.y+'px)';
            })
            /*
            slice1.attr("cx", function (d) {
                // console.log(
                //     d,
                //     map1.latLngToLayerPoint(d.geometry.coordinates),
                //     map1.latLngToLayerPoint(d.geometry.coordinates).x
                // );
                return map1.latLngToLayerPoint(d.geometry.coordinates).x;
            });
            slice1.attr("cy", function (d) {
                return map1.latLngToLayerPoint(d.geometry.coordinates).y;
            });
            feature.attr("r", function (d) {
                return 1 * Math.pow(2, map1.getZoom());
            });*/
        }
        map1.on("zoomanim", e => update(e));
        update({"zoom":map1.getZoom(), "center": map1.getCenter()});
    }
    function createLinesBetweenCountries(map1){
        var dummyData = [
            {
                "origin_code": "ad",
                "dest_code": "de",
                "un_classes": [
                    { label: "UN1", value: 10 },
                    { label: "UN2", value: 22 },
                    { label: "UN3", value: 30 },
                    { label: "UN4", value: 0},
                    { label: "UN5", value: 50 },
                    { label: "UN6", value: 0},
                ]
            },
            {
                "origin_code": "fr",
                "dest_code": "de",
                "un_classes": [
                    { label: "UN1", value: 10 },
                    { label: "UN2", value: 20 },
                    { label: "UN3", value: 3 },
                    { label: "UN4", value: 25 },
                    { label: "UN5", value: 0},
                    { label: "UN5", value: 50 },
                ]
            },
            {
                "origin_code": "br",
                "dest_code": "fr",
                "un_classes": [
                    { label: "UN1", value: 10 },
                    { label: "UN2", value: 0},
                    { label: "UN3", value: 30 },
                    { label: "UN4", value: 0},
                    { label: "UN5", value: 12},
                    { label: "UN6", value: 50 },
                ]
            },
        ]

        var d3Svg = select(map1.getPanes().overlayPane).select("svg")
        d3Svg.append("g").attr("id", "linkGroup")


        const feature = d3Svg.select("#linkGroup")
            .selectAll("line")
            .data(dummyData)
            .enter()
            .append("line")
            .attr("stroke-width", 1)
            .attr("stroke", "black");
/*
        const areaPaths = linkGroups.append("path")
            .attr('fill-opacity', 0.3)
            .attr('stroke', 'black')
            .attr("z-index", 3000)
            .attr('stroke-width', 2.5)
            .attr("d", (d,i) => console.log(d, i ))
*/

        function mapGeometry(link, zoom, center){
            var radius = 20
            var coords1 = map1._latLngToNewLayerPoint(countries[link.origin_code].coordinates, zoom, center)
            var coords2 = map1._latLngToNewLayerPoint(countries[link.dest_code].coordinates, zoom, center)
            var directionVector = {"x": (coords2.x - coords1.x), "y": (coords2.y - coords1.y)};
            var lengthOfVector = Math.sqrt(directionVector.x**2 + directionVector.y**2)
            directionVector.x = directionVector.x/lengthOfVector;
            directionVector.y = directionVector.y/lengthOfVector;
            var newCoords1 = {"x": coords1.x + directionVector.x * radius, "y": coords1.y + directionVector.y * radius};
            // var newCoords2 = {"x": coords2.x - directionVector.x * radius, "y": coords2.y - directionVector.y * radius};
            var newCoords2 = {"x": coords1.x + (coords2.x-coords1.x)/2 , "y": coords1.y + (coords2.y-coords1.y)/2};
            //if(isNaN(newCoords1.x) || isNaN(newCoords2.x) || isNaN(newCoords1.y) || isNaN(newCoords2.y)) console.log(countries, coords1, coords2, directionVector, lengthOfVector, newCoords1, newCoords2)
            return {"coords1": newCoords1, "coords2" : newCoords2}
        }

        function update(e) {
            //var coords = map1.latLngToLayerPoint()

            //var coord = map1._latLngToNewLayerPoint(d.geometry.coordinates, e.zoom, e.center);
            feature
                .attr("x1", d => mapGeometry(d,e.zoom, e.center).coords1.x)
                .attr("y1", d => mapGeometry(d,e.zoom, e.center).coords1.y)
                .attr("x2", d => mapGeometry(d,e.zoom, e.center).coords2.x)
                .attr("y2", d => mapGeometry(d,e.zoom, e.center).coords2.y);

        }
        map1.on("zoomanim", e => update(e));
        update({"zoom":map1.getZoom(), "center": map1.getCenter()});
    }

    let map1;

    function onMount(container) {
        map1 = createMap(container);
        createCountryDonuts(map1);
        createLinesBetweenCountries(map1)

        return {
            destroy: () => {
                map1.remove();
                map1 = null;
            },
        };
    }

    function resizeMap() {
        if (map1) {
            map1.invalidateSize();
        }
    }
</script>

<svelte:window on:resize={resizeMap} />

<link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"
    integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI="
    crossorigin=""
/>
<div id="map" class="w-100 h-full" use:onMount />

<style>
    .map :global(.marker-text) {
        width: 100%;
        text-align: center;
        font-weight: 600;
        background-color: #444;
        color: #eee;
        border-radius: 0.5rem;
    }

    .map :global(.map-marker) {
        width: 30px;
        transform: translateX(-50%) translateY(-25%);
    }
    .leaflet-zoom-anim .svg-zoom-animated > g {
        width: 2000px;
        transition: transform 0.25s cubic-bezier(0,0,0.25,1);
    }
</style>
