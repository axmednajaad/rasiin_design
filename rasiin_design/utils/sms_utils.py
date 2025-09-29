import frappe
import json
from rasiin_design.services.hormuud_sms_service import HormuudSMSService


@frappe.whitelist(allow_guest=False)
def send_sms_via_hormuud(receiver_list, msg, sender_name="Ciribey Gas", success_msg=True):
    """
    Main function to send SMS via Hormuud - integrates with Frappe's SMS system
    """
    try:
        hormuud = HormuudSMSService()
        
        # Debug: Log the incoming data
        frappe.logger().debug(f"Raw receiver_list: {receiver_list}, type: {type(receiver_list)}")
        
        # Handle different input formats
        if isinstance(receiver_list, str):
            try:
                # Try to parse as JSON array if it's a string
                receiver_list = json.loads(receiver_list)
                frappe.logger().debug(f"Parsed JSON receiver_list: {receiver_list}")
            except json.JSONDecodeError:
                # If it's a plain string, split by newlines or commas
                if '\n' in receiver_list:
                    receiver_list = receiver_list.split('\n')
                elif ',' in receiver_list:
                    receiver_list = receiver_list.split(',')
                else:
                    receiver_list = [receiver_list]
        
        # Ensure it's a list
        if not isinstance(receiver_list, list):
            receiver_list = [receiver_list]
        
        frappe.logger().debug(f"Final receiver_list: {receiver_list}")
        
        results = {
            'successful': [],
            'failed': []
        }
        
        # Clean and validate mobile numbers
        valid_numbers = []
        for mobile in receiver_list:
            if mobile and str(mobile).strip():
                # Remove any whitespace and format
                cleaned_mobile = str(mobile).strip()
                valid_numbers.append(cleaned_mobile)
        
        if not valid_numbers:
            frappe.throw("No valid mobile numbers provided")
        
        frappe.logger().debug(f"Valid numbers: {valid_numbers}")
        
        # Send each SMS individually for better tracking
        for mobile in valid_numbers:
            try:
                # Use Basic Auth as per your implementation
                result = hormuud.send_sms_basic_auth(
                    mobile=mobile,
                    message=msg,
                    refid=f"frappe_{frappe.generate_hash(length=8)}"
                )
                
                if result.get('success'):
                    results['successful'].append({
                        'mobile': mobile,
                        'message_id': result.get('data', {}).get('MessageID'),
                        'response': result
                    })
                    
                    # Create SMS Log record for successful send
                    create_sms_log(
                        sender_name=sender_name,
                        sent_on=frappe.utils.nowdate(),
                        message=msg,
                        no_of_requested_sms=1,
                        requested_numbers=mobile,
                        no_of_sent_sms=1,
                        sent_to=mobile,
                        status="Sent",
                        api_response=result
                    )
                else:
                    results['failed'].append({
                        'mobile': mobile,
                        'error': result.get('error', 'Unknown error'),
                        'response': result
                    })
                    
                    # Create SMS Log record for failed send
                    create_sms_log(
                        sender_name=sender_name,
                        sent_on=frappe.utils.nowdate(),
                        message=msg,
                        no_of_requested_sms=1,
                        requested_numbers=mobile,
                        no_of_sent_sms=0,
                        sent_to="",
                        status="Failed",
                        api_response=result,
                        error_message=result.get('error', 'Unknown error')
                    )
                    
            except Exception as e:
                error_msg = f"Failed to send SMS to {mobile}: {str(e)}"
                results['failed'].append({
                    'mobile': mobile,
                    'error': error_msg
                })
                
                # Create SMS Log record for exception
                create_sms_log(
                    sender_name=sender_name,
                    sent_on=frappe.utils.nowdate(),
                    message=msg,
                    no_of_requested_sms=1,
                    requested_numbers=mobile,
                    no_of_sent_sms=0,
                    sent_to="",
                    status="Failed",
                    api_response={"exception": str(e)},
                    error_message=error_msg
                )
                frappe.log_error(error_msg, "Hormuud SMS")
        
        # Show success message if requested
        if success_msg:
            if results['successful']:
                frappe.msgprint(f"SMS sent successfully to {len(results['successful'])} recipients")
            if results['failed']:
                frappe.msgprint(f"Failed to send SMS to {len(results['failed'])} recipients", indicator='red')
            
        if results['failed']:
            frappe.log_error(f"SMS failures: {results['failed']}", "Hormuud SMS")
            
        return results
        
    except Exception as e:
        frappe.log_error(f"SMS sending failed: {str(e)}", "Hormuud SMS")
        frappe.throw(f"Failed to send SMS: {str(e)}")


def create_sms_log(sender_name, sent_on, message, no_of_requested_sms, requested_numbers, no_of_sent_sms, sent_to, status, api_response=None, error_message=None):
    """
    Create SMS Log record for tracking SMS messages
    """
    try:
        sms_log = frappe.get_doc({
            'doctype': 'SMS Log',
            'sender_name': sender_name,
            'sent_on': sent_on,
            'message': message,
            'no_of_requested_sms': no_of_requested_sms,
            'requested_numbers': requested_numbers,
            'no_of_sent_sms': no_of_sent_sms,
            'sent_to': sent_to,
            'status': status,
            'api_response': frappe.as_json(api_response) if api_response else None,
            'error_message': error_message
        })
        sms_log.insert(ignore_permissions=True)
        
        # Commit to ensure the log is saved even if subsequent SMS fail
        frappe.db.commit()
        
        return sms_log.name
        
    except Exception as e:
        frappe.log_error(f"Failed to create SMS Log: {str(e)}", "SMS Log")
        return None


@frappe.whitelist()
def send_bulk_sms_to_customers(message, customer_group=None, territory=None, sender_name=""):
    """
    Send bulk SMS to customers with filters
    """
    filters = {"mobile_no": ["!=", ""]}
    
    if customer_group:
        filters["customer_group"] = customer_group
    if territory:
        filters["territory"] = territory
    
    customers = frappe.get_all("Customer", 
        fields=["name", "customer_name", "mobile_no"],
        filters=filters,
        limit=500  # Safety limit
    )
    
    if not customers:
        return {"success": False, "message": "No customers found with mobile numbers"}
    
    receiver_list = [c['mobile_no'] for c in customers if c.get('mobile_no')]
    
    if not receiver_list:
        return {"success": False, "message": "No valid mobile numbers found"}
    
    # Create a summary SMS Log for the bulk operation
    bulk_sms_log = create_sms_log(
        sender_name=sender_name or "Bulk SMS",
        sent_on=frappe.utils.nowdate(),
        message=message,
        no_of_requested_sms=len(receiver_list),
        requested_numbers=", ".join(receiver_list),
        no_of_sent_sms=0,  # Will be updated after sending
        sent_to="",  # Will be updated after sending
        status="Processing"
    )
    
    results = send_sms_via_hormuud(receiver_list, message, sender_name, success_msg=False)
    
    # Update the bulk SMS Log with final results
    if bulk_sms_log:
        try:
            sms_log_doc = frappe.get_doc("SMS Log", bulk_sms_log)
            sms_log_doc.no_of_sent_sms = len(results['successful'])
            sms_log_doc.sent_to = ", ".join([s['mobile'] for s in results['successful']])
            sms_log_doc.status = "Completed" if results['successful'] else "Failed"
            sms_log_doc.api_response = frappe.as_json(results)
            sms_log_doc.save()
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Failed to update bulk SMS log: {str(e)}", "SMS Log")
    
    success_count = len(results['successful'])
    fail_count = len(results['failed'])
    
    if success_count > 0:
        frappe.msgprint(f"Bulk SMS completed: {success_count} sent, {fail_count} failed")
    
    return {
        "success": True,
        "total_customers": len(customers),
        "sms_sent": success_count,
        "sms_failed": fail_count,
        "failed_numbers": results['failed'],
        "sms_log": bulk_sms_log
    }


@frappe.whitelist()
def test_hormuud_connection():
    """
    Test Hormuud SMS connection
    """
    try:
        hormuud = HormuudSMSService()
        result = hormuud.send_sms_basic_auth(
            mobile="+252613656021",  # Test number - replace with yours
            message="Test connection from Frappe",
            refid="test_connection"
        )
        
        # Log the test attempt
        create_sms_log(
            sender_name="System Test",
            sent_on=frappe.utils.nowdate(),
            message="Test connection from Frappe",
            no_of_requested_sms=1,
            requested_numbers="+252613656021",
            no_of_sent_sms=1 if result.get('success') else 0,
            sent_to="+252613656021" if result.get('success') else "",
            status="Sent" if result.get('success') else "Failed",
            api_response=result
        )
        
        return {
            "success": result.get('success', False),
            "message": result.get('message', 'Test completed'),
            "details": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist(allow_guest=False)
def get_sms_balance():
    """
    Get SMS balance/account status from Hormuud API
    
    Returns:
        dict: Balance information
    """
    try:
        sms_service = HormuudSMSService()
        
        balance_data = sms_service.check_sms_balance()
        
        # Debug: Log the actual response structure
        frappe.logger().info(f"Balance API Raw Response: {balance_data}")
        
        # Check different possible response structures
        if isinstance(balance_data, dict):
            # Option 1: Direct balance in response
            if "balance" in balance_data:
                return {
                    "success": True,
                    "balance": balance_data.get("balance"),
                    "currency": balance_data.get("currency", "USD"),
                    "raw_response": balance_data
                }
            
            # Option 2: Nested in message or data
            elif "message" in balance_data and isinstance(balance_data["message"], dict):
                message_data = balance_data["message"]
                if "balance" in message_data:
                    return {
                        "success": True,
                        "balance": message_data.get("balance"),
                        "currency": message_data.get("currency", "USD"),
                        "raw_response": balance_data
                    }
            
            # Option 3: ResponseCode based
            elif balance_data.get("ResponseCode") == "200":
                return {
                    "success": True,
                    "balance": balance_data.get("balance", balance_data.get("Balance", "N/A")),
                    "currency": balance_data.get("currency", "USD"),
                    "raw_response": balance_data
                }
        
        # If we get here, the response structure is unexpected
        return {
            "success": False,
            "error": "Unexpected API response format",
            "raw_response": balance_data
        }
            
    except Exception as e:
        frappe.log_error(f"SMS Balance Check Error: {str(e)}", "SMS API")
        return {
            "success": False, 
            "error": str(e)
        }


@frappe.whitelist()
def get_sms_logs(filters=None, page_length=20):
    """
    Get SMS Log records with optional filters
    """
    try:
        filters = filters or {}
        
        sms_logs = frappe.get_all(
            "SMS Log",
            fields=[
                "name", "sender_name", "sent_on", "message", 
                "no_of_requested_sms", "no_of_sent_sms", "status"
            ],
            filters=filters,
            order_by="creation desc",
            limit_page_length=page_length
        )
        
        return {
            "success": True,
            "sms_logs": sms_logs
        }
    except Exception as e:
        frappe.log_error(f"Failed to fetch SMS logs: {str(e)}", "SMS Log")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def get_sms_log_details(sms_log_name):
    """
    Get detailed information about a specific SMS Log
    """
    try:
        sms_log = frappe.get_doc("SMS Log", sms_log_name)
        
        return {
            "success": True,
            "sms_log": {
                "name": sms_log.name,
                "sender_name": sms_log.sender_name,
                "sent_on": sms_log.sent_on,
                "message": sms_log.message,
                "no_of_requested_sms": sms_log.no_of_requested_sms,
                "requested_numbers": sms_log.requested_numbers,
                "no_of_sent_sms": sms_log.no_of_sent_sms,
                "sent_to": sms_log.sent_to,
                "status": sms_log.status,
                "api_response": sms_log.api_response,
                "error_message": sms_log.error_message,
                "creation": sms_log.creation
            }
        }
    except Exception as e:
        frappe.log_error(f"Failed to fetch SMS log details: {str(e)}", "SMS Log")
        return {
            "success": False,
            "error": str(e)
        }