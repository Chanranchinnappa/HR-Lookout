'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { organizationsApi, employeesApi, departmentsApi } from '@/lib/api';

interface Organization {
  id: number;
  name: string;
  legal_name?: string;
  email?: string;
  phone?: string;
  city?: string;
  state?: string;
  country?: string;
  tax_id?: string;
  website?: string;
  is_active: boolean;
  created_at?: string;
  employee_count?: number;
  department_count?: number;
}

export default function OrganizationsPage() {
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchOrganizations();
  }, []);

  const fetchOrganizations = async () => {
    try {
      setLoading(true);
      const response = await organizationsApi.getAll();
      const orgs = response.data.results || response.data || [];
      
      // Fetch employee and department counts for each organization
      const orgsWithCounts = await Promise.all(
        orgs.map(async (org: Organization) => {
          try {
            const [empRes, deptRes] = await Promise.all([
              employeesApi.getAll({ organization: org.id }),
              departmentsApi.getAll({ organization: org.id }),
            ]);
            return {
              ...org,
              employee_count: empRes.data.count || 0,
              department_count: deptRes.data.count || 0,
            };
          } catch (err) {
            return { ...org, employee_count: 0, department_count: 0 };
          }
        })
      );
      
      setOrganizations(orgsWithCounts);
      setLoading(false);
    } catch (err: any) {
      console.error('Error fetching organizations:', err);
      setError('Failed to load organizations');
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-white text-xl">Loading organizations...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-center">
          <div className="text-red-400 text-xl mb-4">{error}</div>
          <button
            onClick={fetchOrganizations}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Organizations</h1>
            <p className="text-gray-300 text-lg">Manage your organizations</p>
          </div>
          <Link
            href="/organizations/new"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition shadow-lg font-medium"
          >
            + Add Organization
          </Link>
        </div>

        {/* Organizations Grid */}
        {organizations.length === 0 ? (
          <div className="text-center py-12 bg-slate-800/50 rounded-2xl border border-gray-700">
            <p className="text-gray-300 text-xl mb-4">No organizations found</p>
            <Link
              href="/organizations/new"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Create First Organization
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {organizations.map((org) => (
              <Link
                key={org.id}
                href={`/organizations/${org.id}/departments`}
                className="group"
              >
                <div className="bg-gradient-to-br from-slate-800 to-slate-900 border border-gray-700 rounded-2xl p-6 hover:shadow-2xl hover:shadow-blue-500/20 transition-all hover:scale-105 cursor-pointer">
                  {/* Header with Status Badge */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold text-white mb-2 group-hover:text-blue-400 transition">
                        {org.name}
                      </h3>
                      {org.legal_name && org.legal_name !== org.name && (
                        <p className="text-sm text-gray-400 mb-2">{org.legal_name}</p>
                      )}
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-bold ${
                        org.is_active
                          ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                          : 'bg-red-500/20 text-red-400 border border-red-500/30'
                      }`}
                    >
                      {org.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>

                  {/* Organization Details */}
                  <div className="space-y-3 mb-4">
                    {org.email && (
                      <div className="flex items-center gap-2 text-gray-300">
                        <svg
                          className="w-4 h-4 text-gray-500"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                          />
                        </svg>
                        <span className="text-sm truncate">{org.email}</span>
                      </div>
                    )}

                    {org.tax_id && (
                      <div className="flex items-center gap-2 text-gray-300">
                        <svg
                          className="w-4 h-4 text-gray-500"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                          />
                        </svg>
                        <span className="text-sm">Tax ID: {org.tax_id}</span>
                      </div>
                    )}

                    {(org.city || org.state || org.country) && (
                      <div className="flex items-center gap-2 text-gray-300">
                        <svg
                          className="w-4 h-4 text-gray-500"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                          />
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                          />
                        </svg>
                        <span className="text-sm">
                          {[org.city, org.state, org.country].filter(Boolean).join(', ')}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Stats Row */}
                  <div className="flex items-center justify-between pt-4 border-t border-gray-700">
                    <div className="flex items-center gap-4">
                      {/* Department Count */}
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
                            d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                          />
                        </svg>
                        <span className="text-sm font-semibold">
                          {org.department_count || 0} Depts
                        </span>
                      </div>

                      {/* Employee Count */}
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
                            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                          />
                        </svg>
                        <span className="text-sm font-semibold">
                          {org.employee_count || 0} Emps
                        </span>
                      </div>
                    </div>

                    <div className="text-blue-400 group-hover:text-blue-300 text-sm font-medium flex items-center gap-1">
                      View Departments
                      <svg
                        className="w-4 h-4 group-hover:translate-x-1 transition"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 5l7 7-7 7"
                        />
                      </svg>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
