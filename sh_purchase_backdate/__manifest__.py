# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    "name": "Purchase Backdate | Purchase Confirmation Backdate | Back Date In Purchase | Purchase Order Backdate",
    "author" : "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Purchases",
    "summary": "Backdate and Remarks Backdate Remarks in Odoo Force Date Purchase Order Confirmation Backdate Mass Confirmation Backdate Mass Back Date Mass Backdate Purchase confirm date Purchase Pastdate old date RFQ backdate Purchases Backdate Odoo",
    "description": """In odoo, while you confirm the RFQ it will take the current date as confirmation date and you can not change the date after confirming it so our module is useful for confirm purchase orders with selected confirmation backdate. You can put a custom backdate and remarks in the purchase. You can mass assign backdate in one click. When you mass assign backdate, it asks for remarks in the mass assign wizard. This selected date and remarks are also reflects in the receipts, stock moves, product moves, bill & journal entries.""",
    "version": "15.0.2",
    "depends": ["purchase","stock"],
    "data": [
       
      'security/ir.model.access.csv' ,
      'security/backdate_security.xml',
      'wizard/mass_assign_backdate_wizard.xml',
      'views/purchase_config_settings.xml',
      'views/purchase_order.xml',
      'views/account_move.xml',
      'views/stock_picking.xml',
      'views/stock_move.xml',
      'views/stock_move_line.xml',
      'views/purchase_backdate_multi_action.xml',
        
       
    ],
           
    "auto_install":False,
    "installable": True,
    "application" : True,
    "images": ["static/description/background.png",],     
    "license": "OPL-1",
    "price": 20,
    "currency": "EUR"    
} 
