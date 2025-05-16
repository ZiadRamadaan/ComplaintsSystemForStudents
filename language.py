TEXTS = {
    "English": {
        # Titles and Sections
        "title": "Complaints Management System",
        "admin_login": "Admin Login",
        "student_login": "Student Login",
        "select_section": "Select a Section",
        "file_complaint": "File a New Complaint",
        "manage_complaints": "Manage Complaints",
        "analytics": "Analytics",
        "export_data": "Export Data",
        "logout": "Log out",
        
        # Login
        "username": "Username",
        "password": "Password",
        "login_button": "Login",
        "login_success": "Login successful.",
        "login_error": "Incorrect username or password.",
        "first_login_warning": "Please change your default admin password from the settings.",
        
        # Complaint Form
        "new_complaint": "File a New Complaint",
        "student_id": "Student ID",
        "complaint_type": "Complaint Type",
        "complaint_types": ["Complaint", "Inquiry", "Suggestion"],
        "complaint_content": "Complaint Content",
        "priority": "Complaint Priority",
        "priorities": ["High", "Medium", "Low"],
        "submit": "Submit",
        "fill_fields": "Please fill in all fields.",
        "complaint_success": "Complaint submitted successfully.",
        "complaint_email_success": "Complaint submitted and emails sent successfully!",
        "complaint_email_fail": "Complaint submitted, but failed to send emails.",
        "student_not_found": "Student ID not found.",
        
        # Manage Complaints
        "manage_complaints_title": "View and Manage Complaints",
        "filter_complaints": "Filter Complaints",
        "status": "Status",
        "type": "Type",
        "update_status": "Update Complaint Status",
        "complaint_id": "Complaint ID",
        "new_status": "Select New Status",
        "statuses": ["Pending", "Reviewed", "Closed"],
        "update_button": "Update Status",
        "status_updated": "Complaint status updated.",
        "no_complaints": "No complaints registered.",
        
        # Ratings and Feedback
        "satisfaction": "Customer Satisfaction Rating (Optional)",
        "rating": "Service Rating (1 to 5)",
        "feedback": "Additional Comments",
        "submit_rating": "Submit Rating",
        "rating_success": "Rating submitted. Thank you!",
        
        # Search Complaint
        "search_complaint": "Search for Complaint by ID",
        "search_id": "Enter Complaint ID",
        "search_button": "Search",
        "complaint_details": "Complaint Details:",
        "no_complaint": "No complaint found with this ID.",
        
        # Analytics
        "analytics_title": "Complaint Analytics",
        "by_category": "Complaints by Category",
        "by_status": "Complaints by Status",
        "status_distribution": "Status Distribution",
        "by_priority": "Complaints by Priority",
        "no_data": "No data available for analysis.",
        
        # Export
        "export_title": "Export Data",
        "download_csv": "Download CSV",
        "no_data_export": "No data to export.",
        
        # Notifications and Emails
        "notifications": "Notifications",
        "email_error": "Error while sending email: {e}",
        "email_subject_new": "New Complaint",
        "email_body_new": (
            "New complaint received from student ID: {student_id}.\n"
            "Type: {category}\nPriority: {priority}\n\nContent:\n{content}"
        ),
        "email_subject_update": "Complaint Status Update",
        "email_body_update": "Complaint ID {id} status changed to: {status}.",
        "notification_status": "Complaint ID {id} status updated to {status}.",
        
        # Admin Password Change
        "change_password_title": "Change Admin Password",
        "old_password": "Old Password",
        "new_password": "New Password",
        "confirm_password": "Confirm Password",
        "change_password_button": "Change Password",
        "password_change_success": "Password changed successfully.",
        "password_change_error": "Passwords do not match or invalid input.",
        "incorrect_old_password": "The old password is incorrect.",
        
        # Sidebar and Misc
        "sidebar_change_password": "Change Password",
        "admin_expander": "Are you an admin? Click here to log in",
        "student_info": "Student Information:"
    },
    "Arabic": {
        # Titles and Sections
        "title": "نظام إدارة الشكاوى",
        "admin_login": "تسجيل دخول المسؤول",
        "student_login": "تسجيل دخول الطالب",
        "select_section": "اختر القسم",
        "file_complaint": "تقديم شكوى جديدة",
        "manage_complaints": "إدارة الشكاوى",
        "analytics": "التحليلات",
        "export_data": "تصدير البيانات",
        "logout": "تسجيل الخروج",
        
        # Login
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login_button": "تسجيل الدخول",
        "login_success": "تم تسجيل الدخول بنجاح.",
        "login_error": "اسم المستخدم أو كلمة المرور غير صحيحة.",
        "first_login_warning": "يرجى تغيير كلمة مرور المسؤول الافتراضية من الإعدادات.",
        
        # Complaint Form
        "new_complaint": "تقديم شكوى جديدة",
        "student_id": "الرقم القومي",
        "complaint_type": "نوع الشكوى",
        "complaint_types": ["شكوى", "استفسار", "اقتراح"],
        "complaint_content": "محتوى الشكوى",
        "priority": "أولوية الشكوى",
        "priorities": ["عالية", "متوسطة", "منخفضة"],
        "submit": "إرسال",
        "fill_fields": "من فضلك، املأ جميع الحقول.",
        "complaint_success": "تم تقديم الشكوى بنجاح.",
        "complaint_email_success": "تم تقديم الشكوى وإرسال الإيميلات بنجاح!",
        "complaint_email_fail": "تم تقديم الشكوى ولكن فشل إرسال الإيميلات.",
        "student_not_found": "الرقم القومي غير موجود في النظام.",
        
        # Manage Complaints
        "manage_complaints_title": "عرض وإدارة الشكاوى",
        "filter_complaints": "تصفية الشكاوى",
        "status": "الحالة",
        "type": "النوع",
        "update_status": "تحديث حالة الشكوى",
        "complaint_id": "رقم الشكوى",
        "new_status": "اختر الحالة الجديدة",
        "statuses": ["قيد الانتظار", "تم المراجعة", "مغلقة"],
        "update_button": "تحديث الحالة",
        "status_updated": "تم تحديث حالة الشكوى.",
        "no_complaints": "لا توجد شكاوى مسجلة.",
        
        # Ratings and Feedback
        "satisfaction": "تقييم رضا العملاء (اختياري)",
        "rating": "تقييم الخدمة (من 1 إلى 5)",
        "feedback": "تعليقات إضافية",
        "submit_rating": "إرسال التقييم",
        "rating_success": "تم إرسال التقييم. شكراً لك!",
        
        # Search Complaint
        "search_complaint": "البحث عن شكوى برقم",
        "search_id": "أدخل رقم الشكوى",
        "search_button": "بحث",
        "complaint_details": "تفاصيل الشكوى:",
        "no_complaint": "لا توجد شكوى بهذا الرقم.",
        
        # Analytics
        "analytics_title": "تحليلات الشكاوى",
        "by_category": "الشكاوى حسب النوع",
        "by_status": "الشكاوى حسب الحالة",
        "status_distribution": "توزيع الحالات",
        "by_priority": "الشكاوى حسب الأولوية",
        "no_data": "لا توجد بيانات متاحة للتحليل.",
        
        # Export
        "export_title": "تصدير البيانات",
        "download_csv": "تحميل CSV",
        "no_data_export": "لا توجد بيانات للتصدير.",
        
        # Notifications and Emails
        "notifications": "الإشعارات",
        "email_error": "حدث خطأ أثناء إرسال البريد الإلكتروني: {e}",
        "email_subject_new": "شكوى جديدة",
        "email_body_new": (
            "تم استلام شكوى جديدة من الرقم القومي: {student_id}.\n"
            "النوع: {category}\nالأولوية: {priority}\n\nالمحتوى:\n{content}"
        ),
        "email_subject_update": "تحديث حالة الشكوى",
        "email_body_update": "تم تغيير حالة الشكوى رقم {id} إلى: {status}.",
        "notification_status": "تم تحديث حالة الشكوى رقم {id} إلى {status}.",
        
        # Admin Password Change
        "change_password_title": "تغيير كلمة مرور المسؤول",
        "old_password": "كلمة المرور القديمة",
        "new_password": "كلمة المرور الجديدة",
        "confirm_password": "تأكيد كلمة المرور",
        "change_password_button": "تغيير كلمة المرور",
        "password_change_success": "تم تغيير كلمة المرور بنجاح.",
        "password_change_error": "كلمات المرور غير متطابقة أو الإدخال غير صالح.",
        "incorrect_old_password": "كلمة المرور القديمة غير صحيحة.",
        
        # Sidebar and Misc
        "sidebar_change_password": "تغيير كلمة المرور",
        "admin_expander": "هل أنت مسؤول؟ اضغط هنا لتسجيل الدخول",
        "student_info": "معلومات الطالب:"
    }
}
