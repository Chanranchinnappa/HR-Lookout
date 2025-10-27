//services/web/types/index.ts

// Organization Types
export interface Organization {
  id: number;
  name: string;
  legal_name: string;
  email: string;
  phone?: string;
  website?: string;
  address_line1: string;
  address_line2?: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
  tax_id: string;
  registration_number?: string;
  fiscal_year_start: string;
  currency: string;
  timezone: string;
  logo_url?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  employee_count?: number;
  department_count?: number;
}

// Department Types
export interface Department {
  id: number;
  organization: number;
  organization_name?: string;
  parent_department?: number;
  name: string;
  code: string;
  description?: string;
  head?: number;  // ✅ Added
  head_name?: string;  // ✅ Added
  cost_center?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  employee_count?: number;
}

// Employee Types
export interface Employee {
  id: number;
  employee_id: string;
  organization: number;
  organization_name?: string;
  department?: number;
  department_name?: string;
  manager?: number;
  manager_name?: string;
  first_name: string;
  last_name: string;
  middle_name?: string;
  preferred_name?: string;
  full_name?: string;
  email: string;
  personal_email?: string;
  phone?: string;
  mobile?: string;
  date_of_birth?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  job_title: string;
  employment_status: 'ACTIVE' | 'INACTIVE' | 'ON_LEAVE' | 'TERMINATED';
  employment_type: 'FULL_TIME' | 'PART_TIME' | 'CONTRACT' | 'INTERN';
  hire_date: string;
  termination_date?: string;
  profile_picture?: string;
  bio?: string;
  created_at: string;
  updated_at: string;
}

// API Response Types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
