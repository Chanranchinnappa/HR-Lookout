'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { departmentsApi, organizationsApi, employeesApi } from '@/lib/api';

interface Department {
  id: number;
  name: string;
  code: string;
  description?: string;
  organization: number;
  organization_name?: string;
  head?: number;
  head_name?: string;
  is_active: boolean;
  employee_count?: number;
}

interface Organization {
  id: number;
  name: string;
}

export default function OrganizationDepartmentsPage() {
  const params = useParams();
  const router = useRouter();
  const orgId = params.id as string;

  const [organization, setOrganization] = useState<Organization | null>(null);
  const [departments, setDepartments] = useState<Department[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (orgId) {
      fetchData();
    }
  }, [orgId]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const orgRes = await organizationsApi.getById(parseInt(orgId));
      setOrganization(orgRes.data);

      const deptsRes = await departmentsApi.getAll({ organization: orgId });
      const depts = deptsRes.data.results || deptsRes.data || [];

      const deptsWithCounts = await Promise.all(
        depts.map(async (dept: Department) => {
          try {
            const empRes = await employeesApi.getAll({ department: dept.id });
            return { ...dept, employee_count: empRes.data.count || 0 };
          } catch (err) {
            return { ...dept, employee_count: 0 };
          }
        })
      );

      setDepartments(deptsWithCounts);
      setLoading(false);
    } catch (err: any) {
      console.error('Error fetching data:', err);
      setError('Failed to load departments');
      setLoading(false);
    }
  };

  const getDepartmentIcon = (name: string) => {
    const nameLower = name.toLowerCase();
    
    if (nameLower.includes('engineer') || nameLower.includes('tech') || nameLower.includes('it')) {
      return (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
        </svg>
      );
    }
    if (nameLower.includes('hr') || nameLower.includes('human')) {
      return (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      );
    }
    if (nameLower.includes('finance') || nameLower.includes('account')) {
      return (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    }
    if (nameLower.includes('market') || nameLower.includes('sales')) {
      return (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
        </svg>
      );
    }
    if (nameLower.includes('design') || nameLower.includes('creative')) {
      return (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
        </svg>
      );
    }
    if (nameLower.includes('operation') || nameLower.includes('admin')) {
      return (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      );
    }
    return (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
      </svg>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-white text-xl">Loading departments...</div>
      </div>
    );
  }

  if (error || !organization) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-center">
          <div className="text-red-400 text-xl mb-4">{error || 'Organization not found'}</div>
          <button
            onClick={() => router.push('/organizations')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Back to Organizations
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Breadcrumb */}
        <div className="mb-6">
          <Link
            href="/organizations"
            className="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-2 mb-4"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Organizations
          </Link>
        </div>

        {/* Header with Add Button */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">{organization.name} - Departments</h1>
            <p className="text-gray-300 text-lg">Click on a department to view details</p>
          </div>
          <Link
            href={`/departments/new?organization=${orgId}`}
            className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition shadow-lg font-medium"
          >
            + Add Department
          </Link>
        </div>

        {/* Departments Grid */}
        {departments.length === 0 ? (
          <div className="text-center py-12 bg-slate-800/50 rounded-2xl border border-gray-700">
            <p className="text-gray-300 text-xl mb-4">No departments found for this organization</p>
            <Link
              href={`/departments/new?organization=${orgId}`}
              className="inline-block px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition"
            >
              Create First Department
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {departments.map((dept) => (
              <div
                key={dept.id}
                onClick={() => router.push(`/departments/${dept.id}`)}
                className="bg-gradient-to-br from-slate-800 to-slate-900 border border-gray-700 rounded-2xl p-6 hover:shadow-xl hover:shadow-purple-500/10 transition-all hover:scale-[1.02] cursor-pointer h-full flex flex-col"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="bg-purple-500/10 p-4 rounded-xl text-purple-400">
                    {getDepartmentIcon(dept.name)}
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-bold ${
                      dept.is_active
                        ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                        : 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
                    }`}
                  >
                    {dept.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>

                <h3 className="text-2xl font-bold text-white mb-2">
                  {dept.name}
                </h3>

                <p className="text-sm text-gray-400 mb-3 font-mono">{dept.code}</p>

                {dept.description && (
                  <p className="text-sm text-gray-300 mb-4 line-clamp-2">{dept.description}</p>
                )}

                {dept.head_name && (
                  <div className="flex items-center gap-2 mb-4 text-gray-300">
                    <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold text-sm">
                      {dept.head_name.split(' ').map(n => n[0]).join('')}
                    </div>
                    <div>
                      <p className="text-xs text-gray-500">Head</p>
                      <p className="text-sm font-semibold">{dept.head_name}</p>
                    </div>
                  </div>
                )}

                <div className="flex items-center justify-between pt-4 border-t border-gray-700 mt-auto">
                  <div className="flex items-center gap-2 text-gray-400">
                    <svg
                      className="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"
                      />
                    </svg>
                    <span className="text-sm font-semibold">
                      {dept.employee_count || 0} Employees
                    </span>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      router.push(`/departments/${dept.id}/employees`);
                    }}
                    className="text-purple-400 hover:text-purple-300 text-sm font-medium transition underline"
                  >
                    View Team →
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
