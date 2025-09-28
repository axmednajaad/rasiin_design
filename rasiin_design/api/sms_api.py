import frappe
from frappe import _
from frappe.utils import now_datetime, cstr
import json
from rasiin_design.services.hormuud_sms_service import HormuudSMSService
    
    
    
@frappe.whitelist(allow_guest=False)
def send_sms(mobile_numbers, message, doctype=None, docname=None, use_basic_auth=False):
    """
    Send SMS to one or multiple mobile numbers
    
    Args:
        mobile_numbers (str/list): Single mobile number or list of numbers
        message (str): SMS message content
        doctype (str): Optional - Document type for reference
        docname (str): Optional - Document name for reference
        use_basic_auth (bool): Whether to use Basic Auth instead of Bearer Token
    
    Returns:
        dict: Operation result
    """
    try:
        # Validate inputs
        if not mobile_numbers:
            return {"success": False, "error": "Mobile number(s) are required"}
        
        if not message:
            return {"success": False, "error": "Message content is required"}
        
        # Convert single mobile number to list
        if isinstance(mobile_numbers, str):
            mobile_numbers = [mobile_numbers]
        
        # Clean mobile numbers
        cleaned_numbers = []
        for number in mobile_numbers:
            cleaned = _clean_mobile_number(number)
            if cleaned:
                cleaned_numbers.append(cleaned)
        
        if not cleaned_numbers:
            return {"success": False, "error": "No valid mobile numbers provided"}
        
        # Initialize SMS service
        sms_service = HormuudSMSService()
        
        results = []
        
        if len(cleaned_numbers) == 1:
            # Single SMS
            if use_basic_auth:
                result = sms_service.send_sms_basic_auth(
                    mobile=cleaned_numbers[0],
                    message=message
                )
            else:
                result = sms_service.send_sms(
                    mobile=cleaned_numbers[0],
                    message=message
                )
            results.append(result)
        else:
            # Bulk SMS
            messages = []
            for number in cleaned_numbers:
                messages.append({
                    "mobile": number,
                    "message": message,
                    "refid": f"{doctype}_{docname}" if doctype and docname else "bulk_sms"
                })
            
            if use_basic_auth:
                results = sms_service.send_bulk_sms_basic_auth(messages)
            else:
                results = sms_service.send_bulk_sms_individual(messages)
        
        # Create SMS Log
        log_data = {
            "doctype": "SMS Log",
            "requested_numbers": ", ".join(cleaned_numbers),
            "no_of_requested_sms": len(cleaned_numbers),
            "message": message,
            # "no_of_sent_sms" : ,  # will will give value later
            # "sent_to" : ,
            # "reference_doctype": doctype,
            "sent_on": now_datetime()
        }
        
        sms_log = frappe.get_doc(log_data)
        sms_log.insert(ignore_permissions=True)
        
        # Check for any failures
        failed_messages = []
        for result in results:
            if isinstance(result, dict) and result.get("status") == "error":
                failed_messages.append(result.get("mobile", "Unknown"))
        
        if failed_messages:
            return {
                "success": False, 
                "error": f"Failed to send to {len(failed_messages)} numbers",
                "failed_numbers": failed_messages,
                "log_name": sms_log.name,
                "results": results
            }
        
        return {
            "success": True,
            "message": f"SMS sent successfully to {len(cleaned_numbers)} recipient(s)",
            "log_name": sms_log.name,
            "results": results
        }
        
    except Exception as e:
        frappe.log_error(f"SMS API Error: {str(e)}", "SMS API")
        return {"success": False, "error": str(e)}


@frappe.whitelist(allow_guest=False)
def send_async_sms(mobile_numbers, message, doctype=None, docname=None, use_basic_auth=False):
    """
    Send SMS asynchronously (in background)
    
    Args:
        mobile_numbers (str/list): Single mobile number or list of numbers
        message (str): SMS message content
        doctype (str): Optional - Document type for reference
        docname (str): Optional - Document name for reference
        use_basic_auth (bool): Whether to use Basic Auth instead of Bearer Token
    
    Returns:
        dict: Queue operation result
    """
    try:
        # Validate inputs
        if not mobile_numbers or not message:
            return {"success": False, "error": "Mobile numbers and message are required"}
        
        # Convert single mobile number to list
        if isinstance(mobile_numbers, str):
            mobile_numbers = [mobile_numbers]
        
        # Clean mobile numbers
        cleaned_numbers = []
        for number in mobile_numbers:
            cleaned = _clean_mobile_number(number)
            if cleaned:
                cleaned_numbers.append(cleaned)
        
        if not cleaned_numbers:
            return {"success": False, "error": "No valid mobile numbers provided"}
        
        # Initialize SMS service
        sms_service = HormuudSMSService()
        
        if len(cleaned_numbers) == 1:
            # Single async SMS
            if use_basic_auth:
                sms_service.send_async_sms_basic_auth(
                    mobile=cleaned_numbers[0],
                    message=message
                )
            else:
                sms_service.send_async_sms(
                    mobile=cleaned_numbers[0],
                    message=message
                )
        else:
            # Bulk async SMS
            messages = []
            for number in cleaned_numbers:
                messages.append({
                    "mobile": number,
                    "message": message,
                    "refid": f"{doctype}_{docname}" if doctype and docname else "async_bulk"
                })
            
            if use_basic_auth:
                sms_service.enqueue_bulk_sms_basic_auth(messages)
            else:
                sms_service.enqueue_bulk_sms(messages)
        
        # Create queued SMS log
        log_data = {
            "doctype": "SMS Log",
            "mobile_numbers": ", ".join(cleaned_numbers),
            "message": message,
            "message_length": len(message),
            "total_recipients": len(cleaned_numbers),
            "status": "Queued",
            "sent_via": "basic_auth" if use_basic_auth else "bearer_token",
            "reference_doctype": doctype,
            "reference_name": docname,
            "sent_on": now_datetime()
        }
        
        sms_log = frappe.get_doc(log_data)
        sms_log.insert(ignore_permissions=True)
        
        return {
            "success": True,
            "message": f"SMS queued for {len(cleaned_numbers)} recipient(s)",
            "log_name": sms_log.name
        }
        
    except Exception as e:
        frappe.log_error(f"Async SMS API Error: {str(e)}", "SMS API")
        return {"success": False, "error": str(e)} 
  

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
    
        
    
def _clean_mobile_number(number):
    """
    Clean and validate mobile number format
    """
    if not number:
        return None
    
    # Remove any non-digit characters
    cleaned = ''.join(filter(str.isdigit, str(number)))
    
    # Handle Somali mobile numbers (typically starting with 61, 62, 65, etc.)
    if cleaned.startswith('252'):
        # Already in international format
        return cleaned
    elif cleaned.startswith('0'):
        # Convert local format to international
        return '252' + cleaned[1:]
    elif len(cleaned) == 9:
        # Assume it's already without country code
        return '252' + cleaned
    elif len(cleaned) == 12 and cleaned.startswith('252'):
        # Proper international format
        return cleaned
    else:
        # Return as is, let API handle validation
        return cleaned    