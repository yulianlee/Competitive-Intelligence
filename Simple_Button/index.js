// var URLFETCH1 = 'http://localhost:3000/titles';
// var URLFETCH2 = 'http://localhost:3000/proj_details';
// var URLFETCH3 = 'http://localhost:3000/biddiff';
// var URLFETCH4 = 'http://localhost:3000/bidindex';
// var URLFETCH5 = 'http://localhost:3000/dbsearch';
// var URLFETCH6 = 'http://localhost:3000/company_details';
// var URLFETCH7 = 'http://localhost:3000/agency_plot';
// var URLFETCH8 = 'http://localhost:3000/agency_details';
// var URLFETCH9 = 'http://localhost:3000/bulk_details';
// var URLFETCH10 = 'http://localhost:3000/intro_page';
// var URLFETCH11 = 'http://localhost:3000/intro_plot';
// var URLFETCH12 = 'http://localhost:3000/agency_pie_plot';
// var URLFETCH14 = 'http://localhost:3000/agency_bar_plot';
// var URLFETCH15 = 'http://localhost:3000/agency_line_plot';
// var URLFETCH16 = 'http://localhost:3000/company_whisker_plot';
// var URLFETCH17 = 'http://localhost:3000/company_bar_plot';
// var URLFETCH18 = 'http://localhost:3000/set_category';
// var URLFETCH19 = 'http://localhost:3000/gauge_plot';


var URLFETCH1 = 'https://comp-intel-2.herokuapp.com/titles';
var URLFETCH2 = 'https://comp-intel-2.herokuapp.com/proj_details';
var URLFETCH3 = 'https://comp-intel-2.herokuapp.com/biddiff';
var URLFETCH4 = 'https://comp-intel-2.herokuapp.com/bidindex';
var URLFETCH5 = 'https://comp-intel-2.herokuapp.com/dbsearch';
var URLFETCH6 = 'https://comp-intel-2.herokuapp.com/company_details';
var URLFETCH7 = 'https://comp-intel-2.herokuapp.com/agency_plot';
var URLFETCH8 = 'https://comp-intel-2.herokuapp.com/agency_details';
var URLFETCH9 = 'https://comp-intel-2.herokuapp.com/bulk_details';
var URLFETCH10 = 'https://comp-intel-2.herokuapp.com/intro_page';
var URLFETCH11 = 'https://comp-intel-2.herokuapp.com/intro_plot';
var URLFETCH12 = 'https://comp-intel-2.herokuapp.com/agency_pie_plot';
var URLFETCH14 = 'https://comp-intel-2.herokuapp.com/agency_bar_plot';
var URLFETCH15 = 'https://comp-intel-2.herokuapp.com/agency_line_plot';
var URLFETCH16 = 'https://comp-intel-2.herokuapp.com/company_whisker_plot';
var URLFETCH17 = 'https://comp-intel-2.herokuapp.com/company_bar_plot';
var URLFETCH18 = 'https://comp-intel-2.herokuapp.com/set_category';
var URLFETCH19 = 'https://comp-intel-2.herokuapp.com/gauge_plot';
var mostRecentXHR = undefined;


// Define Ajax
makeAjaxRequest=function(subject,jsonParameters,successCallback){
     $.ajax({
  type: 'GET',
  url: subject,
  data: jsonParameters,
  success:function(data,status,xhr){
    // successful request; do something with the data
	mostRecentXHR = xhr;
    successCallback(data);
  }
});
};


function setpredictedcompetitor(){
  let title = $("#title").val()
  $("#competing_companies").empty()
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH1,{"action":"titleSearch","OutputFromBrowser":title},function(response){

    // console.log(response);
    // set text to response
    var resp = JSON.parse(response);
    // console.log("BREAKER");
    // console.log(resp);
    var resp_final = JSON.parse(resp);
    var MAE = resp_final.MAE;
    var companies = resp_final.companies;
    var topics = resp_final.topics;
    var value = resp_final.value;
    var lower_lim  =  Math.max(value - MAE,0);
    var upper_lim = (value + MAE);

    company_list = [];

    for (var i = 0 ; i < companies.length; i++)
    { company_list.push(companies[i][0])}

    // console.log(companies);
    // console.log(topics);
    // console.log(value);
    // console.log(MAE);
    // $("#MAE").text("$"+MAE);
    $("#similar_1").text(topics[0]);
    $("#similar_2").text(topics[1]);
    $("#similar_3").text(topics[2]);
    $("#value").text("$"+value);
    $("#upper_lim").text("$"+upper_lim);
    $("#lower_lim").text("$"+lower_lim);

    var competitorstring = ""
    for (var i =0; i <company_list.length; i++){
      var competitor = company_list[i]
      var competitor = competitor.toUpperCase()
      competitorstring += "<li><span>" + competitor + "</span> </li>"
    }
    $("#competing_companies").append(competitorstring);
})
};

function getprojectdetails(elem){
	proj = $(elem).text()
	console.log(proj)

	// Create Querying parameters for the get request
	var jsonParameters = {"action":"projectSearch","title":{'type':'Title','query':proj,"num":5,"exact":0}}


	// Create pop out window (blank)
	var my_window = window.open("", "new_window"+proj, "status=1,width=350,height=350");
  // my_window.document.write("<h1>" + proj + "</h1>")
	// // make get request using AJAX
  // my_window.document.write("<h1>" + "Hello" + "</h1>")

	makeAjaxRequest(URLFETCH2,jsonParameters,function(response){

    console.log("response is:" + response)
		result = JSON.parse(JSON.parse(response));
		console.log("result is:" + result)

		// Append Awards and Respondent information
		for (var i = 0; i < result.length; i++) {
			award = ''
			for (var j = 0; j < Object.keys(result[i]['Awards']).length; j++) {
				line = "<tr><ul><li>Awarded To " + result[i]['Awards'][j]['AwardedTo'] + " at " + result[i]['Awards'][j]['AwardedValue'] +"</li></ul></tr>"
				award += line
			}
			respondent = ''
			for (var j = 0; j < Object.keys(result[i]['Respondents']).length; j++) {
				line = "<li>" + result[i]['Respondents'][j]['CompanyName'] + " with a price of  " + result[i]['Respondents'][j]['TotalPrice']  +"</li>"
				respondent += line
			}

      var id = result[0]["_id"]
      var qtnnum = result[0]["QuotationNo"]
      var agency = result[0]["Agency"]
      var pubdate = result[0]["PublishedDate"]
      var proctype = result[0]["ProcurementType"]
      var qtntype = result[0]["QuotationType"]
      var proccat = result[0]["ProcurementCategory"]
      var closingdate = result[0]["TenderClosingDate"]
      var awdval = result[0]["AwardedValue"]

		// Create the content of the popout
    my_window.document.write("<h2>"+ proj +"</h2><br>")
    my_window.document.write("Respondents are:" + respondent +"<br>")
    my_window.document.write("ID is:" + id +"<br><br>")
    my_window.document.write("Awarded To:" + award +"<br><br>");
    my_window.document.write("Quotation Number:" + qtnnum +"<br><br>");
    my_window.document.write("Agency:" + agency +"<br><br>");
    my_window.document.write("Publishing Date:" + pubdate +"<br><br>");
    my_window.document.write("Procurement Type:" + proctype +"<br><br>");
    my_window.document.write("Quotation Type:" + qtntype +"<br><br>");
    my_window.document.write("Procurement Category:" + proccat +"<br><br>");
    my_window.document.write("Closing Date:" + closingdate +"<br><br>");
    my_window.document.write("Awarded Value:" + awdval +"<br><br>");
    }
	})
}


function competitor_dropdown(){

  $("#fig01").empty();
  let company = $("#company_value").val().toLowerCase()
  let outcome = $("#proj_filter1").val().toUpperCase()

  console.log(company)
  $('#fig01title').text(company.toUpperCase())
  console.log("outcome is" + outcome)
  console.log("NOTHING WRONG YET")
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH3,{"OutputFromBrowser":company, "outcome":outcome},function(response){
    console.log("NOTHING WRONG still")

    // set text to response
    var resp = JSON.parse(response);
    // console.log("BREAKER");



    //JSON OBJECT
    var resp_final = JSON.parse(resp);
    !function(mpld3){

      mpld3.register_plugin("htmltooltip", HtmlTooltipPlugin);
      HtmlTooltipPlugin.prototype = Object.create(mpld3.Plugin.prototype);
      HtmlTooltipPlugin.prototype.constructor = HtmlTooltipPlugin;
      HtmlTooltipPlugin.prototype.requiredProps = ["id"];
      HtmlTooltipPlugin.prototype.defaultProps = {labels:null,
                                                  hoffset:0,
                                                  voffset:10};
      function HtmlTooltipPlugin(fig, props){
          mpld3.Plugin.call(this, fig, props);
      };

      HtmlTooltipPlugin.prototype.draw = function(){
         var obj = mpld3.get_element(this.props.id);
         var labels = this.props.labels;
         var tooltip = d3.select("body").append("div")
                      .attr("class", "mpld3-tooltip")
                      .style("position", "absolute")
                      .style("z-index", "10")
                      .style("visibility", "hidden");

         obj.elements()
             .on("mouseover", function(d, i){
                                tooltip.html(labels[i])
                                       .style("visibility", "visible");})
             .on("mousemove", function(d, i){
                    tooltip
                      .style("top", d3.event.pageY + this.props.voffset + "px")
                      .style("left",d3.event.pageX + this.props.hoffset + "px");
                   }.bind(this))
             .on("mouseout",  function(d, i){
                             tooltip.style("visibility", "hidden");});
      };

          mpld3.register_plugin("drag", DragPlugin);
          DragPlugin.prototype = Object.create(mpld3.Plugin.prototype);
          DragPlugin.prototype.constructor = DragPlugin;
          DragPlugin.prototype.requiredProps = ["id"];
          DragPlugin.prototype.defaultProps = {}
          function DragPlugin(fig, props){
              mpld3.Plugin.call(this, fig, props);
              mpld3.insert_css("#" + fig.figid + " path.dragging",
                               {"fill-opacity": "1.0 !important",
                                "stroke-opacity": "1.0 !important"});
          };

          DragPlugin.prototype.draw = function(){
              var obj = mpld3.get_element(this.props.id);

              var drag = d3.behavior.drag()
                  .origin(function(d) { return {x:obj.ax.x(d[0]),
                                                y:obj.ax.y(d[1])}; })
                  .on("dragstart", dragstarted)
                  .on("drag", dragged)
                  .on("dragend", dragended);

              obj.elements()
                 .data(obj.offsets)
                 .style("cursor", "default")
                 .call(drag);

              function dragstarted(d) {
                d3.event.sourceEvent.stopPropagation();
                d3.select(this).classed("dragging", true);
              }

              function dragged(d, i) {
                d[0] = obj.ax.x.invert(d3.event.x);
                d[1] = obj.ax.y.invert(d3.event.y);
                d3.select(this)
                  .attr("transform", "translate(" + [d3.event.x,d3.event.y] + ")");
              }

              function dragended(d) {
                d3.select(this).classed("dragging", false);
              }
          }

         mpld3.draw_figure("fig01", resp_final);
    }(mpld3);
})

};

function competitor_dropdown2(){
  $("#fig03").empty();
  let company = $("#company_value2").val().toLowerCase()
  let outcome = $("#proj_filter2").val().toUpperCase()
  $('#fig02title').text(company.toUpperCase())
  console.log(company)
  console.log(outcome)

  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH3,{"OutputFromBrowser":company,'outcome':outcome},function(response){

    // set text to response
    var resp = JSON.parse(response);
    // console.log("BREAKER");


    //JSON OBJECT
    var resp_final = JSON.parse(resp);
    !function(mpld3){

      mpld3.register_plugin("htmltooltip", HtmlTooltipPlugin);
      HtmlTooltipPlugin.prototype = Object.create(mpld3.Plugin.prototype);
      HtmlTooltipPlugin.prototype.constructor = HtmlTooltipPlugin;
      HtmlTooltipPlugin.prototype.requiredProps = ["id"];
      HtmlTooltipPlugin.prototype.defaultProps = {labels:null,
                                                  hoffset:0,
                                                  voffset:10};
      function HtmlTooltipPlugin(fig, props){
          mpld3.Plugin.call(this, fig, props);
      };

      HtmlTooltipPlugin.prototype.draw = function(){
         var obj = mpld3.get_element(this.props.id);
         var labels = this.props.labels;
         var tooltip = d3.select("body").append("div")
                      .attr("class", "mpld3-tooltip")
                      .style("position", "absolute")
                      .style("z-index", "10")
                      .style("visibility", "hidden");

         obj.elements()
             .on("mouseover", function(d, i){
                                tooltip.html(labels[i])
                                       .style("visibility", "visible");})
             .on("mousemove", function(d, i){
                    tooltip
                      .style("top", d3.event.pageY + this.props.voffset + "px")
                      .style("left",d3.event.pageX + this.props.hoffset + "px");
                   }.bind(this))
             .on("mouseout",  function(d, i){
                             tooltip.style("visibility", "hidden");});
      };

          mpld3.register_plugin("drag", DragPlugin);
          DragPlugin.prototype = Object.create(mpld3.Plugin.prototype);
          DragPlugin.prototype.constructor = DragPlugin;
          DragPlugin.prototype.requiredProps = ["id"];
          DragPlugin.prototype.defaultProps = {}
          function DragPlugin(fig, props){
              mpld3.Plugin.call(this, fig, props);
              mpld3.insert_css("#" + fig.figid + " path.dragging",
                               {"fill-opacity": "1.0 !important",
                                "stroke-opacity": "1.0 !important"});
          };

          DragPlugin.prototype.draw = function(){
              var obj = mpld3.get_element(this.props.id);

              var drag = d3.behavior.drag()
                  .origin(function(d) { return {x:obj.ax.x(d[0]),
                                                y:obj.ax.y(d[1])}; })
                  .on("dragstart", dragstarted)
                  .on("drag", dragged)
                  .on("dragend", dragended);

              obj.elements()
                 .data(obj.offsets)
                 .style("cursor", "default")
                 .call(drag);

              function dragstarted(d) {
                d3.event.sourceEvent.stopPropagation();
                d3.select(this).classed("dragging", true);
              }

              function dragged(d, i) {
                d[0] = obj.ax.x.invert(d3.event.x);
                d[1] = obj.ax.y.invert(d3.event.y);
                d3.select(this)
                  .attr("transform", "translate(" + [d3.event.x,d3.event.y] + ")");
              }

              function dragended(d) {
                d3.select(this).classed("dragging", false);
              }
          }

         mpld3.draw_figure("fig03", resp_final);
    }(mpld3);
})

};



function bidindex(){
  $("#fig02").empty();
  let company = $("#company_value").val()
  console.log(company)


  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH4,{"OutputFromBrowser":company},function(response){

    // set text to response
    var resp = JSON.parse(response);
    // console.log("BREAKER");



    //JSON OBJECT
    var resp_final = JSON.parse(resp);
    !function(mpld3){

      mpld3.register_plugin("htmltooltip", HtmlTooltipPlugin);
      HtmlTooltipPlugin.prototype = Object.create(mpld3.Plugin.prototype);
      HtmlTooltipPlugin.prototype.constructor = HtmlTooltipPlugin;
      HtmlTooltipPlugin.prototype.requiredProps = ["id"];
      HtmlTooltipPlugin.prototype.defaultProps = {labels:null,
                                                  hoffset:0,
                                                  voffset:10};
      function HtmlTooltipPlugin(fig, props){
          mpld3.Plugin.call(this, fig, props);
      };

      HtmlTooltipPlugin.prototype.draw = function(){
         var obj = mpld3.get_element(this.props.id);
         var labels = this.props.labels;
         var tooltip = d3.select("body").append("div")
                      .attr("class", "mpld3-tooltip")
                      .style("position", "absolute")
                      .style("z-index", "10")
                      .style("visibility", "hidden");

         obj.elements()
             .on("mouseover", function(d, i){
                                tooltip.html(labels[i])
                                       .style("visibility", "visible");})
             .on("mousemove", function(d, i){
                    tooltip
                      .style("top", d3.event.pageY + this.props.voffset + "px")
                      .style("left",d3.event.pageX + this.props.hoffset + "px");
                   }.bind(this))
             .on("mouseout",  function(d, i){
                             tooltip.style("visibility", "hidden");});
      };

          mpld3.register_plugin("drag", DragPlugin);
          DragPlugin.prototype = Object.create(mpld3.Plugin.prototype);
          DragPlugin.prototype.constructor = DragPlugin;
          DragPlugin.prototype.requiredProps = ["id"];
          DragPlugin.prototype.defaultProps = {}
          function DragPlugin(fig, props){
              mpld3.Plugin.call(this, fig, props);
              mpld3.insert_css("#" + fig.figid + " path.dragging",
                               {"fill-opacity": "1.0 !important",
                                "stroke-opacity": "1.0 !important"});
          };

          DragPlugin.prototype.draw = function(){
              var obj = mpld3.get_element(this.props.id);

              var drag = d3.behavior.drag()
                  .origin(function(d) { return {x:obj.ax.x(d[0]),
                                                y:obj.ax.y(d[1])}; })
                  .on("dragstart", dragstarted)
                  .on("drag", dragged)
                  .on("dragend", dragended);

              obj.elements()
                 .data(obj.offsets)
                 .style("cursor", "default")
                 .call(drag);

              function dragstarted(d) {
                d3.event.sourceEvent.stopPropagation();
                d3.select(this).classed("dragging", true);
              }

              function dragged(d, i) {
                d[0] = obj.ax.x.invert(d3.event.x);
                d[1] = obj.ax.y.invert(d3.event.y);
                d3.select(this)
                  .attr("transform", "translate(" + [d3.event.x,d3.event.y] + ")");
              }

              function dragended(d) {
                d3.select(this).classed("dragging", false);
              }
          }

         mpld3.draw_figure("fig02", resp_final);
    }(mpld3);
})

};

function bidindex2(){
  $("#fig04").empty();
  let company = $("#company_value2").val()
  var prev_company = company;
  console.log(company)


  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH4,{"OutputFromBrowser":company},function(response){

    // set text to response
    var resp = JSON.parse(response);
    // console.log("BREAKER")


    //JSON OBJECT
    var resp_final = JSON.parse(resp);
    !function(mpld3){

      mpld3.register_plugin("htmltooltip", HtmlTooltipPlugin);
      HtmlTooltipPlugin.prototype = Object.create(mpld3.Plugin.prototype);
      HtmlTooltipPlugin.prototype.constructor = HtmlTooltipPlugin;
      HtmlTooltipPlugin.prototype.requiredProps = ["id"];
      HtmlTooltipPlugin.prototype.defaultProps = {labels:null,
                                                  hoffset:0,
                                                  voffset:10};
      function HtmlTooltipPlugin(fig, props){
          mpld3.Plugin.call(this, fig, props);
      };

      HtmlTooltipPlugin.prototype.draw = function(){
         var obj = mpld3.get_element(this.props.id);
         var labels = this.props.labels;
         var tooltip = d3.select("body").append("div")
                      .attr("class", "mpld3-tooltip")
                      .style("position", "absolute")
                      .style("z-index", "10")
                      .style("visibility", "hidden");

         obj.elements()
             .on("mouseover", function(d, i){
                                tooltip.html(labels[i])
                                       .style("visibility", "visible");})
             .on("mousemove", function(d, i){
                    tooltip
                      .style("top", d3.event.pageY + this.props.voffset + "px")
                      .style("left",d3.event.pageX + this.props.hoffset + "px");
                   }.bind(this))
             .on("mouseout",  function(d, i){
                             tooltip.style("visibility", "hidden");});
      };

          mpld3.register_plugin("drag", DragPlugin);
          DragPlugin.prototype = Object.create(mpld3.Plugin.prototype);
          DragPlugin.prototype.constructor = DragPlugin;
          DragPlugin.prototype.requiredProps = ["id"];
          DragPlugin.prototype.defaultProps = {}
          function DragPlugin(fig, props){
              mpld3.Plugin.call(this, fig, props);
              mpld3.insert_css("#" + fig.figid + " path.dragging",
                               {"fill-opacity": "1.0 !important",
                                "stroke-opacity": "1.0 !important"});
          };

          DragPlugin.prototype.draw = function(){
              var obj = mpld3.get_element(this.props.id);

              var drag = d3.behavior.drag()
                  .origin(function(d) { return {x:obj.ax.x(d[0]),
                                                y:obj.ax.y(d[1])}; })
                  .on("dragstart", dragstarted)
                  .on("drag", dragged)
                  .on("dragend", dragended);

              obj.elements()
                 .data(obj.offsets)
                 .style("cursor", "default")
                 .call(drag);

              function dragstarted(d) {
                d3.event.sourceEvent.stopPropagation();
                d3.select(this).classed("dragging", true);
              }

              function dragged(d, i) {
                d[0] = obj.ax.x.invert(d3.event.x);
                d[1] = obj.ax.y.invert(d3.event.y);
                d3.select(this)
                  .attr("transform", "translate(" + [d3.event.x,d3.event.y] + ")");
              }

              function dragended(d) {
                d3.select(this).classed("dragging", false);
              }
          }

         mpld3.draw_figure("fig04", resp_final);
    }(mpld3);
})

};



function dbsearch(){
  $('#id').empty()
  $('#title').empty()
  $('#agency').empty()
  $('#publisheddate').empty()
  $('#procurementtype').empty()
  $('#quotationtype').empty()
  $('#procurementcategory').empty()
  $('#tenderclosing').empty()
  $('#respondents').empty()
  $('#awardedto').empty()
  let value = $("#proj_input").val();
  type = $("#proj_search").val() // type of search , via ID or Title
	query = $('#proj_input').val() // searches

	// Create Query parameters
	var jsonParameters = {'OutputFromBrowser':{'type':type,'query':query,"exact":0}}

	// Make get request
	makeAjaxRequest(URLFETCH5,jsonParameters,function(response){

		console.log("dbsearch response is:"+response)
		final_resp = JSON.parse(JSON.parse(response))

    var result = final_resp[0]

    var id = result._id;
    var title = result.Title;
    var agency = result.Agency;
    var pubdate = result.PublishedDate;
    var qtntype = result.QuotationType;
    var proccat = result.ProcurementCategory;
    var proctype = result.ProcurementType;
    var closingdate = result.TenderClosingDate;
    var respondents = result.Respondents;
    var winner = result.Awards[0]["AwardedTo"]
    var winning_amt = result.Awards[0]["AwardedValue"]


    $("#id").text(id);
    $("#title").text(title)
    $("#agency").text(agency)
    $("#publisheddate").text(pubdate)
    $("#procurementtype").text(proctype)
    $("#quotationtype").text(qtntype);
    $("#procurementcategory").text(proccat)
    $("#tenderclosing").text(closingdate)

    $("#awardedto").text(winner+"for winning amount of: $"+winning_amt)


    var all_resp =""

    // for(var i = 0;i <Object.values(respondents).length; i++){
    //   i+=1
    // }
    for (var i = 0; i <Object.values(respondents).length; i++) {
      var company_name = Object.values(respondents)[i]["CompanyName"]
      var price = Object.values(respondents)[i]["TotalPrice"]


      $("#respondents").append("<li><span class='fake-link'>" + company_name + "</span> with a price of: "+ price +"</li>")
      // var item = Object.values(respondents[i])
      // var company_name = item[i]
      // // var value = item[i]["AwardedTo"]
      // all_resp +=  company_name + value

    }
    // $("#respondents").innerHTML(all_resp)
})

};


function company1_details(){
  var company = $("#company_value").val()
  console.log(company)
  var Company = company.toUpperCase();
  $('#company1name').text(Company);

  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH6,{"OutputFromBrowser":company},function(response){

    console.log("response from python:" + response);
    // set text to response
    var resp = JSON.parse(response);
    // console.log("BREAKER");
    console.log("response after being parsed:" + resp);


    //JSON OBJECT
    var resp_final = JSON.parse(resp);


    var bid = resp_final['winRate'][0];
    var wins = resp_final['winRate'][1];
    var winrate = resp_final['winRate'][2];
    var totalbid = resp_final['totalSum'][0];
    var valwon  =  resp_final['totalSum'][1];
    var bidrange = "Between"+ '$'+resp_final['bidRange'][0]+' and $'+resp_final['bidRange'][1];
    var fg = resp_final['fg']
    // $('#company2name').text(company);
    $("#company1_bid").text(bid);
    $("#company1_wins").text(wins);
    $("#company1_winrate").text(winrate);
    $("#company1_totalbid").text("$" + totalbid);
    $("#company1_valwon").text(valwon);
    $("#company1_bidrange").text(bidrange);
    $("#fg1").text(fg);
}
)};



function company2_details(){
  let company = $("#company_value2").val()
  console.log(company)
  var Company = company.toUpperCase();
  $('#company2name').text(Company);

  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH6,{"OutputFromBrowser":company},function(response){

    console.log("response from python for company 2:" + response);
    // set text to response
    var resp = JSON.parse(response);
    // console.log("BREAKER");
    console.log("response after being parsed for company 2:" + resp);


    //JSON OBJECT
    var resp_final = JSON.parse(resp);


    var bid = resp_final['winRate'][0];
    var wins = resp_final['winRate'][1];
    var winrate = resp_final['winRate'][2];
    var totalbid = resp_final['totalSum'][0];
    var valwon  =  resp_final['totalSum'][1];
    var bidrange = "Between"+ '$'+resp_final['bidRange'][0]+' and $'+resp_final['bidRange'][1];
    var fg = resp_final['fg'];

    $("#company2_bid").text(bid);
    $("#company2_wins").text(wins);
    $("#company2_winrate").text(winrate);
    $("#company2_totalbid").text("$" + totalbid);
    $("#company2_valwon").text(valwon);
    $("#company2_bidrange").text(bidrange);
    $("#fg2").text(fg);
}

)};



function agencyplot(){
  $("#AgencyPlot").empty();
	var agency = $("#agency").val()
	// Create Query Parameters

  makeAjaxRequest(URLFETCH7,{"OutputFromBrowser":agency},function(response){

    // set text to response
    var resp = JSON.parse(response);

    //JSON OBJECT
    var resp_final = JSON.parse(resp);
    !function(mpld3){

      mpld3.register_plugin("htmltooltip", HtmlTooltipPlugin);
      HtmlTooltipPlugin.prototype = Object.create(mpld3.Plugin.prototype);
      HtmlTooltipPlugin.prototype.constructor = HtmlTooltipPlugin;
      HtmlTooltipPlugin.prototype.requiredProps = ["id"];
      HtmlTooltipPlugin.prototype.defaultProps = {labels:null,
                                                  hoffset:0,
                                                  voffset:10};
      function HtmlTooltipPlugin(fig, props){
          mpld3.Plugin.call(this, fig, props);
      };

      HtmlTooltipPlugin.prototype.draw = function(){
         var obj = mpld3.get_element(this.props.id);
         var labels = this.props.labels;
         var tooltip = d3.select("body").append("div")
                      .attr("class", "mpld3-tooltip")
                      .style("position", "absolute")
                      .style("z-index", "10")
                      .style("visibility", "hidden");

         obj.elements()
             .on("mouseover", function(d, i){
                                tooltip.html(labels[i])
                                       .style("visibility", "visible");})
             .on("mousemove", function(d, i){
                    tooltip
                      .style("top", d3.event.pageY + this.props.voffset + "px")
                      .style("left",d3.event.pageX + this.props.hoffset + "px");
                   }.bind(this))
             .on("mouseout",  function(d, i){
                             tooltip.style("visibility", "hidden");});
      };

          mpld3.register_plugin("drag", DragPlugin);
          DragPlugin.prototype = Object.create(mpld3.Plugin.prototype);
          DragPlugin.prototype.constructor = DragPlugin;
          DragPlugin.prototype.requiredProps = ["id"];
          DragPlugin.prototype.defaultProps = {}
          function DragPlugin(fig, props){
              mpld3.Plugin.call(this, fig, props);
              mpld3.insert_css("#" + fig.figid + " path.dragging",
                               {"fill-opacity": "1.0 !important",
                                "stroke-opacity": "1.0 !important"});
          };

          DragPlugin.prototype.draw = function(){
              var obj = mpld3.get_element(this.props.id);

              var drag = d3.behavior.drag()
                  .origin(function(d) { return {x:obj.ax.x(d[0]),
                                                y:obj.ax.y(d[1])}; })
                  .on("dragstart", dragstarted)
                  .on("drag", dragged)
                  .on("dragend", dragended);

              obj.elements()
                 .data(obj.offsets)
                 .style("cursor", "default")
                 .call(drag);

              function dragstarted(d) {
                d3.event.sourceEvent.stopPropagation();
                d3.select(this).classed("dragging", true);
              }

              function dragged(d, i) {
                d[0] = obj.ax.x.invert(d3.event.x);
                d[1] = obj.ax.y.invert(d3.event.y);
                d3.select(this)
                  .attr("transform", "translate(" + [d3.event.x,d3.event.y] + ")");
              }

              function dragended(d) {
                d3.select(this).classed("dragging", false);
              }
          }
         mpld3.draw_figure("AgencyPlot", resp_final);
    }(mpld3);
})

};

function agencydetails(){
  $("#top3bynum").empty()
  $("#top3byval").empty()
  let title = $("#agency").val()
  $('#agencyname').text($("#agency").val().toUpperCase())

  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH8,{"OutputFromBrowser":title},function(response){

    // console.log(response);
    // set text to response
    var resp = JSON.parse(response);
    // console.log("BREAKER");
    // console.log(resp);
    var resp_final = JSON.parse(resp);
    console.log(resp)
    awarded_count = resp_final.totalAwards;
    total_value = resp_final.totalValue;
    avg_value = resp_final.avgValue;
    plowest = resp_final.pLowest;
    tendency = resp_final.tendency
    $('#awarded_proj_count').text(awarded_count)
    $('#total_award').text("$"+total_value)
    $('#avg_award').text("$"+avg_value)
    $('#lowestprob').text(plowest)
    $('#tendency').text(tendency)

    result = JSON.parse(JSON.parse(response))
		var data = JSON.parse(result.data)


		var AwardValue = []
		var details = ""
		var counts = {}
		var value = {}

		// parse data
		data.forEach(function(d){
			AwardValue.push(parseFloat(d.AwardedValue))
			if(counts.hasOwnProperty(d.AwardedTo)){
				counts[d.AwardedTo] += 1
				value[d.AwardedTo] += d.AwardedValue
			}
			else{
				counts[d.AwardedTo] = 1
				value[d.AwardedTo] = d.AwardedValue
			}
		})
		console.log(AwardValue)

		// Sort the data by total num and total value
		var keysSorted = Object.keys(counts).sort(function(a,b){return counts[b]-counts[a]})
		var keysSortedVal = Object.keys(value).sort(function(a,b){return value[b]-value[a]})
		data.sort(function(a, b){
		    return keysSorted.indexOf(a.AwardedTo) - keysSorted.indexOf(b.AwardedTo)
		});

		// Append data into a table like display (bottom of agency Detail page)
		var tracker = 0
		var tddetail =""
		data.forEach(function(d){
			if(d.AwardedTo == tracker){
				details += "<li><span class='fake-link' onclick='popoutProjectD(this)'>" + d.Title + "</span> for $" + d.AwardedValue +"</li>"
			}
			else if(tracker == 0){
				tracker = d.AwardedTo
				details += "<tr style='text-transform: capitalize'><td><span <span class='fake-link' onclick='companyDetail(button = false,elem=this)'>"+ tracker +"</span></td>\
			<td><ol><li><span class='fake-link'>" + d.Title + "</span> for $" + d.AwardedValue +"</li>"
			}
			else{
				tracker = d.AwardedTo
				details += "</ol></td></tr><tr style='text-transform: capitalize'><td><span <span class='fake-link' onclick='companyDetail(button = false,elem=this)'>"+ tracker +"</span></td>\
			<td><ol><li><span class='fake-link'>" + d.Title + "</span> for $" + d.AwardedValue +"</li>"
			}
		})

		details += "</ol></td></tr>"


		// Append top3 informations
		var top3bynum = ""
		var top3byvalue =""
		for (var i = 0; i <3; i++) {
			top3bynum += "<li><span class='fake-link' onclick='companyDetail(button = false,elem=this)'>" + keysSorted[i].toUpperCase() + "</span> with  "+ counts[keysSorted[i]]+" projects</li>"
			top3byvalue += "<li><span class='fake-link' onclick='companyDetail(button = false,elem=this)'>" + keysSortedVal[i].toUpperCase() + "</span> with  $"+ value[keysSortedVal[i]]+" </li>"
		}

  $("#top3bynum").append(top3bynum);
  $("#top3byval").append(top3byvalue);
})
};

function bulksearch(){
  $("#awardedto").empty()
  $("#id").empty()
  $("#title").empty()
  $("#agency").empty()
  $("#publisheddate").empty()
  $("#procurementtype").empty()
  $("#quotationtype").empty()
  $("#tenderclosing").empty()
  $("#awardeddate").empty()
  $("#no_awarded").empty()
  $("#proc_cat").empty()
  $("#qtn_num").empty()

	let query = $('#bulk').val() // searches
	// Create Query parameters
  console.log(query)
	var jsonParameters = {'OutputFromBrowser':query}

	// Make get request
	makeAjaxRequest(URLFETCH9,jsonParameters,function(response){

		console.log("bulk_tenders response is:"+response)
		result = JSON.parse(JSON.parse(response))

    // var result = final_resp[0]

    var id = result._id;
    var title = result.title;
    var agency = result.agency;
    var pubdate = result.pdate;
    var qtntype = result.qtype;
    var proctype = result.ptype;
    var closingdate = result.cdate;
    var quotationnumber = result.qno
    var awardeddate = result.date;
    var no_awarded = result.no_awarded;
    var procurementmethod = result.method;
    var awardeddate = result.date;
    var pcategory = result.pcat;
    // var respondents = result.Respondents;
    var winners = result.awards
    var keys = Object.keys(winners)
    // var winning_amt = result.Awards[0]["AwardedValue"]
    var winnerstring = ""
    for (var i =0; i <keys.length; i++){
      var entry = winners[i]
      var awardedto = entry["AwardedTo"]
      var awardedval = entry["AwardedValue"]

      winnerstring += "<li><span class='fake-link'>" + awardedto + "</span> for "+ awardedval +"</li>"
    }


    $("#id").text(id);
    $("#title").text(title)
    $("#agency").text(agency)
    $("#publisheddate").text(pubdate)
    $("#procurementtype").text(proctype)
    $("#quotationtype").text(qtntype);
    $("#tenderclosing").text(closingdate)
    $("#tenderclosing").text(closingdate)
    $("#awardeddate").text(awardeddate)
    $("#no_awarded").text(no_awarded)
    $("#qtn_num").text(quotationnumber)
    $("#proc_cat").text(pcategory)
    $("#awardedto").append(winnerstring)

    // var all_resp =""
    //
    // // for(var i = 0;i <Object.values(respondents).length; i++){
    // //   i+=1
    // // }
    // for (var i = 0; i <Object.values(respondents).length; i++) {
    //   var company_name = Object.values(respondents)[i]["CompanyName"]
    //   var price = Object.values(respondents)[i]["TotalPrice"]
    //
    //
    //   $("#respondents").append("<li><span class='fake-link'>" + company_name + "</span> with a price of: "+ price +"</li>")
    //   // var item = Object.values(respondents[i])
    //   // var company_name = item[i]
    //   // // var value = item[i]["AwardedTo"]
    //   // all_resp +=  company_name + value
    //
    // }
    // $("#respondents").innerHTML(all_resp)
})

};

function setintropage(){
  let category = $("#categoryselect").val()
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH10,{"OutputFromBrowser":category},function(response){

    // console.log(response);
    // set text to response
    var resp = JSON.parse(response);
    console.log(resp)
    var resp_final = JSON.parse(resp);
    var final = resp_final[0]
    var final2 = resp_final[1]
    var final3 = resp_final[2]
    var final4 = resp_final[3]
    var final5 = resp_final[4]

    $('#c_val_1').text(final5.mc5[0][0].toUpperCase()+"    With Total Awarded Value of :   "+ final5.mc5[0][1])
    $('#c_val_2').text(final5.mc5[1][0].toUpperCase()+"    With Total Awarded Value of :   "+ final5.mc5[1][1])
    $('#c_val_3').text(final5.mc5[2][0].toUpperCase()+"    With Total Awarded Value of :   "+ final5.mc5[2][1])
    // $('#c_val_4').text(final5.mc5[3][0].toUpperCase()+"    With Total Awarded Value of :   "+ final5.mc5[3][1])
    // $('#c_val_5').text(final5.mc5[4][0].toUpperCase()+"    With Total Awarded Value of :   "+ final5.mc5[4][1])


    $('#c_count_1').text(final4.mc4[0][0].toUpperCase()+"    With Project Count of :   "+ final4.mc4[0][1])
    $('#c_count_2').text(final4.mc4[1][0].toUpperCase()+"    With Project Count of :   "+ final4.mc4[1][1])
    $('#c_count_3').text(final4.mc4[2][0].toUpperCase()+"    With Project Count of :   "+ final4.mc4[2][1])
    // $('#c_count_4').text(final4.mc4[3][0].toUpperCase()+"    With Project Count of :   "+ final4.mc4[3][1])
    // $('#c_count_5').text(final4.mc4[4][0].toUpperCase()+"    With Project Count of :   "+ final4.mc4[4][1])


   $('#a_val_1').text(final3.mc3[0][0].toUpperCase()+"    With Total Awarded Value of :   "+ final3.mc3[0][1])
   $('#a_val_2').text(final3.mc3[1][0].toUpperCase()+"    With Total Awarded Value of :   "+ final3.mc3[1][1])
   $('#a_val_3').text(final3.mc3[2][0].toUpperCase()+"    With Total Awarded Value of :   "+ final3.mc3[2][1])
   // $('#a_val_4').text(final3.mc3[3][0].toUpperCase()+"    With Total Awarded Value of :   "+ final3.mc3[3][1])
   // $('#a_val_5').text(final3.mc3[4][0].toUpperCase()+"    With Total Awarded Value of :   "+ final3.mc3[4][1])


   $('#a_count_1').text(final2.mc2[0][0].toUpperCase()+"    With Project Count of :   "+ final2.mc2[0][1])
   $('#a_count_2').text(final2.mc2[1][0].toUpperCase()+"    With Project Count of :   "+ final2.mc2[1][1])
   $('#a_count_3').text(final2.mc2[2][0].toUpperCase()+"    With Project Count of :   "+ final2.mc2[2][1])
   // $('#a_count_4').text(final2.mc2[3][0].toUpperCase()+"    With Project Count of :   "+ final2.mc2[3][1])
   // $('#a_count_5').text(final2.mc2[4][0].toUpperCase()+"    With Project Count of :   "+ final2.mc2[4][1])

   $("#topval1").text(final.top1[0]);
   $("#topagency1").text(final.top1[1].toUpperCase());
   $("#awardedto1").text(final.top1[2].toUpperCase())
   $("#awarded1").text(final.top1[3].toUpperCase())
   $("#pcat1").text(final.top1[4].toUpperCase())
   $("#pmethod1").text(final.top1[5].toUpperCase())
   $("#ptype1").text(final.top1[6].toUpperCase())
   $("#id1").text(final.top1[7].toUpperCase())
   $("#title1").text(final.top1[8].toUpperCase())

   $("#topval2").text(final.top_2[0]);
   $("#topagency2").text(final.top_2[1].toUpperCase());
   $("#awardedto2").text(final.top_2[2].toUpperCase())
   $("#awarded2").text(final.top_2[3].toUpperCase())
   $("#pcat2").text(final.top_2[4].toUpperCase())
   $("#pmethod2").text(final.top_2[5].toUpperCase())
   $("#ptype2").text(final.top_2[6].toUpperCase())
   $("#id2").text(final.top_2[7].toUpperCase())
   $("#title2").text(final.top_2[8].toUpperCase())

   $("#topval3").text(final.top3[0]);
   $("#topagency3").text(final.top3[1].toUpperCase());
   $("#awardedto3").text(final.top3[2].toUpperCase())
   $("#awarded3").text(final.top3[3].toUpperCase())
   $("#pcat3").text(final.top3[4].toUpperCase())
   $("#pmethod3").text(final.top3[5].toUpperCase())
   $("#ptype3").text(final.top3[6].toUpperCase())
   $("#id3").text(final.top3[7].toUpperCase())
   $("#title3").text(final.top3[8].toUpperCase())
})
};


function introplot1(){
  let category = $("#categoryselect").val()
  console.log(category)
  console.log('./pygal/'+category+'.svg')
  $("#competing_companies").empty()
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH11,{"OutputFromBrowser":category},function(response){
    document.getElementById("introplot").setAttribute('data','./pygal/'+category+'.svg');
    // console.log(response)
    // console.log(typeof(response));
    // // set text to response
    // var resp = JSON.parse(response);
    // console.log(resp)
    // var resp_final = JSON.parse(resp);
})
};

function agencypie(){
  var agency = $("#agency").val()
  console.log(agency)
  console.log('./pygal/'+agency+'.svg')
  // $("#competing_companies").empty()
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH12,{"OutputFromBrowser":agency},function(response){
    document.getElementById("AgencyPiePlot").setAttribute('data','./pygal/'+agency+'.svg');
    // console.log(response)
    // console.log(typeof(response));
    // // set text to response
    // var resp = JSON.parse(response);
    // console.log(resp)
    // var resp_final = JSON.parse(resp);
})
};


function agency_bar(){
  $("#agency_bar_plot").empty();
  let agency = $("#agency").val()
  let year = $('#year').val()

  console.log('ths is the agency' + agency)
  console.log(year)
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH14,{"OutputFromBrowser":agency,'year':year},function(response){
    document.getElementById("agency_bar_plot").setAttribute('data','./pygal/'+agency+'bar.svg');
})
};


function agency_line(){
  $("#agency_line_plot").empty();
  let agency = $("#agency").val()

  console.log(agency)

  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH15,{"OutputFromBrowser":agency},function(response){

    // set text to response
    var resp = JSON.parse(response);
    // console.log("BREAKER");


    //JSON OBJECT
    var resp_final = JSON.parse(resp);
    !function(mpld3){

      mpld3.register_plugin("htmltooltip", HtmlTooltipPlugin);
      HtmlTooltipPlugin.prototype = Object.create(mpld3.Plugin.prototype);
      HtmlTooltipPlugin.prototype.constructor = HtmlTooltipPlugin;
      HtmlTooltipPlugin.prototype.requiredProps = ["id"];
      HtmlTooltipPlugin.prototype.defaultProps = {labels:null,
                                                  hoffset:0,
                                                  voffset:10};
      function HtmlTooltipPlugin(fig, props){
          mpld3.Plugin.call(this, fig, props);
      };

      HtmlTooltipPlugin.prototype.draw = function(){
         var obj = mpld3.get_element(this.props.id);
         var labels = this.props.labels;
         var tooltip = d3.select("body").append("div")
                      .attr("class", "mpld3-tooltip")
                      .style("position", "absolute")
                      .style("z-index", "10")
                      .style("visibility", "hidden");

         obj.elements()
             .on("mouseover", function(d, i){
                                tooltip.html(labels[i])
                                       .style("visibility", "visible");})
             .on("mousemove", function(d, i){
                    tooltip
                      .style("top", d3.event.pageY + this.props.voffset + "px")
                      .style("left",d3.event.pageX + this.props.hoffset + "px");
                   }.bind(this))
             .on("mouseout",  function(d, i){
                             tooltip.style("visibility", "hidden");});
      };

          mpld3.register_plugin("drag", DragPlugin);
          DragPlugin.prototype = Object.create(mpld3.Plugin.prototype);
          DragPlugin.prototype.constructor = DragPlugin;
          DragPlugin.prototype.requiredProps = ["id"];
          DragPlugin.prototype.defaultProps = {}
          function DragPlugin(fig, props){
              mpld3.Plugin.call(this, fig, props);
              mpld3.insert_css("#" + fig.figid + " path.dragging",
                               {"fill-opacity": "1.0 !important",
                                "stroke-opacity": "1.0 !important"});
          };

          DragPlugin.prototype.draw = function(){
              var obj = mpld3.get_element(this.props.id);

              var drag = d3.behavior.drag()
                  .origin(function(d) { return {x:obj.ax.x(d[0]),
                                                y:obj.ax.y(d[1])}; })
                  .on("dragstart", dragstarted)
                  .on("drag", dragged)
                  .on("dragend", dragended);

              obj.elements()
                 .data(obj.offsets)
                 .style("cursor", "default")
                 .call(drag);

              function dragstarted(d) {
                d3.event.sourceEvent.stopPropagation();
                d3.select(this).classed("dragging", true);
              }

              function dragged(d, i) {
                d[0] = obj.ax.x.invert(d3.event.x);
                d[1] = obj.ax.y.invert(d3.event.y);
                d3.select(this)
                  .attr("transform", "translate(" + [d3.event.x,d3.event.y] + ")");
              }

              function dragended(d) {
                d3.select(this).classed("dragging", false);
              }
          }

         mpld3.draw_figure("agency_line_plot", resp_final);
    }(mpld3);
})

};

function companywhisker(){
  let company = $("#company_value").val()
  // $("#competing_companies").empty()
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH16,{"OutputFromBrowser":company},function(response){
    document.getElementById("company_whisker_plot").setAttribute('data','./pygal/'+company+'box&whisker.svg');
    // console.log(response)
    // console.log(typeof(response));
    // // set text to response
    // var resp = JSON.parse(response);
    // console.log(resp)
    // var resp_final = JSON.parse(resp);
})
};

function companywhisker2(){
  let company = $("#company_value2").val()
  // $("#competing_companies").empty()
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH16,{"OutputFromBrowser":company},function(response){
    document.getElementById("company_whisker_plot2").setAttribute('data','./pygal/'+company+'box&whisker.svg');
    // console.log(response)
    // console.log(typeof(response));
    // // set text to response
    // var resp = JSON.parse(response);
    // console.log(resp)
    // var resp_final = JSON.parse(resp);
})
};

function companybar(){
  let company = $("#company_value").val()
  let year = $("#company_years").val()
  // $("#competing_companies").empty()
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH17,{"OutputFromBrowser":company,"year":year},function(response){
    document.getElementById("company_bar_plot").setAttribute('data','./pygal/'+company+'bar_plot.svg');
    // console.log(response)
    // console.log(typeof(response));
    // // set text to response
    // var resp = JSON.parse(response);
    // console.log(resp)
    // var resp_final = JSON.parse(resp);
})
};

function companybar2(){
  let company = $("#company_value2").val()
  let year = $("#company_years2").val()
  // $("#competing_companies").empty()
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH17,{"OutputFromBrowser":company,"year":year},function(response){
    document.getElementById("company_bar_plot2").setAttribute('data','./pygal/'+company+'bar_plot.svg');
    // console.log(response)
    // console.log(typeof(response));
    // // set text to response
    // var resp = JSON.parse(response);
    // console.log(resp)
    // var resp_final = JSON.parse(resp);
})
};
function setcategory(){
  let agency = $("#agency").val()
  let year = $('#year_filter').val()

  makeAjaxRequest(URLFETCH18,{"OutputFromBrowser":agency,'year':year},function(response){
    var resp = JSON.parse(response);
    console.log('procurement categories are' +resp)
    var resp_final = JSON.parse(resp);

    var cats = resp_final.cats;

    for (var i=0; i<cats.length; i++){
      $('#category_filter').append('<option>'+cats[i].toUpperCase()+'</option>')
    };
    // console.log(response)
    // console.log(typeof(response));
    // // set text to response
    // var resp = JSON.parse(response);
    // console.log(resp)
    // var resp_final = JSON.parse(resp);
})
};

function agency_gauge(){
  let agency = $("#agency").val()
  let year = $("#year_filter").val()
  let proc_cat = $('#category_filter').val()
  console.log('LOOK HERE' +proc_cat)
  // $("#competing_companies").empty()
  //Here, we are sending the JSON object with OutputFromBrowser as the key to the value title.
  makeAjaxRequest(URLFETCH19,{"OutputFromBrowser":agency,"year":year,"proc_cat":proc_cat},function(response){
    console.log('loaded?')
    document.getElementById("agency_gauge_plot").setAttribute('data','./pygal/'+agency+'gauge_plot.svg');
    // console.log(response)
    // console.log(typeof(response));
    // // set text to response
    // var resp = JSON.parse(response);
    // console.log(resp)
    // var resp_final = JSON.parse(resp);
})
};
