from  openerp.osv import osv, fields
from openerp import models, api
from openerp import tools

class salesperson(osv.Model): 
    _name = 'sales_report_custom.salesperson'
    _description = "Sales Team List"
    _auto = False
    _rec_name = 'salesperson_id'
  
  
    _columns = {
        'salesperson_id' : fields.many2one('res.users', string='Salesperson'),
        'team_id': fields.many2one('crm.team', 'Sales Team', readonly=True, oldname='section_id'),
        }
    
    
    def init(self, cr):
          tools.drop_view_if_exists(cr, self._table)
          cr.execute("""CREATE or REPLACE VIEW %s as (
          SELECT row_number() over() AS id,
                ru.id AS salesperson_id,
                ru.sale_team_id AS team_id,
                ct.user_id AS leader_id
                FROM crm_team ct,
                res_users ru
           WHERE ct.id = ru.sale_team_id )""" % (self._table))
