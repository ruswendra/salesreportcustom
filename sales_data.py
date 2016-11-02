from  openerp.osv import osv, fields
from openerp import models, api
import time, datetime, calendar
from openerp import tools
from datetime import date
class sales_data(osv.Model): 
    _name = 'sales_report_custom.sales_data'
    _description = "Sales Orders Statistics"
    _auto = False
    _rec_name = 'date'
#     def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
#         if not context:
#             context = {}
#         context.update({
#         'date': '2016-10-01'
#         })
#         print  context.get('date', False)
#         result = super(salesdata, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu)
#         return result
    def get_start_date_of_month(self):
        month_start_date = date.today().replace(day=1)
        return month_start_date
    def get_last_date_of_month(self):
        date = datetime.datetime.now()
        month_end_date = datetime.datetime(date.year, date.month, 1) + datetime.timedelta(days=calendar.monthrange(date.year, date.month)[1] - 1)
        return month_end_date    
    
     
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        date_trans = self.env.context.get('date_transaction', False)  # ambil data dari form sebelumnya untuk dijadikan domain
        sales_id = self.env.context.get('salesperson', False)
        print sales_id
        period = self.env.context.get('period_filter', False)
        date_from = self.env.context.get('date_transaction_from', False)
        date_to = self.env.context.get('date_transaction_to', False)
        if period == 'Monthly':
         domain = [("date", ">=", self.get_start_date_of_month()), ("date", "<=", self.get_last_date_of_month()), ("salesperson_id", 'in', sales_id) ]
        elif period == 'Periodic':
         domain = [("date", ">=", date_from), ("date", "<=", date_to), ("salesperson_id", "=", sales_id) ]   
        else:
         domain = [("date", "=", date_trans), ("salesperson_id", "in", sales_id) ]
        res = super(sales_data, self).search_read(domain, fields, offset, limit, order)
        return res
     
#     
    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False, lazy=True):
        date_trans = context.get('date_transaction', False)  # ambil data dari form sebelumnya untuk dijadikan domain
        sales_id = context.get('salesperson', False)
        period = context.get('period_filter', False)
        date_from = context.get('date_transaction_from', False)
        date_to = context.get('date_transaction_to', False)
        print date_trans
        month_start = self.get_start_date_of_month().strftime("%Y-%m-%d")
        if period == 'Monthly':
         domain = [("date", ">=", self.get_start_date_of_month().strftime("%Y-%m-%d")), ("date", "<=", self.get_last_date_of_month().strftime("%Y-%m-%d")), ("salesperson_id", "in", sales_id) ]
        elif period == 'Periodic':
         domain = [("date", ">=", date_from), ("date", "<=", date_to), ("salesperson_id", "in", sales_id) ]   
        else:
         domain = [("date", "=", date_trans), ("salesperson_id", "in", sales_id) ]
        return super(sales_data, self).read_group(cr, uid, domain, fields, groupby, offset, limit, context, orderby, lazy)    
#     
#     def _getDateTransaction(self):
#         date_trans = self.env.context.get('date', False)
#         print 'oke Sekali'
#         print date_trans
#         return [('date', '=', date_trans)]    
#     
#     
#     @api.depends('quantity', 'unit_price')
#     def _compute_total(self):
#      for record in self:
#         record.total = record.quantity * record.unit_price
#         
    _columns = {
        'date': fields.date('Tanggal Transaksi', readonly=True),
        'price_total': fields.float('Harga Total', readonly=True),
        'product_id': fields.many2one('product.product', 'Product', readonly=True),
        'salesperson_id': fields.many2one('res.users', 'Salesperson', readonly=True),
        'team_id': fields.many2one('crm.team', 'Sales Team', readonly=True, oldname='section_id'),
        }

    def _select(self):
        select_str = """
            WITH currency_rate as (%s)
             SELECT min(l.id) as id,
                   to_date(cast(s.date_order as TEXT),'YYYY-MM-DD')  AS date, 
                   t.uom_id as product_uom,
                   l.product_id as product_id, 
                   sum(l.price_total / COALESCE(cr.rate, 1.0)) as price_total,
                   s.user_id as salesperson_id,
                   s.team_id as team_id,
                  s.state as state
        """ % self.pool['res.currency']._select_companies_rates()
        return select_str

    def _from(self):
        from_str = """
                sale_order_line l
                      join sale_order s on (l.order_id=s.id)
                      join res_partner partner on s.partner_id = partner.id
                        left join product_product p on (l.product_id=p.id)
                            left join product_template t on (p.product_tmpl_id=t.id)
                    left join product_uom u on (u.id=l.product_uom)
                    left join product_uom u2 on (u2.id=t.uom_id)
                    left join product_pricelist pp on (s.pricelist_id = pp.id)
                    left join currency_rate cr on (cr.currency_id = pp.currency_id and
                        cr.company_id = s.company_id and
                        cr.date_start <= coalesce(s.date_order, now()) and
                        (cr.date_end is null or cr.date_end > coalesce(s.date_order, now())))
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY l.product_id,
                    l.order_id,
                    t.uom_id,
                    t.categ_id,
                    s.date_order,
                    s.partner_id,
                    s.user_id,
                    s.state,
                    s.company_id,
                    s.pricelist_id,
                    s.project_id,
                    s.team_id,
                    p.product_tmpl_id,
                    partner.country_id,
                    partner.commercial_partner_id
        """
        return group_by_str

    def init(self, cr):
        # self._table = sale_report_custom
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))

    
  

    
    
