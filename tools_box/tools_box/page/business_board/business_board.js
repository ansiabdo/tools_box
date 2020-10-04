// var prev_year;
// var cur_year;

frappe.pages['business_board'].on_page_load = function(wrapper) {
	this.page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Sales Analytics',
		single_column: true,
		// btn: set_secondary_action('Refresh', () => refresh(), 'octicon octicon-sync')


	});
	// add a standard menu item
	// this.page.add_menu_item('Send Email', () => open_email_dialog(), true)
	//this.page.set_secondary_action('Refresh', () => refresh(), 'octicon octicon-sync');
	//let $btn = this.page.set_secondary_action('Refresh', () => refresh(), 'octicon octicon-sync');
	// let $btn = this.page.set_secondary_action('Refresh', () => refresh(), 'octicon octicon-sync');
	window.year_form = '\
		<div class="container">\
			  <h2>GRACECO LIMITED SALES BY MONTH COMPARISON CHART</h2>\
			  <p>Select year below to create chart.</p>\
			  <form class="form-inline" action="javascript:void(0);">\
			        <div class="form-group">\
				      <label for="year1">Year1:</label>\
				      <select name="year1" class="form-control" id="year1">\
				      <option value="2021">2021</option>\
				      <option value="2020">2020</option>\
				      <option value="2019" selected>2019</option>\
				      <option value="2018">2018</option>\
				      <option value="2017">2017</option>\
				      </select>\
				    </div>\
			        <div class="form-group">\
				      <label for="year2">Year2:</label>\
				      <select name="year2" class="form-control" id="year2">\
				      <option value="2021">2021</option>\
				      <option value="2020" selected>2020</option>\
				      <option value="2019">2019</option>\
				      <option value="2018">2018</option>\
				      <option value="2017">2017</option>\
				      </select>\
				    </div>\
				    <button class="btn btn-default" onclick="window.get_form_data()">Submit</button>\
				    <div class="form-group text-right">\
				    	<button class="btn btn-primary" onclick="window.sales_by_month.export();">Export</button>\
				    </div>\
			  </form>\
			</div>\
	';

	window.territory_form = '\
		<div class="container">\
				<h2>SALES BY TERRITORY CHART</h2>\
				<p>Select year below to create chart.</p>\
				<form class="form-inline" action="javascript:void(0);">\
							<div class="form-group">\
							<label for="year1">Year:</label>\
							<select name="year1" class="form-control" id="territory_form_data" onchange="window.get_sales_by_territory_data();">\
							<option value="2021">2021</option>\
							<option value="2020" selected>2020</option>\
							<option value="2019">2019</option>\
							<option value="2018">2018</option>\
							<option value="2017">2017</option>\
							</select>\
						</div>\
								<!--<button class="btn btn-default" onclick="window.get_sales_by_territory_data()">Submit</button>-->\
						<div class="form-group text-right">\
							<button class="btn btn-primary" onclick="window.sales_by_territory.export()">Export</button>\
						</div>\
				</form>\
			</div>\
	';

	window.revenue_form = '\
		<div class="container">\
				<h2>SALES BY REVENUE CENTER CHART</h2>\
				<p>Select year below to create chart.</p>\
				<form class="form-inline" action="javascript:void(0);">\
							<div class="form-group">\
							<label for="year1">Year:</label>\
							<select name="year1" class="form-control" id="revenue_form_data" onchange="window.get_sales_by_revenue_data();">\
							<option value="2021">2021</option>\
							<option value="2020" selected>2020</option>\
							<option value="2019">2019</option>\
							<option value="2018">2018</option>\
							<option value="2017">2017</option>\
							</select>\
						</div>\
								<!--<button class="btn btn-default" onclick="window.get_sales_by_revenue_data()">Submit</button>-->\
						<div class="form-group text-right">\
							<button class="btn btn-primary" onclick="window.sales_by_revenue.export()">Export</button>\
						</div>\
				</form>\
			</div>\
	';


window.formatter = new Intl.NumberFormat('en-NG', {
		style: 'currency',
		currency: 'NGN',
			});

	$(frappe.render_template(window.year_form + '<div id="sales_by_month"></div><hr>' /*+ window.territory_form + '<div id="territory_chart"></div><hr>\
	' + window.revenue_form */ + '<div id="revenue_chart"></div><hr>', this.page)).prependTo($('.layout-main'));




    ///////////////////////////////////////////////////
		//TEST BLOCK
		//////////////////////////////////////////////////
		// frappe.call({
    // method: "tools_box.tools_box.page.business_board.business_board_revenue_analytics.get_territory_sales_analytics", //dotted path to server method
		// args: {
		// 	year: 2019,
		// 	// year2: 2019
		// },
		// callback: function(r) {
		// 	console.log(r);
    //     // code snippet
	  //   }
		// })

		///////////////////////////////////////////////////
		// MONTHLY SALES
		//////////////////////////////////////////////////
	window.get_form_data = function(){
		var year1 = document.getElementById('year1').value;
		var year2 = document.getElementById('year2').value;
		if(year1 === year2){
			alert("year should not be same.");
		} else {
		window.frappe_function_call(year1, year2);
		// return [year1.value, year2.value];
		}
	};


	window.frappe_function_call = function(year1, year2){
	frappe.call({
    method: "tools_box.tools_box.page.business_board.business_board_revenue_analytics.get_analytics_by_month", //dotted path to server method
    args: {
        year1: year1,
        year2: year2,
    },
    callback: function(r) {
        // code snippet
				// console.log(r['message'].sum_pre_year[0]['sum(grand_total)']);
				window.prev_year = r['message'][0].monthly_data;
				window.cur_year = r['message'][1].monthly_data;
				window.prev_year_total = r['message'][0].revenue;
				window.cur_year_total = r['message'][1].revenue;

	// alert(window.prev_year);
	window.sales_by_month = new frappe.Chart( "#sales_by_month", { // or DOM element
	data: {
	labels: ["Jan", "Feb", "Mar", "Apr",
		"May", "Jun", "Jul", "Aug", "sep", "Oct", "Nov", "Dec"],

	datasets: [
		{
			name: year1.toString(), chartType: 'bar',
			values: window.prev_year //[13.598543311000002, 16.634005808, 16.746215782, 17.428022391, 18.596850557, 13.298477978, 21.620331215, 16.798215305000003, 13.019099271, 21.826471183000002, 19.949361703, 21.683302756] //[prev_year] //[25, 40, 30, 35, 8, 52, 17, 5, 10, 6, 12, 45]
		},
		{
			name: year2.toString(), chartType: 'bar',
			values: window.cur_year //[12.062496003, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] //[25, 50, 10, 15, 18, 32, 27, 14, 35, 8, 52, 17]
		}

		// ,
		// {
		// 	name: "Yet Another", chartType: 'line',
		// 	values: [15, 20, 3, 15, 58, 12, 17, 37]
		// }
	],

	yMarkers: [{ label: "Marker", value: 250,
		options: { labelPos: 'left' }}],
	yRegions: [{ label: "Region", start: 0, end: 280,
		options: { labelPos: 'right' }}]
	},

	title: "Graceco " + year1 + "/" + year2 + " Sales Analytics. " + year1 + " :" + formatter.format(window.prev_year_total) +"; " + year2 + ": " + formatter.format(window.cur_year_total),
	type: 'axis-mixed', // or 'bar', 'line', 'pie', 'percentage'
	height: 500,
	colors: ['blue', 'red'],

	tooltipOptions: {
		formatTooltipX: d => (d + '').toUpperCase(),
		formatTooltipY: d => d + ' MN',
	}
	});
	},
	error: function(r){
		alert("Error: Please check your internet connection.");
	},
	})
	};


///////////////////////////////////////////////////
// SALES BY TERRITORY
//////////////////////////////////////////////////


window.get_sales_by_territory_data = function(){
	// var territory_data = document.getElementById('territory_form_data').value;

	window.territory_function_call(document.getElementById('territory_form_data').value);
	// return [year1.value, year2.value];
};

window.territory_function_call = function(year){
frappe.call({
	method: "tools_box.tools_box.page.business_board.business_board_revenue_analytics.get_territory_sales_analytics", //dotted path to server method
	args: {
			year: year
	},
	callback: function(r) {
			// console.log(r);
			window.territory_sum = r['message'][1];
			window.territory_data_list = r['message'][0];

// alert(window.prev_year);
window.sales_by_territory = new frappe.Chart( "#territory_chart", { // or DOM element
data: {
labels: ["Lagos", "South West", "South South", "South East", "North", "International"],

datasets: [
	{
		name: year.toString(), chartType: 'bar',
		values: window.territory_data_list //[13.598543311000002, 16.634005808, 16.746215782, 17.428022391, 18.596850557, 13.298477978, 21.620331215, 16.798215305000003, 13.019099271, 21.826471183000002, 19.949361703, 21.683302756] //[prev_year] //[25, 40, 30, 35, 8, 52, 17, 5, 10, 6, 12, 45]
	}
],

yMarkers: [{ label: "Marker", value: 2.0,
	options: { labelPos: 'left' }}],
yRegions: [{ label: "Region", start: 0, end: 2.5,
	options: { labelPos: 'right' }}]
},

title: "Sales by Territory  Analytics. " + year + " :" + formatter.format(window.territory_sum) +"; ",
type: 'axis-mixed', // or 'bar', 'line', 'pie', 'percentage'
height: 300,
colors: ['blue'],

tooltipOptions: {
	formatTooltipX: d => (d + '').toUpperCase(),
	formatTooltipY: d => d + ' BN',
}
});
},
error: function(r){
	alert("Error: Please check your internet connection.");
},
})
};



///////////////////////////////////////////////////
// SALES BY REVENUE
//////////////////////////////////////////////////
window.get_sales_by_revenue_data = function(){
	// var territory_data = document.getElementById('territory_form_data').value;

	window.revenue_function_call(document.getElementById('revenue_form_data').value);
	// return [year1.value, year2.value];
};


window.revenue_function_call = function(year){
frappe.call({
	method: "tools_box.tools_box.page.business_board.business_board_revenue_analytics.get_analytics_by_revenue_center", //dotted path to server method
	args: {
			year: year
	},
	callback: function(r) {
			// console.log(r['message']);
			window.revenue_data_list = r['message'];
			window.revenue_center_total_list = r['message'].revenue;

// alert(window.prev_year);
window.sales_by_revenue = new frappe.Chart( "#revenue_chart", { // or DOM element
	data: {
		labels: ["Jan", "Feb", "Mar", "Apr",
			"May", "Jun", "Jul", "Aug", "sep", "Oct", "Nov", "Dec"],

		datasets: [
			{
				name: "Baker's Choice", chartType: 'bar',
				values: window.revenue_data_list.bakers_choice
			},
			{
				name: "Graceco Foods", chartType: 'bar',
				values: window.revenue_data_list.graceco_foods
			},
			{
				name: "Princess Snacks", chartType: 'bar',
				values: window.revenue_data_list.princess_snacks
			}
		],

		yMarkers: [{ label: "Marker", value: 0,
			options: { labelPos: 'left' }}],
		yRegions: [{ label: "Region", start: 0, end: 300,
			options: { labelPos: 'right' }}]
		},

		title: "Sales by Revenue Center - BAKER'S CHOICE: " + formatter.format(window.revenue_center_total_list[0]) + "; GRACECO FOODS: " + formatter.format(window.revenue_center_total_list[2]) + "; PRINCESS SNACKS: " + formatter.format(window.revenue_center_total_list[1]) + "; TOTAL REVENUE: " + formatter.format(window.revenue_center_total_list[0]+window.revenue_center_total_list[1]+window.revenue_center_total_list[2]),
		type: 'axis-mixed', // or 'bar', 'line', 'pie', 'percentage'
		height: 500,
		colors: ['blue', 'red', 'green'],

		tooltipOptions: {
			formatTooltipX: d => (d + '').toUpperCase(),
			formatTooltipY: d => d + ' MN',
		}
});
},
error: function(r){
	alert("Error: Please check your internet connection.");
},
})
};


///////////////////////////////////////////////////
// METHOD CALL
///////////////////////////////////////////////////
	var date = new Date();
	var year = date.getFullYear();


	window.frappe_function_call(year-1, year);
	// window.territory_function_call(year);
	window.revenue_function_call(year);
  //display on page load
	}





	frappe.pages['business_board'].on_page_show = () => {
		frappe.breadcrumbs.add("GRACECO LIMITED by Ghorz");

	// var query = frappe.model.sql("select email from tabUser	where first_name='email'");
	// console.log('Hello');

};
