# frappe-bench/apps/rasiin_design/rasiin_design/services/hormuud_sms_service.py

from typing import Dict, Optional
from frappe.utils.background_jobs import enqueue
import requests
import json
import frappe
from datetime import datetime
import time
import base64

class HormuudSMSService:
    def __init__(self):
        self.settings = frappe.get_single("Custom Sms Settings")
        BASE_URL = self.settings.sms_gateway_url
        self.TOKEN_ENDPOINT = f"{BASE_URL}/token"
        self.SMS_ENDPOINT = f"{BASE_URL}/api/sms/Send"  # Basic Auth endpoint
        self.BEARER_SMS_ENDPOINT = f"{BASE_URL}/api/SendSMS"  # Bearer Token endpoint
        self.BULK_SMS_ENDPOINT = f"{BASE_URL}/api/Outbound/SendBulkSMS"
        self.CHECK_SMS_BALANCE_ENDPOINT = f"{BASE_URL}/api/checkbalance"
        self.username = self.settings.get_password('sms_api_username')
        self.password = self.settings.get_password('sms_api_password')
        self.cache_key = "hormuud_sms_token"
        self.sender_id = self.settings.sender_name
        self.sms_character_limit = self.settings.sms_character_limit
        self.RESPONSE_CODES = {
            "200": "SUCCESS",
            "201": "Authentication Failed",
            "203": "Invalid Sender ID", 
            "204": "Zero Balance (Prepaid Account)",
            "205": "Insufficient Balance (Prepaid Account)",
            "206": "The allowed message parts are exceeded",
            "207": "Wrong mobile number",
            "500": "Unknown Error"
        }
        
    
    def _handle_api_response(self, response_data: dict, operation: str = "SMS") -> dict:
        """
        Centralized response handler for all Hormuud API responses
        """
        if not isinstance(response_data, dict):
            return {
                "success": False,
                "error": f"Invalid response format from {operation} API",
                "raw_response": response_data
            }
        
        response_code = response_data.get("ResponseCode")
        response_message = response_data.get("ResponseMessage", "")
        
        # If no ResponseCode, check if it's a success structure
        if not response_code:
            # Check if it has success indicators
            if response_data.get("success") or "MessageID" in response_data:
                return {
                    "success": True,
                    "message": f"{operation} completed successfully",
                    "data": response_data,
                    "raw_response": response_data
                }
            else:
                return {
                    "success": False,
                    "error": f"Unknown response format from {operation} API",
                    "raw_response": response_data
                }
        
        # Map response code to human-readable message
        status_message = self.RESPONSE_CODES.get(response_code, "Unknown Status Code")
        
        if response_code == "200":
            return {
                "success": True,
                "message": f"{operation} sent successfully",
                "data": response_data,
                "response_code": response_code,
                "status_message": status_message,
                "raw_response": response_data
            }
        else:
            # All other codes are errors
            error_details = {
                "success": False,
                "error": status_message,
                "response_code": response_code,
                "api_message": response_message,
                "status_message": status_message,
                "raw_response": response_data
            }
            
            # Add specific handling for common errors
            if response_code in ["204", "205"]:
                error_details["action_required"] = "Please recharge your SMS account"
            elif response_code == "201":
                error_details["action_required"] = "Check your API credentials"
            elif response_code == "203":
                error_details["action_required"] = "Check your sender ID configuration"
            elif response_code == "207":
                error_details["action_required"] = "Verify the mobile number format"
            
            return error_details    

    def _get_basic_auth_header(self) -> str:
        """Generate Basic Auth header"""
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"

    def _post_with_retry(self, url: str, headers: Dict, data: Dict, 
                        retries: int = 2, timeout: int = 10) -> Optional[requests.Response]:
        """
        Modified retry mechanism that:
        1. Prevents duplicate SMS sends
        2. Only retries on clear failures
        3. Validates responses before considering successful
        """
        last_exception = None
        last_response = None
        
        for attempt in range(retries + 1):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=timeout)
                
                # First validate the response looks successful
                if response.status_code == 200:
                    response_data = response.json()
                    if self._is_valid_response(response_data):
                        frappe.logger().debug(f"SMS API success on attempt {attempt+1}")
                        return response
                    else:
                        # If response is invalid but HTTP 200, log and retry
                        frappe.logger().warning(f"Invalid API response: {response_data}")
                        last_response = response
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.RequestException as e:
                last_exception = e
                frappe.logger().warning(f"Attempt {attempt+1} failed: {str(e)}")
                
            # Don't retry if we got a 200 but just invalid content
            if last_response and last_response.status_code == 200:
                break
                
            if attempt < retries:
                wait_time = min(2 ** attempt, 5)  # Cap at 5 seconds
                time.sleep(wait_time)
        
        # If we got a 200 response but invalid content, return it anyway
        if last_response and last_response.status_code == 200:
            return last_response
            
        raise Exception(f"POST to {url} failed after {retries+1} attempts. Last error: {str(last_exception)}")

    def _is_valid_response(self, response_data: dict) -> bool:
        """Check if API response indicates success"""
        return (
            isinstance(response_data, dict) and
            response_data.get("ResponseCode") == "200"
        )
        
    def _validate_message(self, message: str):
        """Validate message content and length"""
        if not message:
            frappe.throw("Message cannot be empty")
        if len(message) > self.sms_character_limit:
            frappe.throw(f"Message exceeds {self.sms_character_limit} character limit")   

    def _generate_token(self):
        """Generate Bearer token for token-based authentication"""
        payload = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(self.TOKEN_ENDPOINT, data=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            token = data.get("access_token")
            frappe.cache().set_value(self.cache_key, token, expires_in_sec=50)
            return token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Token generation failed: {e}")

    def _get_valid_token(self):
        """Get valid Bearer token from cache or generate new one"""
        token = frappe.cache().get_value(self.cache_key)
        if token:
            return token
        return self._generate_token()

    def check_sms_balance(self):
        """
        Endpoint: /api/checkbalance
        Checks the sms balance
        """
        
        token = self._get_valid_token()
        
        payload = {
            "service" : "smsapi"
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = self._post_with_retry(self.CHECK_SMS_BALANCE_ENDPOINT, headers, payload)
            response_data = response.json()
            return self._handle_api_response(response_data, "SMS")
            
        except Exception as e:
            frappe.log_error(f"Basic Auth SMS failed: {str(e)}")
            raise Exception(f"Basic Auth SMS sending failed: {str(e)}")
        
    def send_sms_basic_auth(self, mobile: str, message: str, refid="0", validity=0, delivery=0):
        """
        Send SMS using Basic Authentication as per Hormuud API documentation
        Endpoint: /api/sms/Send
        Method: POST
        Auth: Basic Auth
        """
        self._validate_message(message)
        
        # Prepare payload according to Hormuud Basic Auth API documentation
        payload = {
            "refid": refid,
            "mobile": mobile,
            "message": message,
            "senderid": self.sender_id,
            "validity": validity,
            "delivery": delivery
        }
        
        # Prepare headers with Basic Auth
        headers = {
            "Content-Type": "application/json",
            "Authorization": self._get_basic_auth_header()
        }
        
        try:
            response = self._post_with_retry(self.SMS_ENDPOINT, headers, payload)
            response_data = response.json()
            return self._handle_api_response(response_data, "SMS")
        except Exception as e:
            frappe.log_error(f"Basic Auth SMS failed: {str(e)}")
            raise Exception(f"Basic Auth SMS sending failed: {str(e)}")

    def send_sms(self, mobile: str, message: str, refid="0", validity=0):
        """
        Send SMS using Bearer Token authentication (original method)
        Endpoint: /api/SendSMS
        Method: POST  
        Auth: Bearer Token
        """
        self._validate_message(message)
        
        token = self._get_valid_token()
        payload = {
            "senderid": self.sender_id,
            "refid": refid,
            "mobile": mobile,
            "message": message,
            "validity": validity
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = self._post_with_retry(self.BEARER_SMS_ENDPOINT, headers, payload)
        response_data = response.json()
        return self._handle_api_response(response_data, "SMS")

    def send_bulk_sms_basic_auth(self, messages: list):
        """
        Send bulk SMS using Basic Authentication
        Sends each SMS individually using Basic Auth endpoint
        """
        results = []
        for msg in messages:
            try:
                result = self.send_sms_basic_auth(
                    mobile=msg["mobile"],
                    message=msg["message"],
                    refid=msg.get("refid", "bulk-ref"),
                    validity=msg.get("validity", 0),
                    delivery=msg.get("delivery", 0)
                )
                results.append({
                    "mobile": msg["mobile"],
                    "status": "success",
                    "response": result
                })
            except Exception as e:
                frappe.logger().error(f"Failed to send Basic Auth SMS to {msg['mobile']}: {str(e)}")
                results.append({
                    "mobile": msg["mobile"],
                    "status": "error",
                    "error": str(e)
                })
        return results

    def send_bulk_sms_individual(self, messages: list):
        """
        Sends each SMS message individually using self.send_sms().
        Useful for better tracking, retries, or logging.
        """
        results = []
        for msg in messages:
            try:
                result = self.send_sms(
                    mobile=msg["mobile"],
                    message=msg["message"],
                    refid=msg.get("refid", "bulk-ref"),
                    validity=msg.get("validity", 0)
                )
                results.append({
                    "mobile": msg["mobile"],
                    "status": "success",
                    "response": result
                })
            except Exception as e:
                frappe.logger().error(f"Failed to send SMS to {msg['mobile']}: {str(e)}")
                results.append({
                    "mobile": msg["mobile"],
                    "status": "error",
                    "error": str(e)
                })
        return results

    def send_bulk_sms(self, messages: list):
        """
        Sends SMS messages using Hormuud's bulk API in chunks of 20.
        Automatically handles batching if more than 20 messages are provided.
        """
        if not messages:
            return []

        token = self._get_valid_token()
        now = datetime.utcnow().isoformat()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        results = []

        def chunk_list(data, chunk_size):
            for i in range(0, len(data), chunk_size):
                yield data[i:i + chunk_size]

        for chunk in chunk_list(messages, 20):
            bulk_payload = []
            for msg in chunk:
                bulk_payload.append({
                    "refid": msg.get("refid", "bulk-ref"),
                    "mobile": msg["mobile"],
                    "message": msg["message"],
                    "senderid": self.sender_id,
                    "mType": 0,        # or -1 if required
                    "eType": 0,        # or -1 if required
                    "validity": msg.get("validity", 0),
                    "delivery": msg.get("delivery", 0),
                    "UDH": "",
                    "RequestDate": msg.get("RequestDate", now)
                })

            try:
                response = self._post_with_retry(self.BULK_SMS_ENDPOINT, headers, bulk_payload)
                # results.append(response.json())
                response_data = response.json()
                handled_response = self._handle_api_response(response_data, "Bulk SMS")
                results.append(handled_response)
            except Exception as e:
                frappe.logger().error(f"Bulk SMS chunk failed: {str(e)}")
                results.append({"error": str(e), "chunk": bulk_payload})

        return results

    def send_async_sms(self, mobile: str, message: str, refid="0", validity=0):
        """Queue SMS for background sending using Bearer Token"""
        enqueue(
            method=self.send_sms,
            queue='short',
            mobile=mobile,
            message=message,
            refid=refid,
            validity=validity
        )

    def send_async_sms_basic_auth(self, mobile: str, message: str, refid="0", validity=0, delivery=0):
        """Queue SMS for background sending using Basic Auth"""
        enqueue(
            method=self.send_sms_basic_auth,
            queue='short',
            mobile=mobile,
            message=message,
            refid=refid,
            validity=validity,
            delivery=delivery
        )
        
    def enqueue_bulk_sms(self, messages: list):
        """Send SMS in background using bulk logic"""
        enqueue(
            method=self.send_bulk_sms,
            queue='long',
            messages=messages
        )

    def enqueue_bulk_sms_basic_auth(self, messages: list):
        """Send SMS in background using Basic Auth"""
        enqueue(
            method=self.send_bulk_sms_basic_auth,
            queue='long',
            messages=messages
        )