function getpie_svg(details){
    let colors = d3.scaleOrdinal()
        .domain(["Vegetables", "Fruits", "Carbohydrates", "Proteins"])
        .range(["green", "indianred", "peru", "purple"]);
    const svg = d3.create("svg").attr("width", 250).attr("height", 100);

    // since data that i need to pass is an object, need to pass a function(d or data) which returns d.percent from details and sort null will sort in the order given
    let data = d3.pie()
                .sort(null)
                .value(function(d) {
                        return d.percentage_meal;
                })(details);
                console.log(data);
    let segments = d3.arc() //arc generator fucntion
        .innerRadius(0)
        .outerRadius(50)
        .padAngle(.02)
        .padRadius(5);

    // path elements for different sections
    let sections = svg.append("g")
                        .attr("transform", "translate(50, 50)")
                        .selectAll("path")
                        .data(data); //join data

    //append path elements
    x = sections.enter()

    x.append("path")
    .attr("d", segments)
    .attr("fill", function(d) {
                return colors(d.data.foodgroup_name);
        });
    display_legend(svg, data, colors);
   

    return svg;
}

function display_legend(svg, data, colors){
    // Make legend data unique since foodgroups maybe repearted in sections
    legend_data = {}
    for(d_id in data){
        legend_data[data[d_id].data.foodgroup_name] = data[d_id];
    }

    let legends = svg.append("g").attr("transform", "translate(110, -22)").selectAll(".legends").data(Object.values(legend_data));
    let legend = legends.enter().append("g").attr("transform", function(d, i) {
        return "translate(0," + (i + 1) * 22 + ")";
    });
    legend.append("rect").attr("width", 20).attr("height", 20).attr("fill", function(d) {
        return colors(d.data.foodgroup_name);
    });
    legend.append("text").text(function(d) {
            return d.data.foodgroup_name;
        })
        .attr("fill", function(d) {
            return colors(d.data.foodgroup_name);
        })
        .attr("x", 30)
        .attr("y", 22);
}








