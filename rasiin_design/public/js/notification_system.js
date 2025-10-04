/**
 * ====================================================================
 * Centralized Notification System
 * ====================================================================
 * This file contains the NotificationSystem class and global helper
 * functions to manage notification instances throughout the application.
 *
 * Key features:
 * - Manages the notification bell, dropdown, and real-time updates.
 * - Handles component lifecycle by properly destroying and re-initializing
 * when the UI is redrawn.
 * - Uses bound event handlers for robust cleanup to prevent memory leaks.
 */

// --- Global Instance Management ---

const notificationInstances = new Map();

/**
 * Initializes a notification system for a specific container.
 * If one already exists for the container, it destroys the old one first.
 * @param {string} containerSelector - The CSS selector for the container.
 * @returns {NotificationSystem} The new notification system instance.
 */
function initNotificationSystem(containerSelector = 'body') {
    // If an instance for this container already exists, destroy it to prevent memory leaks.
    if (notificationInstances.has(containerSelector)) {
        // console.log(`Destroying existing notification system for: ${containerSelector}`);
        const oldInstance = notificationInstances.get(containerSelector);
        oldInstance.destroy(); // Clean up old event listeners and timers
        notificationInstances.delete(containerSelector);
    }
    
    // console.log(`Initializing new notification system for: ${containerSelector}`);
    const notificationSystem = new NotificationSystem(containerSelector);
    notificationInstances.set(containerSelector, notificationSystem);
    return notificationSystem;
}

/**
 * Gets an existing notification system instance for a container.
 * @param {string} containerSelector - The CSS selector for the container.
 * @returns {NotificationSystem|undefined}
 */
function getNotificationSystem(containerSelector = 'body') {
    return notificationInstances.get(containerSelector);
}

/**
 * Manually refreshes the notification list for all active instances.
 */
function refreshAllNotifications() {
    notificationInstances.forEach(system => system.refresh());
}

/**
 * Destroys all active notification system instances and clears the registry.
 */
function destroyAllNotificationSystems() {
    notificationInstances.forEach(system => system.destroy());
    notificationInstances.clear();
}



class NotificationSystem {
    constructor(containerSelector = 'body') {
        this.containerSelector = containerSelector;
        this.dropdownVisible = false;
        this.clickInProgress = false;
        this.processingNotifications = new Set();
        this.lastClickTime = 0;
        this.CLICK_DEBOUNCE_DELAY = 300;

        // **Bind 'this' to event handlers for proper removal in destroy()**
        this.handleBellClick = this.handleBellClick.bind(this);
        this.handleNotificationClick = this.handleNotificationClick.bind(this);
        this.handleOutsideClick = this.handleOutsideClick.bind(this);
        this.handleEscapeKey = this.handleEscapeKey.bind(this);
        this.handleKeyboardNavigation = this.handleKeyboardNavigation.bind(this);
        this.handleResize = this.handleResize.bind(this);
        this.handleRealtimeUpdate = this.handleRealtimeUpdate.bind(this);

        this.init();
    }

    init() {
        this.setupNotificationEvents();
        this.fetchAndRenderNotifications();
        this.setupRealtimeListener();
    }

    fetchAndRenderNotifications() {
        frappe.db.get_list("Notification Log", {
            fields: ["name", "subject", "document_type", "document_name", "creation"],
            filters: {
                for_user: frappe.session.user,
                read: 0
            },
            order_by: "creation desc",
            limit: 20
        }).then(notifications => {
            // console.log("Fetched notifications:", notifications);
            const badge = $(this.containerSelector).find('.notification-badge');
            const list = $(this.containerSelector).find('.notification-list');
            list.empty();

            if (notifications.length > 0) {
                badge.text(notifications.length).show();
                
                notifications.forEach(notif => {
                    const time_ago = frappe.datetime.prettyDate(notif.creation);
                    const item = $(`
                        <li class="notification-item" 
                            tabindex="0"
                            data-log-name="${notif.name}"
                            data-doc-type="${notif.document_type}" 
                            data-doc-name="${notif.document_name}">
                            <div class="notification-icon">
                                <i class="fa fa-info-circle"></i>
                            </div>
                            <div class="notification-content">
                                <div class="subject">${notif.subject}</div>
                                <div class="time">${time_ago}</div>
                            </div>
                            <div class="notification-unread-dot"></div>
                        </li>
                    `);
                    list.append(item);
                });
            } else {
                badge.hide();
                list.append('<li class="no-notifications">No new notifications</li>');
            }
        });
    }

    setupNotificationEvents() {
        // console.log("Setting up notification events in:", this.containerSelector);
        
        // Use the pre-bound handlers
        $(document).on('click', `${this.containerSelector} .notification-bell-container`, this.handleBellClick);
        $(document).on('click', `${this.containerSelector} .notification-item`, this.handleNotificationClick);
        $(document).on('click', this.handleOutsideClick);
        $(document).on('keydown', this.handleEscapeKey);
        $(document).on('click', `${this.containerSelector} .notification-dropdown`, (e) => e.stopPropagation());
        $(document).on('keydown', `${this.containerSelector} .notification-dropdown`, this.handleKeyboardNavigation);
        $(window).on('resize', this.handleResize);
        
        this.setupScrollHandlers();
    }

    handleBellClick(e) {
        const now = Date.now();
        if (now - this.lastClickTime < this.CLICK_DEBOUNCE_DELAY) return;
        this.lastClickTime = now;
        
        if (this.clickInProgress) return;
        this.clickInProgress = true;
        
        e.stopPropagation();
        e.preventDefault();
        
        const $dropdown = $(this.containerSelector).find('.notification-dropdown');
        const isCurrentlyVisible = this.dropdownVisible;
        
        this.closeAllNotificationDropdowns();
        
        if (!isCurrentlyVisible) {
            this.openNotificationDropdown($dropdown);
        }
        
        setTimeout(() => { this.clickInProgress = false; }, 150);
    }

    handleNotificationClick(e) {
        const $target = $(e.currentTarget);
        if ($target.hasClass('no-notifications')) {
            e.stopPropagation();
            return;
        }
        
        const now = Date.now();
        const log_name = $target.data('log-name');
        
        // Debounce same notification clicks
        if (now - this.lastClickTime < this.CLICK_DEBOUNCE_DELAY && this.processingNotifications.has(log_name)) {
            // console.log("Same notification click debounced");
            e.stopPropagation();
            e.preventDefault();
            return;
        }
        this.lastClickTime = now;
        
        // console.log("Notification item clicked");
        const doc_type = $target.data('doc-type');
        const doc_name = $target.data('doc-name');

        if (!log_name || !doc_type || !doc_name) {
            // console.error("Missing notification data:", { log_name, doc_type, doc_name });
            return;
        }

        // Prevent duplicate processing
        if (this.processingNotifications.has(log_name)) {
            // console.log("Notification already being processed:", log_name);
            return;
        }

        this.processingNotifications.add(log_name);
        // console.log("Processing notification:", log_name);

        // Close dropdown immediately when item is clicked
        this.closeAllNotificationDropdowns();

        // Mark as read with enhanced error handling - using the same pattern as your working code
        this.markNotificationAsRead(log_name)
            .then(() => {
                // console.log("Successfully marked as read:", log_name);
                // Refresh notifications
                this.fetchAndRenderNotifications();
                // Navigate to the document
                this.navigateToDocument(doc_type, doc_name);
            })
            .catch((error) => {
                // console.error("Error processing notification:", error);
                // Even if marking fails, still navigate and refresh
                this.fetchAndRenderNotifications();
                this.navigateToDocument(doc_type, doc_name);
            })
            .then(() => {
                // Remove from processing set after a delay to prevent rapid re-clicks
                // Using .then() instead of .finally() for compatibility
                setTimeout(() => {
                    this.processingNotifications.delete(log_name);
                }, 1000);
            });
    }

    handleOutsideClick(e) {
        if (!this.dropdownVisible) return;
        
        const $target = $(e.target);
        const isClickInside = $target.closest(`${this.containerSelector} .notification-bell-container`).length > 0 || 
                              $target.closest(`${this.containerSelector} .notification-dropdown`).length > 0;
        
        if (!isClickInside) {
            this.closeAllNotificationDropdowns();
        }
    }

    handleKeyboardNavigation(e) {
        if (!this.dropdownVisible) return;

        const $items = $(this.containerSelector).find('.notification-item:not(.no-notifications)');
        if (!$items.length) return;

        const $focused = $(':focus');
        let index = $items.index($focused);

        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                index = (index + 1) % $items.length;
                $items.eq(index).focus();
                break;
            case 'ArrowUp':
                e.preventDefault();
                index = (index - 1 + $items.length) % $items.length;
                $items.eq(index).focus();
                break;
            case 'Enter': case ' ':
                if ($focused.hasClass('notification-item')) {
                    e.preventDefault();
                    $focused.trigger('click');
                }
                break;
            case 'Tab':
                setTimeout(() => {
                    if (!$(this.containerSelector).find('.notification-dropdown').find(':focus').length) {
                        this.closeAllNotificationDropdowns();
                    }
                }, 10);
                break;
        }
    }

    setupScrollHandlers() {
        const list = document.querySelector(`${this.containerSelector} .notification-list`);
        if (!list) return;

        const handleWheel = (e) => {
            if (!this.dropdownVisible) return;
            const { scrollTop, clientHeight, scrollHeight } = e.currentTarget;
            if ((scrollTop === 0 && e.deltaY < 0) || (scrollTop + clientHeight >= scrollHeight - 1 && e.deltaY > 0)) {
                e.preventDefault();
            }
        };
        list.addEventListener('wheel', handleWheel, { passive: false });
    }

    closeAllNotificationDropdowns() {
        const $dropdown = $(this.containerSelector).find('.notification-dropdown');
        if ($dropdown.length && this.dropdownVisible) {
            $dropdown.removeClass('show');
            this.dropdownVisible = false;
        }
    }

    openNotificationDropdown($dropdown) {
        if (!$dropdown.length) return;
        $dropdown.addClass('show');
        this.dropdownVisible = true;
        setTimeout(() => $dropdown.find('.notification-item:first').focus(), 100);
    }

    markNotificationAsRead(log_name) {
        return new Promise((resolve, reject) => {
            // console.log("Attempting to mark notification as read via server method:", log_name);
            
            frappe.call({
                method: 'rasiin_design.api.notification.mark_notification_as_read',
                args: {
                    log_name: log_name
                },
                callback: function(r) {
                    if (r.message && r.message.status === 'success') {
                        // console.log("Notification marked as read successfully via server method");
                        resolve();
                    } else {
                        // console.error("Failed to mark notification as read:", r.message);
                        // Even if it fails, we reject but the .then() block in the caller will still navigate
                        reject(r.message || "Unknown server error");
                    }
                },
                error: function(r) {
                    // console.error("AJAX Error marking notification as read:", r);
                    reject(r);
                }
            });
        });
    }

    navigateToDocument(doc_type, doc_name) {
        if (doc_type && doc_name) {
            // console.log("Navigating to:", doc_type, doc_name);
            try {
                // Add small delay to ensure notification is processed
                setTimeout(() => {
                    frappe.set_route('Form', doc_type, doc_name);
                }, 100);
            } catch (error) {
                // console.error("Navigation error:", error);
                // Fallback navigation
                setTimeout(() => {
                    window.location.href = `/app/${frappe.router.slug(doc_type)}/${doc_name}`;
                }, 100);
            }
        } else {
            // console.error("Invalid document type or name for navigation");
        }
    }

    handleEscapeKey(e) {
        if (e.key === 'Escape' && this.dropdownVisible) {
            this.closeAllNotificationDropdowns();
        }
    }
    
    handleResize() {
        if (this.dropdownVisible && window.innerWidth < 768) {
            this.closeAllNotificationDropdowns();
        }
    }
    
    handleRealtimeUpdate(data) {
        // // console.log("Real-time notification received:", data);
        // frappe.show_alert("New Notification", 5);
        //  // console.log("Real-time notification received:", data);
    
        if (data.type === 'new_notice') {
            frappe.show_alert({
                message: __("New Notification"),
                indicator: 'blue'
            }, 5);
            // this.fetchAndRenderNotifications();
        }
        else if (data.type === 'notification_read') {
            // frappe.show_alert({
            //     message: __("Notification Marked as read success"),
            //     indicator: 'blue'
            // }, 5);
            // // console.log("Notification marked as read:", data.log_name);
            // this.fetchAndRenderNotifications();
        }

        //
        this.fetchAndRenderNotifications();
    }

    setupRealtimeListener() {
        frappe.realtime.on("new_notification", this.handleRealtimeUpdate);
    }
    
    refresh() {
        this.fetchAndRenderNotifications();
    }

    destroy() {
        // console.log(`Destroying notification system and cleaning up events for: ${this.containerSelector}`);

        // Remove all event listeners using the saved references to the bound handlers
        $(document).off('click', `${this.containerSelector} .notification-bell-container`, this.handleBellClick);
        $(document).off('click', `${this.containerSelector} .notification-item`, this.handleNotificationClick);
        $(document).off('click', this.handleOutsideClick);
        $(document).off('keydown', this.handleEscapeKey);
        $(document).off('click', `${this.containerSelector} .notification-dropdown`);
        $(document).off('keydown', `${this.containerSelector} .notification-dropdown`, this.handleKeyboardNavigation);
        $(window).off('resize', this.handleResize);

        // Turn off the realtime listener to prevent duplicate notifications
        frappe.realtime.off("new_notification", this.handleRealtimeUpdate);
    }
}