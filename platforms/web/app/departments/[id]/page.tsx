'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { departmentsApi, employeesApi } from '@/lib/api';

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
  created_at?: string;
}

export default function DepartmentDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const deptId = params.id as string;

  const [department, setDepartment] = useState<Department | null>(null);
  const [employeeCount, setEmployeeCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (deptId) {
      fetchData();
    }
  }, [deptId]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const deptRes = await departmentsApi.getById(parseInt(deptId));
      setDepartment(deptRes.data);

      const empsRes = await employeesApi.getAll({ department: deptId });
      setEmployeeCount(empsRes.data.count || 0);

      setLoading(false);
    } catch (err: any) {
      console.error('Error fetching department:', err);
      setError('Failed to load department details');
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!department) return;

    if (employeeCount > 0) {
      alert(`Cannot delete department with ${employeeCount} employees. Please reassign or delete employees first.`);
      return;
    }

    try {
      setDeleting(true);
      await departmentsApi.delete(parseInt(deptId));
      alert('Department deleted successfully!');
      router.push('/departments');
    } catch (err: any) {
      const errorMsg = err.response?.data?.message || err.message;
      alert('Error deleting department: ' + errorMsg);
      setDeleting(false);
      setShowDeleteModal(false);
    }
  };

  const getDepartmentIcon = (name: string) => {
    const nameLower = name?.toLowerCase() || '';
    
    if (nameLower.includes('engineer') || nameLower.includes('tech')) {
      return (
        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
        </svg>
      );
    }
    if (nameLower.includes('design') || nameLower.includes('creative')) {
      return (
        <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
        </svg>
      );
    }
    return (
      <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
      </svg>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-white text-xl">Loading department details...</div>
      </div>
    );
  }

  if (error || !department) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-center">
          <div className="text-red-400 text-xl mb-4">{error || 'Department not found'}</div>
          <button
            onClick={() => router.push('/departments')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Back to Departments
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <Link href="/departments" className="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Departments
          </Link>
        </div>

        <div className="bg-gradient-to-br from-slate-900 to-slate-950 rounded-2xl shadow-2xl border border-gray-800 overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-900 to-indigo-900 p-8">
            <div className="flex items-center gap-6">
              <div className="bg-purple-800/30 p-5 rounded-xl text-purple-300 backdrop-blur-sm border border-purple-700/30">
                {getDepartmentIcon(department.name)}
              </div>
              <div className="flex-1">
                <h1 className="text-4xl font-bold text-white mb-2">{department.name}</h1>
                <p className="text-purple-200 text-lg font-mono">{department.code}</p>
                {department.organization_name && (
                  <p className="text-purple-300 text-sm mt-1">{department.organization_name}</p>
                )}
              </div>
              <span className={`px-4 py-2 rounded-full text-sm font-bold self-start ${
                department.is_active 
                  ? 'bg-green-900/40 text-green-300 border border-green-700/50' 
                  : 'bg-gray-800/40 text-gray-400 border border-gray-700/50'
              }`}>
                {department.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>

          {/* Body */}
          <div className="p-8">
            {department.description && (
              <div className="mb-6 bg-slate-800/30 p-4 rounded-lg border border-gray-800">
                <label className="block text-sm font-medium text-gray-400 mb-2">Description</label>
                <p className="text-gray-200 text-base leading-relaxed">{department.description}</p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              {department.head_name && (
                <div className="bg-slate-800/30 p-4 rounded-lg border border-gray-800">
                  <label className="block text-sm font-medium text-gray-400 mb-3">Department Head</label>
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center text-white font-bold text-lg shadow-lg">
                      {department.head_name.split(' ').map(n => n[0]).join('')}
                    </div>
                    <p className="text-white text-lg font-semibold">{department.head_name}</p>
                  </div>
                </div>
              )}

              <div className="bg-slate-800/30 p-4 rounded-lg border border-gray-800">
                <label className="block text-sm font-medium text-gray-400 mb-3">Employees</label>
                <div className="flex items-center gap-3">
                  <svg className="w-8 h-8 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                  <p className="text-white text-2xl font-bold">{employeeCount}</p>
                </div>
              </div>

              {department.created_at && (
                <div className="bg-slate-800/30 p-4 rounded-lg border border-gray-800">
                  <label className="block text-sm font-medium text-gray-400 mb-2">Created</label>
                  <p className="text-gray-200 text-base">
                    {new Date(department.created_at).toLocaleDateString()}
                  </p>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="space-y-3 pt-6 border-t border-gray-800">
              <button
                onClick={() => router.push(`/departments/${department.id}/employees`)}
                className="w-full bg-blue-700 text-white py-3 rounded-lg hover:bg-blue-600 transition font-medium shadow-lg flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                View Department Employees ({employeeCount})
              </button>

              <div className="flex gap-3">
                <button
                  onClick={() => router.push(`/departments/${department.id}/edit`)}
                  className="flex-1 bg-purple-700 text-white py-3 rounded-lg hover:bg-purple-600 transition font-medium"
                >
                  Edit Department
                </button>
                <button
                  onClick={() => setShowDeleteModal(true)}
                  className="flex-1 bg-red-900/60 text-red-200 py-3 rounded-lg hover:bg-red-800/70 transition font-medium border border-red-800/50"
                >
                  Delete Department
                </button>
              </div>
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
                <h3 className="text-2xl font-bold text-white">Delete Department?</h3>
              </div>

              {employeeCount > 0 && (
                <div className="bg-yellow-900/20 border border-yellow-800/40 rounded-lg p-4 mb-4">
                  <p className="text-yellow-400 font-semibold text-sm">⚠️ Warning</p>
                  <p className="text-yellow-200 text-sm mt-1">
                    This department has {employeeCount} employee{employeeCount !== 1 ? 's' : ''}
                  </p>
                </div>
              )}

              <p className="text-gray-300 mb-6">
                Are you sure you want to delete <span className="font-bold text-white">{department.name}</span>? 
                This action cannot be undone.
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
                  disabled={deleting || employeeCount > 0}
                  className="flex-1 bg-red-900/60 text-red-200 py-3 rounded-lg hover:bg-red-800/70 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed border border-red-800/50"
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
