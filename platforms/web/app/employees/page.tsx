'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { employeesApi, organizationsApi } from '@/lib/api';

interface Employee {
  id: number;
  employee_id: string;
  full_name: string;
  first_name: string;
  last_name: string;
  email: string;
  job_title: string;
  status: string;
  department: number;
  department_name?: string;
  organization: number;
  organization_name?: string;
}

interface Organization {
  id: number;
  name: string;
}

export default function EmployeesPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const statusFromUrl = searchParams.get('status') || '';

  const [employees, setEmployees] = useState<Employee[]>([]);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState(statusFromUrl);
  const [orgFilter, setOrgFilter] = useState('');
  const [jobTitleFilter, setJobTitleFilter] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    fetchOrganizations();
  }, []);

  useEffect(() => {
    fetchEmployees();
  }, [currentPage, searchQuery, statusFilter, orgFilter, jobTitleFilter]);

  const fetchOrganizations = async () => {
    try {
      const response = await organizationsApi.getAll();
      setOrganizations(response.data.results || response.data || []);
    } catch (err) {
      console.error('Error fetching organizations:', err);
    }
  };

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      setError(null);

      const params: any = {
        page: currentPage,
      };
      if (statusFilter) params.status = statusFilter;
      if (orgFilter) params.organization = orgFilter;
      if (jobTitleFilter) params.job_title = jobTitleFilter;
      if (searchQuery) params.search = searchQuery;

      const response = await employeesApi.getAll(params);
      const data = response.data;

      if (data.results) {
        setEmployees(data.results);
        setTotalCount(data.count);
        const calculatedPages = Math.ceil(data.count / 10);
        setTotalPages(calculatedPages);
        
        if (currentPage > calculatedPages && calculatedPages > 0) {
          setCurrentPage(calculatedPages);
          return;
        }
      } else {
        setEmployees(data);
      }

      setLoading(false);
    } catch (err: any) {
      console.error('Error fetching employees:', err);
      setError('Failed to load employees');
      setLoading(false);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  if (loading && employees.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-white text-xl">Loading employees...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-center">
          <div className="text-red-400 text-xl mb-4">{error}</div>
          <button
            onClick={fetchEmployees}
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
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Employees</h1>
          <p className="text-gray-300 text-lg">Manage all employees across the organization</p>
        </div>

        <div className="mb-6 bg-slate-800/50 border border-gray-700 rounded-xl p-4">
          <div className="flex items-center gap-2 mb-2">
            <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-white font-semibold">Status Legend:</span>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-green-500 rounded-full"></span>
              <span className="text-sm text-gray-300">Active</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-yellow-500 rounded-full"></span>
              <span className="text-sm text-gray-300">On Leave</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-gray-500 rounded-full"></span>
              <span className="text-sm text-gray-300">Inactive</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 bg-red-500 rounded-full"></span>
              <span className="text-sm text-gray-300">Terminated</span>
            </div>
          </div>
        </div>

        <div className="mb-6 space-y-4">
          <div className="flex gap-4 flex-wrap">
            <input
              type="text"
              placeholder="Search employees by name, email, or ID..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setCurrentPage(1);
              }}
              className="flex-1 min-w-[250px] px-4 py-3 bg-slate-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
            />
            <Link
              href="/employees/new"
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition shadow-lg font-medium whitespace-nowrap"
            >
              + Add Employee
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">Organization</label>
              <select
                value={orgFilter}
                onChange={(e) => {
                  setOrgFilter(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-3 bg-slate-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              >
                <option value="">All Organizations</option>
                {organizations.map((org) => (
                  <option key={org.id} value={org.id}>
                    {org.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">Job Title</label>
              <input
                type="text"
                placeholder="Filter by job title"
                value={jobTitleFilter}
                onChange={(e) => {
                  setJobTitleFilter(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-3 bg-slate-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">Status</label>
              <select
                value={statusFilter}
                onChange={(e) => {
                  setStatusFilter(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-3 bg-slate-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20"
              >
                <option value="">All Status</option>
                <option value="ACTIVE">Active</option>
                <option value="INACTIVE">Inactive</option>
                <option value="ON_LEAVE">On Leave</option>
                <option value="TERMINATED">Terminated</option>
              </select>
            </div>

            <div className="flex items-end">
              <button
                onClick={() => {
                  setSearchQuery('');
                  setStatusFilter('');
                  setOrgFilter('');
                  setJobTitleFilter('');
                  setCurrentPage(1);
                }}
                className="w-full px-4 py-3 bg-slate-700 text-white rounded-lg hover:bg-slate-600 transition font-medium"
              >
                Clear Filters
              </button>
            </div>
          </div>
        </div>

        {employees.length === 0 ? (
          <div className="text-center py-12 bg-slate-800/50 rounded-2xl border border-gray-700">
            <p className="text-gray-300 text-xl mb-2">No employees found</p>
            <p className="text-gray-400 text-sm">
              {searchQuery || statusFilter || orgFilter || jobTitleFilter ? 'Try adjusting your filters' : 'Get started by adding an employee.'}
            </p>
          </div>
        ) : (
          <>
            <div className="overflow-x-auto bg-slate-800/50 backdrop-blur-sm rounded-2xl shadow-2xl border border-gray-700">
              <table className="min-w-full">
                <thead className="bg-slate-900/70">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">
                      Employee
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">
                      Email
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">
                      Job Title
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-bold text-gray-300 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {employees.map((employee) => (
                    <tr key={employee.id} className="hover:bg-slate-700/30 transition">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="flex-shrink-0 h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white font-bold">
                            {employee.first_name[0]}{employee.last_name[0]}
                          </div>
                          <div className="ml-4">
                            <div className="text-sm font-semibold text-white">
                              {employee.first_name} {employee.last_name}
                            </div>
                            <div className="text-sm text-gray-400">{employee.employee_id}</div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {employee.email}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {employee.job_title}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          <span
                            className={`w-3 h-3 rounded-full ${
                              employee.status === 'ACTIVE'
                                ? 'bg-green-500'
                                : employee.status === 'INACTIVE'
                                ? 'bg-gray-500'
                                : employee.status === 'ON_LEAVE'
                                ? 'bg-yellow-500'
                                : 'bg-red-500'
                            }`}
                          ></span>
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-bold ${
                              employee.status === 'ACTIVE'
                                ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                                : employee.status === 'INACTIVE'
                                ? 'bg-gray-500/20 text-gray-400 border border-gray-500/30'
                                : employee.status === 'ON_LEAVE'
                                ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                                : 'bg-red-500/20 text-red-400 border border-red-500/30'
                            }`}
                          >
                            {employee.status}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm space-x-3">
                        <Link
                          href={`/employees/${employee.id}`}
                          className="text-cyan-400 hover:text-cyan-300 font-medium transition"
                        >
                          Details
                        </Link>
                        <Link
                          href={`/employees/${employee.id}/edit`}
                          className="text-blue-400 hover:text-blue-300 font-medium transition"
                        >
                          Edit
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {totalPages > 0 && (
              <div className="mt-6 flex items-center justify-between">
                <p className="text-sm text-gray-300">
                  Page {currentPage} of {totalPages} ({totalCount} total employees)
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={handlePreviousPage}
                    disabled={currentPage === 1}
                    className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
                  >
                    Previous
                  </button>
                  <button
                    onClick={handleNextPage}
                    disabled={currentPage >= totalPages}
                    className="px-4 py-2 bg-slate-700 text-white rounded-lg hover:bg-slate-600 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
