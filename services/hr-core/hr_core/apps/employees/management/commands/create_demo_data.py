"""
Django management command to create comprehensive demo data for HR-Lookout.

Usage:
    docker-compose exec hr-core python manage.py create_demo_data
    docker-compose exec hr-core python manage.py create_demo_data --clear
"""

from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, date
import random

from hr_core.apps.employees.models import Employee, Department, Document
from hr_core.apps.employees.models.employee import EmploymentStatus
from hr_core.apps.organizations.models import Organization


class Command(BaseCommand):
    help = 'Creates comprehensive demo data for HR-Lookout system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing data before creating demo data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing all existing data...'))
            self.clear_data()
            self.stdout.write(self.style.SUCCESS('✓ Data cleared'))

        self.stdout.write(self.style.WARNING('Creating demo data...'))
        
        try:
            organizations = self.create_organizations()
            departments = self.create_departments(organizations)
            employees = self.create_employees(organizations, departments)
            self.create_documents(employees)
                
            self.stdout.write(self.style.SUCCESS('\n' + '='*60))
            self.stdout.write(self.style.SUCCESS('✓ Demo data created successfully!'))
            self.stdout.write(self.style.SUCCESS('='*60))
            self.print_summary()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Error: {str(e)}'))
            raise

    def clear_data(self):
        """Clear all existing data"""
        Document.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()
        Organization.objects.all().delete()

    def create_organizations(self):
        """Create 5 sample organizations"""
        self.stdout.write('\n📊 Creating organizations...')
        
        orgs_data = [
            {
                'name': 'TechCorp Global',
                'legal_name': 'TechCorp Global Inc.',
                'email': 'info@techcorp.com',
                'phone': '+1-555-0100',
                'website': 'https://techcorp.com',
                'address_line1': '123 Innovation Drive',
                'city': 'San Francisco',
                'state': 'CA',
                'postal_code': '94105',
                'country': 'USA',
                'tax_id': 'TC-123456789',
                'registration_number': 'REG-TC-2020',
                'fiscal_year_start': date(2025, 1, 1),
                'currency': 'USD',
                'timezone': 'America/Los_Angeles',
            },
            {
                'name': 'DataSystems Ltd',
                'legal_name': 'DataSystems Limited',
                'email': 'contact@datasystems.co.uk',
                'phone': '+44-20-7946-0958',
                'website': 'https://datasystems.co.uk',
                'address_line1': '45 Tech Park',
                'city': 'London',
                'state': 'England',
                'postal_code': 'SW1A 1AA',
                'country': 'UK',
                'tax_id': 'DS-GB987654321',
                'registration_number': 'REG-DS-2019',
                'fiscal_year_start': date(2025, 4, 1),
                'currency': 'GBP',
                'timezone': 'Europe/London',
            },
            {
                'name': 'InnovateLabs',
                'legal_name': 'InnovateLabs Private Limited',
                'email': 'hello@innovatelabs.in',
                'phone': '+91-80-4567-8900',
                'website': 'https://innovatelabs.in',
                'address_line1': '12 Cyber City',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'postal_code': '560001',
                'country': 'India',
                'tax_id': 'IN-GSTIN-123456',
                'registration_number': 'REG-IL-2021',
                'fiscal_year_start': date(2025, 4, 1),
                'currency': 'INR',
                'timezone': 'Asia/Kolkata',
            },
            {
                'name': 'CloudVentures',
                'legal_name': 'CloudVentures Australia Pty Ltd',
                'email': 'info@cloudventures.com.au',
                'phone': '+61-2-9876-5432',
                'website': 'https://cloudventures.com.au',
                'address_line1': '88 Cloud Street',
                'city': 'Sydney',
                'state': 'NSW',
                'postal_code': '2000',
                'country': 'Australia',
                'tax_id': 'CV-AU123456789',
                'registration_number': 'REG-CV-2022',
                'fiscal_year_start': date(2025, 7, 1),
                'currency': 'AUD',
                'timezone': 'Australia/Sydney',
            },
            {
                'name': 'FutureWorks GmbH',
                'legal_name': 'FutureWorks GmbH',
                'email': 'kontakt@futureworks.de',
                'phone': '+49-30-1234-5678',
                'website': 'https://futureworks.de',
                'address_line1': '10 Innovationstrasse',
                'city': 'Berlin',
                'state': 'Berlin',
                'postal_code': '10115',
                'country': 'Germany',
                'tax_id': 'FW-DE987654321',
                'registration_number': 'REG-FW-2020',
                'fiscal_year_start': date(2025, 1, 1),
                'currency': 'EUR',
                'timezone': 'Europe/Berlin',
            },
        ]

        organizations = []
        for org_data in orgs_data:
            org = Organization.objects.create(**org_data)
            organizations.append(org)
            self.stdout.write(f'  ✓ Created: {org.name}')

        return organizations

    def create_departments(self, organizations):
        """Create departments with globally unique base names"""
        self.stdout.write('\n🏢 Creating departments...')
        
        departments = []
        dept_counter = 1
        
        # Use completely unique names
        all_dept_names = [
            'Human Resources', 'Engineering', 'Sales', 'Marketing', 'Finance',
            'Operations', 'Customer Success', 'Product Development',
            'IT Infrastructure', 'Legal Affairs', 'Research Innovation',
            'Creative Design', 'Quality Assurance', 'Business Development',
            'Strategic Planning', 'Client Relations', 'Data Analytics'
        ]
        
        random.shuffle(all_dept_names)
        
        idx = 0
        for org in organizations:
            num_depts = random.randint(2, 4)
            
            for _ in range(num_depts):
                if idx >= len(all_dept_names):
                    break
                    
                dept_name = all_dept_names[idx]
                dept = Department.objects.create(
                    organization=org,
                    name=dept_name,
                    description=f"{dept_name} for {org.name}",
                    cost_center=f"CC-{dept_counter:03d}",
                    is_active=True
                )
                departments.append(dept)
                self.stdout.write(f'  ✓ Created: {dept.name} (Code: {dept.code}) @ {org.name}')
                dept_counter += 1
                idx += 1

        return departments

    def create_employees(self, organizations, departments):
        """Create 25-30 employees with realistic data"""
        self.stdout.write('\n👥 Creating employees...')
        
        first_names = [
            'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
            'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
            'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
        ]
        
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson',
        ]
        
        job_titles = [
            'Software Engineer', 'Senior Software Engineer', 'Engineering Manager',
            'HR Manager', 'HR Specialist', 'Recruiter',
            'Sales Manager', 'Sales Executive', 'Account Manager',
            'Marketing Manager', 'Content Writer', 'Marketing Specialist',
            'Financial Analyst', 'Accountant', 'Finance Manager',
            'Product Manager', 'Product Owner', 'Operations Manager',
        ]
        
        statuses = [
            EmploymentStatus.ACTIVE,
            EmploymentStatus.ACTIVE,
            EmploymentStatus.ACTIVE,
            EmploymentStatus.ACTIVE,
            EmploymentStatus.ACTIVE,
            EmploymentStatus.ON_LEAVE,
            EmploymentStatus.INACTIVE,
        ]

        employees = []
        
        for dept in departments:
            num_employees = random.randint(1, 3)
            
            for _ in range(num_employees):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                
                days_ago = random.randint(0, 1095)
                hire_date = datetime.now().date() - timedelta(days=days_ago)
                
                age_in_days = random.randint(25*365, 60*365)
                date_of_birth = datetime.now().date() - timedelta(days=age_in_days)
                
                employee = Employee.objects.create(
                    organization=dept.organization,
                    department=dept,
                    first_name=first_name,
                    last_name=last_name,
                    email=f"{first_name.lower()}.{last_name.lower()}.{random.randint(1,999)}@{dept.organization.name.lower().replace(' ', '')}.com",
                    phone=f"+1-555-{random.randint(1000, 9999)}",
                    job_title=random.choice(job_titles),
                    status=random.choice(statuses),
                    hire_date=hire_date,
                    date_of_birth=date_of_birth,
                    address_line1=f"{random.randint(1, 999)} Main Street",
                    city=dept.organization.city,
                    state=dept.organization.state,
                    postal_code=dept.organization.postal_code,
                    country=dept.organization.country,
                    emergency_contact_name=f"{random.choice(first_names)} {random.choice(last_names)}",
                    emergency_contact_phone=f"+1-555-{random.randint(1000, 9999)}",
                    emergency_contact_relationship=random.choice(['Spouse', 'Parent', 'Sibling'])
                )
                
                employees.append(employee)
                self.stdout.write(f'  ✓ Created: {employee.get_full_name()} - {employee.job_title}')

        self.stdout.write('\n👔 Assigning managers...')
        dept_employees = {}
        for emp in employees:
            if emp.department_id not in dept_employees:
                dept_employees[emp.department_id] = []
            dept_employees[emp.department_id].append(emp)
        
        for dept_id, emps in dept_employees.items():
            if len(emps) > 1:
                manager = emps[0]
                for emp in emps[1:]:
                    emp.manager = manager
                    emp.save()
                    self.stdout.write(f'  ✓ {emp.get_full_name()} → {manager.get_full_name()}')

        return employees

    def create_documents(self, employees):
        """Create sample documents"""
        self.stdout.write('\n📄 Creating documents...')
        
        doc_types = ['CONTRACT', 'ID_PROOF', 'EDUCATION', 'EXPERIENCE']
        doc_titles = {
            'CONTRACT': 'Employment Contract',
            'ID_PROOF': 'Government ID',
            'EDUCATION': 'Degree Certificate',
            'EXPERIENCE': 'Experience Letter'
        }
        
        selected = random.sample(employees, k=min(len(employees) // 2, len(employees)))
        
        for emp in selected:
            num_docs = random.randint(1, 3)
            for doc_type in random.sample(doc_types, min(num_docs, len(doc_types))):
                Document.objects.create(
                    organization=emp.organization,
                    employee=emp,
                    title=doc_titles[doc_type],
                    document_type=doc_type,
                    file_key=f"documents/{emp.employee_id}/{doc_type.lower()}.pdf",
                    file_name=f"{doc_type.lower()}.pdf",
                    file_size=random.randint(50000, 5000000),
                    mime_type='application/pdf',
                    is_archived=False
                )
                self.stdout.write(f'  ✓ Created: {doc_titles[doc_type]} for {emp.get_full_name()}')

    def print_summary(self):
        """Print summary"""
        self.stdout.write('\n📊 SUMMARY:')
        self.stdout.write(f'  Organizations: {Organization.objects.count()}')
        self.stdout.write(f'  Departments:   {Department.objects.count()}')
        self.stdout.write(f'  Employees:     {Employee.objects.count()}')
        self.stdout.write(f'  Documents:     {Document.objects.count()}')
        self.stdout.write('\n🌐 View at: http://localhost:3000')
