
#  bench --site dcode.com console
import frappe

# --- 1. Define Notification Details ---
subject_text = "Important System Notice"
# 'email_content' is the correct DocType field for the notification body/message.
message_content = "The server will undergo brief, essential maintenance tonight at midnight UTC."
link_to_document = "/app/user" # Optional: Link to a specific DocType or page

# --- 2. Get All Active System Users ---
# This filter targets users who are enabled and specifically marked as 'System User'.
# Adjust filters if you want to include other user types (e.g., Website Users).
users_to_notify = frappe.get_list(
    "User",
    filters={"enabled": 1, "user_type": "System User"},
    fields=["name"],
    pluck="name"
)

# --- 3. Create Notification Log Entries for Each User ---
for user_name in users_to_notify:
    # Use frappe.new_doc() to create a new document
    doc = frappe.new_doc("Notification Log")
    
    # Set the required and desired fields
    doc.subject = subject_text
    doc.email_content = message_content  # Stores the notification text
    doc.type = "Alert"                   # Type of notification
    doc.for_user = user_name             # The recipient
    doc.link = link_to_document          # Optional link to follow
    doc.from_user = "Administrator"      # Set the sender
    
    # Set 'read' to 0 (unread) so users see it as new
    doc.read = 0 
    
    # Save the document to the database
    doc.insert(ignore_permissions=True)
    
# --- 4. Commit Changes and Realtime Push ---
# Commit all database changes to make the Notification Log entries permanent
frappe.db.commit() 
print(f"Successfully created {len(users_to_notify)} Notification Log entries.")

# Realtime Push: Signals to the UI to update the notification bell immediately.
# FIX: Removed the invalid keyword argument 'is_private'.
frappe.publish_realtime(
    event='notification',
    message="New System Notification",
    user='all'  # 'user="all"' targets all active, logged-in users.
)
