'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { departmentsApi, organizationsApi, employeesApi } from '@/lib/api';

interface Organization {
  id: number;
  name: string;
}

interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  organization: number;
}

interface Department {
  id: number;
  name: string;
  code: string;
  description: string;
  organization: number;
  head: number | null;
  is_active: boolean;
}

export default function EditDepartmentPage() {
  const params = useParams();
  const router = useRouter();
  const deptId = params.id as string;

  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [filteredEmployees, setFilteredEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [formData, setFormData] = useState({
    name: '',
    code: '',
    description: '',
    organization: '',
    head: '',
    is_active: true,
  });

  useEffect(() => {
    fetchData();
  }, [deptId]);

  useEffect(() => {
    if (formData.organization) {
      const filtered = employees.filter(
        (emp) => emp.organization === parseInt(formData.organization)
      );
      setFilteredEmployees(filtered);
    } else {
      setFilteredEmployees([]);
    }
  }, [formData.organization, employees]);

  const fetchData = async () => {
    try {
      const [deptRes, orgsRes, empsRes] = await Promise.all([
        departmentsApi.getById(parseInt(deptId)),
        organizationsApi.getAll(),
        employeesApi.getAll(),
      ]);

      const dept = deptRes.data;
      setFormData({
        name: dept.name,
        code: dept.code,
        description: dept.description || '',
        organization: dept.organization.toString(),
        head: dept.head?.toString() || '',
        is_active: dept.is_active,
      });

      setOrganizations(orgsRes.data.results || orgsRes.data || []);
      setEmployees(empsRes.data.results || empsRes.data || []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching data:', err);
      alert('Failed to load department data');
      router.push('/departments');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSaving(true);
      await departmentsApi.update(parseInt(deptId), {
        ...formData,
        organization: parseInt(formData.organization),
        head: formData.head ? parseInt(formData.head) : null,
      });
      alert('Department updated successfully!');
      router.push(`/departments/${deptId}`);
    } catch (err: any) {
      alert('Error: ' + (err.response?.data?.message || err.message));
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-3xl mx-auto">
        <div className="mb-8">
          <button
            onClick={() => router.back()}
            className="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-2 mb-4"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
          <h1 className="text-4xl font-bold text-white mb-2">Edit Department</h1>
          <p className="text-gray-300 text-lg">Update department information</p>
        </div>

        <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-8 shadow-2xl border border-gray-700">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-2 text-gray-300">Organization *</label>
                <select
                  required
                  value={formData.organization}
                  onChange={(e) => setFormData({ ...formData, organization: e.target.value, head: '' })}
                  className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                >
                  <option value="">Select Organization</option>
                  {organizations.map((org) => (
                    <option key={org.id} value={org.id}>
                      {org.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">Department Name *</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                  placeholder="e.g., Engineering"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">Department Code *</label>
                <input
                  type="text"
                  required
                  value={formData.code}
                  onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                  placeholder="e.g., ENG01"
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-2 text-gray-300">Description</label>
                <textarea
                  rows={4}
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                  placeholder="Brief description of the department"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">Department Head</label>
                <select
                  value={formData.head}
                  onChange={(e) => setFormData({ ...formData, head: e.target.value })}
                  className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                  disabled={!formData.organization}
                >
                  <option value="">Select Head (Optional)</option>
                  {filteredEmployees.map((emp) => (
                    <option key={emp.id} value={emp.id}>
                      {emp.first_name} {emp.last_name}
                    </option>
                  ))}
                </select>
                {!formData.organization && (
                  <p className="text-xs text-gray-500 mt-1">Select an organization first</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">Status</label>
                <select
                  value={formData.is_active ? 'true' : 'false'}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.value === 'true' })}
                  className="w-full px-4 py-3 bg-slate-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
                >
                  <option value="true">Active</option>
                  <option value="false">Inactive</option>
                </select>
              </div>
            </div>

            <div className="flex gap-4 pt-6 border-t border-gray-700">
              <button
                type="button"
                onClick={() => router.back()}
                className="flex-1 bg-slate-800 text-white py-3 rounded-lg hover:bg-slate-700 transition font-medium"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={saving}
                className="flex-1 bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition font-medium disabled:opacity-50"
              >
                {saving ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
