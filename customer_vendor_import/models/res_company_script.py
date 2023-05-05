from odoo import fields, models, api
import pandas as pd
from odoo.modules.module import get_module_path


class ResCompany(models.Model):
    _inherit = 'res.company'

    def import_customer(self):
        payment_term_dict = {}
        payment_term_obj = self.env['account.payment.term']
        for payment_term in payment_term_obj.search([]):
            payment_term_dict.update({payment_term.name: payment_term.id})

        currency_type_dict = {}
        for currency_type in self.env['res.currency'].search([]):
            currency_type_dict.update({currency_type.name: currency_type.id})

        title_obj = self.env['res.partner.title']
        title_dict = {}
        for title in title_obj.search([]):
            title_dict.update({title.name: title.id})

        state_obj = self.env['res.country.state']
        state_dict = {}
        for state in state_obj.search([('country_id.code', 'in', ('CA', 'US'))]):
            state_dict.update({state.code: state.id})

        country_obj = self.env['res.country']
        country_dict = {}
        for country in country_obj.search([]):
            country_dict.update({country.code: country.id})

        shipping_country_dict = {}
        for country in country_obj.search([]):
            shipping_country_dict.update({country.code: country.id})

        module_path = get_module_path('customer_vendor_import')
        module_path += '/models/customer_list.xlsx'
        excel_data = pd.read_excel(module_path)
        data = pd.DataFrame(excel_data, columns=['Active Status', 'Customer', 'Currency', 'Main Phone',
                                                 'Job Title', 'Main Email', 'Terms', 'Invoice to 1', 'Invoice to 2',
                                                 'Invoice(city)', 'Invoice(state)', 'Invoice(zip)', 'Invoice to 5 country',
                                                 'Ship to 1', 'Ship to 2', 'Ship to 3(city)', 'Ship to 4(state)', 'Ship (zip)',
                                                 'Ship to 5(Country)'
                                                 ])
        for active, name, currency_id, phone, title, email, property_payment_term_id, street1, street2, inv_city, \
            inv_state, inv_zip, inv_country, shipping_street1, shipping_street2, ship_city, ship_state, ship_zip, shipping_country \
                in zip(data['Active Status'], data['Customer'], data['Currency'],
                       data['Main Phone'], data['Job Title'], data['Main Email'], data['Terms'], data['Invoice to 1'],
                       data['Invoice to 2'], data['Invoice(city)'], data['Invoice(state)'], data['Invoice(zip)'], data['Invoice to 5 country'],
                       data['Ship to 1'], data['Ship to 2'], data['Ship to 3(city)'], data['Ship to 4(state)'], data['Ship (zip)'], data['Ship to 5(Country)']):

            if property_payment_term_id in payment_term_dict:
                property_payment_term_id_1 = payment_term_dict.get(property_payment_term_id)
            else:
                property_payment_term_id_1 = payment_term_obj.create({'name': property_payment_term_id}).id

            if title in title_dict:
                title_1 = title_dict.get(title)
            else:
                title_1 = False
                if str(title) != 'nan':
                    title_1 = title_obj.create({'name': title}).id

            state_1 = False
            if inv_state in state_dict:
                state_1 = state_dict.get(inv_state)

            if inv_country in country_dict:
                country_1 = country_dict.get(inv_country)
            else:
                country_1 = False
                if str(inv_country) != 'nan':
                    country_1 = country_obj.create({'name': inv_country}).id

            if shipping_country in shipping_country_dict:
                shipping_country_1 = shipping_country_dict.get(country)
            else:
                shipping_country_1 = False
                if str(shipping_country) != 'nan':
                    shipping_country_1 = country_obj.create({'name': shipping_country}).id

            ship_state_1 = False
            if ship_state in state_dict:
                ship_state_1 = state_dict.get(ship_state)

            if str(active) == 'active':
                active = True
            if str(name) == 'nan':
                name = False
            if str(currency_id) == 'nan':
                currency_id = False
            if str(phone) == 'nan':
                phone = False
            if str(email) == 'nan':
                email = False
            if str(street1) == 'nan':
                street1 = ''
            if str(street2) == 'nan':
                street2 = ''
            if str(inv_city) == 'nan':
                inv_city = ''
            if str(inv_zip) == 'nan':
                inv_zip = ''
            if str(inv_country) == 'nan':
                country_1 = False
            if str(shipping_street1) == 'nan':
                shipping_street1 = ''
            if str(shipping_street2) == 'nan':
                shipping_street2 = ''
            if str(ship_city) == 'nan':
                ship_city = ''
            if str(ship_zip) == 'nan':
                ship_zip = ''
            if str(shipping_country) == 'nan':
                shipping_country_1 = False

            partner_dict = {
                'customer_rank': True,
                'active': active,
                'name': name,
                'currency_id': currency_id,
                'phone': phone,
                'title': title_1,
                'email': email,
                'property_payment_term_id': property_payment_term_id_1,
                'company_type': 'company',

            }

            customer = self.env['res.partner'].create(partner_dict)
            if customer:
                if street1:
                    self.env['res.partner'].create({
                        'parent_id': customer.id,
                        'name': name,
                        'company_type': 'person',
                        'customer_rank': True,
                        'active': active,
                        'type': 'invoice',
                        'street': street1,
                        'street2':street2,
                        'city': inv_city,
                        'state_id': state_1,
                        'country_id': country_1,
                        'zip': inv_zip,
                    })
                if shipping_street1:
                    self.env['res.partner'].create({
                        'parent_id': customer.id,
                        'name': name,
                        'company_type': 'person',
                        'customer_rank': True,
                        'active': active,
                        'type': 'delivery',
                        'street': shipping_street1,
                        'street2': shipping_street2,
                        'city': ship_city,
                        'state_id': ship_state_1,
                        'country_id': shipping_country_1,
                        'zip': ship_zip,
                    })

    def import_vendor(self):
        payment_term_dict = {}
        payment_term_obj = self.env['account.payment.term']
        for payment_term in payment_term_obj.search([]):
            payment_term_dict.update({payment_term.name: payment_term.id})

        currency_type_dict = {}
        for currency_type in self.env['res.currency'].search([]):
            currency_type_dict.update({currency_type.name: currency_type.id})

        title_obj = self.env['res.partner.title']
        title_dict = {}
        for title in title_obj.search([]):
            title_dict.update({title.name: title.id})

        state_obj = self.env['res.country.state']
        state_dict = {}
        for state in state_obj.search([('country_id.code', 'in', ('CA', 'US'))]):
            state_dict.update({state.code: state.id})

        country_obj = self.env['res.country']
        country_dict = {}
        for country in country_obj.search([]):
            country_dict.update({country.code: country.id})

        shipping_country_dict = {}
        for country in country_obj.search([]):
            shipping_country_dict.update({country.code: country.id})

        module_path = get_module_path('customer_vendor_import')
        module_path += '/models/vendor_list.xlsx'
        excel_data = pd.read_excel(module_path)
        data = pd.DataFrame(excel_data, columns=['Active Status', 'Vendor', 'Currency', 'Main Phone',
                                                 'Job Title', 'Main Email', 'Terms', 'Bill from 1', 'Bill from 2',
                                                 'Bill(city)', 'Bill(state)', 'Bill(zip)', 'Bill(country)',
                                                 'Ship from 1', 'Ship from 2', 'City(Ship)', 'State(Ship)',
                                                 'Zip(Ship)', 'Country(Ship)'
                                                 ])
        for active, name, currency_id, phone, title, email, property_payment_term_id, street1, street2, bill_city, \
            bill_state, bill_zip, bill_country, shipping_street1, shipping_street2, ship_city, ship_state, ship_zip, shipping_country in zip(
            data['Active Status'], data['Vendor'], data['Currency'],
            data['Main Phone'], data['Job Title'], data['Main Email'], data['Terms'], data['Bill from 1'],
            data['Bill from 2'], data['Bill(city)'], data['Bill(state)'], data['Bill(zip)'], data['Bill(country)'],
            data['Ship from 1'], data['Ship from 2'], data['City(Ship)'], data['State(Ship)'], data['Zip(Ship)'], data['Country(Ship)']):

            if property_payment_term_id in payment_term_dict:
                property_payment_term_id_1 = payment_term_dict.get(property_payment_term_id)
            else:
                property_payment_term_id_1 = False
                if str(property_payment_term_id) != 'nan':
                    property_payment_term_id_1 = payment_term_obj.create({'name': property_payment_term_id}).id
                    payment_term_dict.update({property_payment_term_id: property_payment_term_id_1})

            if title in title_dict:
                title_1 = title_dict.get(title)
            else:
                title_1 = False
                if str(title) != 'nan':
                    title_1 = title_obj.create({'name': title}).id

            state_1 = False
            if bill_state in state_dict:
                state_1 = state_dict.get(bill_state)


            if bill_country in country_dict:
                country_1 = country_dict.get(bill_country)
            else:
                country_1 = False
                if str(bill_country) != 'nan':
                    country_1 = country_obj.create({'name': bill_country}).id

            ship_state_1 = False
            if ship_state in state_dict:
                ship_state_1 = state_dict.get(ship_state)

            if shipping_country in shipping_country_dict:
                shipping_country_1 = shipping_country_dict.get(country)
            else:
                shipping_country_1 = False
                if str(shipping_country) != 'nan':
                    shipping_country_1 = country_obj.create({'name': shipping_country}).id

            if str(active) == 'active':
                active = True
            if str(name) == 'nan':
                name = False
            if str(currency_id) == 'nan':
                currency_id = False
            if str(phone) == 'nan':
                phone = False
            if str(email) == 'nan':
                email = False
            if str(street1) == 'nan':
                street1 = ''
            if str(street2) == 'nan':
                street2 = ''
            if str(bill_city) == 'nan':
                bill_city = ''
            if str(bill_zip) == 'nan':
                bill_zip = ''
            if str(bill_country) == 'nan':
                country_1 = False
            if str(shipping_street1) == 'nan':
                shipping_street1 = ''
            if str(shipping_street2) == 'nan':
                shipping_street2 = ''
            if str(ship_city) == 'nan':
                ship_city = ''
            if str(ship_zip) == 'nan':
                ship_zip = ''
            if str(shipping_country) == 'nan':
                shipping_country_1 = False

            partner_dict = {
                'supplier_rank': True,
                'active': active,
                'name': name,
                'currency_id': currency_id,
                'phone': phone,
                'title': title_1,
                'email': email,
                'property_supplier_payment_term_id': property_payment_term_id_1,
                'company_type': 'company',

            }

            customer = self.env['res.partner'].create(partner_dict)
            if customer:
                if street1:
                    self.env['res.partner'].create({
                        'parent_id': customer.id,
                        'name': name,
                        'company_type': 'person',
                        'supplier_rank': True,
                        'active': active,
                        'type': 'invoice',
                        'street': street1,
                        'street2':street2,
                        'city': bill_city,
                        'state_id': state_1,
                        'country_id': country_1,
                        'zip': bill_zip,
                    })
                if shipping_street1:
                    self.env['res.partner'].create({
                        'parent_id': customer.id,
                        'name': name,
                        'company_type': 'person',
                        'supplier_rank': True,
                        'active': active,
                        'type': 'delivery',
                        'street': shipping_street1,
                        'street2': shipping_street2,
                        'city': ship_city,
                        'state_id': ship_state_1,
                        'country_id': shipping_country_1,
                        'zip': ship_zip,
                    })
