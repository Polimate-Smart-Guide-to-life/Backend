# Generated manually to populate initial FAQ data

from django.db import migrations


def populate_faqs(apps, schema_editor):
    """Populate FAQ data from mock data"""
    FAQCategory = apps.get_model('faqs', 'FAQCategory')
    FAQSubcategory = apps.get_model('faqs', 'FAQSubcategory')
    FAQItem = apps.get_model('faqs', 'FAQItem')

    # Define categories and their data
    categories_data = [
        {
            'name': 'Academic Policies',
            'icon': 'book',
            'description': 'Grading, attendance, and course policies',
            'order': 1,
            'subcategories': [
                {'name': 'Grading', 'order': 1},
                {'name': 'Attendance', 'order': 2},
                {'name': 'Courses', 'order': 3},
            ],
            'faqs': [
                {
                    'question': 'What is the grading system?',
                    'answer': 'We use a letter grading system: A (90-100), B (80-89), C (70-79), D (60-69), F (below 60). Plus and minus grades are also used (e.g., A-, B+).',
                    'subcategory': 'Grading',
                    'tags': ['grades', 'grading'],
                    'order': 1,
                },
                {
                    'question': 'How do I appeal a grade?',
                    'answer': 'To appeal a grade, submit a written request to your professor within 7 days of receiving the grade. Include specific reasons and supporting documentation.',
                    'subcategory': 'Grading',
                    'tags': ['appeal', 'grades'],
                    'order': 2,
                },
                {
                    'question': 'What is the attendance policy?',
                    'answer': 'Students are expected to attend at least 80% of classes. Excessive absences may result in grade reduction or course failure.',
                    'subcategory': 'Attendance',
                    'tags': ['attendance', 'absence'],
                    'order': 1,
                },
                {
                    'question': 'Can I retake a failed course?',
                    'answer': 'Yes, you can retake a failed course. The new grade will replace the previous grade in your GPA calculation. Contact the registrar for approval.',
                    'subcategory': 'Courses',
                    'tags': ['retake', 'failed'],
                    'order': 1,
                },
            ],
        },
        {
            'name': 'Registration',
            'icon': 'calendar',
            'description': 'Course registration and enrollment',
            'order': 2,
            'subcategories': [
                {'name': 'Course Registration', 'order': 1},
                {'name': 'Add/Drop', 'order': 2},
            ],
            'faqs': [
                {
                    'question': 'How do I register for classes?',
                    'answer': 'Log into the student portal, go to Course Registration, select your desired courses, and click Register. Registration opens based on your class standing.',
                    'subcategory': 'Course Registration',
                    'tags': ['register', 'classes'],
                    'order': 1,
                },
                {
                    'question': 'What is the registration deadline?',
                    'answer': 'Registration typically opens 4 weeks before the semester and closes on the last day of the add/drop period, usually the second week of classes.',
                    'subcategory': 'Course Registration',
                    'tags': ['deadline', 'registration'],
                    'order': 2,
                },
                {
                    'question': 'How do I add or drop a class?',
                    'answer': 'During the add/drop period, use the Course Registration section in the portal. After the deadline, you need permission from the registrar and may incur fees.',
                    'subcategory': 'Add/Drop',
                    'tags': ['add', 'drop'],
                    'order': 1,
                },
                {
                    'question': 'What are prerequisites?',
                    'answer': 'Prerequisites are required courses you must complete before enrolling in an advanced course. The system will prevent registration if prerequisites are not met.',
                    'subcategory': 'Course Registration',
                    'tags': ['prerequisites'],
                    'order': 3,
                },
            ],
        },
        {
            'name': 'Financial Aid',
            'icon': 'wallet',
            'description': 'Financial assistance and scholarships',
            'order': 3,
            'subcategories': [
                {'name': 'Application', 'order': 1},
                {'name': 'Scholarships', 'order': 2},
                {'name': 'Loans', 'order': 3},
                {'name': 'Issues', 'order': 4},
            ],
            'faqs': [
                {
                    'question': 'How do I apply for financial aid?',
                    'answer': 'Complete the FAFSA form online at fafsa.gov and submit required documents to the Financial Aid Office by the priority deadline.',
                    'subcategory': 'Application',
                    'tags': ['fafsa', 'financial aid'],
                    'order': 1,
                },
                {
                    'question': 'When are scholarships available?',
                    'answer': 'Scholarship applications open in the fall for the following academic year. Deadlines vary by scholarship. Check the Financial Aid portal regularly.',
                    'subcategory': 'Scholarships',
                    'tags': ['scholarships'],
                    'order': 1,
                },
                {
                    'question': 'How do student loans work?',
                    'answer': 'Student loans must be repaid with interest. Federal loans offer better terms than private loans. Complete entrance counseling before receiving funds.',
                    'subcategory': 'Loans',
                    'tags': ['loans', 'student loans'],
                    'order': 1,
                },
                {
                    'question': 'What happens if I lose financial aid?',
                    'answer': 'Contact the Financial Aid Office immediately. You may need to appeal or establish a payment plan. Late payments may affect registration.',
                    'subcategory': 'Issues',
                    'tags': ['appeal', 'aid'],
                    'order': 1,
                },
            ],
        },
        {
            'name': 'Campus Services',
            'icon': 'business',
            'description': 'Library, health, and support services',
            'order': 4,
            'subcategories': [
                {'name': 'Library', 'order': 1},
                {'name': 'Health', 'order': 2},
            ],
            'faqs': [
                {
                    'question': 'Where is the library located?',
                    'answer': 'The main library is in Building A, 2nd floor. It\'s open Monday-Friday 8am-10pm, weekends 10am-6pm. Extended hours during finals.',
                    'subcategory': 'Library',
                    'tags': ['library', 'study'],
                    'order': 1,
                },
                {
                    'question': 'How do I reserve a study room?',
                    'answer': 'Use the library website or mobile app to reserve study rooms up to 2 weeks in advance. Rooms can be booked for 2-hour blocks.',
                    'subcategory': 'Library',
                    'tags': ['study room', 'reserve'],
                    'order': 2,
                },
                {
                    'question': 'Where is the health center?',
                    'answer': 'The Student Health Center is in Building C, 1st floor. Hours are Monday-Friday 9am-5pm. Appointments required for non-emergencies.',
                    'subcategory': 'Health',
                    'tags': ['health', 'medical'],
                    'order': 1,
                },
                {
                    'question': 'How do I access counseling services?',
                    'answer': 'Call the Counseling Center at (555) 123-4567 or visit Building D, 3rd floor. Services are free and confidential for all students.',
                    'subcategory': 'Health',
                    'tags': ['counseling', 'mental health'],
                    'order': 2,
                },
            ],
        },
        {
            'name': 'Housing',
            'icon': 'home',
            'description': 'On-campus housing and residence life',
            'order': 5,
            'subcategories': [
                {'name': 'On-Campus', 'order': 1},
            ],
            'faqs': [
                {
                    'question': 'How do I apply for on-campus housing?',
                    'answer': 'Submit a housing application through the Housing Portal by May 1st for fall semester. Priority is given to first-year students.',
                    'subcategory': 'On-Campus',
                    'tags': ['housing', 'dorm'],
                    'order': 1,
                },
                {
                    'question': 'What are the housing costs?',
                    'answer': 'On-campus housing ranges from $8,000-$12,000 per academic year depending on room type and meal plan selection.',
                    'subcategory': 'On-Campus',
                    'tags': ['costs', 'housing'],
                    'order': 2,
                },
                {
                    'question': 'Can I change my room assignment?',
                    'answer': 'Room change requests open after the first month of each semester. Submit a request through the Housing Portal. Changes depend on availability.',
                    'subcategory': 'On-Campus',
                    'tags': ['room change'],
                    'order': 3,
                },
            ],
        },
        {
            'name': 'Technology',
            'icon': 'laptop',
            'description': 'IT support and tech resources',
            'order': 6,
            'subcategories': [
                {'name': 'Account', 'order': 1},
                {'name': 'Network', 'order': 2},
                {'name': 'Support', 'order': 3},
            ],
            'faqs': [
                {
                    'question': 'How do I reset my student portal password?',
                    'answer': 'Go to the login page and click "Forgot Password". Enter your student ID and email. You\'ll receive a reset link within minutes.',
                    'subcategory': 'Account',
                    'tags': ['password', 'reset'],
                    'order': 1,
                },
                {
                    'question': 'How do I access Wi-Fi on campus?',
                    'answer': 'Connect to "CampusWiFi" network and log in with your student credentials. Download the campus Wi-Fi app for easier connection.',
                    'subcategory': 'Network',
                    'tags': ['wifi', 'internet'],
                    'order': 1,
                },
                {
                    'question': 'Where can I get help with my laptop?',
                    'answer': 'Visit the IT Help Desk in Building B, 1st floor, or call (555) 987-6543. They can help with software, hardware, and network issues.',
                    'subcategory': 'Support',
                    'tags': ['it', 'tech support'],
                    'order': 1,
                },
            ],
        },
        {
            'name': 'Student Life',
            'icon': 'people',
            'description': 'Clubs, dining, and campus activities',
            'order': 7,
            'subcategories': [
                {'name': 'Clubs', 'order': 1},
                {'name': 'Dining', 'order': 2},
                {'name': 'Athletics', 'order': 3},
            ],
            'faqs': [
                {
                    'question': 'How do I join student clubs?',
                    'answer': 'Attend the Student Activities Fair at the beginning of each semester or visit the Student Activities Office. Most clubs welcome new members year-round.',
                    'subcategory': 'Clubs',
                    'tags': ['clubs', 'activities'],
                    'order': 1,
                },
                {
                    'question': 'What dining options are available?',
                    'answer': 'We have 3 dining halls, a food court with multiple vendors, and several cafes across campus. Meal plans are required for on-campus students.',
                    'subcategory': 'Dining',
                    'tags': ['dining', 'food'],
                    'order': 1,
                },
                {
                    'question': 'How do I get involved in sports?',
                    'answer': 'Try out for varsity teams or join intramural sports. Contact the Athletics Department or visit the Recreation Center for intramural registration.',
                    'subcategory': 'Athletics',
                    'tags': ['sports', 'athletics'],
                    'order': 1,
                },
            ],
        },
    ]

    # Create categories and their data
    for cat_data in categories_data:
        category, created = FAQCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'icon': cat_data.get('icon', ''),
                'description': cat_data.get('description', ''),
                'order': cat_data.get('order', 0),
            }
        )

        # Create subcategories
        for subcat_data in cat_data.get('subcategories', []):
            subcategory, _ = FAQSubcategory.objects.get_or_create(
                name=subcat_data['name'],
                category=category,
                defaults={'order': subcat_data.get('order', 0)}
            )

            # Create FAQs for this subcategory
            for faq_data in cat_data.get('faqs', []):
                if faq_data.get('subcategory') == subcat_data['name']:
                    FAQItem.objects.get_or_create(
                        question=faq_data['question'],
                        category=category,
                        subcategory=subcategory,
                        defaults={
                            'answer': faq_data['answer'],
                            'tags': faq_data.get('tags', []),
                            'order': faq_data.get('order', 0),
                        }
                    )


def reverse_populate_faqs(apps, schema_editor):
    """Reverse migration - delete all FAQ data"""
    FAQItem = apps.get_model('faqs', 'FAQItem')
    FAQSubcategory = apps.get_model('faqs', 'FAQSubcategory')
    FAQCategory = apps.get_model('faqs', 'FAQCategory')

    # Delete in order to respect foreign key constraints
    FAQItem.objects.all().delete()
    FAQSubcategory.objects.all().delete()
    FAQCategory.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_faqs, reverse_populate_faqs),
    ]
