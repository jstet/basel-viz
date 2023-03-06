<script>

    import {
        select, selectAll,
        arc,
        chord,
        scaleOrdinal,
        range,
        descending,
        rgb, ribbon
    } from "d3";


    export let flows;
    export let points;
    export let coords;
    export let no_exports;


    var mat
    var listOfNames
    // functions

    const q_mat = (n) => [...Array(n)].map(_ => Array(n).fill(0)); // initialize quadratic matrix with n rows and n columns
    let summedFlows; // todo only do once, right now, map does the same.
    $: {
        const all_origin_codes = [...points.map(item => item.origin_code), ...no_exports.map(item => item.origin_code)];
        const originCodesMap = all_origin_codes.reduce((acc, cur, i) => {
            acc.set(cur, i);
            return acc;
        }, new Map());

        mat = q_mat(Object.keys(points).length + Object.keys(no_exports).length); // sum of locations
        const originCodesOrder = Object.fromEntries(originCodesMap); // array to reference matrix locations

        // Flows
        summedFlows = {};
        let keysOfOriginCode = Object.keys(originCodesOrder);

        // Then sort by using the keys to lookup the values in the original object:
        keysOfOriginCode.sort(function(a, b) { return originCodesOrder[a] - originCodesOrder[b] });
        listOfNames = keysOfOriginCode.map((key) => {
            if(!isNaN(key)) return coords[parseInt(key)].name
            else return coords[key].name
        })
        Object.keys(flows).forEach((key) => {
            summedFlows[key] = flows[key].map((d) => {
                return {
                    total: d.un_classes.reduce(
                        (partial, current) => partial + current.value,
                        0
                    ),
                    destination_code: d.destination_code,
                    origin_code: d.origin_code
                };
            });
            summedFlows = Object.values(summedFlows).flat()
        });

        for (const flow of summedFlows) {
            const origin_index = originCodesOrder[flow.origin_code]
            const destination_index = originCodesOrder[flow.destination_code]
            mat[origin_index][destination_index] = flow.total // origins are rows, destinations are columns
        }

        //Normalze Matrix to 100
        //getTotal:
        const total = mat.reduce((partial, current) => {
            const currentTotal = current.reduce((partialInner, currentInner) => partialInner + currentInner, 0)
            return partial + currentTotal;
        }, 0)

        //applyTotal
        mat = mat.map((currentList) => {
            return currentList.map(val => val * 100 / total )
        })

        /*//////////////////////////////////////////////////////////
        ////////////////// Set up the Data /////////////////////////
        //////////////////////////////////////////////////////////*/

        /*Sums up to exactly 100*/
        drawChord(mat, listOfNames)
    }

    function drawChord(baseMatrix, listOfNames) {

        const opacityValueBase = 0.8
        /*//////////////////////////////////////////////////////////
         ////////////////// Set up the Data /////////////////////////
         //////////////////////////////////////////////////////////*/

        var NameProvider = listOfNames;
        var matrix2 = baseMatrix
        /*Sums up to exactly 100*/

        var colors = ["#C4C4C4", "#69B40F", "#EC1D25", "#C8125C",
            "#008FC8", "#10218B", "#134B24", "#737373"];
        /*Initiate the color scale*/
        var fillColorScale = scaleOrdinal()
            .domain(range(NameProvider.length))
            .range(colors);
        /*//////////////////////////////////////////////////////////
        /////////////// Initiate Chord Diagram /////////////////////
        //////////////////////////////////////////////////////////*/
        var margin = {top: 30, right: 25, bottom: 20, left: 25},
            width = 1200 - margin.left - margin.right,
            height = 800 - margin.top - margin.bottom,
            innerRadius = Math.min(width, height) * .29,
            outerRadius = innerRadius * 1.04;
        /*Initiate the SVG*/
        var svg1 = select("#Chord")
        svg1.select("svg").remove()
        var svg2 = svg1.append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("svg:g")
            .attr("transform", "translate(" + (margin.left + width / 2) + "," + (margin.top + height / 2) + ")");

        var layout = chord()
            .padAngle(0.04)
            .sortSubgroups(descending) /*sort the chords inside an arc from high to low*/
            .sortChords(descending) /*which chord should be shown on top when chords cross. Now the biggest chord is at the bottom*/


        /*//////////////////////////////////////////////////////////
        ////////////////// Draw outer Arcs /////////////////////////
        //////////////////////////////////////////////////////////*/

        var arc2 = arc()
            .innerRadius(innerRadius)
            .outerRadius(outerRadius);

        var g = svg2.selectAll("g.group")
            .data(layout(matrix2).groups)
            .enter().append("svg:g")
            .attr("class", function (d) {
                return "group " + NameProvider[d.index];
            });

        g.append("svg:path")
            .attr("class", "arc")
            .style("stroke", function (d) {
                return fillColorScale(d.index);
            })
            .style("fill", function (d) {
                return fillColorScale(d.index);
            })
            .attr("d", arc2)
            .style("opacity", 1);

        /*//////////////////////////////////////////////////////////
        ////////////////// Initiate Ticks //////////////////////////
        //////////////////////////////////////////////////////////*/

        var ticks = svg2.selectAll("g.group").append("svg:g")
            .attr("class", function (d) {
                return "ticks " + NameProvider[d.index];
            })
            .selectAll("g.ticks")
            .attr("class", "ticks")
            .data(groupTicks)
            .enter().append("svg:g")
            .attr("transform", function (d) {
                return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
                    + "translate(" + outerRadius + 40 + ",0)";
            });

        /*Append the tick around the arcs*/
        ticks.append("svg:line")
            .attr("x1", 1)
            .attr("y1", 0)
            .attr("x2", 5)
            .attr("y2", 0)
            .attr("class", "ticks")
            .style("stroke", "#000");

        /*Add the labels for the %'s*/
        ticks.append("svg:text")
            .attr("x", 8)
            .attr("dy", ".35em")
            .attr("class", "tickLabels")
            .attr("transform", function (d) {
                return d.angle > Math.PI ? "rotate(180)translate(-16)" : null;
            })
            .style("text-anchor", function (d) {
                return d.angle > Math.PI ? "end" : null;
            })
            .text(function (d) {
                return d.label;
            })
            .attr('opacity', 1);

        /*//////////////////////////////////////////////////////////
        ////////////////// Initiate Names //////////////////////////
        //////////////////////////////////////////////////////////*/

        g.append("svg:text")
            .each(function (d) {
                d.angle = (d.startAngle + d.endAngle) / 2;
            })
            .attr("dy", ".35em")
            .attr("class", "titles")
            .attr("text-anchor", function (d) {
                return d.angle > Math.PI ? "end" : null;
            })
            .attr("transform", function (d) {
                return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
                    + "translate(" + (innerRadius + 55) + ")"
                    + (d.angle > Math.PI ? "rotate(180)" : "");
            })
            .attr('opacity', 1)
            .text(function (d, i) {
                return NameProvider[i];
            });

        /*//////////////////////////////////////////////////////////
        //////////////// Initiate inner chords /////////////////////
        //////////////////////////////////////////////////////////*/

        var chords2 = svg2.selectAll("path.chord")
            .data(layout(matrix2))
            .enter()
            .append("svg:path")
            .attr("class", "chord")
            .style("stroke", function (d) {
                return rgb(fillColorScale(d.source.index)).darker();
            })
            .style("fill", function (d) {
                return fillColorScale(d.source.index);
            })
            .attr("d", ribbon().radius(innerRadius))
            .attr('opacity', opacityValueBase);



        /*Returns an array of tick angles and labels, given a group*/
        function groupTicks(d) {
            var k = (d.endAngle - d.startAngle) / d.value;
            return range(0, d.value, 1).map(function (v, i) {
                return {
                    angle: v * k + d.startAngle,
                    label: i % 5 ? null : v + "%"
                };
            });
        }

        function fade(opacity) {
            return function (d, i) {
                svg1.selectAll("path.chord")
                    .filter(function (innerD) {
                        return innerD.source.index != i.index && innerD.target.index != i.index;
                    })
                    .transition()
                    .style("stroke-opacity", opacity)
                    .style("fill-opacity", opacity);
            };

        }
        selectAll(".group")
            .on("mouseover", fade(.02))
            .on("mouseout", fade(.80));

        /*Show all the text*/
        selectAll("g.group").selectAll("line")
            .transition().duration(100)
            .style("stroke","#000");
        /*Same for the %'s*/
        svg2.selectAll("g.group")
            .transition().duration(100)
            .selectAll(".tickLabels").style("opacity",1);
        /*And the Names of each Arc*/
        svg2.selectAll("g.group")
            .transition().duration(100)
            .selectAll(".titles").style("opacity",1);
    }

    function onMount(container) {
        drawChord(mat, listOfNames)
    }
</script>

<div class="h-full w-full bg-white-300" id="Chord" use:onMount></div>

<style >
    body {
        overflow: hidden;
        margin: 0;
        font-size: 14px;
        font-family: 'Raleway', sans-serif;
        text-align: center;
        /*font-family: Oswald;*/
        /*font-family: "Helvetica Neue", Helvetica;*/
    }

    line {
        stroke: #000;
        stroke-width: 1px;
    }

    text {
        font-size: 10px;
    }

    path.chord {
        fill-opacity: .80;
    }

    a {
        text-decoration: none;
        color: #6B6B6B;
    }
    #Chord {
    }
</style>
