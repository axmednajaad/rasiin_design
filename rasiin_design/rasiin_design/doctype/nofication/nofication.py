# Copyright (c) 2023, Rasiin and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Nofication(Document):
	def after_insert(self):
		event = "new_notice"
		# msg = {"content" : "This updated Encounter"}
		frappe.publish_realtime(event)
