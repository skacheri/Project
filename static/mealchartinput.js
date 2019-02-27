//www.knowlarity.com/blog/creating-pie-chart-d3-js-step-step/ -->
    // https://www.youtube.com/watch?v=P8KNr0pDqio
    // https://www.dashingd3js.com/lessons/d3-and-html-forms


function show_input_chart(){
    // const width = 1000;
    // const height = 500;
    let colors = d3.scaleOrdinal()
        .domain(["Vegetables", "Fruits", "Carbohydrates", "Proteins"])
        .range(["green", "orange", "saddlebrown", "darkviolet"]);

    let svg = d3.select('#pie_chart').append('svg').attr('width', 1000).attr('height', 500);

    let details = [{
        foodgroup: "Vegetables",
        percent: 40,
        select_id: "meal_component_40"
    }, {
        foodgroup: "Fruits",
        percent: 10,
        select_id: "meal_component_10"
    }, {
        foodgroup: "Carbohydrates",
        percent: 25,
        select_id: "meal_component_25"
    }, {
        foodgroup: "Proteins",
        percent: 25,
        select_id: "meal_component_2_25"
    }]

    // since data that i need to pass is an object, need to pass a function(d or data) which returns d.percent from details and sort null will sort in the order given
    let data = d3.pie()
                .sort(null)
                .value(function(d) {return d.percent})(details);

    let segments = d3.arc() //arc generator fucntion
        .innerRadius(0)
        .outerRadius(200)
        .padAngle(.01)
        .padRadius(50);

    // path elements for different sections
    let sections = svg.append("g").attr("transform", "translate(500, 250)")
        .selectAll("path").data(data); //join data

    //append path elements and attach onclick handlers to them
    sections.enter()
            .append("path")
            .attr("d", segments)
            .attr("fill", function(d) {
                return colors(d.data.foodgroup);
                })
            ///////////////////////////////////////////////////////////////////
            //want to add a border outside the plate to make it more platelike/
            ///////////////////////////////////////////////////////////////////
            .on("click", function(d) {
                let current_foodgroup = d.data.next_foodgroup ? d.data.next_foodgroup : d.data.foodgroup;
                let next_foodgroup = "";
                for(let idx=0;idx<details.length;idx++){
                    if(details[idx].foodgroup == current_foodgroup){
                        next_id = (idx+1)%details.length;
                        next_foodgroup = details[next_id].foodgroup;
                        break;
                    }
                }
                d.data.next_foodgroup = next_foodgroup;
                d3.select(this)
                    .attr("fill", function(d) {
                        return colors(d.data.next_foodgroup);
                    });
                $("select[name='"+d.data.select_id+"']").val(d.data.next_foodgroup);
            });
    
    show_section_labels(data, segments);
    display_legend(svg, data, colors);
    
    let oil_data = [{name: "Unsaturated fat"},
                    {name: "Saturated fat"},
                    {name: "Trans fat"}];
    
    let circle_oil = svg.append("circle")
                        .attr("cx", 290)
                        .attr("cy", 125)
                        .attr("r", 40)
                        .attr("fill", "red")
                        .style("opacity", 0.5);

    let oil_text = svg.append("text")
                    .attr("x", 265)
                    .attr("y", 125)
                    .data(oil_data)
                    .text(function(d){
                        return d.name;
                        })
                    .on("click", function(d){
                        let current_name = d.next_name ? d.next_name : d.name;
                        let next_name = "";
                        for(let id=0;id<oil_data.length;id++){
                            if(oil_data[id].name == current_name){
                                next_id = (id+1)%(oil_data.length);
                                next_name = oil_data[next_id].name;
                                break;
                            }
                        }
                        d.next_name = next_name;
                        d3.select(this)
                            .text(function(d) {
                                return d.next_name;
                            });
                    });


    let drink_data = [{name: "Water"},
                        {name:"Juice"}, 
                        {name:"Dairy"},
                        {name:"Soda"},
                        {name:"Tea no sugar"},
                        {name:"Coffee no sugar"},
                        {name:"Tea & sugar"},
                        {name:"Coffee & sugar"}];

    let circle_drink = svg.append("circle")
                        .attr("cx", 750)
                        .attr("cy", 125)
                        .attr("r", 75)
                        .attr("fill", "lightblue");


        let drink_text = svg.append("text")
                        .attr("x", 715)
                        .attr("y", 130)
                        .data(drink_data)
                        .text(function(d){
                            return d.name;
                        })
                        .on("click", function(d){
                        let current_name = d.next_name ? d.next_name : d.name;
                        let next_name = "";
                        for(let id=0;id<drink_data.length;id++){
                            if(drink_data[id].name == current_name){
                                next_id = (id+1)%(drink_data.length);
                                next_name = drink_data[next_id].name;
                                break;
                            }
                        }
                        d.next_name = next_name;
                        d3.select(this)
                            .text(function(d) {
                                return d.next_name;
                            });
                        });
}



function show_section_labels(data, segments){
    let content = d3.select("g").selectAll("text").data(data);
    content.enter().append("text").each(function(d) {
        let center = segments.centroid(d);
        d3.select(this).attr("x", center[0]).attr("y", center[1])
            .text(d.data.percent);
    });
}

function display_legend(svg, data, colors){
    let legends = svg.append("g").attr("transform", "translate(750, 300)").selectAll(".legends").data(data);
    let legend = legends.enter().append("g").attr("transform", function(d, i) {
        return "translate(0," + (i + 1) * 30 + ")";
    });
    legend.append("rect").attr("width", 20).attr("height", 20).attr("fill", function(d) {
        return colors(d.data.foodgroup);
    });
    legend.append("text").text(function(d) {
            return d.data.foodgroup;
        })
        .attr("fill", function(d) {
            return colors(d.data.foodgroup);
        })
        .attr("x", 30)
        .attr("y", 15);
}
$(show_input_chart);