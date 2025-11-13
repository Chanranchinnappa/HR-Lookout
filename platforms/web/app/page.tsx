'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { authApi, tokenManager, organizationsApi, employeesApi, departmentsApi } from '@/lib/api';

interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
}

interface Stats {
  organizations: number;
  departments: number;
  employees: number;
}

interface Organization {
  id: number;
  name: string;
  description?: string;
}

interface Department {
  id: number;
  name: string;
  organization?: number;
}

interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
}

export default function Home() {
  const [user, setUser] = useState<User | null>(null);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [stats, setStats] = useState<Stats>({ organizations: 0, departments: 0, employees: 0 });
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      const token = tokenManager.get();
      
      if (!token) {
        router.push('/login');
        return;
      }

      try {
        const response = await authApi.getCurrentUser();
        setUser(response.data);
        await fetchData();
      } catch (error) {
        console.error('Auth check failed:', error);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  const fetchData = async () => {
    try {
      const [orgsRes, deptsRes, empsRes] = await Promise.all([
        organizationsApi.getAll().catch(() => ({ data: { results: [] } })),
        departmentsApi.getAll().catch(() => ({ data: { results: [] } })),
        employeesApi.getAll().catch(() => ({ data: { results: [] } })),
      ]);

      const orgsData = orgsRes.data.results || [];
      const deptsData = deptsRes.data.results || [];
      const empsData = empsRes.data.results || [];

      setOrganizations(orgsData);
      setDepartments(deptsData);
      setEmployees(empsData);
      
      setStats({
        organizations: orgsData.length,
        departments: deptsData.length,
        employees: empsData.length,
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const handleLogout = async () => {
    await authApi.logout();
    router.push('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with Logout */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">HR Lookout</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            Welcome back, {user?.first_name || user?.username}!
          </h2>
          <p className="text-gray-600">
            <span className="font-medium">Email:</span> {user?.email}
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Organizations Card */}
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-gray-900">Organizations</h3>
              <span className="text-3xl font-bold text-blue-600">{stats.organizations}</span>
            </div>
            <p className="text-gray-600 text-sm mb-4">Manage company organizations and structure</p>
            <Link
              href="/organizations"
              className="inline-block px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm"
            >
              View All →
            </Link>
          </div>

          {/* Departments Card */}
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-gray-900">Departments</h3>
              <span className="text-3xl font-bold text-green-600">{stats.departments}</span>
            </div>
            <p className="text-gray-600 text-sm mb-4">Manage departments and teams</p>
            <Link
              href="/departments"
              className="inline-block px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors text-sm"
            >
              View All →
            </Link>
          </div>

          {/* Employees Card */}
          <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-gray-900">Employees</h3>
              <span className="text-3xl font-bold text-purple-600">{stats.employees}</span>
            </div>
            <p className="text-gray-600 text-sm mb-4">Manage employee information and records</p>
            <Link
              href="/employees"
              className="inline-block px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors text-sm"
            >
              View All →
            </Link>
          </div>
        </div>

        {/* System Information */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
          <div className="flex items-start">
            <svg className="w-6 h-6 text-blue-500 mt-0.5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div>
              <h3 className="text-sm font-medium text-blue-900">System Information</h3>
              <p className="mt-1 text-sm text-blue-700">
                You are logged in with Django native authentication. Your session is secured with token-based authentication.
              </p>
            </div>
          </div>
        </div>

        {/* Recent Items Preview */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Organizations */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Organizations</h3>
            {organizations.length > 0 ? (
              <ul className="space-y-2">
                {organizations.slice(0, 5).map((org) => (
                  <li key={org.id}>
                    <Link
                      href={`/organizations/${org.id}`}
                      className="text-blue-600 hover:text-blue-800 hover:underline"
                    >
                      {org.name}
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-sm">No organizations yet</p>
            )}
          </div>

          {/* Recent Departments */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Departments</h3>
            {departments.length > 0 ? (
              <ul className="space-y-2">
                {departments.slice(0, 5).map((dept) => (
                  <li key={dept.id}>
                    <Link
                      href={`/departments/${dept.id}`}
                      className="text-green-600 hover:text-green-800 hover:underline"
                    >
                      {dept.name}
                    </Link>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-sm">No departments yet</p>
            )}
          </div>

          {/* Recent Employees */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Employees</h3>
            {employees.length > 0 ? (
              <ul className="space-y-2">
                {employees.slice(0, 5).map((emp) => (
                  <li key={emp.id}>
                    <Link
                      href={`/employees/${emp.id}`}
                      className="text-purple-600 hover:text-purple-800 hover:underline"
                    >
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
