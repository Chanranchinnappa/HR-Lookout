'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { employeesApi } from '@/lib/api';

interface Employee {
  id: number;
  employee_id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone_number?: string;
  job_title: string;
  hire_date?: string;
  date_of_birth?: string;
  status: string;
  department: number;
  department_name?: string;
  organization: number;
  organization_name?: string;
}

export default function EmployeeDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const empId = params.id as string;

  const [employee, setEmployee] = useState<Employee | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (empId) {
      fetchEmployee();
    }
  }, [empId]);

  const fetchEmployee = async () => {
    try {
      setLoading(true);
      const response = await employeesApi.getById(parseInt(empId));
      setEmployee(response.data);
      setLoading(false);
    } catch (err: any) {
      console.error('Error fetching employee:', err);
      setError('Failed to load employee details');
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!employee) return;

    try {
      setDeleting(true);
      await employeesApi.delete(parseInt(empId));
      alert('Employee deleted successfully!');
      router.push('/employees');
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || err.message;
      alert('Error deleting employee: ' + errorMsg);
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-white text-xl">Loading employee details...</div>
      </div>
    );
  }

  if (error || !employee) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-center">
          <div className="text-red-400 text-xl mb-4">{error || 'Employee not found'}</div>
          <button
            onClick={() => router.push('/employees')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Back to Employees
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Breadcrumb */}
        <div className="mb-6">
          <Link
            href="/employees"
            className="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-2"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Employees
          </Link>
        </div>

        {/* Employee Card */}
        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl shadow-2xl border border-gray-700 overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-cyan-600 p-8">
            <div className="flex items-center gap-6">
              <div className="w-24 h-24 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white font-bold text-3xl border-4 border-white/30 shadow-xl">
                {employee.first_name[0]}{employee.last_name[0]}
              </div>
              <div className="flex-1">
                <h1 className="text-4xl font-bold text-white mb-2">
                  {employee.first_name} {employee.last_name}
                </h1>
                <p className="text-blue-100 text-xl mb-1">{employee.job_title}</p>
                <p className="text-blue-200 text-sm font-mono">ID: {employee.employee_id}</p>
              </div>
              <span
                className={`px-4 py-2 rounded-full text-sm font-bold self-start ${
                  employee.status === 'ACTIVE'
                    ? 'bg-green-900/40 text-green-200 border border-green-700/50'
                    : employee.status === 'INACTIVE'
                    ? 'bg-gray-800/40 text-gray-300 border border-gray-700/50'
                    : employee.status === 'ON_LEAVE'
                    ? 'bg-yellow-900/40 text-yellow-200 border border-yellow-700/50'
                    : 'bg-red-900/40 text-red-200 border border-red-700/50'
                }`}
              >
                {employee.status}
              </span>
            </div>
          </div>

          {/* Details */}
          <div className="p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="bg-slate-800/50 p-4 rounded-lg border border-gray-700">
                <label className="block text-sm font-medium text-gray-400 mb-2">Email</label>
                <p className="text-white text-lg">{employee.email}</p>
              </div>

              {employee.phone_number && (
                <div className="bg-slate-800/50 p-4 rounded-lg border border-gray-700">
                  <label className="block text-sm font-medium text-gray-400 mb-2">Phone</label>
                  <p className="text-white text-lg">{employee.phone_number}</p>
                </div>
              )}

              <div className="bg-slate-800/50 p-4 rounded-lg border border-gray-700">
                <label className="block text-sm font-medium text-gray-400 mb-2">Department</label>
                <p className="text-white text-lg">{employee.department_name || 'N/A'}</p>
              </div>

              <div className="bg-slate-800/50 p-4 rounded-lg border border-gray-700">
                <label className="block text-sm font-medium text-gray-400 mb-2">Organization</label>
                <p className="text-white text-lg">{employee.organization_name || 'N/A'}</p>
              </div>

              {employee.hire_date && (
                <div className="bg-slate-800/50 p-4 rounded-lg border border-gray-700">
                  <label className="block text-sm font-medium text-gray-400 mb-2">Hire Date</label>
                  <p className="text-white text-lg">{new Date(employee.hire_date).toLocaleDateString()}</p>
                </div>
              )}

              {employee.date_of_birth && (
                <div className="bg-slate-800/50 p-4 rounded-lg border border-gray-700">
                  <label className="block text-sm font-medium text-gray-400 mb-2">Date of Birth</label>
                  <p className="text-white text-lg">{new Date(employee.date_of_birth).toLocaleDateString()}</p>
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="flex gap-4 pt-6 border-t border-gray-700">
              <button
                onClick={() => router.push(`/employees/${employee.id}/edit`)}
                className="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition font-medium shadow-lg"
              >
                Edit Employee
              </button>
              <button
                onClick={() => setShowDeleteModal(true)}
                className="flex-1 bg-red-900/50 text-red-300 py-3 rounded-lg hover:bg-red-900/70 transition font-medium border border-red-800/40"
              >
                Delete Employee
              </button>
            </div>
          </div>
        </div>

        {/* Delete Confirmation Modal */}
        {showDeleteModal && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-gradient-to-br from-slate-900 to-slate-950 rounded-2xl p-8 max-w-md w-full border border-red-900/30 shadow-2xl">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 rounded-full bg-red-900/30 flex items-center justify-center border border-red-800/50">
                  <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-white">Delete Employee?</h3>
              </div>

              <p className="text-gray-300 mb-6">
                Are you sure you want to delete{' '}
                <span className="font-bold text-white">
                  {employee.first_name} {employee.last_name}
                </span>
                ? This action cannot be undone.
              </p>

              <div className="flex gap-4">
                <button
                  onClick={() => setShowDeleteModal(false)}
                  disabled={deleting}
                  className="flex-1 bg-slate-800 text-white py-3 rounded-lg hover:bg-slate-700 transition font-medium disabled:opacity-50"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDelete}
                  disabled={deleting}
                  className="flex-1 bg-red-900/50 text-red-300 py-3 rounded-lg hover:bg-red-900/70 transition font-medium disabled:opacity-50 border border-red-800/40"
                >
                  {deleting ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
