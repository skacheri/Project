function getmeal_svg(details){
    let colors = d3.scaleOrdinal()
        .domain(["Vegetables", "Fruits", "Carbohydrates", "Proteins"])
        .range(["green", "orange", "saddlebrown", "darkviolet"]);
    const svg = d3.create("svg").attr("width", 275).attr("height", 250);

    // since data that i need to pass is an object, need to pass a function(d or data) which returns d.percent from details and sort null will sort in the order given
    let data = d3.pie()
                .sort(null)
                .value(function(d) {
                    if (d.percentage_meal == 40 || d.percentage_meal ==25 || d.percentage_meal == 10) {
                        return d.percentage_meal
                    }
                })(details);
                console.log(data);
    let segments = d3.arc() //arc generator fucntion
        .innerRadius(0)
        .outerRadius(100)
        .padAngle(.01)
        .padRadius(5);

    // path elements for different sections
    let sections = svg.append("g").attr("transform", "translate(125, 100)")
        .selectAll("path").data(data); //join data

    //append path elements and attach onclick handlers to them
    x = sections.enter()

    x.append("path")
    .attr("d", segments)
    .attr("fill", function(d) {
            return colors(d.data.foodgroup_name);
        });

    function show_section_labels(data, segments){
    let content = d3.select("g").selectAll("text").data(data);
    content.enter().append("text").each(function(d) {
        let center = segments.centroid(d);
        d3.select(this).attr("x", center[0]).attr("y", center[1])
            .text(d.data.percent);
    });
}

    let circle_drink = svg.append("circle")
                        .attr("cx", 230)
                        .attr("cy", 35)
                        .attr("r", 23)
                        .attr("fill", "lightblue");



    return svg;
}
