from  openerp.osv import osv, fields
from openerp import models, api
import time
import datetime
import calendar
import re

class sales_inquiry(osv.osv): 
    _name = 'sales_report_custom.sales_inquiry'
    
    @api.multi
    def action_wizard_close(self):
     return {'type': 'ir.actions.act_window_close'}
 
    @api.multi
    def _get_salesperson_filter(self):  # cek untuk filtering data salesperson
      self.env.cr.execute("""WITH RECURSIVE sales_hier AS (
      SELECT name,user_id,login,leader,leader_id FROM sales_team_hier where leader_id = %s
      UNION  ALL
      SELECT e.name,e.user_id,e.login,e.leader,e.leader_id
      FROM   sales_hier c
      JOIN   sales_team_hier e ON e.leader_id = c.user_id)
     SELECT user_id FROM   sales_hier
     UNION
     SELECT user_id
     FROM sales_team_hier where user_id = %s
      """, (self.env.user.id, self.env.user.id))
      sales_id = self.env.cr.fetchall()
      return [('salesperson_id', 'in', sales_id)]
    
    def _get_default_sales_ids(self):
     print 'masuk default?'
     self.env.cr.execute("""WITH RECURSIVE sales_hier AS (
      SELECT name,user_id,login,leader,leader_id FROM sales_team_hier where leader_id = %s
      UNION  ALL
      SELECT e.name,e.user_id,e.login,e.leader,e.leader_id
      FROM   sales_hier c
      JOIN   sales_team_hier e ON e.leader_id = c.user_id)
     SELECT user_id FROM   sales_hier
     UNION
     SELECT user_id
     FROM sales_team_hier where user_id = %s
      """, (self.env.user.id, self.env.user.id))
     sales_id = self.env.cr.fetchall()
     salIds = []
     ids = self.env['sales_report_custom.salesperson'].search([('salesperson_id', '=', 1)])
#      for sales in ids:
#          salIds.append(sales.id)
#      print salIds 
     return ids.id

    _columns = {
        'period_filter'    :fields.selection([('Monthly', 'Monthly'), ('Daily', 'Daily'), ('Periodic', 'Periodic')], default='Monthly', string='Periode Transaksi', required=True),
        'date_transaction' : fields.date('Tanggal Transaksi', required=True),
        'sales_ids' : fields.many2many('sales_report_custom.salesperson', 'rel_salesperson', 'sid', 'uid', 'Salesperson', domain=_get_salesperson_filter, required=True),
        'date_transaction_from'   :fields.date('Tanggal Transaksi dari'),
        'date_transaction_to':fields.date('Tanggal Transaksi sampai'),
        }
    _defaults = {
        'date_transaction_from' : lambda*a : time.strftime("%Y-%m-%d"),
        'date_transaction_to': lambda*a : time.strftime("%Y-%m-%d"),
        'date_transaction'  : lambda*a : time.strftime("%Y-%m-%d"),
    
     }
    
    def extract_string_to_int(self, sales_id):
      return [int(s) for s in re.findall(r'\b\d+\b', sales_id)]
    
    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        print 'argument ini'
        if not args:
            args = []
        if not context:
            context = {}
        ids = []
        if name and operator in ['=', 'ilike']:
            ids = self.search(cr, user, [('login', '=', name)] + args, limit=limit, context=context)
        if not ids:
            ids = self.search(cr, user, [('name', operator, name)] + args, limit=limit, context=context)
        res = super(sales_inquiry, self).name_search(cr, user, name, args, operator, context)
        return res 
    
    @api.multi
    def action_open_form_report(self):  # This is also a comment in Python
        sales_form = self.env.ref('sales_report_custom.sales_data', False) 
        print sales_form
        for obj in self:
         date_trans = obj.date_transaction
         sales_id = str(obj.sales_ids)
         period_fil = obj.period_filter
         date_from = obj.date_transaction_from
         date_to = obj.date_transaction_to
         sales_ids = self.extract_string_to_int(sales_id)  # extract string to id(integer)
         print sales_id
         print sales_ids
         salIds = []
         sales_id_temp = self.env['sales_report_custom.salesperson'].search([('id', 'in', sales_ids)])
         for sales in sales_id_temp:
          salIds.append(sales.salesperson_id.id)
         print salIds 
         return {
            'name':'Sales Data',
            'type': 'ir.actions.act_window',
            'res_model': 'sales_report_custom.sales_data',
            'view_type': 'form',
            'view_mode': 'tree,pivot,graph',
            'res_id': self.id,
            'target': 'self',
            'context':{'date_transaction_from':date_from, 'date_transaction_to':date_to, 'date_transaction': date_trans, 'salesperson':salIds, "search_default_date_transaction":'1', "period_filter":period_fil},
          
        }


