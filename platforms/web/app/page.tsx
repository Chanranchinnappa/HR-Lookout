'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_super_admin: boolean;
  role?: {
    id: number;
    name: string;
    level: string;
    description: string;
  };
  permissions: string[];
}

interface Stats {
  organizations: number;
  departments: number;
  employees: number;
}

interface Organization {
  id: number;
  name: string;
}

interface Department {
  id: number;
  name: string;
}

interface Employee {
  id: number;
  first_name: string;
  last_name: string;
}

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [stats, setStats] = useState<Stats>({ organizations: 0, departments: 0, employees: 0 });
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      const token = localStorage.getItem('token');
      console.log('Token from localStorage:', token);

      if (!token) {
        console.warn('No token found, redirecting to login');
        alert("No token found, please login again.");
        router.push('/login');
        return;
      }

      try {
        // Fetch user profile
        console.log('Fetching profile...');
        const profileRes = await fetch('http://localhost:8000/api/v1/auth/profile/', {
          headers: { 'Authorization': `Token ${token}` }
        });

        console.log('Profile response status:', profileRes.status);

        if (profileRes.ok) {
          const userData = await profileRes.json();
          console.log('User data:', userData);
          setUser(userData);
        } else {
          const errorText = await profileRes.text();
          console.error('Profile fetch failed:', profileRes.status, errorText);
          alert(`Failed to fetch profile. Status ${profileRes.status}: ${errorText}`);
          localStorage.removeItem('token');
          router.push('/login');
          return;
        }

        // Fetch organizations
        const orgsRes = await fetch('http://localhost:8000/api/v1/organizations/', {
          headers: { 'Authorization': `Token ${token}` }
        });
        if (orgsRes.ok) {
          const orgsData = await orgsRes.json();
          setOrganizations(orgsData);
          setStats(prev => ({ ...prev, organizations: orgsData.length }));
        }

        // Fetch departments
        const deptsRes = await fetch('http://localhost:8000/api/v1/departments/', {
          headers: { 'Authorization': `Token ${token}` }
        });
        if (deptsRes.ok) {
          const deptsData = await deptsRes.json();
          setDepartments(deptsData);
          setStats(prev => ({ ...prev, departments: deptsData.length }));
        }

        // Fetch employees
        const empsRes = await fetch('http://localhost:8000/api/v1/employees/', {
          headers: { 'Authorization': `Token ${token}` }
        });
        if (empsRes.ok) {
          const empsData = await empsRes.json();
          setEmployees(empsData);
          setStats(prev => ({ ...prev, employees: empsData.length }));
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        alert(`Dashboard fetch error: ${error}`);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [router]);

  const handleLogout = async () => {
    const token = localStorage.getItem('token');
    try {
      await fetch('http://localhost:8000/api/v1/auth/logout/', {
        method: 'POST',
        headers: { 'Authorization': `Token ${token}` }
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
    localStorage.removeItem('token');
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">HR Lookout</h1>
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md transition-colors"
          >
            Logout
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            Welcome back, {user?.first_name || user?.username}!
          </h2>
          <div className="space-y-1">
            <p className="text-gray-600">
              <span className="font-medium">Email:</span> {user?.email}
            </p>
            {user?.role && (
              <p className="text-gray-600">
                <span className="font-medium">Role:</span>{' '}
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                  {user.role.name}
                </span>
                {user.is_super_admin && (
                  <span className="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    Super Admin
                  </span>
                )}
              </p>
            )}
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Organizations</h3>
                <p className="text-sm text-gray-600">Manage company organizations and structure</p>
              </div>
              <span className="text-3xl font-bold text-blue-600">{stats.organizations}</span>
            </div>
            <Link href="/organizations" className="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium">View All →</Link>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Departments</h3>
                <p className="text-sm text-gray-600">Manage departments and teams</p>
              </div>
              <span className="text-3xl font-bold text-green-600">{stats.departments}</span>
            </div>
            <Link href="/departments" className="inline-flex items-center text-green-600 hover:text-green-800 font-medium">View All →</Link>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Employees</h3>
                <p className="text-sm text-gray-600">Manage employee information and records</p>
              </div>
              <span className="text-3xl font-bold text-purple-600">{stats.employees}</span>
            </div>
            <Link href="/employees" className="inline-flex items-center text-purple-600 hover:text-purple-800 font-medium">View All →</Link>
          </div>
        </div>

        {/* System Info */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">System Information</h3>
              <p className="mt-1 text-sm text-blue-700">
                You are logged in with Django native authentication. Your session is secured with token-based authentication.
              </p>
            </div>
          </div>
        </div>

        {/* Recent Items Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Organizations</h3>
            {organizations.length > 0 ? (
              <ul className="space-y-2">
                {organizations.slice(0, 5).map((org) => (
                  <li key={org.id}>
                    <Link href={`/organizations/${org.id}`} className="text-blue-600 hover:text-blue-800 hover:underline">
                      {org.name}
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-sm">No organizations yet</p>
            )}
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Departments</h3>
            {departments.length > 0 ? (
              <ul className="space-y-2">
                {departments.slice(0, 5).map((dept) => (
                  <li key={dept.id}>
                    <Link href={`/departments/${dept.id}`} className="text-green-600 hover:text-green-800 hover:underline">
                      {dept.name}
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-sm">No departments yet</p>
            )}
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Employees</h3>
            {employees.length > 0 ? (
              <ul className="space-y-2">
                {employees.slice(0, 5).map((emp) => (
                  <li key={emp.id}>
                    <Link href={`/employees/${emp.id}`} className="text-purple-600 hover:text-purple-800 hover:underline">
                      {emp.first_name} {emp.last_name}
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-sm">No employees yet</p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
