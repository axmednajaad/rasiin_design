
import frappe

@frappe.whitelist()
def mark_notification_as_read(log_name):
	"""
	Marks a Notification Log as read without triggering timestamp checks.
	This is safe for this operation as we are only updating the 'read' status.
	"""
	try:
		frappe.db.set_value('Notification Log', log_name, 'read', 1, update_modified=False)
		# We use db.set_value to avoid document timestamp validation and hooks (which are not needed here)
		# update_modified=False is crucial to prevent this write from causing a timestamp conflict with other operations.
		frappe.db.commit() # Commit the change to the database immediately
		return {"status": "success"}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "mark_notification_as_read Failed")
		return {"status": "error", "message": str(e)}