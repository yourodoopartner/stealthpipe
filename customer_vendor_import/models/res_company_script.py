from odoo import fields, models, api
import pandas as pd
from odoo.modules.module import get_module_path


class ResCompany(models.Model):
    _inherit = 'res.company'

    def import_customer(self):
        payment_term_dict = {}
        payment_term_obj = self.env['account.payment.term']
        payment_term_ids = payment_term_obj.search([])
        for payment_term in payment_term_ids:
            payment_term_dict.update({payment_term.name: payment_term.id})

        currency_type_dict = {}
        invoice_currency_type_ids = self.env['res.currency'].search([])
        for currency_type in invoice_currency_type_ids:
            currency_type_dict.update({currency_type.name: currency_type.id})

        title_obj = self.env['res.partner.title']
        title_dict = {}
        title_ids = title_obj.search([])
        for title in title_ids:
            title_dict.update({title.name: title.id})

        country_obj = self.env['res.country']
        country_dict = {}
        country_ids = country_obj.search([])
        for country in country_ids:
            country_dict.update({country.name: country.id})
        shipping_country_dict = {}
        shipping_country_ids = country_obj.search([])
        for country in shipping_country_ids:
            shipping_country_dict.update({country.name: country.id})

        module_path = get_module_path('customer_vendor_import')
        module_path += '/models/customer_list.xlsx'
        excel_data = pd.read_excel(module_path)
        data = pd.DataFrame(excel_data, columns=['Active Status', 'Customer', 'Currency', 'Main Phone',
                                                 'Job Title', 'Main Email', 'Terms', 'Invoice to 1', 'Invoice to 2',
                                                 'Invoice to 3', 'Invoice to 4', 'Invoice to 5', 'Ship to 1',
                                                 'Ship to 2',
                                                 'Ship to 3',
                                                 'Ship to 4', 'Ship to 5'
                                                 ])
        for active, name, currency_id, phone, title, email, property_payment_term_id, street11, street12, street21, \
            street22, country, shipping_street11, shipping_street12, shipping_street21, shipping_street22, shipping_country \
                in zip(data['Active Status'], data['Customer'], data['Currency'],
                       data['Main Phone'], data['Job Title'], data['Main Email'], data['Terms'], data['Invoice to 1'],
                       data['Invoice to 2'], data['Invoice to 3'], data['Invoice to 4'], data['Invoice to 5'],
                       data['Ship to 1'], data['Ship to 2'], data['Ship to 3'], data['Ship to 4'], data['Ship to 5']):

            if property_payment_term_id in payment_term_dict:
                property_payment_term_id_1 = payment_term_dict.get(property_payment_term_id)
            else:
                property_payment_term_id_1 = payment_term_obj.create({'name': property_payment_term_id}).id

            if title in title_dict:
                title_1 = title_dict.get(title)
            else:
                if str(title) == 'nan':
                    title_1 = False
                else:
                    title_1 = title_obj.create({'name': title}).id

            if country in country_dict:
                country_1 = country_dict.get(country)
            else:
                if str(country) == 'nan':
                    country_1 = False
                else:
                    existing_country = country_obj.search([('name', '=', country)])
                    if existing_country:
                        country_1 = existing_country.id
                    else:
                        country_1 = country_obj.create({'name': country}).id

            if shipping_country in shipping_country_dict:
                shipping_country_1 = shipping_country_dict.get(country)
            else:
                if str(shipping_country) == 'nan':
                    shipping_country_1 = False
                else:
                    existing_country = country_obj.search([('name', '=', shipping_country)])
                    if existing_country:
                        shipping_country_1 = existing_country.id
                    else:
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
            if str(street11) == 'nan':
                street11 = ''
            if str(street12) == 'nan':
                street12 = ''
            if str(street21) == 'nan':
                street21 = ''
            if str(street22) == 'nan':
                street22 = ''
            if str(country) == 'nan':
                country_1 = False
            if str(shipping_street11) == 'nan':
                shipping_street11 = ''
            if str(shipping_street12) == 'nan':
                shipping_street12 = ''
            if str(shipping_street21) == 'nan':
                shipping_street21 = ''
            if str(shipping_street22) == 'nan':
                shipping_street22 = ''
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
                'street': str(street11) + str(street12),
                'street2': str(street21) + str(street22),
                'country_id': country_1,

            }

            customer = self.env['res.partner'].create(partner_dict)
            customer.write({'child_ids': [
                (0, 0, {
                    'name': name,
                    'type': 'delivery',
                    'active': active,
                    'customer_rank': True,
                    'street': str(shipping_street11) + str(shipping_street12),
                    'street2': str(shipping_street21) + str(shipping_street22),
                    'country_id': shipping_country_1,
                })]})

    def import_vendor(self):
        payment_term_dict = {}
        payment_term_obj = self.env['account.payment.term']
        payment_term_ids = payment_term_obj.search([])
        for payment_term in payment_term_ids:
            payment_term_dict.update({payment_term.name: payment_term.id})

        currency_type_dict = {}
        invoice_currency_type_ids = self.env['res.currency'].search([])
        for currency_type in invoice_currency_type_ids:
            currency_type_dict.update({currency_type.name: currency_type.id})

        title_obj = self.env['res.partner.title']
        title_dict = {}
        title_ids = title_obj.search([])
        for title in title_ids:
            title_dict.update({title.name: title.id})

        country_obj = self.env['res.country']
        country_dict = {}
        country_ids = country_obj.search([])
        for country in country_ids:
            country_dict.update({country.name: country.id})

        shipping_country_dict = {}
        shipping_country_ids = country_obj.search([])
        for country in shipping_country_ids:
            shipping_country_dict.update({country.name: country.id})

        module_path = get_module_path('customer_vendor_import')
        module_path += '/models/vendor_list.xlsx'
        excel_data = pd.read_excel(module_path)
        data = pd.DataFrame(excel_data, columns=['Active Status', 'Vendor', 'Currency', 'Main Phone',
                                                 'Job Title', 'Main Email', 'Terms', 'Bill from 1', 'Bill from 2',
                                                 'Bill from 3', 'Bill from 4', 'Bill from 5', 'Ship from 1',
                                                 'Ship from 2',
                                                 'Ship from 3',
                                                 'Ship from 4', 'Ship from 5'
                                                 ])
        for active, name, currency_id, phone, title, email, property_payment_term_id, street11, street12, street21, \
            street22, country, shipping_street11, shipping_street12, shipping_street21, shipping_street22, shipping_country in zip(
            data['Active Status'], data['Vendor'], data['Currency'],
            data['Main Phone'], data['Job Title'], data['Main Email'], data['Terms'], data['Bill from 1'],
            data['Bill from 2'], data['Bill from 3'], data['Bill from 4'], data['Bill from 5'],
            data['Ship from 1'], data['Ship from 2'], data['Ship from 3'], data['Ship from 4'], data['Ship from 5']):

            if property_payment_term_id in payment_term_dict:
                property_payment_term_id_1 = payment_term_dict.get(property_payment_term_id)
            else:
                if str(property_payment_term_id) == 'nan':
                    property_payment_term_id_1 = False
                else:
                    property_payment_term_id_1 = payment_term_obj.create({'name': property_payment_term_id}).id

            if title in title_dict:
                title_1 = title_dict.get(title)
            else:
                if str(title) == 'nan':
                    title_1 = False
                else:
                    title_1 = title_obj.create({'name': title}).id

            if country in country_dict:
                country_1 = country_dict.get(country)
            else:
                if str(country) == 'nan':
                    country_1 = False
                else:
                    existing_country = country_obj.search([('name', '=', country)])
                    if existing_country:
                        country_1 = existing_country.id
                    else:
                        country_1 = country_obj.create({'name': country}).id

            if shipping_country in shipping_country_dict:
                shipping_country_1 = shipping_country_dict.get(country)
            else:
                if str(shipping_country) == 'nan':
                    shipping_country_1 = False
                else:
                    existing_country = country_obj.search([('name', '=', shipping_country)])
                    if existing_country:
                        shipping_country_1 = existing_country.id
                    else:
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
            if str(street11) == 'nan':
                street11 = ''
            if str(street12) == 'nan':
                street12 = ''
            if str(street21) == 'nan':
                street21 = ''
            if str(street22) == 'nan':
                street22 = ''
            if str(country) == 'nan':
                country_1 = False
            if str(shipping_street11) == 'nan':
                shipping_street11 = ''
            if str(shipping_street12) == 'nan':
                shipping_street12 = ''
            if str(shipping_street21) == 'nan':
                shipping_street21 = ''
            if str(shipping_street22) == 'nan':
                shipping_street22 = ''
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
                'street': str(street11) + str(street12),
                'street2': str(street21) + str(street22),
                'country_id': country_1,

            }

            customer = self.env['res.partner'].create(partner_dict)
            customer.write({'child_ids': [
                (0, 0, {
                    'name': name,
                    'type': 'delivery',
                    'active': active,
                    'customer_rank': True,
                    'street': str(shipping_street11) + str(shipping_street12),
                    'street2': str(shipping_street21) + str(shipping_street22),
                    'country_id': shipping_country_1,
                })]})
