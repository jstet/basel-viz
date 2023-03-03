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
        GeoJSON,
        svg,
    } from "leaflet";
    import { palette } from "$lib/data/palette";
    import {
        geoTransform,
        select,
        geoPath,
        arc,
        pie,
        scaleOrdinal,
        scaleLog,
    } from "d3";

    export let flows;
    export let points;
    export let coords;
    export let no_exports;

    // $: console.log(coords)

    let summedFlows;
    let summedPoints;
    let lineWidthScale;
    let DonutSizeScale;
    const innerRad = 7;
    const minimumDonutWidth = 3;
    const maximumDonutWidth = 15;
    const circleBorderColor = "#525252"
    const greyLinkColor = "#525252"


    $: {
        // Flows
        summedFlows = {};
        Object.keys(flows).forEach((key) => {
            summedFlows[key] = flows[key].map((d) => {
                return {
                    total: d.un_classes.reduce(
                        (partial, current) => partial + current.value,
                        0
                    ),
                    original: d,
                };
            });
        });

        let maxFlowAmount = 0;
        let minFlowAmount = 999999999999 // the highest flow is around 30 Million, this should be a good starting point
        for (const flow of [
            ...summedFlows.bidirectional,
            ...summedFlows.unidirectional,
        ]) {
            if (flow.total > maxFlowAmount) {
                maxFlowAmount = flow.total;
            }
            if (flow.total < minFlowAmount) {
                if (flow.total === 0) console.log("Backend still hasnt fixed the zero in Object: ", flow)
                else minFlowAmount = flow.total;
            }
        }
        //console.log("maxFlowAmount: ", maxFlowAmount)
        lineWidthScale = scaleLog()
            .base(Math.E) // todo find appropriate function to describe data
            .domain([minFlowAmount, maxFlowAmount]) // min and max values the trash amount can take
            .range([1, 7]); // min and max width of lines for the flows

        // Points
        summedPoints = {};
        summedPoints = points.map((d) => {
            return {
                total: d.un_classes.reduce(
                    (partial, current) => partial + current.value,
                    0
                ),
                original: d,
            };
        });

        let maxPointAmount = 0;
        let minPointAmount = 999999999999 // the highest flow is around 30 Million, this should be a good starting point
        for (const point of summedPoints) {
            if (point.total > maxPointAmount) {
                maxPointAmount = point.total;
            }
            if (point.total < minPointAmount) {
                minPointAmount = point.total;
            }
        }
        //console.log("maxPointAmount: ", maxPointAmount)
        DonutSizeScale = scaleLog()
            .base(Math.E) // todo find appropriate function to describe data
            .domain([minPointAmount, maxPointAmount]) // min and max values the trash amount can take
            .range([minimumDonutWidth, maximumDonutWidth]); // min and max width of the donut
    }

    const initialView = [20, 0];

    const UnClassesColorScale = scaleOrdinal()
        .domain(palette.labels)
        .range(palette.colors); // bold from carto.com

    function createMap(container) {
        // Setting initial position and zoom of map and restricting zoom
        let m = map(container, {
            preferCanvas: false,
            maxZoom: 9,
            minZoom: 3,
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

    function createEmptyCircles(map1, zoom, center) {
        //Adds a svg to the map which always contains all the things we add into it
        var d3Svg = select(map1.getPanes().overlayPane).select("svg");
        // if stuff already there, delete first
        select("#CircleGroup").remove();

        d3Svg.append("g").attr("id", "CircleGroup");
        var circleGroups = d3Svg
            .select("#CircleGroup")
            .selectAll("circle")
            .data(no_exports)
            .enter()
            .append("circle")
            .attr("r", innerRad + minimumDonutWidth)
            .attr("stroke", circleBorderColor)
            .attr("stroke-width", 2)
            .attr("fill", "none")
            .attr("class", "leaflet-zoom-hide")
            .attr("cx", function (d) {
                var coord = map1._latLngToNewLayerPoint(
                    coords[d.origin_code].coordinates,
                    zoom,
                    center
                );
                return coord.x;
            })
            .attr("cy", function (d) {
                var coord = map1._latLngToNewLayerPoint(
                    coords[d.origin_code].coordinates,
                    zoom,
                    center
                );
                return coord.y;
            })
            .attr("class", "leaflet-zoom-hide");
    }

    function createCountryDonuts(map1, zoom, center) {
        //Adds a svg to the map which always contains all the things we add into it
        var d3Svg = select(map1.getPanes().overlayPane).select("svg");
        // if stuff already there, delete first
        select("#donutGroup").remove();

        d3Svg.append("g").attr("id", "donutGroup");
        var donutGroups = d3Svg
            .select("#donutGroup")
            .selectAll("g")
            .data(summedPoints)
            .enter()
            .append("g");

        donutGroups
            .attr("style", function (d) {
                var coord = map1._latLngToNewLayerPoint(
                    coords[d.original.origin_code].coordinates,
                    zoom,
                    center
                );
                return (
                    "transform: translate(" + coord.x + "px," + coord.y + "px)"
                );
            })
            .attr("class", "leaflet-zoom-hide");

        // pie generator
        var pie1 = pie()
            .sort(null)
            .value(function (d) {
                return d.value;
            });

        // Donut border
        var outerCircle = donutGroups
            .selectAll("circle")
            .data(d => [d])
            .enter()
            .append("circle")
            .attr("stroke", circleBorderColor)
            .attr("stroke-width", 2)
            .attr("r", d => { if (d.original.origin_code==="gb") {
                console.log("data : ", d);
            };
                return innerRad + DonutSizeScale(d.total) +1
            })
            .attr("cx", "0").attr("cy", "0").attr("fill", "none")

        //slices
        var slice1 = donutGroups
            .selectAll("path")
            .data((d) => {
                const test = pie1(d.original.un_classes);
                test.forEach((element) => (element.data.total = d.total));
                return test;
            })
            .enter()
            .append("path")
            .attr("fill", function (d) {
                return UnClassesColorScale(d.data.label);
            })
            .attr("d", (d) => {
                return arc()
                    .innerRadius(innerRad)
                    .outerRadius(innerRad + DonutSizeScale(d.data.total))(d);
            });

    }

    function createLinesBetweenCountries(map1, zoom, center) {
        var d3Svg = select(map1.getPanes().overlayPane).select("svg");
        // if stuff already there, delete first
        select("#linkGroup").remove();
        select("#greyLinkGroup").remove();

        d3Svg
            .append("g")
            .attr("id", "greyLinkGroup")
            .attr("class", "leaflet-zoom-hide");

        d3Svg
            .append("g")
            .attr("id", "linkGroup")
            .attr("class", "leaflet-zoom-hide");
        var greyLinks = d3Svg
            .select("#greyLinkGroup")
            .selectAll("line")
            .data(summedFlows.unidirectional)
            .enter()
            .append("line")
            .attr("stroke-width", 1)
            .attr("stroke", greyLinkColor)
            .style("stroke-dasharray", "3, 3");

        var coloredLinks = d3Svg
            .select("#linkGroup")
            .selectAll("line")
            .data([...summedFlows.bidirectional, ...summedFlows.unidirectional])
            .enter()
            .append("line")
            .attr("stroke-width", (d) => lineWidthScale(d.total))
            .attr("stroke", function (d) {
                const max = d.original.un_classes.reduce((prev, current) =>
                    prev.value > current.value ? prev : current
                );
                return UnClassesColorScale(max.label);
            });

        function mapGeometry(link, zoom, center, zeroflow = false) {


            var radius = innerRad + minimumDonutWidth;
            if (zeroflow === false) {

                var coords1 = map1._latLngToNewLayerPoint(
                    coords[link.original.origin_code].coordinates,
                    zoom,
                    center
                );
                var coords2 = map1._latLngToNewLayerPoint(
                    coords[link.original.destination_code].coordinates,
                    zoom,
                    center
                );
            } else {

                // change the direction of the relationship between the two nodes destination and origin
                var coords1 = map1._latLngToNewLayerPoint(
                    coords[link.original.destination_code].coordinates,
                    zoom,
                    center
                );
                var coords2 = map1._latLngToNewLayerPoint(
                    coords[link.original.origin_code].coordinates,
                    zoom,
                    center
                );
            }

            var directionVector = {
                x: coords2.x - coords1.x,
                y: coords2.y - coords1.y,
            };
            var lengthOfVector = Math.sqrt(
                directionVector.x ** 2 + directionVector.y ** 2
            );
            directionVector.x = directionVector.x / lengthOfVector;
            directionVector.y = directionVector.y / lengthOfVector;
            var newCoords1 = {
                x: coords1.x + directionVector.x * radius,
                y: coords1.y + directionVector.y * radius,
            };
            var newCoords2 = {
                x: coords1.x + (coords2.x - coords1.x) / 2,
                y: coords1.y + (coords2.y - coords1.y) / 2,
            };
            return {coords1: newCoords1, coords2: newCoords2};
        }

        // update grey links before colored links, so they are underneath them
        greyLinks
            .attr("x1", (d) => mapGeometry(d, zoom, center, true).coords1.x)
            .attr("y1", (d) => mapGeometry(d, zoom, center, true).coords1.y)
            .attr("x2", (d) => mapGeometry(d, zoom, center, true).coords2.x)
            .attr("y2", (d) => mapGeometry(d, zoom, center, true).coords2.y);

        coloredLinks
            .attr("x1", (d) => mapGeometry(d, zoom, center).coords1.x)
            .attr("y1", (d) => mapGeometry(d, zoom, center).coords1.y)
            .attr("x2", (d) => mapGeometry(d, zoom, center).coords2.x)
            .attr("y2", (d) => mapGeometry(d, zoom, center).coords2.y);
    }

    let map1;

    function onMount(container) {
        map1 = createMap(container);
        map1.attributionControl.setPosition('topright')
        svg({clickable: true}).addTo(map1);
        map1.on("zoomanim", (e) => {
            createLinesBetweenCountries(map1, e.zoom, e.center);
            createEmptyCircles(map1, e.zoom, e.center);
            createCountryDonuts(map1, e.zoom, e.center);
        });
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

    $: {
        if (map1 && coords) {
            createLinesBetweenCountries(map1, map1.getZoom(), map1.getCenter());
            createEmptyCircles(map1, map1.getZoom(), map1.getCenter());
            createCountryDonuts(map1, map1.getZoom(), map1.getCenter());
        }
    }
</script>

<svelte:window on:resize={resizeMap}/>

<link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"
        integrity="sha256-kLaT2GOSpHechhsozzB+flnD+zUyjE2LlfWPgU04xyI="
        crossorigin=""
/>
<div id="map" class="w-100 h-full z-0" use:onMount/>

<style global>
    :global(.leaflet-zoom-anim #donutGroup > g) {
        transition: transform 0.25s cubic-bezier(0, 0, 0.25, 1);
    }
</style>
