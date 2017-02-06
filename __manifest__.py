{
    'name' : 'Biometric Device Integration',
    'version' : '1.0',
    
    'author' : 'Gaurav Sahu, David Tran',
    
    'category' : 'Human Resources',
    'website' : 'https://www.erponline.vn',
    
    'description': 'A Module for Biometric Device Integration',
    
    'depends': ['hr_attendance'],

    'data' : [
        'data/schedule.xml',
        'views/biometric_machine_view.xml',
        'views/hr_employee_views.xml',
#         'report/daily_attendance_view.xml',        
        'wizard/schedule_wizard.xml',
    ],
    'installable': True
}
