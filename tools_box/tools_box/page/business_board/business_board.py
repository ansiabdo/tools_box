from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc



###########################################################
# SALES BY MONTH
##########################################################
months = [i for i in range(1, 13)] # 12 months calendar

@frappe.whitelist()
def get_chart_results(year1, year2):
    prev_year_result = [] # result arrays
    cur_year_result = []
    for x in months: #query the database for result by monthly
        prev_year_result.append(round(filter_null(compute_year_month(f'{int(year1)}', f'{x}')[0]['sum(grand_total)'])/1000000, 3))
        cur_year_result.append(round(filter_null(compute_year_month(f'{int(year2)}', f'{x}')[0]['sum(grand_total)'])/1000000, 3))


    return [prev_year_result], [cur_year_result], [compute_year_total(int(year1))], [compute_year_total(int(year2))]#[year[0]['sum(grand_total)']]


def compute_year_month(year, month):
    year = frappe.db.sql(
        f"""SELECT sum(grand_total) FROM `tabSales Invoice` WHERE posting_date>='{int(year)}-{int(month)}-01' AND posting_date<='{int(year)}-{int(month)}-31'""",
        as_dict=True
    )
    return year

def compute_year_total(year):
    data = frappe.db.sql(
        f"""SELECT sum(grand_total) FROM `tabSales Invoice` WHERE posting_date>='{int(year)}-01-01' AND posting_date<='{int(year)}-12-31';""",
        as_dict=True
    )
    return data

def filter_null(data):
    if type(data)!=float:
        value = 0.0
        return value
    return data



##################################################################
# territory_list
##################################################################



@frappe.whitelist()
def get_sales_by_territory(year):
    lagos_result = filter_null(frappe.db.sql(filter_territory(lagos, year), as_dict=True)[0]['sum(grand_total)'])
    south_west_result = filter_null(frappe.db.sql(filter_territory(south_west, year), as_dict=True)[0]['sum(grand_total)'])
    south_east_result = filter_null(frappe.db.sql(filter_territory(south_east, year), as_dict=True)[0]['sum(grand_total)'])
    south_south_result = filter_null(frappe.db.sql(filter_territory(south_south, year), as_dict=True)[0]['sum(grand_total)'])
    north_zone_result = filter_null(frappe.db.sql(filter_territory(north_zone, year), as_dict=True)[0]['sum(grand_total)'])
    # nigeria_result = filter_null(frappe.db.sql(filter_territory(nigeria, 2019), as_dict=True)[0]['sum(grand_total)'])
    international_result = filter_null(frappe.db.sql(filter_territory(international, year), as_dict=True)[0]['sum(grand_total)'])
    #all_territories_result = filter_null(frappe.db.sql(filter_territory(all_territories, year), as_dict=True)[0]['sum(grand_total)'])
    sales_territory_result_set = [lagos_result, south_west_result, south_east_result, south_south_result, north_zone_result, international_result] #, all_territories_result]
    sales_territory_result_sum = sum(sales_territory_result_set)
    for x, y in enumerate(sales_territory_result_set):
        sales_territory_result_set[x] = round(y/1000000000, 2)

    # print(lagos_result)
    return sales_territory_result_sum, sales_territory_result_set



lagos = ['Agege', 'Ajeromi-ifelodun', 'Alimosho', 'Amuwo-Odofin', 'Apapa', 'Badagry', 'Epe', 'Eti-Osa',
            'Ibeju-Lekki', 'Ifako-Ijaye', 'Ikeja', 'Ikorodu', 'Kosofe', 'Lagos', 'Lagos Island', 'Lagos Zone',
            'Lagos Mainland', 'MM Tier 1', 'MM Tier 2', 'Mushin', 'Ojo', 'Oshodi-Isolo', 'Shomolu', 'Surulere', 'Nigeria']

south_west = ['Akure', 'Ekiti', 'Ibadan', 'Ife', 'Kwara', 'Ogun', 'Okitipupa', 'Ondo', 'Osun', 'Oyo', 'Ilorin', 'South', 'West Zone', 'Tanke', 'South West Zone']
south_south = ['Benin', 'Rivers', 'Akwa Ibom', 'Bayelsa', 'Delta', 'South South Zone']
south_east = ['Abia', 'Anambra', 'Enugu', 'Imo', 'South East Zone']
north_zone = ['Abuja', 'Kaduna', 'Kano', 'Bauchi', 'Benue', 'Northern Zone', 'Plateau']
international = ['International', 'Canada', 'Ghana', 'UK', 'USA']
nigeria = ['Nigeria']
all_territories = ['All Territories']



def filter_territory(territory_list, year):
    query = """SELECT sum(grand_total) FROM `tabSales Invoice` WHERE (""" #territory='abia' OR territory='anambra' OR territory='abia' OR territory='enugu' OR territory='imo' OR territory='south east zone';
    for t in territory_list:
        if (len(territory_list)-1 == territory_list.index(t)):
            query += f"territory='{t}')"
        else:
            query += f"territory='{t}' OR "
    query += f" AND (posting_date>='{int(year)}-01-01' and posting_date<='{int(year)}-12-31')"
    return query

# def get_territory_by_month(filter_territory, month):




# @frappe.whitelist()
# def get_2019_analytics():
    # sum_pre_year = frappe.db.sql(
    #     """SELECT sum(grand_total) FROM `tabSales Invoice` WHERE posting_date>='2019-01-01' AND posting_date<='2019-12-31';""",
    #     as_dict=True
    # )
    # sum_cur_year = frappe.db.sql(
    #     """SELECT sum(grand_total) FROM `tabSales Invoice` WHERE posting_date>='2020-01-01' AND posting_date<='2020-12-31';""",
    #     as_dict=True
    # )
    # prev_year = frappe.db.sql(
    #     """SELECT grand_total, posting_date FROM `tabSales Invoice` WHERE posting_date>='2019-01-01' AND posting_date<='2019-12-31' ORDER BY posting_date ASC;""",
    #     as_dict=True
    # )
    # cur_year = frappe.db.sql(
    #     """SELECT grand_total, posting_date FROM `tabSales Invoice` WHERE posting_date>='2020-01-01' AND posting_date<='2020-12-31' ORDER BY posting_date ASC;""",
    #     as_dict=True
    # )
    # return {'sum_pre_year': sum_pre_year, 'sum_cur_year': sum_cur_year, 'prev_year': prev_year, 'cur_year': cur_year}
